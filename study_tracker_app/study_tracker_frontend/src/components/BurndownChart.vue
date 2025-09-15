<script setup>
import { Line } from 'vue-chartjs';
import { computed } from 'vue';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

const props = defineProps({
  /** 学習記録データの配列。 */
  records: Array,
  /** 目標とする総学習時間。 */
  totalHours: Number, 
});

/** チャート表示用のデータを計算します。 */
const chartData = computed(() => {
  if (!props.records || props.records.length === 0) {
    return { labels: [], datasets: [] };
  }
  const sortedRecords = [...props.records].sort((a, b) => new Date(a.date) - new Date(b.date));
  const plannedData = [];
  const actualData = [];
  const dates = [];
  let remainingPlanned = props.totalHours;
  let remainingActual = props.totalHours;

  sortedRecords.forEach(record => {
    dates.push(record.date);
    remainingPlanned -= parseFloat(record.planned_hours);
    remainingActual -= parseFloat(record.actual_hours);
    plannedData.push(remainingPlanned);
    actualData.push(remainingActual);
  });

  return {
    labels: dates,
    datasets: [
      {
        label: '残りの予定時間 (h)',
        borderColor: '#f87979',
        data: plannedData,
      },
      {
        label: '残りの実績時間 (h)',
        borderColor: '#007bff',
        data: actualData,
      }
    ],
  };
});
const chartOptions = { responsive: true, maintainAspectRatio: false };
</script>

<template>
  <Line :data="chartData" :options="chartOptions" />
</template>