<script setup>
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { path: '/',            label: 'Дашборд',      icon: '▦' },
  { path: '/employees',   label: 'Сотрудники',   icon: '◉' },
  { path: '/departments', label: 'Отделы',        icon: '⊞' },
  { path: '/documents',   label: 'Документы',    icon: '◧' },
  { path: '/budget',      label: 'Бюджет',       icon: '◈' },
  { path: '/contractors', label: 'Контрагенты',  icon: '◎' },
  { path: '/positions',   label: 'Должности',    icon: '◉' },
  { path: '/olap',        label: 'OLAP-анализ',  icon: '◫' },
]

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<template>
  <aside class="w-56 bg-slate-900 text-white flex flex-col min-h-screen shrink-0">
    <div class="px-5 py-5 border-b border-slate-700">
      <h1 class="text-base font-bold text-white tracking-wide">Бухгалтерия</h1>
      <p class="text-xs text-slate-500 mt-0.5">Учётная система</p>
    </div>

    <nav class="flex-1 py-3">
      <RouterLink
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-5 py-2.5 text-sm transition-colors"
        :class="isActive(item.path)
          ? 'bg-blue-600 text-white font-medium'
          : 'text-slate-400 hover:bg-slate-800 hover:text-white'"
      >
        <span class="text-base w-4 text-center select-none">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <div class="px-5 py-4 border-t border-slate-700">
      <p class="text-xs text-slate-600">v0.1.0</p>
    </div>
  </aside>
</template>
