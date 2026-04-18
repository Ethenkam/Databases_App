<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { api } from '../services/api'
import OlapControls from '../components/OlapControls.vue'
import OlapTable from '../components/OlapTable.vue'
import OlapChart from '../components/OlapChart.vue'

const API_BASE = 'http://localhost:8000/api'

// ── Состояние ────────────────────────────────────────────────────────────────
const operation = ref('rollup-dept')

const departments = ref([])
const contractors = ref([])
const items = ref([])
const quarters = ref([])

const selectedDeptId = ref(null)
const selectedContrInn = ref(null)
const diceDeptId = ref(null)
const diceItemId = ref(null)
const diceQuarter = ref(null)

const loading = ref(false)
const error = ref('')
const result = ref(null)

// ── Загрузка справочников ────────────────────────────────────────────────────
async function loadDictionaries() {
  try {
    const [deps, contrs, itms, qs] = await Promise.all([
      api.getAll('department', 1, 1000),
      api.getAll('contractor', 1, 1000),
      api.getAll('budget-item', 1, 1000),
      api.olap.rollupByQuarter(),
    ])
    departments.value = deps.items || []
    contractors.value = contrs.items || []
    items.value = itms.items || []
    quarters.value = (qs || []).map(q => ({
      year: q.budget_year,
      quarter: q.budget_quarter,
    }))
  } catch (e) {
    console.error('Ошибка загрузки справочников:', e)
  }
}

// ── Применить операцию ───────────────────────────────────────────────────────
async function apply() {
  loading.value = true
  error.value = ''
  result.value = null
  try {
    switch (operation.value) {
      case 'rollup-dept':
        result.value = await api.olap.rollupByDept()
        break
      case 'rollup-item':
        result.value = await api.olap.rollupByItem()
        break
      case 'rollup-quarter':
        result.value = await api.olap.rollupByQuarter()
        break
      case 'slice-dept':
        if (!selectedDeptId.value) { error.value = 'Выберите отдел'; break }
        result.value = await api.olap.sliceByDept(selectedDeptId.value)
        break
      case 'slice-contractor':
        if (!selectedContrInn.value) { error.value = 'Выберите контрагента'; break }
        result.value = await api.olap.sliceByContractor(selectedContrInn.value)
        break
      case 'dice': {
        const params = {}
        if (diceDeptId.value != null) params.dept_id = diceDeptId.value
        if (diceItemId.value != null) params.item_id = diceItemId.value
        if (diceQuarter.value) {
          const [y, q] = diceQuarter.value.split('-')
          params.budget_year = Number(y)
          params.budget_quarter = Number(q)
        }
        result.value = await api.olap.dice(params)
        break
      }
      case 'drilldown-dept':
        if (!selectedDeptId.value) { error.value = 'Выберите отдел'; break }
        result.value = await api.olap.drilldownDept(selectedDeptId.value)
        break
      case 'cross-dept-item':
        result.value = await api.olap.crossDeptItem()
        break
    }
  } catch (e) {
    error.value = 'Ошибка загрузки данных: ' + (e?.message || 'unknown')
    console.error(e)
  } finally {
    loading.value = false
  }
}

// ── Колонки таблицы ──────────────────────────────────────────────────────────
const tableColumns = computed(() => {
  switch (operation.value) {
    case 'rollup-dept':
      return [
        { key: 'dept_name', label: 'Отдел' },
        { key: 'total_plan', label: 'Σ План, ₽', format: 'number' },
        { key: 'total_fact', label: 'Σ Факт, ₽', format: 'number' },
        { key: 'deviation', label: 'Отклонение, ₽', format: 'number', deviation: true },
        { key: 'doc_count', label: 'Документов', format: 'number' },
      ]
    case 'rollup-item':
      return [
        { key: 'item_name', label: 'Статья' },
        { key: 'item_category', label: 'Категория' },
        { key: 'total_plan', label: 'Σ План, ₽', format: 'number' },
        { key: 'total_fact', label: 'Σ Факт, ₽', format: 'number' },
        { key: 'deviation', label: 'Отклонение, ₽', format: 'number', deviation: true },
        { key: 'doc_count', label: 'Документов', format: 'number' },
      ]
    case 'rollup-quarter':
      return [
        { key: 'budget_year', label: 'Год' },
        { key: 'budget_quarter', label: 'Квартал' },
        { key: 'total_plan', label: 'Σ План, ₽', format: 'number' },
        { key: 'total_fact', label: 'Σ Факт, ₽', format: 'number' },
        { key: 'deviation', label: 'Отклонение, ₽', format: 'number', deviation: true },
      ]
    default:
      return []
  }
})

