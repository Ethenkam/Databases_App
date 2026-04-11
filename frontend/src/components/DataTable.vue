<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  columns:  { type: Array,   required: true },
  rows:     { type: Array,   default: () => [] },
  total:    { type: Number,  default: 0 },
  page:     { type: Number,  default: 1 },
  pageSize: { type: Number,  default: 20 },
  loading:  { type: Boolean, default: false },
})

const emit = defineEmits(['update:page', 'add', 'edit', 'delete'])

const sortKey = ref('')
const sortDir = ref('asc')

function toggleSort(key) {
  if (sortKey.value === key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortDir.value = 'asc'
  }
}

const sortedRows = computed(() => {
  if (!sortKey.value) return props.rows
  const col = props.columns.find(c => c.key === sortKey.value)
  return [...props.rows].sort((a, b) => {
    const va = col?.render ? col.render(a) : (a[sortKey.value] ?? '')
    const vb = col?.render ? col.render(b) : (b[sortKey.value] ?? '')
    if (va === vb) return 0
    const cmp = String(va).localeCompare(String(vb), 'ru', { numeric: true })
    return sortDir.value === 'asc' ? cmp : -cmp
  })
})

const totalPages = computed(() => Math.max(1, Math.ceil(props.total / props.pageSize)))

const pageNumbers = computed(() => {
  const tp = totalPages.value
  const cur = props.page
  if (tp <= 7) return Array.from({ length: tp }, (_, i) => i + 1)
  const set = new Set([1, tp, cur])
  if (cur > 1) set.add(cur - 1)
  if (cur < tp) set.add(cur + 1)
  return [...set].sort((a, b) => a - b)
})

function cellValue(col, row) {
  if (col.render) return col.render(row)
  const v = row[col.key]
  return v !== null && v !== undefined ? v : '—'
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">

    <!-- Toolbar -->
    <div class="flex items-center justify-between px-5 py-3 border-b border-gray-100 bg-gray-50/60">
      <span class="text-sm text-gray-500">Всего записей: <strong class="text-gray-700">{{ total }}</strong></span>
      <button
        @click="$emit('add')"
        class="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 active:bg-blue-800 transition-colors"
      >
        <span class="text-lg leading-none">+</span> Добавить
      </button>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-100">
            <th
              v-for="col in columns"
              :key="col.key"
              class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap cursor-pointer select-none hover:bg-gray-50 transition-colors"
              @click="toggleSort(col.key)"
            >
              {{ col.label }}
              <span v-if="sortKey === col.key" class="ml-1 text-blue-500 font-bold">
                {{ sortDir === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide w-32">
              Действия
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td :colspan="columns.length + 1" class="py-12 text-center text-gray-400 text-sm">
              <span class="inline-block animate-pulse">Загрузка данных...</span>
            </td>
          </tr>
          <tr v-else-if="!sortedRows.length">
            <td :colspan="columns.length + 1" class="py-12 text-center text-gray-400 text-sm">
              Нет данных
            </td>
          </tr>
          <tr
            v-else
            v-for="(row, i) in sortedRows"
            :key="i"
            class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              class="px-4 py-2.5 text-gray-700 whitespace-nowrap max-w-[220px] truncate"
              :title="String(cellValue(col, row))"
            >
              {{ cellValue(col, row) }}
            </td>
            <td class="px-4 py-2.5 text-right whitespace-nowrap">
              <button
                @click="$emit('edit', row)"
                class="text-blue-600 hover:text-blue-800 text-xs font-medium mr-3 transition-colors"
              >
                Изменить
              </button>
              <button
                @click="$emit('delete', row)"
                class="text-red-500 hover:text-red-700 text-xs font-medium transition-colors"
              >
                Удалить
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-between px-5 py-3 border-t border-gray-100 bg-gray-50/60">
      <span class="text-sm text-gray-500">
        Страница {{ page }} из {{ totalPages }}
      </span>
      <div class="flex items-center gap-1">
        <button
          :disabled="page <= 1"
          @click="$emit('update:page', page - 1)"
          class="px-2.5 py-1.5 text-sm rounded-lg border border-gray-200 bg-white hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >←</button>

        <template v-for="(num, idx) in pageNumbers" :key="num">
          <span
            v-if="idx > 0 && pageNumbers[idx - 1] < num - 1"
            class="px-1.5 text-gray-400 text-sm select-none"
          >…</span>
          <button
            @click="$emit('update:page', num)"
            class="px-2.5 py-1.5 text-sm rounded-lg border transition-colors min-w-[36px]"
            :class="num === page
              ? 'bg-blue-600 text-white border-blue-600 font-medium'
              : 'bg-white border-gray-200 hover:bg-gray-50 text-gray-700'"
          >{{ num }}</button>
        </template>

        <button
          :disabled="page >= totalPages"
          @click="$emit('update:page', page + 1)"
          class="px-2.5 py-1.5 text-sm rounded-lg border border-gray-200 bg-white hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >→</button>
      </div>
    </div>
  </div>
</template>
