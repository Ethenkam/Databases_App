<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../services/api'

const activeTab = ref('dept')

const tabs = [
  { key: 'dept',    label: 'По отделам' },
  { key: 'item',    label: 'По статьям' },
  { key: 'quarter', label: 'По кварталам' },
  { key: 'drill',   label: 'Детализация по отделу' },
]

// ── Rollup by dept ─────────────────────────────────────────────────────────────
const deptData   = ref([])
const deptLoad   = ref(false)

async function loadDept() {
  deptLoad.value = true
  try { deptData.value = await api.olap.rollupByDept() }
  catch { deptData.value = [] }
  finally { deptLoad.value = false }
}

// ── Rollup by item ─────────────────────────────────────────────────────────────
const itemData = ref([])
const itemLoad = ref(false)

async function loadItem() {
  itemLoad.value = true
  try { itemData.value = await api.olap.rollupByItem() }
  catch { itemData.value = [] }
  finally { itemLoad.value = false }
}

// ── Rollup by quarter ──────────────────────────────────────────────────────────
const quarterData = ref([])
const quarterLoad = ref(false)

async function loadQuarter() {
  quarterLoad.value = true
  try { quarterData.value = await api.olap.rollupByQuarter() }
  catch { quarterData.value = [] }
  finally { quarterLoad.value = false }
}

// ── Drilldown by dept ──────────────────────────────────────────────────────────
const deptOptions    = ref([])
const selectedDeptId = ref(null)
const drillData      = ref(null)
const drillLoad      = ref(false)

async function loadDrilldown() {
  if (!selectedDeptId.value) return
  drillLoad.value = true
  drillData.value = null
  try { drillData.value = await api.olap.drilldownDept(selectedDeptId.value) }
  catch { drillData.value = null }
  finally { drillLoad.value = false }
}

// ── Init ───────────────────────────────────────────────────────────────────────
onMounted(async () => {
  const depts = await api.getAll('department', 1, 1000)
  deptOptions.value = depts.items.map(d => ({ value: d.dept_id, label: d.dept_name }))
  await Promise.all([loadDept(), loadItem(), loadQuarter()])
})

