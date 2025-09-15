<template>
  <div class="home-container">
    <header class="header">
      <h1>学習トラッカー</h1>
    </header>

    <div class="main-content">
      <aside class="left-panel">
        <LearningForm 
          :records="records"
          :topics="topics"
          @record-saved="fetchRecordsAndTopics"
          @topic-saved="fetchRecordsAndTopics"
        />
      </aside>

      <section class="right-panel">
        <div class="filter-controls">
          <div class="filter-item">
            <label for="topic-filter">テーマ選択:</label>
            <select id="topic-filter" v-model="selectedTopicId">
              <option value="" disabled selected>テーマを選択してください</option>
              <option v-for="topic in topics" :key="topic.id" :value="topic.id">
                {{ topic.title }}
              </option>
            </select>
          </div>
          <div class="filter-item">
            <label for="month-filter">月選択:</label>
            <select id="month-filter" v-model="selectedMonth">
              <option v-for="month in availableMonths" :key="month" :value="month">
                {{ month }}
              </option>
            </select>
          </div>
        </div>

        <div class="chart-container">
          <LearningChart
            v-if="selectedMonth"
            :records="filteredRecordsByTopicAndMonth"
            :selected-month="selectedMonth"
          />
          <div v-else class="loading-message">
            <p>データを読み込み中...</p>
          </div>
        </div>

        <div class="list-container">
          <LearningRecordFilteredList
            :records="filteredRecordsByTopicAndMonth"
            :topics="topics"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import LearningForm from '@/components/LearningForm.vue';
import LearningChart from '@/components/LearningChart.vue';
import LearningRecordFilteredList from '@/components/LearningRecordFilteredList.vue';
import { getRecords, getTopics } from '@/api/api.js';

/**
 * @typedef {Object} LearningRecord
 * @property {number} id - 記録のID。
 * @property {number} topic - 関連するテーマのID。
 * @property {string} date - 学習記録の日付（'YYYY-MM-DD'）。
 * @property {number} minutes - 実績時間（分）。
 * @property {number} planned_minutes - 予定時間（分）。
 * @property {string} memo - 記録のメモ。
 */

/**
 * @typedef {Object} Topic
 * @property {number} id - テーマのID。
 * @property {string} title - テーマのタイトル。
 */

/**
 * @type {import('vue').Ref<Array<LearningRecord>>}
 * APIから取得したすべての学習記録を格納するリアクティブな配列。
 */
const records = ref([]);
/**
 * @type {import('vue').Ref<Array<Topic>>}
 * APIから取得したすべてのテーマを格納するリアクティブな配列。
 */
const topics = ref([]);

/**
 * @type {import('vue').Ref<string | number>}
 * フィルタリング用に選択されたテーマのID。
 */
const selectedTopicId = ref('');
/**
 * @type {import('vue').Ref<string>}
 * フィルタリング用に選択された月。形式は'YYYY-MM'。
 * onMountedで現在の月に更新します。
 */
const selectedMonth = ref('');

/**
 * @function fetchRecordsAndTopics
 * APIから学習記録とテーマのリストを両方とも非同期で取得する関数。
 * 取得に成功すると、`records`と`topics`のリアクティブな参照が更新されます。
 * @async
 * @returns {Promise<void>}
 */
const fetchRecordsAndTopics = async () => {
  try {
    const [recordsResponse, topicsResponse] = await Promise.all([getRecords(), getTopics()]);
    records.value = recordsResponse.data;
    topics.value = topicsResponse.data;
    console.log('データを再取得しました。');
  } catch (error) {
    console.error('データの取得に失敗しました:', error);
  }
};

/**
 * @type {import('vue').ComputedRef<Array<string>>}
 * 2025年4月から現在月を含む3ヶ月未来までの月を生成する算出プロパティ。
 */
const availableMonths = computed(() => {
  const months = new Set();
  const today = new Date();
  const currentYear = today.getFullYear();
  const currentMonth = today.getMonth() + 1;

  // 過去の月（2025年4月以降）を追加
  const startYear = 2025;
  const startMonth = 4;
  let year = startYear;
  let month = startMonth;
  while (true) {
    const formattedMonth = String(month).padStart(2, '0');
    months.add(`${year}-${formattedMonth}`);

    if (year === currentYear && month === currentMonth) break;

    month++;
    if (month > 12) {
      month = 1;
      year++;
    }
  }

  // 未来の月（3ヶ月分）を追加
  for (let i = 0; i <= 3; i++) {
    const futureDate = new Date(today.getFullYear(), today.getMonth() + i, 1);
    const futureYear = futureDate.getFullYear();
    const futureMonth = (futureDate.getMonth() + 1).toString().padStart(2, '0');
    months.add(`${futureYear}-${futureMonth}`);
  }

  return [...months].sort();
});

/**
 * @type {import('vue').ComputedRef<Array<LearningRecord>>}
 * 選択されたテーマと月でフィルタリングされた学習記録のリスト。
 * このプロパティは、グラフとリストの両方のコンポーネントに渡されます。
 */
const filteredRecordsByTopicAndMonth = computed(() => {
  return records.value.filter(record => {
    const topicMatch = !selectedTopicId.value || record.topic === selectedTopicId.value;
    const recordMonth = record.date ? record.date.substring(0, 7) : '';
    const monthMatch = !selectedMonth.value || recordMonth === selectedMonth.value;
    return topicMatch && monthMatch;
  });
});

/**
 * コンポーネントがマウントされたときに実行されるライフサイクルフック。
 */
onMounted(async () => {
  await fetchRecordsAndTopics();
  // 初回ロード時に現在の月をデフォルト選択
  const today = new Date();
  const year = today.getFullYear();
  const month = (today.getMonth() + 1).toString().padStart(2, '0');
  selectedMonth.value = `${year}-${month}`;
});
</script>

---
### **スタイル修正**

```css
<style scoped>
.home-container {
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.main-content {
  display: flex;
  gap: 2rem;
  /* flexアイテムの折り返しを無効にすることで、必ず横並びにする */
  /* flex-wrap: wrap; */
  align-items: flex-start;
}

.left-panel {
  /* 幅を固定 */
  width: 300px;
}

.right-panel {
  /* calc() を使用して、親コンテナから左パネルの幅とギャップを引いた残りの幅を確保 */
  width: calc(100% - 300px - 2rem);
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.filter-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chart-container {
  /* グラフの縦幅・横幅を拡大 */
  width: 100%;
  height: 600px;
}

.list-container {
  /* 学習記録一覧の縦幅を拡大 */
  min-height: 400px;
}

.loading-message {
  text-align: center;
  padding: 20px;
  font-style: italic;
  color: #888;
}
</style>