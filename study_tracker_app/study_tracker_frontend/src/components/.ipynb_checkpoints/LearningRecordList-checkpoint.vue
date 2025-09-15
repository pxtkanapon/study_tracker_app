<template>
  <div class="record-list">
    <h2>学習記録一覧</h2>
    <p v-if="records.length === 0">まだ学習記録がありません。</p>
    <ul v-else>
      <li v-for="record in records" :key="record.id" class="record-item">
        <div class="record-details">
          <strong>{{ getTopicTitle(record.topic) }}</strong>
          <span> ({{ record.date }}): {{ record.minutes }} 分</span>
          <p v-if="record.memo">{{ record.memo }}</p>
        </div>
        <div class="record-actions">
          <button @click="editRecord(record)" class="edit-button">編集</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

/**
 * @typedef {Object} LearningRecord
 * @property {number} id - 記録のID。
 * @property {number} topic - 関連するテーマのID。
 * @property {string} date - 学習記録の日付。
 * @property {number} minutes - 学習時間（分）。
 * @property {string} memo - 記録のメモ。
 */

/**
 * @typedef {Object} Topic
 * @property {number} id - テーマのID。
 * @property {string} title - テーマのタイトル。
 */

/**
 * props定義。親コンポーネントから記録とテーマリストを受け取る。
 * @type {{ records: Array<LearningRecord>, topics: Array<Topic> }}
 */
const props = defineProps({
  records: {
    type: Array,
    required: true,
  },
  topics: {
    type: Array,
    required: true,
  },
});

/**
 * emits定義。編集イベントを親コンポーネントに通知する。
 * @type {(event: 'edit-record', record: LearningRecord) => void}
 */
const emit = defineEmits(['edit-record']);

/**
 * テーマIDからテーマ名を取得するヘルパー関数。
 * @param {number} topicId - テーマのID。
 * @returns {string} テーマのタイトル。見つからない場合は'不明なテーマ'。
 */
const getTopicTitle = (topicId) => {
  const topic = props.topics.find((t) => t.id === topicId);
  return topic ? topic.title : '不明なテーマ';
};

/**
 * 編集ボタンがクリックされたときに、レコードを親コンポーネントに送る関数。
 * @param {LearningRecord} record - 編集対象の学習記録。
 */
const editRecord = (record) => {
  emit('edit-record', record);
};
</script>

<style scoped>
.record-list {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.record-item:last-child {
  border-bottom: none;
}

.record-details strong {
  font-size: 1.1em;
}

.edit-button {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 4px;
}
</style>