// Строки для таблицы основной операции
const tableRows = computed(() => {
  if (!result.value) return []
  if (['rollup-dept', 'rollup-item', 'rollup-quarter'].includes(operation.value)) {
    return result.value
  }
  return []
})

// ── Данные для графика ───────────────────────────────────────────────────────
const chartInfo = computed(() => {
  if (!result.value) return null

  if (operation.value === 'rollup-dept') {
    const data = result.value
    return {
      type: 'bar',
      title: 'План vs Факт по отделам',
      data: {
        labels: data.map(r => r.dept_name),
        datasets: [
          {
            label: 'План',
            data: data.map(r => Number(r.total_plan)),
            backgroundColor: 'rgba(59, 130, 246, 0.7)',
          },
          {
            label: 'Факт',
            data: data.map(r => Number(r.total_fact)),
            backgroundColor: 'rgba(16, 185, 129, 0.7)',
          },
        ],
      },
    }
  }

  if (operation.value === 'rollup-item') {
    const data = result.value
    const palette = [
      '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
      '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16',
    ]
    return {
      type: 'pie',
      title: 'Доли расходов по статьям (факт)',
      data: {
        labels: data.map(r => r.item_name),
        datasets: [{
          data: data.map(r => Number(r.total_fact)),
          backgroundColor: data.map((_, i) => palette[i % palette.length]),
        }],
      },
    }
  }

  if (operation.value === 'rollup-quarter') {
    const data = result.value
    return {
      type: 'line',
      title: 'Динамика бюджета по кварталам',
      data: {
        labels: data.map(r => `${r.budget_year} Q${r.budget_quarter}`),
        datasets: [
          {
            label: 'План',
            data: data.map(r => Number(r.total_plan)),
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.15)',
            tension: 0.3,
            fill: true,
          },
          {
            label: 'Факт',
            data: data.map(r => Number(r.total_fact)),
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.15)',
            tension: 0.3,
            fill: true,
          },
        ],
      },
    }
  }

  if (operation.value === 'cross-dept-item') {
    const pivot = result.value
    const itemsSet = new Set()
    pivot.forEach(d => Object.keys(d.items || {}).forEach(n => itemsSet.add(n)))
    const itemNames = Array.from(itemsSet)
    const palette = [
      '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
      '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16',
    ]
    const datasets = itemNames.map((name, i) => ({
      label: name,
      data: pivot.map(d => Number(d.items?.[name]?.total_fact || 0)),
      backgroundColor: palette[i % palette.length],
    }))
    return {
      type: 'stacked-bar',
      title: 'Кросс-таблица Отдел × Статья (факт)',
      data: {
        labels: pivot.map(d => d.dept_name),
        datasets,
      },
    }
  }

  return null
})

// ── Кросс-таблица ────────────────────────────────────────────────────────────
const crossItemNames = computed(() => {
  if (operation.value !== 'cross-dept-item' || !result.value) return []
  const set = new Set()
  result.value.forEach(d => Object.keys(d.items || {}).forEach(n => set.add(n)))
  return Array.from(set)
})

function crossCell(dept, itemName) {
  const cell = dept.items?.[itemName]
  if (!cell) return '—'
  return Number(cell.total_fact).toLocaleString('ru-RU', {
    minimumFractionDigits: 0, maximumFractionDigits: 0,
  })
}

// ── Форматирование ───────────────────────────────────────────────────────────
const fmt = v =>
  v != null
    ? Number(v).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : '—'

function deviationClass(val) {
  const n = Number(val)
  if (n > 0) return 'text-emerald-600 font-medium'
  if (n < 0) return 'text-red-500 font-medium'
  return 'text-gray-500'
}

// ── Экспорт ──────────────────────────────────────────────────────────────────
const exportMap = {
  'rollup-dept': 'rollup-by-dept',
  'rollup-item': 'rollup-by-item',
  'rollup-quarter': 'rollup-by-quarter',
  'cross-dept-item': 'cross-dept-item',
  'slice-dept': 'slice-by-dept',
  'slice-contractor': 'slice-by-contractor',
}

const canExport = computed(() => !!exportMap[operation.value])

