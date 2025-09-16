<template>
  <div class="learning-record-list">
    <h3>学習記録一覧</h3>
    <table>
      <thead>
        <tr>
          <th>日付</th>
          <th>テーマ</th>
          <th>予定 (分)</th>
          <th>実績 (分)</th>
          <th>メモ</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="record in records" :key="record.id">
          <td>{{ record.date }}</td>
          <td>{{ getTopicTitle(record.topic) }}</td>
          <td>{{ record.planned_minutes }}</td>
          <td>{{ record.minutes }}</td>
          <td>{{ record.memo }}</td>
          <td>
            <button class="edit-btn" @click="$emit('edit-record', record)">編集</button>
            <button class="delete-btn" @click="$emit('delete-record', record.id)">削除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

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
   * 表示する学習記録の配列。
   */
  records: {
    type: Array,
    required: true,
  },
  /**
   * @type {Array<Topic>}
   * 学習テーマの配列。テーマIDからタイトルを取得するために使用されます。
   */
  topics: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits([
  /**
   * @event edit-record
   * 編集ボタンがクリックされたときに発生するイベント。
   * @param {LearningRecord} record - 編集対象の学習記録オブジェクト。
   */
  'edit-record',
  /**
   * @event delete-record
   * 削除ボタンがクリックされたときに発生するイベント。
   * @param {number} recordId - 削除対象の学習記録のID。
   */
  'delete-record',
]);

/**
 * テーマIDからテーマのタイトルを取得するヘルパー関数。
 * @param {number} topicId - 検索するテーマのID。
 * @returns {string} 見つかったテーマのタイトル、または'不明'。
 */
const getTopicTitle = (topicId) => {
  const topic = props.topics.find(t => t.id === topicId);
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

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f4f4f4;
  font-weight: bold;
}

tr:hover {
  background-color: #f1f1f1;
}

.edit-btn, .delete-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.edit-btn {
  background-color: #ffc107;
  color: #fff;
}

.delete-btn {
  background-color: #dc3545;
  color: #fff;
}
</style>