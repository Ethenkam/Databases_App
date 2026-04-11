<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const fmt = v => v != null ? Number(v).toLocaleString('ru-RU', { minimumFractionDigits: 2 }) : '—'

const columns = [
  { key: 'doc_id',        label: 'ID' },
  { key: 'doc_date',      label: 'Дата' },
  { key: 'type_name',     label: 'Тип' },
  { key: 'dept_name',     label: 'Отдел' },
  { key: 'item_name',     label: 'Статья' },
  { key: 'contr_name',    label: 'Контрагент' },
  { key: 'resp_emp_name', label: 'Ответственный' },
  { key: 'doc_amount', label: 'Сумма, ₽', render: r => fmt(r.doc_amount) },
]

const deptOptions     = ref([])
const itemOptions     = ref([])
const typeOptions     = ref([])
const contrOptions    = ref([])
const empOptions      = ref([])

const formFields = computed(() => [
  { key: 'doc_id',      label: 'ID',              type: 'number', required: true, createOnly: true },
  { key: 'doc_date',    label: 'Дата',            type: 'date',   required: true },
  { key: 'dept_id',     label: 'Отдел',           type: 'select', required: true, options: deptOptions.value },
  { key: 'type_id',     label: 'Тип документа',   type: 'select', required: true, options: typeOptions.value },
  { key: 'item_id',     label: 'Статья бюджета',  type: 'select', required: true, options: itemOptions.value },
  { key: 'resp_emp_id', label: 'Ответственный',   type: 'select', required: true, options: empOptions.value },
  { key: 'contr_inn',   label: 'Контрагент',      type: 'select', options: contrOptions.value },
  { key: 'doc_amount',  label: 'Сумма',           type: 'number' },
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
    const data = await api.getAll('document', p, pageSize)
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
  const [depts, items, types, contrs, emps] = await Promise.all([
    api.getAll('department',  1, 1000),
    api.getAll('budget-item', 1, 1000),
    api.getAll('doc-type',    1, 1000),
    api.getAll('contractor',  1, 1000),
    api.getAll('employee',    1, 1000),
  ])
  deptOptions.value  = depts.items.map(d => ({ value: d.dept_id,      label: d.dept_name }))
  itemOptions.value  = items.items.map(i => ({ value: i.item_id,      label: i.item_name }))
  typeOptions.value  = types.items.map(t => ({ value: t.type_id,      label: t.type_name }))
  contrOptions.value = contrs.items.map(c => ({ value: c.contr_inn,   label: `${c.contr_inn} — ${c.contr_name}` }))
  empOptions.value   = emps.items.map(e => ({
    value: e.emp_id,
    label: `${e.last_name} ${e.first_name}`,
  }))
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
  if (!confirm(`Удалить документ #${row.doc_id}?`)) return
  try {
    await api.delete('document', row.doc_id)
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
      await api.update('document', currentRow.value.doc_id, data)
    } else {
      await api.create('document', data)
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
      <h1 class="text-2xl font-bold text-gray-800">Документы</h1>
      <p class="text-sm text-gray-500 mt-1">Бухгалтерские и финансовые документы</p>
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
      :title="isEdit ? 'Редактировать документ' : 'Добавить документ'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>
