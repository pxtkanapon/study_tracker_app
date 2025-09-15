<template>
  <div class="learning-form">
    <h2>{{ isEditing ? '学習記録の編集' : '学習記録の追加' }}</h2>
    <form @submit.prevent="submitRecord">
      <div class="form-group">
        <label for="topic">テーマ:</label>
        <select id="topic" v-model="selectedTopic" required>
          <option disabled value="">テーマを選択してください</option>
          <option v-for="topic in topics" :key="topic.id" :value="topic.id">{{ topic.title }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="date">日付:</label>
        <input type="date" id="date" v-model="recordDate" required />
      </div>
      <div class="form-group">
        <label for="planned-minutes">予定時間 (分):</label>
        <input type="number" id="planned-minutes" v-model="plannedMinutes" min="0" />
      </div>
      <div class="form-group">
        <label for="actual-minutes">実績時間 (分):</label>
        <input type="number" id="actual-minutes" v-model="studyMinutes" min="0" />
      </div>
      <div class="form-group">
        <label for="memo">メモ:</label>
        <textarea id="memo" v-model="recordMemo"></textarea>
      </div>
      <button type="submit" class="submit-button">{{ isEditing ? '記録を更新' : '記録を保存' }}</button>
      <button v-if="isEditing" @click="cancelEdit" type="button" class="cancel-button">キャンセル</button>
    </form>

    <hr class="separator" />

    <h3>新しいテーマの追加</h3>
    <TopicForm @topic-saved="fetchTopics" />

    <hr class="separator" />

    <h3>テーマ名の修正</h3>
    <TopicEditForm :topics="topics" @topic-updated="fetchTopics" />

    <hr class="separator" />

    <LearningRecordList :records="records" :topics="topics" @edit-record="handleEdit" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getTopics, getRecords, createRecord, updateRecord } from '../api/api.js';
import TopicForm from './TopicForm.vue';
import TopicEditForm from './TopicEditForm.vue';
import LearningRecordList from './LearningRecordList.vue';

/**
 * 学習テーマのリストを格納するリアクティブな参照。
 * @type {import('vue').Ref<Array<Object>>}
 */
const topics = ref([]);

/**
 * 全ての学習記録を格納するリアクティブな参照。
 * @type {import('vue').Ref<Array<Object>>}
 */
const records = ref([]);

/**
 * 選択された学習テーマのID。
 * @type {import('vue').Ref<string>}
 */
const selectedTopic = ref('');

/**
 * 学習記録の日付。
 * @type {import('vue').Ref<string>}
 */
const recordDate = ref('');

/**
 * 学習時間（分） - 実績。
 * @type {import('vue').Ref<number|null>}
 */
const studyMinutes = ref(null);

/**
 * 学習時間（分） - 予定。
 * @type {import('vue').Ref<number|null>}
 */
const plannedMinutes = ref(null);

/**
 * 学習記録のメモ。
 * @type {import('vue').Ref<string>}
 */
const recordMemo = ref('');

/**
 * 編集中の学習記録のID。nullの場合は新規作成モード。
 * @type {import('vue').Ref<number|null>}
 */
const editingRecordId = ref(null);

/**
 * 現在が編集モードかどうかを示す真偽値。
 * @type {import('vue').Ref<boolean>}
 */
const isEditing = ref(false);

/**
 * バックエンドから学習テーマのリストを取得する非同期関数。
 * @async
 * @returns {Promise<void>}
 */
const fetchTopics = async () => {
  try {
    const response = await getTopics();
    topics.value = response.data;
  } catch (error) {
    console.error('テーマの取得に失敗しました:', error);
  }
};

/**
 * 全ての学習記録を取得する非同期関数。
 * @async
 * @returns {Promise<void>}
 */
const fetchRecords = async () => {
  try {
    const response = await getRecords();
    records.value = response.data;
  } catch (error) {
    console.error('学習記録の取得に失敗しました:', error);
  }
};

/**
 * 学習記録フォームのデータをバックエンドに送信（または更新）する非同期関数。
 * 既存の記録があるか日付とテーマで判定し、あれば更新、なければ新規作成します。
 * @async
 * @returns {Promise<void>}
 */
const submitRecord = async () => {
  try {
    // 既存の記録を検索
    const existingRecord = records.value.find(record =>
      record.topic === selectedTopic.value && record.date === recordDate.value
    );

    // 入力が空の場合、0として扱う
    const minutesToSave = studyMinutes.value === null ? 0 : studyMinutes.value;
    const plannedMinutesToSave = plannedMinutes.value === null ? 0 : plannedMinutes.value;

    const dataToSend = {
      topic: selectedTopic.value,
      date: recordDate.value,
      minutes: minutesToSave,
      planned_minutes: plannedMinutesToSave,
      memo: recordMemo.value,
    };

    if (isEditing.value) {
      // 既存の記録があれば更新
      await updateRecord({ ...dataToSend, id: editingRecordId.value });
      alert('学習記録が正常に更新されました！');
      isEditing.value = false;
    } else {
      // 既存の記録がなければ新規作成
      await createRecord(dataToSend);
      alert('学習記録が正常に保存されました！');
    }
    
    // フォームをリセット
    resetForm();

    // 記録リストを最新の状態に更新
    await fetchRecords(); 

  } catch (error) {
    console.error('学習記録の登録/更新に失敗しました:', error);
    alert('学習記録の登録/更新に失敗しました。');
  }
};

/**
 * フォームをリセットするヘルパー関数。
 */
const resetForm = () => {
  selectedTopic.value = '';
  recordDate.value = '';
  studyMinutes.value = null;
  plannedMinutes.value = null;
  recordMemo.value = '';
  editingRecordId.value = null;
};

/**
 * LearningRecordListから編集イベントを受け取り、フォームにデータをロードする関数。
 * @param {Object} record - 編集対象の学習記録。
 */
const handleEdit = (record) => {
  selectedTopic.value = record.topic;
  recordDate.value = record.date;
  studyMinutes.value = record.minutes;
  plannedMinutes.value = record.planned_minutes;
  recordMemo.value = record.memo;
  editingRecordId.value = record.id;
  isEditing.value = true;
};

/**
 * 編集モードをキャンセルし、フォームをリセットする関数。
 */
const cancelEdit = () => {
  resetForm();
  isEditing.value = false;
};

// コンポーネントがDOMにマウントされたときに、初期データ（テーマと記録）を取得
onMounted(() => {
  fetchTopics();
  fetchRecords();
});
</script>

<style scoped>
.learning-form {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input[type="date"],
input[type="number"],
textarea,
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.submit-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #45a049;
}

.cancel-button {
  background-color: #f44336;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-left: 10px;
}

.cancel-button:hover {
  background-color: #d32f2f;
}

.separator {
  margin: 30px 0;
  border: 0;
  border-top: 1px solid #eee;
}
</style>