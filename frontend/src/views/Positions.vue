<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const columns = [
  { key: 'position_id',    label: 'ID' },
  { key: 'position_name',  label: 'Наименование' },
  { key: 'position_grade', label: 'Грейд' },
  { key: 'min_salary', label: 'Мин. зарплата, ₽',
    render: r => r.min_salary != null ? Number(r.min_salary).toLocaleString('ru-RU') : '—' },
]

const formFields = computed(() => [
  { key: 'position_id',    label: 'ID',             type: 'number', required: true, createOnly: true },
  { key: 'position_name',  label: 'Наименование',   type: 'text',   required: true },
  { key: 'position_grade', label: 'Грейд',          type: 'text' },
  { key: 'min_salary',     label: 'Мин. зарплата',  type: 'number', required: true },
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
    const data = await api.getAll('position', p, pageSize)
    rows.value  = data.items
    total.value = data.total
    page.value  = p
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

onMounted(() => loadPage(1))

function openAdd() {
  isEdit.value    = false
  formData.value  = {}
  saveError.value = ''
  showModal.value = true
}

function openEdit(row) {
  isEdit.value    = true
  currentRow.value = row
  formData.value  = { ...row }
  saveError.value = ''
  showModal.value = true
}

async function handleDelete(row) {
  if (!confirm(`Удалить должность «${row.position_name}»?`)) return
  try {
    await api.delete('position', row.position_id)
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
      await api.update('position', currentRow.value.position_id, data)
    } else {
      await api.create('position', data)
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
      <h1 class="text-2xl font-bold text-gray-800">Должности</h1>
      <p class="text-sm text-gray-500 mt-1">Справочник должностей и грейдов</p>
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
      :title="isEdit ? 'Редактировать должность' : 'Добавить должность'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>
