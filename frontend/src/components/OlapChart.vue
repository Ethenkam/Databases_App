<script setup>
import { computed } from 'vue'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js'
import { Bar, Pie, Line } from 'vue-chartjs'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement,
)

const props = defineProps({
  type: { type: String, required: true }, // 'bar' | 'pie' | 'line' | 'stacked-bar'
  data: { type: Object, required: true },
  title: { type: String, default: '' },
})

const chartOptions = computed(() => {
  const base = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
      title: props.title
        ? { display: true, text: props.title, font: { size: 14, weight: '600' } }
        : { display: false },
    },
  }
  if (props.type === 'stacked-bar') {
    return {
      ...base,
      scales: {
        x: { stacked: true },
        y: { stacked: true, beginAtZero: true },
      },
    }
  }
  if (props.type === 'bar' || props.type === 'line') {
    return {
      ...base,
      scales: { y: { beginAtZero: true } },
    }
  }
  return base
})
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-4" style="height: 400px;">
    <Bar v-if="type === 'bar' || type === 'stacked-bar'" :data="data" :options="chartOptions" />
    <Pie v-else-if="type === 'pie'" :data="data" :options="chartOptions" />
    <Line v-else-if="type === 'line'" :data="data" :options="chartOptions" />
    <div v-else class="flex items-center justify-center h-full text-gray-400 text-sm">
      Неизвестный тип графика
    </div>
  </div>
</template>
