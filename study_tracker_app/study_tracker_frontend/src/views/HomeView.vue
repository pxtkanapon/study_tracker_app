<template>
  <div class="home-container">
    <header class="header">
      <h1>学習トラッカー</h1>
    </header>

    <div class="main-content">
      <aside class="left-panel">
        <Calendar 
          :records="records"
          :initialMonth="selectedMonth"
          @date-selected="handleDateSelected"
          @month-changed="handleMonthChanged"
        />
        <LearningForm 
          :records="records"
          :topics="topics"
          :editingRecord="editingRecord"
          @record-saved="handleRecordSaved"
          @topic-saved="fetchRecordsAndTopics"
          @cancel-edit="cancelEdit"
        />
      </aside>

      <section class="right-panel">
        <div class="filter-controls">
          <div class="filter-item">
            <label for="topic-filter">テーマ選択:</label>
            <select id="topic-filter" v-model="selectedTopicId">
              <option value="" disabled selected>テーマを選択してください</option>
              <option value="">全テーマを表示</option>
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
            @edit-record="handleEditRecord"
            @delete-record="handleDeleteRecord"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import LearningForm from '@/components/LearningForm.vue';
import LearningChart from '@/components/LearningChart.vue';
import LearningRecordFilteredList from '@/components/LearningRecordFilteredList.vue';
import Calendar from '@/components/Calendar.vue';
import { getRecords, getTopics, deleteRecord } from '@/api/api.js';
import { format } from 'date-fns';

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
 * コンポーネントの初期化時に当月に設定されます。
 */
const selectedMonth = ref(format(new Date(), 'yyyy-MM'));

/**
 * @type {import('vue').Ref<LearningRecord | null>}
 * 編集対象の記録を格納するリアクティブな変数。
 */
const editingRecord = ref(null);

/**
 * @function fetchRecordsAndTopics
 * APIから学習記録とテーマのリストを両方とも非同期で取得する関数。
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
 */
const filteredRecordsByTopicAndMonth = computed(() => {
  return records.value.filter(record => {
    // テーマのフィルタリング
    const topicMatch = !selectedTopicId.value || record.topic === selectedTopicId.value;

    // 月のフィルタリング
    const recordMonth = record.date ? record.date.substring(0, 7) : '';
    const monthMatch = !selectedMonth.value || recordMonth === selectedMonth.value;

    // 実績時間（minutes）が0の場合でも表示されるように修正
    // 既存の record.minutes === 0 のチェックは不要
    const minutesMatch = record.minutes !== null && record.minutes >= 0;

    return topicMatch && monthMatch && minutesMatch;
  });
});

/**
 * カレンダーから日付が選択されたときに実行される関数。
 * @param {string} date - 選択された日付（'YYYY-MM-DD'形式）。
 */
const handleDateSelected = (date) => {
  selectedMonth.value = date.substring(0, 7);
  console.log(`カレンダーで選択された日付の月: ${selectedMonth.value}`);
};

/**
 * カレンダーで表示月が変更されたときに実行される関数。
 * @param {string} month - 選択された月（'YYYY-MM'形式）。
 */
const handleMonthChanged = (month) => {
  selectedMonth.value = month;
  console.log(`カレンダーで表示月が変更されました: ${selectedMonth.value}`);
};

/**
 * 学習記録の編集ボタンがクリックされたときに実行される関数。
 * @param {LearningRecord} record - 編集対象の学習記録オブジェクト。
 */
const handleEditRecord = (record) => {
  editingRecord.value = { ...record };
  console.log('編集する記録:', editingRecord.value);
};

/**
 * 学習記録の削除ボタンがクリックされたときに実行される関数。
 * @param {number} recordId - 削除対象の学習記録のID。
 * @async
 */
const handleDeleteRecord = async (recordId) => {
  if (confirm('本当にこの記録を削除しますか？')) {
    try {
      await deleteRecord(recordId);
      await fetchRecordsAndTopics();
      console.log('記録を削除しました。');
    } catch (error) {
      console.error('記録の削除に失敗しました:', error);
    }
  }
};

/**
 * 学習記録が保存された後に実行される関数。
 * @async
 */
const handleRecordSaved = async () => {
  await fetchRecordsAndTopics();
  cancelEdit();
};

/**
 * 編集をキャンセルし、フォームを初期状態に戻す関数。
 */
const cancelEdit = () => {
  editingRecord.value = null;
};

/**
 * コンポーネントがマウントされたときに実行されるライフサイクルフック。
 */
onMounted(async () => {
  await fetchRecordsAndTopics();
});
</script>
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
      height: 400px;
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