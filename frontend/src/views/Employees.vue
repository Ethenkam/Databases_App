<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const columns = [
  { key: 'emp_id',    label: 'ID' },
  { key: 'full_name', label: 'ФИО',
    render: r => [r.last_name, r.first_name, r.middle_name].filter(Boolean).join(' ') },
  { key: 'position_name', label: 'Должность' },
  { key: 'dept_name',     label: 'Отдел' },
  { key: 'salary', label: 'Зарплата, ₽',
    render: r => r.salary != null ? Number(r.salary).toLocaleString('ru-RU') : '—' },
  { key: 'hire_date', label: 'Дата найма' },
]

const deptOptions     = ref([])
const positionOptions = ref([])

const formFields = computed(() => [
  { key: 'emp_id',      label: 'ID',            type: 'number', required: true, createOnly: true },
  { key: 'last_name',   label: 'Фамилия',       type: 'text',   required: true },
  { key: 'first_name',  label: 'Имя',           type: 'text',   required: true },
  { key: 'middle_name', label: 'Отчество',       type: 'text' },
  { key: 'dept_id',     label: 'Отдел',         type: 'select', required: true, options: deptOptions.value },
  { key: 'position_id', label: 'Должность',     type: 'select', required: true, options: positionOptions.value },
  { key: 'salary',      label: 'Зарплата',      type: 'number', required: true },
  { key: 'hire_date',   label: 'Дата найма',    type: 'date',   required: true },
  { key: 'birth_date',  label: 'Дата рождения', type: 'date' },
  { key: 'education',   label: 'Образование',   type: 'text' },
  { key: 'inn',         label: 'ИНН',           type: 'text' },
  { key: 'snils',       label: 'СНИЛС',         type: 'text' },
  { key: 'emp_phone',   label: 'Телефон',       type: 'text' },
  { key: 'emp_email',   label: 'Email',         type: 'email' },
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
    const data = await api.getAll('employee', p, pageSize)
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
  const [depts, positions] = await Promise.all([
    api.getAll('department', 1, 1000),
    api.getAll('position', 1, 1000),
  ])
  deptOptions.value     = depts.items.map(d => ({ value: d.dept_id, label: d.dept_name }))
  positionOptions.value = positions.items.map(p => ({ value: p.position_id, label: p.position_name }))
  await loadPage(1)
})

function openAdd() {
  isEdit.value    = false
  formData.value  = {}
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
  if (!confirm(`Удалить сотрудника #${row.emp_id} — ${row.last_name} ${row.first_name}?`)) return
  try {
    await api.delete('employee', row.emp_id)
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
      await api.update('employee', currentRow.value.emp_id, data)
    } else {
      await api.create('employee', data)
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
      <h1 class="text-2xl font-bold text-gray-800">Сотрудники</h1>
      <p class="text-sm text-gray-500 mt-1">Управление кадровым составом</p>
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
      :title="isEdit ? 'Редактировать сотрудника' : 'Добавить сотрудника'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>
