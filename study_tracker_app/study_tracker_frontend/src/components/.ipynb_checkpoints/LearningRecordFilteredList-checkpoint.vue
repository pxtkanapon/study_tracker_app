<template>
  <div class="learning-record-list">
    <h3>学習記録一覧</h3>
    <div v-if="records.length > 0">
      <table>
        <thead>
          <tr>
            <th>日付</th>
            <th>テーマ</th>
            <th>計画時間 (分)</th>
            <th>実績時間 (分)</th>
            <th>メモ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in sortedRecords" :key="record.id">
            <td>{{ record.date }}</td>
            <td>{{ getTopicTitle(record.topic) }}</td>
            <td>{{ record.planned_minutes }}</td>
            <td>{{ record.minutes }}</td>
            <td>{{ record.memo }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="no-records">
      <p>この月にはまだ学習記録がありません。</p>
    </div>
  </div>
</template>

<script setup>
import { computed, toRefs } from 'vue';

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

const props = defineProps({
  /**
   * @type {Array<LearningRecord>}
   * フィルタリングされた学習記録の配列。
   */
  records: {
    type: Array,
    required: true,
  },
  /**
   * @type {Array<Topic>}
   * すべてのテーマの配列。
   */
  topics: {
    type: Array,
    required: true,
  },
});

const { records, topics } = toRefs(props);

/**
 * @type {import('vue').ComputedRef<Array<LearningRecord>>}
 * 日付の降順でソートされた学習記録の配列。
 */
const sortedRecords = computed(() => {
  return [...records.value].sort((a, b) => b.date.localeCompare(a.date));
});

/**
 * 指定されたトピックIDに対応するテーマのタイトルを取得する。
 * @param {number} topicId - 検索するテーマのID。
 * @returns {string} テーマのタイトル。見つからない場合は'不明'。
 */
const getTopicTitle = (topicId) => {
  const topic = topics.value.find((t) => t.id === topicId);
  return topic ? topic.title : '不明';
};
</script>

<style scoped>
.learning-record-list {
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h3 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #eee;
  padding-bottom: 0.5rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th,
td {
  padding: 0.75rem;
  border-bottom: 1px solid #ddd;
  text-align: left;
}

th {
  background-color: #f4f4f4;
  font-weight: bold;
  color: #555;
}

tr:hover {
  background-color: #f9f9f9;
}

.no-records {
  text-align: center;
  padding: 2rem;
  color: #888;
}
</style>