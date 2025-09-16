<template>
  <div class="learning-form-container">
    <h2>{{ isEditing ? '学習記録の編集' : '学習記録の追加' }}</h2>
    <form @submit.prevent="saveRecord">
      <div class="form-group">
        <label for="record-date">日付:</label>
        <input type="date" id="record-date" v-model="form.date" required>
      </div>
      <div class="form-group">
        <label for="record-topic">テーマ:</label>
        <select id="record-topic" v-model="form.topic" required>
          <option value="" disabled selected>テーマを選択</option>
          <option v-for="topic in topics" :key="topic.id" :value="topic.id">
            {{ topic.title }}
          </option>
        </select>
        <button type="button" @click="showTopicForm = true">新規テーマ</button>
      </div>
      <div class="form-group">
        <label for="record-planned">計画時間 (分):</label>
        <input type="number" id="record-planned" v-model.number="form.planned_minutes" min="0" required>
      </div>
      <div class="form-group">
        <label for="record-minutes">実績時間 (分):</label>
        <input type="number" id="record-minutes" v-model.number="form.minutes" min="0" required>
      </div>
      <div class="form-group">
        <label for="record-memo">メモ:</label>
        <textarea id="record-memo" v-model="form.memo"></textarea>
      </div>
      <div class="form-actions">
        <button type="submit">{{ isEditing ? '更新' : '追加' }}</button>
        <button type="button" v-if="isEditing" @click="cancelEdit">キャンセル</button>
      </div>
    </form>
    
    <div v-if="showTopicForm" class="modal-overlay" @click.self="showTopicForm = false">
      <div class="modal-content">
        <h4>新規テーマを追加</h4>
        <input type="text" v-model="newTopicTitle" placeholder="テーマ名">
        <div class="modal-actions">
          <button @click="saveNewTopic">保存</button>
          <button @click="showTopicForm = false">閉じる</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, defineProps, defineEmits } from 'vue';
import { createRecord, updateRecord, createTopic } from '@/api/api.js';
import { format } from 'date-fns';

/**
 * @typedef {Object} LearningRecord
 * @property {number | null} id - 記録のID。新規作成時はnull。
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
   * @type {Array<Topic>}
   * すべてのテーマの配列。
   */
  topics: {
    type: Array,
    default: () => [],
  },
  /**
   * @type {LearningRecord | null}
   * 編集対象の学習記録オブジェクト。編集時のみ値が設定されます。
   */
  editingRecord: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['record-saved', 'topic-saved', 'cancel-edit']);

/**
 * @type {import('vue').Ref<LearningRecord>}
 * フォームの入力データを格納するリアクティブなオブジェクト。
 */
const form = ref({
  id: null,
  topic: '',
  date: format(new Date(), 'yyyy-MM-dd'),
  minutes: 0,
  planned_minutes: 0,
  memo: '',
});

/**
 * @type {import('vue').Ref<boolean>}
 * 新規テーマ追加フォームの表示状態を管理するフラグ。
 */
const showTopicForm = ref(false);

/**
 * @type {import('vue').Ref<string>}
 * 新規追加するテーマのタイトルを格納するリアクティブな変数。
 */
const newTopicTitle = ref('');

/**
 * @type {import('vue').ComputedRef<boolean>}
 * フォームが編集モードかどうかを判定する算出プロパティ。
 */
const isEditing = computed(() => !!props.editingRecord);

/**
 * フォームの入力値を初期状態にリセットします。
 */
const resetForm = () => {
  form.value = {
    id: null,
    topic: '',
    date: format(new Date(), 'yyyy-MM-dd'),
    minutes: 0,
    planned_minutes: 0,
    memo: '',
  };
};

/**
 * `editingRecord`プロパティの変更を監視し、フォームのデータを更新します。
 * プロパティに値が渡されたらフォームにセットし、`null`になったらフォームをリセットします。
 */
watch(() => props.editingRecord, (newRecord) => {
  if (newRecord) {
    form.value = { ...newRecord };
  } else {
    resetForm();
  }
}, { immediate: true });

/**
 * フォームの入力データをAPIに送信し、保存（新規作成または更新）します。
 * @async
 */
const saveRecord = async () => {
  try {
    if (isEditing.value) {
      await updateRecord(form.value);
    } else {
      await createRecord(form.value);
    }
    emit('record-saved');
  } catch (error) {
    console.error('記録の保存に失敗しました:', error);
  }
};

/**
 * 新規テーマを保存します。
 * @async
 */
const saveNewTopic = async () => {
  if (newTopicTitle.value.trim()) {
    try {
      await createTopic({ title: newTopicTitle.value });
      emit('topic-saved');
      newTopicTitle.value = '';
      showTopicForm.value = false;
    } catch (error) {
      console.error('テーマの保存に失敗しました:', error);
    }
  }
};

/**
 * 編集をキャンセルし、親コンポーネントに通知します。
 */
const cancelEdit = () => {
  emit('cancel-edit');
};
</script>

<style scoped>
.learning-form-container {
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

input, select, textarea {
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  font-weight: bold;
}

button[type="submit"] {
  background-color: #42b983;
}

button[type="button"] {
  background-color: #6c757d;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>