function setTab(key) {
  activeTab.value = key
}

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
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">OLAP-анализ</h1>
      <p class="text-sm text-gray-500 mt-1">Многомерный анализ бюджета и документов</p>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 mb-6 bg-gray-100 p-1 rounded-xl w-fit">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="setTab(tab.key)"
        class="px-4 py-2 text-sm font-medium rounded-lg transition-colors"
        :class="activeTab === tab.key
          ? 'bg-white text-blue-600 shadow-sm'
          : 'text-gray-500 hover:text-gray-700'"
      >{{ tab.label }}</button>
    </div>

    <!-- ── Rollup by Dept ─────────────────────────────────────────────────────── -->
    <div v-show="activeTab === 'dept'">
      <div v-if="deptLoad" class="py-10 text-center text-gray-400 text-sm animate-pulse">Загрузка...</div>
      <div v-else class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100">
              <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Отдел</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ План, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ Факт, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Отклонение, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Документов</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!deptData.length">
              <td colspan="5" class="py-8 text-center text-gray-400">Нет данных</td>
            </tr>
            <tr
              v-for="row in deptData"
              :key="row.dept_id"
              class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
            >
              <td class="px-4 py-2.5 font-medium text-gray-800">{{ row.dept_name }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_plan) }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_fact) }}</td>
              <td class="px-4 py-2.5 text-right" :class="deviationClass(row.deviation)">{{ fmt(row.deviation) }}</td>
              <td class="px-4 py-2.5 text-right text-gray-600">{{ row.doc_count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Rollup by Item ─────────────────────────────────────────────────────── -->
    <div v-show="activeTab === 'item'">
      <div v-if="itemLoad" class="py-10 text-center text-gray-400 text-sm animate-pulse">Загрузка...</div>
      <div v-else class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100">
              <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Статья</th>
              <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Категория</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ План, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ Факт, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Отклонение, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Документов</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!itemData.length">
              <td colspan="6" class="py-8 text-center text-gray-400">Нет данных</td>
            </tr>
            <tr
              v-for="row in itemData"
              :key="row.item_id"
              class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
            >
              <td class="px-4 py-2.5 font-medium text-gray-800">{{ row.item_name }}</td>
              <td class="px-4 py-2.5 text-gray-500 text-xs">{{ row.item_category || '—' }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_plan) }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_fact) }}</td>
              <td class="px-4 py-2.5 text-right" :class="deviationClass(row.deviation)">{{ fmt(row.deviation) }}</td>
              <td class="px-4 py-2.5 text-right text-gray-600">{{ row.doc_count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Rollup by Quarter ──────────────────────────────────────────────────── -->
    <div v-show="activeTab === 'quarter'">
      <div v-if="quarterLoad" class="py-10 text-center text-gray-400 text-sm animate-pulse">Загрузка...</div>
      <div v-else class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100">
              <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Год</th>
              <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Квартал</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ План, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ Факт, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Отклонение, ₽</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!quarterData.length">
              <td colspan="5" class="py-8 text-center text-gray-400">Нет данных</td>
            </tr>
            <tr
              v-for="row in quarterData"
              :key="`${row.budget_year}-${row.budget_quarter}`"
              class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
            >
              <td class="px-4 py-2.5 font-medium text-gray-800">{{ row.budget_year }}</td>
              <td class="px-4 py-2.5 text-gray-600">Q{{ row.budget_quarter }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_plan) }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_fact) }}</td>
              <td class="px-4 py-2.5 text-right" :class="deviationClass(row.deviation)">{{ fmt(row.deviation) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Drilldown by Dept ──────────────────────────────────────────────────── -->
    <div v-show="activeTab === 'drill'">
      <div class="flex items-center gap-3 mb-5">
        <label class="text-sm font-medium text-gray-600">Выберите отдел:</label>
        <select
          v-model="selectedDeptId"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 min-w-[220px]"
        >
          <option :value="null">— выберите —</option>
          <option v-for="opt in deptOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
        </select>
        <button
          @click="loadDrilldown"
          :disabled="!selectedDeptId"
          class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >Загрузить</button>
      </div>

      <div v-if="drillLoad" class="py-10 text-center text-gray-400 text-sm animate-pulse">Загрузка...</div>

      <div v-else-if="drillData" class="space-y-6">
        <!-- Summary -->
        <div class="grid grid-cols-4 gap-4">
          <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Отдел</p>
            <p class="font-semibold text-gray-800 text-sm">{{ drillData.department?.dept_name }}</p>
          </div>
          <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Σ План</p>
            <p class="font-bold text-emerald-700">{{ fmt(drillData.summary?.total_plan) }} ₽</p>
          </div>
          <div class="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Σ Факт</p>
            <p class="font-bold text-amber-700">{{ fmt(drillData.summary?.total_fact) }} ₽</p>
          </div>
          <div class="bg-violet-50 border border-violet-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Сотрудников / Документов</p>
            <p class="font-bold text-violet-700">
              {{ drillData.summary?.employee_count }} / {{ drillData.summary?.doc_count }}
            </p>
          </div>
        </div>

        <!-- Employees -->
        <div v-if="drillData.employees?.length" class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
          <div class="px-4 py-3 border-b border-gray-100 bg-gray-50">
            <h3 class="text-sm font-semibold text-gray-700">Сотрудники ({{ drillData.employees.length }})</h3>
          </div>
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-100">
                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-500 uppercase">ФИО</th>
                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-500 uppercase">Должность</th>
                <th class="px-4 py-2 text-right text-xs font-semibold text-gray-500 uppercase">Зарплата, ₽</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="e in drillData.employees"
                :key="e.emp_id"
                class="border-b border-gray-50 last:border-0 hover:bg-blue-50/20"
              >
                <td class="px-4 py-2 text-gray-800">{{ e.last_name }} {{ e.first_name }}</td>
                <td class="px-4 py-2 text-gray-600 text-xs">{{ e.position_name }}</td>
                <td class="px-4 py-2 text-right text-gray-700">{{ fmt(e.salary) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Budget -->
        <div v-if="drillData.budget?.length" class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
          <div class="px-4 py-3 border-b border-gray-100 bg-gray-50">
            <h3 class="text-sm font-semibold text-gray-700">Бюджет ({{ drillData.budget.length }} строк)</h3>
          </div>
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-100">
                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-500 uppercase">Статья</th>
                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-500 uppercase">Период</th>
                <th class="px-4 py-2 text-right text-xs font-semibold text-gray-500 uppercase">План, ₽</th>
                <th class="px-4 py-2 text-right text-xs font-semibold text-gray-500 uppercase">Факт, ₽</th>
                <th class="px-4 py-2 text-right text-xs font-semibold text-gray-500 uppercase">Откл., ₽</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="b in drillData.budget"
                :key="`${b.item_id}-${b.budget_year}-${b.budget_quarter}`"
                class="border-b border-gray-50 last:border-0 hover:bg-blue-50/20"
              >
                <td class="px-4 py-2 text-gray-800">{{ b.item_name }}</td>
                <td class="px-4 py-2 text-gray-500 text-xs">{{ b.budget_year }} Q{{ b.budget_quarter }}</td>
                <td class="px-4 py-2 text-right text-gray-700">{{ fmt(b.plan_rub) }}</td>
                <td class="px-4 py-2 text-right text-gray-700">{{ fmt(b.fact_rub) }}</td>
                <td class="px-4 py-2 text-right" :class="deviationClass(Number(b.plan_rub) - Number(b.fact_rub))">
                  {{ fmt(Number(b.plan_rub) - Number(b.fact_rub)) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-else-if="!drillLoad && !drillData && selectedDeptId" class="py-10 text-center text-gray-400 text-sm">
        Нет данных
      </div>
      <div v-else-if="!selectedDeptId" class="py-10 text-center text-gray-400 text-sm">
        Выберите отдел для детализации
      </div>
    </div>
  </div>
</template>
