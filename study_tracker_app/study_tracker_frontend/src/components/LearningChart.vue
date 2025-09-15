<template>
  <div class="chart-container">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { ref, watch, computed} from 'vue';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale,
} from 'chart.js';

// Chart.jsのコンポーネントを登録
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale
);

/**
 * @typedef {Object} LearningRecord
 * @property {number} id - 記録のID。
 * @property {number} topic - 関連するテーマのID。
 * @property {string} date - 学習記録の日付（'YYYY-MM-DD'）。
 * @property {number} minutes - 実績時間（分）。
 * @property {number} planned_minutes - 予定時間（分）。
 */

/**
 * props定義。親コンポーネントからフィルタリングされた記録と月情報を受け取る。
 * @type {{ records: Array<LearningRecord>, selectedMonth: string }}
 */
const props = defineProps({
  records: {
    type: Array,
    required: true,
  },
  selectedMonth: {
    type: String,
    required: true,
  },
});

/**
 * チャートに表示するデータセットを計算する算出プロパティ。
 * @returns {Object} Chart.jsで描画するためのデータオブジェクト。
 */
const chartData = computed(() => {
  // 選択された月に一致する記録をフィルタリング
  const recordsInMonth = props.records.filter(
    (record) => record.date.startsWith(props.selectedMonth)
  );

  // 月の最初の日から最後の日までの日付配列を作成
  const year = parseInt(props.selectedMonth.substring(0, 4));
  const month = parseInt(props.selectedMonth.substring(5, 7));
  const daysInMonth = new Date(year, month, 0).getDate();
  const labels = Array.from({ length: daysInMonth }, (_, i) => i + 1);

  // 日ごとの予定時間と実績時間を集計
  const plannedData = new Array(daysInMonth).fill(0);
  const actualData = new Array(daysInMonth).fill(0);

  recordsInMonth.forEach((record) => {
    const day = parseInt(record.date.substring(8, 10)) - 1;
    plannedData[day] += record.planned_minutes;
    actualData[day] += record.minutes;
  });

  return {
    labels: labels,
    datasets: [
      {
        label: '予定',
        backgroundColor: '#42A5F5',
        borderColor: '#42A5F5',
        data: plannedData,
      },
      {
        label: '実績',
        backgroundColor: '#66BB6A',
        borderColor: '#66BB6A',
        data: actualData,
      },
    ],
  };
});

/**
 * チャートのオプション設定。
 * @type {Object}
 */
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'テーマ別 月間学習時間',
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed.y !== null) {
            label += context.parsed.y + ' 分';
          }
          return label;
        },
      },
    },
  },
});
</script>

<style scoped>
.chart-container {
  height: 300px;
  width: 400px;
}
</style>