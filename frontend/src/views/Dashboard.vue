<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { api } from '../services/api'

const router = useRouter()

const cards = [
  { label: 'Сотрудники',     endpoint: 'employee',    path: '/employees',   color: 'blue' },
  { label: 'Отделы',          endpoint: 'department',  path: '/departments', color: 'indigo' },
  { label: 'Документы',       endpoint: 'document',    path: '/documents',   color: 'violet' },
  { label: 'Бюджет',          endpoint: 'budget',      path: '/budget',      color: 'emerald' },
  { label: 'Контрагенты',     endpoint: 'contractor',  path: '/contractors', color: 'amber' },
  { label: 'Должности',       endpoint: 'position',    path: '/positions',   color: 'sky' },
  { label: 'Статьи бюджета',  endpoint: 'budget-item', path: null,           color: 'teal' },
  { label: 'Типы документов', endpoint: 'doc-type',    path: null,           color: 'rose' },
]

const counts = ref({})
const loading = ref(true)

const colors = {
  blue:    { wrap: 'bg-blue-50 border-blue-200',     num: 'text-blue-600',    btn: 'bg-blue-600 hover:bg-blue-700' },
  indigo:  { wrap: 'bg-indigo-50 border-indigo-200', num: 'text-indigo-600',  btn: 'bg-indigo-600 hover:bg-indigo-700' },
  violet:  { wrap: 'bg-violet-50 border-violet-200', num: 'text-violet-600',  btn: 'bg-violet-600 hover:bg-violet-700' },
  emerald: { wrap: 'bg-emerald-50 border-emerald-200', num: 'text-emerald-600', btn: 'bg-emerald-600 hover:bg-emerald-700' },
  amber:   { wrap: 'bg-amber-50 border-amber-200',   num: 'text-amber-600',   btn: 'bg-amber-600 hover:bg-amber-700' },
  sky:     { wrap: 'bg-sky-50 border-sky-200',       num: 'text-sky-600',     btn: 'bg-sky-600 hover:bg-sky-700' },
  teal:    { wrap: 'bg-teal-50 border-teal-200',     num: 'text-teal-600',    btn: 'bg-teal-600 hover:bg-teal-700' },
  rose:    { wrap: 'bg-rose-50 border-rose-200',     num: 'text-rose-600',    btn: 'bg-rose-600 hover:bg-rose-700' },
}

onMounted(async () => {
  const results = await Promise.allSettled(
    cards.map(c => api.getAll(c.endpoint, 1, 1))
  )
  results.forEach((r, i) => {
    counts.value[cards[i].endpoint] = r.status === 'fulfilled' ? r.value.total : '?'
  })
  loading.value = false
})
</script>

<template>
  <div class="p-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800">Дашборд</h1>
      <p class="text-sm text-gray-500 mt-1">Обзор данных учётной системы</p>
    </div>

    <!-- Stat cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
      <div
        v-for="card in cards"
        :key="card.endpoint"
        class="rounded-xl border p-5 flex flex-col gap-3"
        :class="colors[card.color].wrap"
      >
        <p class="text-sm font-medium text-gray-600">{{ card.label }}</p>
        <p class="text-3xl font-bold tracking-tight" :class="colors[card.color].num">
          <span v-if="loading" class="opacity-30">—</span>
          <span v-else>{{ counts[card.endpoint] ?? '?' }}</span>
        </p>
        <button
          v-if="card.path"
          @click="router.push(card.path)"
          class="mt-auto text-xs text-white px-3 py-1.5 rounded-lg font-medium transition-colors"
          :class="colors[card.color].btn"
        >
          Перейти →
        </button>
        <span v-else class="mt-auto text-xs text-gray-400 italic">Справочник</span>
      </div>
    </div>

    <!-- Quick nav -->
    <div>
      <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Быстрый переход</h2>
      <div class="flex flex-wrap gap-2">
        <RouterLink
          v-for="item in [
            { path: '/employees',   label: 'Сотрудники' },
            { path: '/departments', label: 'Отделы' },
            { path: '/documents',   label: 'Документы' },
            { path: '/budget',      label: 'Бюджет' },
            { path: '/contractors', label: 'Контрагенты' },
            { path: '/positions',   label: 'Должности' },
            { path: '/olap',        label: 'OLAP-анализ' },
          ]"
          :key="item.path"
          :to="item.path"
          class="px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm text-gray-700 hover:border-blue-400 hover:text-blue-600 transition-colors shadow-sm"
        >
          {{ item.label }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>
