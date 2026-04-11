<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const columns = [
  { key: 'dept_id',         label: 'ID' },
  { key: 'dept_name',       label: 'Наименование' },
  { key: 'emp_count',       label: 'Сотрудников' },
  { key: 'floor_num',       label: 'Этаж' },
  { key: 'room_num',        label: 'Кабинет' },
  { key: 'dept_phone',      label: 'Телефон' },
  { key: 'head_emp_name',   label: 'Руководитель' },
  { key: 'created_date',    label: 'Создан' },
]

const empOptions = ref([])

const formFields = computed(() => [
  { key: 'dept_id',           label: 'ID',            type: 'number', required: true, createOnly: true },
  { key: 'dept_name',         label: 'Наименование',  type: 'text',   required: true, fullWidth: true },
  { key: 'emp_count',         label: 'Кол-во сотр.',  type: 'number' },
  { key: 'floor_num',         label: 'Этаж',          type: 'number' },
  { key: 'room_num',          label: 'Кабинет',       type: 'text' },
  { key: 'dept_phone',        label: 'Телефон',       type: 'text' },
  { key: 'dept_email',        label: 'Email',         type: 'email' },
  { key: 'created_date',      label: 'Дата создания', type: 'date' },
  { key: 'head_emp_id',       label: 'Руководитель',  type: 'select', options: empOptions.value },
  { key: 'head_appoint_date', label: 'Дата назначения', type: 'date' },
])

const rows     = ref([])
const total    = ref(0)
const page     = ref(1)
const pageSize = 20
const loading  = ref(false)
const error    = ref('')

const showModal  = ref(false)
const isEdit     = ref(false)
const formData   = ref({})
const currentRow = ref(null)
const saveError  = ref('')

async function loadPage(p) {
  loading.value = true
  error.value   = ''
  try {
    const data = await api.getAll('department', p, pageSize)
    rows.value  = data.items
    total.value = data.total
    page.value  = p
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const emps = await api.getAll('employee', 1, 1000)
  empOptions.value = emps.items.map(e => ({
    value: e.emp_id,
    label: `${e.last_name} ${e.first_name}${e.middle_name ? ' ' + e.middle_name : ''}`,
  }))
  await loadPage(1)
})

function openAdd() {
  isEdit.value    = false
  formData.value  = { emp_count: 0 }
  saveError.value = ''
  showModal.value = true
}

function openEdit(row) {
  isEdit.value     = true
  currentRow.value = row
  formData.value   = { ...row }
  saveError.value  = ''
  showModal.value  = true
}

async function handleDelete(row) {
  if (!confirm(`Удалить отдел «${row.dept_name}»?`)) return
  try {
    await api.delete('department', row.dept_id)
    await loadPage(page.value)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка удаления'
  }
}

function pickFields(raw, edit) {
  const keys = formFields.value
    .filter(f => !(f.createOnly && edit))
    .map(f => f.key)
  return Object.fromEntries(keys.map(k => [k, raw[k] === '' ? null : raw[k]]))
}

async function handleSubmit(raw) {
  saveError.value = ''
  try {
    const data = pickFields(raw, isEdit.value)
    if (isEdit.value) {
      await api.update('department', currentRow.value.dept_id, data)
    } else {
      await api.create('department', data)
    }
    showModal.value = false
    await loadPage(page.value)
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Ошибка сохранения'
  }
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Отделы</h1>
      <p class="text-sm text-gray-500 mt-1">Структурные подразделения организации</p>
    </div>
    <div v-if="error" class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
      {{ error }}
    </div>
    <DataTable
      :columns="columns" :rows="rows" :total="total"
      :page="page" :page-size="pageSize" :loading="loading"
      @update:page="loadPage" @add="openAdd" @edit="openEdit" @delete="handleDelete"
    />
    <FormModal
      v-if="showModal"
      :title="isEdit ? 'Редактировать отдел' : 'Добавить отдел'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>
