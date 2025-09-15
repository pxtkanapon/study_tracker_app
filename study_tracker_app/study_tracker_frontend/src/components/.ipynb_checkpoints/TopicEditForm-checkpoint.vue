<template>
  <div class="topic-edit-form">
    <form @submit.prevent="updateSelectedTopic">
      <div class="form-group">
        <label for="edit-topic-select">修正するテーマ:</label>
        <select id="edit-topic-select" v-model="selectedTopicId" required>
          <option disabled value="">テーマを選択してください</option>
          <option v-for="topic in topics" :key="topic.id" :value="topic.id">
            {{ topic.title }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="new-topic-title">新しいテーマ名:</label>
        <input type="text" id="new-topic-title" v-model="newTopicTitle" required />
      </div>
      <button type="submit" class="submit-button">テーマ名を修正</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue';
import { updateTopic } from '../api/api.js';

/**
 * props定義。LearningFormからテーマリストを受け取る。
 * @type {{ topics: Array<Object> }}
 */
const props = defineProps({
  topics: {
    type: Array,
    required: true,
  },
});

/**
 * emits定義。テーマが更新されたことを親コンポーネントに通知する。
 * @type {(event: 'topic-updated') => void}
 */
const emit = defineEmits(['topic-updated']);

/**
 * ユーザーが選択したテーマのIDを格納するリアクティブな参照。
 * @type {import('vue').Ref<string>}
 */
const selectedTopicId = ref('');

/**
 * ユーザーが入力した新しいテーマ名を格納するリアクティブな参照。
 * @type {import('vue').Ref<string>}
 */
const newTopicTitle = ref('');

/**
 * ユーザーが選択したテーマが変更されたら、新しいテーマ名入力欄を更新する。
 */
watch(selectedTopicId, (newId) => {
  const selected = props.topics.find((topic) => topic.id === newId);
  if (selected) {
    newTopicTitle.value = selected.title;
  }
});

/**
 * 選択されたテーマ名をバックエンドで更新する非同期関数。
 * @async
 * @returns {Promise<void>}
 */
const updateSelectedTopic = async () => {
  if (!selectedTopicId.value || !newTopicTitle.value) {
    alert('テーマを選択し、新しいテーマ名を入力してください。');
    return;
  }
  
  try {
    const updatedData = {
      id: selectedTopicId.value,
      title: newTopicTitle.value,
    };
    await updateTopic(updatedData);
    alert('テーマ名が正常に修正されました！');

    // 親コンポーネントにテーマリストの再取得を通知
    emit('topic-updated');
    
  } catch (error) {
    console.error('テーマ名の修正に失敗しました:', error);
    alert('テーマ名の修正に失敗しました。');
  }
};
</script>

<style scoped>
.topic-edit-form {
  padding: 15px;
  background-color: #f0f0f0;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input[type="text"],
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.submit-button {
  background-color: #2196F3;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #0b7dda;
}
</style>