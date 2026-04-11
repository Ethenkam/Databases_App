<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const fmt = v => v != null ? Number(v).toLocaleString('ru-RU', { minimumFractionDigits: 2 }) : '—'

const columns = [
  { key: 'dept_name',      label: 'Отдел' },
  { key: 'item_name',      label: 'Статья' },
  { key: 'budget_year',    label: 'Год' },
  { key: 'budget_quarter', label: 'Квартал' },
  { key: 'plan_rub', label: 'План, ₽',    render: r => fmt(r.plan_rub) },
  { key: 'fact_rub', label: 'Факт, ₽',    render: r => fmt(r.fact_rub) },
  { key: 'deviation', label: 'Отклонение, ₽',
    render: r => {
      if (r.plan_rub == null || r.fact_rub == null) return '—'
      return fmt(Number(r.plan_rub) - Number(r.fact_rub))
    },
  },
  { key: 'approved_date', label: 'Дата утв.' },
]

const deptOptions = ref([])
const itemOptions = ref([])

const formFields = computed(() => [
  { key: 'dept_id',        label: 'Отдел',          type: 'select', required: true, createOnly: true, options: deptOptions.value },
  { key: 'item_id',        label: 'Статья бюджета', type: 'select', required: true, createOnly: true, options: itemOptions.value },
  { key: 'budget_year',    label: 'Год',            type: 'number', required: true, createOnly: true },
  { key: 'budget_quarter', label: 'Квартал (1–4)',  type: 'number', required: true, createOnly: true },
  { key: 'plan_rub',       label: 'План (руб.)',     type: 'number', required: true },
  { key: 'fact_rub',       label: 'Факт (руб.)',     type: 'number', required: true },
  { key: 'approved_date',  label: 'Дата утверждения', type: 'date' },
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

// Composite key: dept_id/item_id/year/quarter
function budgetKey(row) {
  return `${row.dept_id}/${row.item_id}/${row.budget_year}/${row.budget_quarter}`
}

async function loadPage(p) {
  loading.value = true
  error.value   = ''
  try {
    const data = await api.getAll('budget', p, pageSize)
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
  const [depts, items] = await Promise.all([
    api.getAll('department',  1, 1000),
    api.getAll('budget-item', 1, 1000),
  ])
  deptOptions.value = depts.items.map(d => ({ value: d.dept_id, label: d.dept_name }))
  itemOptions.value = items.items.map(i => ({ value: i.item_id, label: i.item_name }))
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
  if (!confirm(`Удалить запись бюджета (${row.dept_name}, ${row.item_name}, ${row.budget_year} кв.${row.budget_quarter})?`)) return
  try {
    await api.delete('budget', budgetKey(row))
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
      await api.update('budget', budgetKey(currentRow.value), data)
    } else {
      await api.create('budget', data)
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
      <h1 class="text-2xl font-bold text-gray-800">Бюджет</h1>
      <p class="text-sm text-gray-500 mt-1">Плановые и фактические расходы по отделам</p>
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
      :title="isEdit ? 'Редактировать запись бюджета' : 'Добавить запись бюджета'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>
