<script setup>
import { computed } from 'vue'

const props = defineProps({
  operation: { type: String, required: true },
  departments: { type: Array, default: () => [] },
  contractors: { type: Array, default: () => [] },
  items: { type: Array, default: () => [] },
  quarters: { type: Array, default: () => [] },
  selectedDeptId: { type: [Number, null], default: null },
  selectedContrInn: { type: [String, null], default: null },
  diceDeptId: { type: [Number, null], default: null },
  diceItemId: { type: [Number, null], default: null },
  diceQuarter: { type: [String, null], default: null },
})

const emit = defineEmits([
  'update:operation',
  'update:selectedDeptId',
  'update:selectedContrInn',
  'update:diceDeptId',
  'update:diceItemId',
  'update:diceQuarter',
  'apply',
])

const operations = [
  { key: 'rollup-dept',       label: 'Roll-up по отделу' },
  { key: 'rollup-item',       label: 'Roll-up по статье' },
  { key: 'rollup-quarter',    label: 'Roll-up по кварталу' },
  { key: 'slice-dept',        label: 'Срез по отделу' },
  { key: 'slice-contractor',  label: 'Срез по контрагенту' },
  { key: 'dice',              label: 'Dice' },
  { key: 'drilldown-dept',    label: 'Drill-down по отделу' },
  { key: 'cross-dept-item',   label: 'Кросс-таблица Отдел × Статья' },
]

const showDeptSelect = computed(() =>
  ['slice-dept', 'drilldown-dept'].includes(props.operation)
)
const showContractorSelect = computed(() => props.operation === 'slice-contractor')
const showDice = computed(() => props.operation === 'dice')

// Безопасные парсеры: Vue 3 убирает атрибут value при :value="null",
// из-за чего $event.target.value возвращает текст опции (truthy строку).
// Используем явную проверку на пустую строку.
function toIntOrNull(raw) {
  if (raw === '' || raw === null || raw === undefined) return null
  const n = Number(raw)
  return isNaN(n) ? null : n
}

function toStrOrNull(raw) {
  return (raw === '' || raw === null || raw === undefined) ? null : raw
}

function setOp(key) {
  emit('update:operation', key)
}
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-5 mb-6">
    <h2 class="text-sm font-semibold text-gray-700 mb-3">Операция</h2>
    <div class="flex flex-wrap gap-2 mb-4">
      <button
        v-for="op in operations"
        :key="op.key"
        @click="setOp(op.key)"
        class="px-3 py-1.5 text-sm font-medium rounded-lg border transition-colors"
        :class="operation === op.key
          ? 'bg-blue-600 text-white border-blue-600'
          : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'"
      >{{ op.label }}</button>
    </div>

    <!-- Фильтры -->
    <div class="flex flex-wrap items-end gap-4">
      <!-- Срез/Drill-down по отделу -->
      <div v-if="showDeptSelect" class="flex flex-col gap-1">
        <label class="text-xs font-medium text-gray-500">Отдел</label>
        <select
          :value="selectedDeptId ?? ''"
          @change="$emit('update:selectedDeptId', toIntOrNull($event.target.value))"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm min-w-[220px] focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">— выберите —</option>
          <option v-for="d in departments" :key="d.dept_id" :value="d.dept_id">
            {{ d.dept_name }}
          </option>
        </select>
      </div>

      <!-- Срез по контрагенту -->
      <div v-if="showContractorSelect" class="flex flex-col gap-1">
        <label class="text-xs font-medium text-gray-500">Контрагент</label>
        <select
          :value="selectedContrInn ?? ''"
          @change="$emit('update:selectedContrInn', toStrOrNull($event.target.value))"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm min-w-[260px] focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">— выберите —</option>
          <option v-for="c in contractors" :key="c.contr_inn" :value="c.contr_inn">
            {{ c.contr_name }} ({{ c.contr_inn }})
          </option>
        </select>
      </div>

      <!-- Dice -->
      <template v-if="showDice">
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-gray-500">Отдел</label>
          <select
            :value="diceDeptId ?? ''"
            @change="$emit('update:diceDeptId', toIntOrNull($event.target.value))"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm min-w-[200px] focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">— любой —</option>
            <option v-for="d in departments" :key="d.dept_id" :value="d.dept_id">
              {{ d.dept_name }}
            </option>
          </select>
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-gray-500">Статья</label>
          <select
            :value="diceItemId ?? ''"
            @change="$emit('update:diceItemId', toIntOrNull($event.target.value))"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm min-w-[200px] focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">— любая —</option>
            <option v-for="it in items" :key="it.item_id" :value="it.item_id">
              {{ it.item_name }}
            </option>
          </select>
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-gray-500">Квартал</label>
          <select
            :value="diceQuarter ?? ''"
            @change="$emit('update:diceQuarter', toStrOrNull($event.target.value))"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm min-w-[160px] focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">— любой —</option>
            <option v-for="q in quarters" :key="`${q.year}-${q.quarter}`" :value="`${q.year}-${q.quarter}`">
              {{ q.year }} Q{{ q.quarter }}
            </option>
          </select>
        </div>
      </template>

      <button
        @click="$emit('apply')"
        class="px-5 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
      >Применить</button>
    </div>
  </div>
</template>
