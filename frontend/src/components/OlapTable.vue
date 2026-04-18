<script setup>
const props = defineProps({
  columns: { type: Array, required: true },
  rows: { type: Array, default: () => [] },
  emptyText: { type: String, default: 'Нет данных' },
  title: { type: String, default: '' },
})

const fmt = v =>
  v != null && v !== ''
    ? (typeof v === 'number' || !isNaN(Number(v)))
      ? Number(v).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
      : v
    : '—'

function cellValue(row, col) {
  const val = row[col.key]
  if (col.format === 'number') return fmt(val)
  if (col.format === 'date' && val) return new Date(val).toLocaleDateString('ru-RU')
  return val ?? '—'
}

function cellClass(row, col) {
  if (col.format === 'number') return 'text-right text-gray-700'
  if (col.deviation) {
    const n = Number(row[col.key])
    if (n > 0) return 'text-right text-emerald-600 font-medium'
    if (n < 0) return 'text-right text-red-500 font-medium'
    return 'text-right text-gray-500'
  }
  return 'text-gray-700'
}
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
    <div v-if="title" class="px-4 py-3 border-b border-gray-100 bg-gray-50">
      <h3 class="text-sm font-semibold text-gray-700">{{ title }}</h3>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-100">
            <th
              v-for="col in columns"
              :key="col.key"
              class="px-4 py-2.5 text-xs font-semibold text-gray-500 uppercase tracking-wide"
              :class="col.format === 'number' ? 'text-right' : 'text-left'"
            >{{ col.label }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!rows.length">
            <td :colspan="columns.length" class="py-8 text-center text-gray-400">
              {{ emptyText }}
            </td>
          </tr>
          <tr
            v-for="(row, i) in rows"
            :key="i"
            class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              class="px-4 py-2.5"
              :class="cellClass(row, col)"
            >{{ cellValue(row, col) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