async function exportFile(format) {
  const reportType = exportMap[operation.value]
  if (!reportType) return

  const params = { format }
  if (operation.value === 'slice-dept') {
    if (!selectedDeptId.value) { error.value = 'Выберите отдел'; return }
    params.dept_id = selectedDeptId.value
  }
  if (operation.value === 'slice-contractor') {
    if (!selectedContrInn.value) { error.value = 'Выберите контрагента'; return }
    params.contr_inn = selectedContrInn.value
  }

  try {
    const resp = await axios.get(`${API_BASE}/export/${reportType}`, {
      params,
      responseType: 'blob',
    })
    const blob = new Blob([resp.data], {
      type: format === 'csv'
        ? 'text/csv;charset=utf-8'
        : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${reportType}.${format}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } catch (e) {
    error.value = 'Не удалось скачать файл'
    console.error(e)
  }
}

// ── Init ─────────────────────────────────────────────────────────────────────
// Операции, не требующие фильтров — применяем сразу при переключении вкладки
const AUTO_APPLY_OPS = new Set(['rollup-dept', 'rollup-item', 'rollup-quarter', 'cross-dept-item'])

onMounted(async () => {
  await loadDictionaries()
  await apply()
})

watch(operation, () => {
  // Сбрасываем предыдущий результат чтобы не показывать чужие данные
  result.value = null
  error.value = ''
  if (AUTO_APPLY_OPS.has(operation.value)) {
    apply()
  }
})
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">OLAP-анализ</h1>
      <p class="text-sm text-gray-500 mt-1">Многомерный анализ бюджета и документов</p>
    </div>

    <!-- Панель управления -->
    <OlapControls
      v-model:operation="operation"
      :departments="departments"
      :contractors="contractors"
      :items="items"
      :quarters="quarters"
      v-model:selectedDeptId="selectedDeptId"
      v-model:selectedContrInn="selectedContrInn"
      v-model:diceDeptId="diceDeptId"
      v-model:diceItemId="diceItemId"
      v-model:diceQuarter="diceQuarter"
      @apply="apply"
    />

    <!-- Кнопки экспорта -->
    <div v-if="canExport" class="flex gap-2 mb-4">
      <button
        @click="exportFile('csv')"
        class="px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors"
      >Скачать CSV</button>
      <button
        @click="exportFile('xlsx')"
        class="px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors"
      >Скачать Excel</button>
    </div>

    <!-- Ошибка -->
    <div v-if="error" class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg">
      {{ error }}
    </div>

    <!-- Загрузка -->
    <div v-if="loading" class="py-10 text-center text-gray-400 text-sm animate-pulse">
      Загрузка...
    </div>

    <!-- Результат -->
    <div v-else-if="result" class="space-y-6">
      <!-- График (для Roll-up и кросс-таблицы) -->
      <OlapChart
        v-if="chartInfo"
        :type="chartInfo.type"
        :data="chartInfo.data"
        :title="chartInfo.title"
      />

      <!-- Таблица для Roll-up операций -->
      <OlapTable
        v-if="tableColumns.length"
        :columns="tableColumns"
        :rows="tableRows"
      />

      <!-- Срез по отделу -->
      <template v-if="operation === 'slice-dept' && result.department">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
          <p class="text-xs text-gray-500 mb-1">Отдел</p>
          <p class="font-semibold text-gray-800">{{ result.department.dept_name }}</p>
        </div>
        <OlapTable
          title="Бюджет"
          :columns="[
            { key: 'item_name', label: 'Статья' },
            { key: 'budget_year', label: 'Год' },
            { key: 'budget_quarter', label: 'Квартал' },
            { key: 'plan_rub', label: 'План, ₽', format: 'number' },
            { key: 'fact_rub', label: 'Факт, ₽', format: 'number' },
          ]"
          :rows="result.budget"
        />
        <OlapTable
          title="Документы"
          :columns="[
            { key: 'doc_id', label: 'ID' },
            { key: 'doc_date', label: 'Дата', format: 'date' },
            { key: 'type_name', label: 'Тип' },
            { key: 'item_name', label: 'Статья' },
            { key: 'doc_amount', label: 'Сумма, ₽', format: 'number' },
            { key: 'contr_name', label: 'Контрагент' },
            { key: 'resp_emp_name', label: 'Ответственный' },
          ]"
          :rows="result.documents"
        />
      </template>

      <!-- Срез по контрагенту -->
      <template v-if="operation === 'slice-contractor' && result.contractor">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
          <p class="text-xs text-gray-500 mb-1">Контрагент</p>
          <p class="font-semibold text-gray-800">{{ result.contractor.contr_name }}</p>
          <p class="text-xs text-gray-500 mt-1">ИНН: {{ result.contractor.contr_inn }}</p>
        </div>
        <OlapTable
          title="Документы"
          :columns="[
            { key: 'doc_id', label: 'ID' },
            { key: 'doc_date', label: 'Дата', format: 'date' },
            { key: 'type_name', label: 'Тип' },
            { key: 'dept_name', label: 'Отдел' },
            { key: 'item_name', label: 'Статья' },
            { key: 'doc_amount', label: 'Сумма, ₽', format: 'number' },
            { key: 'resp_emp_name', label: 'Ответственный' },
          ]"
          :rows="result.documents"
        />
      </template>

      <!-- Dice -->
      <template v-if="operation === 'dice'">
        <OlapTable
          title="Бюджет (по фильтрам)"
          :columns="[
            { key: 'dept_name', label: 'Отдел' },
            { key: 'item_name', label: 'Статья' },
            { key: 'budget_year', label: 'Год' },
            { key: 'budget_quarter', label: 'Квартал' },
            { key: 'plan_rub', label: 'План, ₽', format: 'number' },
            { key: 'fact_rub', label: 'Факт, ₽', format: 'number' },
          ]"
          :rows="result.budget || []"
        />
        <OlapTable
          title="Документы (по фильтрам)"
          :columns="[
            { key: 'doc_id', label: 'ID' },
            { key: 'doc_date', label: 'Дата', format: 'date' },
            { key: 'dept_name', label: 'Отдел' },
            { key: 'item_name', label: 'Статья' },
            { key: 'type_name', label: 'Тип' },
            { key: 'doc_amount', label: 'Сумма, ₽', format: 'number' },
            { key: 'contr_name', label: 'Контрагент' },
          ]"
          :rows="result.documents || []"
        />
      </template>

      <!-- Drill-down по отделу -->
      <template v-if="operation === 'drilldown-dept' && result.department">
        <div class="grid grid-cols-4 gap-4">
          <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Отдел</p>
            <p class="font-semibold text-gray-800 text-sm">{{ result.department.dept_name }}</p>
          </div>
          <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Σ План</p>
            <p class="font-bold text-emerald-700">{{ fmt(result.summary?.total_plan) }} ₽</p>
          </div>
          <div class="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Σ Факт</p>
            <p class="font-bold text-amber-700">{{ fmt(result.summary?.total_fact) }} ₽</p>
          </div>
          <div class="bg-violet-50 border border-violet-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Сотрудников / Документов</p>
            <p class="font-bold text-violet-700">
              {{ result.summary?.employee_count }} / {{ result.summary?.doc_count }}
            </p>
          </div>
        </div>

        <OlapTable
          v-if="result.employees?.length"
          :title="`Сотрудники (${result.employees.length})`"
          :columns="[
            { key: 'last_name', label: 'Фамилия' },
            { key: 'first_name', label: 'Имя' },
            { key: 'position_name', label: 'Должность' },
            { key: 'salary', label: 'Зарплата, ₽', format: 'number' },
          ]"
          :rows="result.employees"
        />
        <OlapTable
          v-if="result.budget?.length"
          :title="`Бюджет (${result.budget.length})`"
          :columns="[
            { key: 'item_name', label: 'Статья' },
            { key: 'budget_year', label: 'Год' },
            { key: 'budget_quarter', label: 'Квартал' },
            { key: 'plan_rub', label: 'План, ₽', format: 'number' },
            { key: 'fact_rub', label: 'Факт, ₽', format: 'number' },
          ]"
          :rows="result.budget"
        />
        <OlapTable
          v-if="result.documents?.length"
          :title="`Документы (${result.documents.length})`"
          :columns="[
            { key: 'doc_id', label: 'ID' },
            { key: 'doc_date', label: 'Дата', format: 'date' },
            { key: 'type_name', label: 'Тип' },
            { key: 'item_name', label: 'Статья' },
            { key: 'doc_amount', label: 'Сумма, ₽', format: 'number' },
            { key: 'contr_name', label: 'Контрагент' },
            { key: 'resp_emp_name', label: 'Ответственный' },
          ]"
          :rows="result.documents"
        />
      </template>

      <!-- Кросс-таблица -->
      <template v-if="operation === 'cross-dept-item'">
        <div class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
          <div class="px-4 py-3 border-b border-gray-100 bg-gray-50">
            <h3 class="text-sm font-semibold text-gray-700">Отдел × Статья (факт, ₽)</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-50 border-b border-gray-100">
                  <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase sticky left-0 bg-gray-50">Отдел</th>
                  <th
                    v-for="name in crossItemNames"
                    :key="name"
                    class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase whitespace-nowrap"
                  >{{ name }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="!result.length">
                  <td :colspan="crossItemNames.length + 1" class="py-8 text-center text-gray-400">
                    Нет данных
                  </td>
                </tr>
                <tr
                  v-for="dept in result"
                  :key="dept.dept_id"
                  class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
                >
                  <td class="px-4 py-2.5 font-medium text-gray-800 sticky left-0 bg-white">
                    {{ dept.dept_name }}
                  </td>
                  <td
                    v-for="name in crossItemNames"
                    :key="name"
                    class="px-4 py-2.5 text-right text-gray-700"
                  >{{ crossCell(dept, name) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </div>

    <div v-else class="py-10 text-center text-gray-400 text-sm">
      Выберите операцию и нажмите «Применить»
    </div>
  </div>
</template>
