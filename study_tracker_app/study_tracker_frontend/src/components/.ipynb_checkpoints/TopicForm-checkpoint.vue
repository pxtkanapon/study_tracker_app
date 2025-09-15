<template>
  <div class="topic-form">
    <h4>新規学習テーマの追加</h4>
    <form @submit.prevent="submitTopic">
      <div class="form-group">
        <label for="topic-name">テーマ名:</label>
        <input type="text" id="topic-name" v-model="topicName" required>
      </div>
      <button type="submit" class="btn-save">保存</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { createTopic } from '@/api/api.js';

const topicName = ref('');

/**
 * @event topic-saved
 * 新しいテーマが正常に保存されたときに親コンポーネントに通知します。
 */
const emit = defineEmits(['topic-saved']);

/**
 * @function submitTopic
 * 新しい学習テーマをAPI経由で保存します。
 * @async
 * @returns {Promise<void>}
 */
const submitTopic = async () => {
  if (!topicName.value) {
    alert('テーマ名を入力してください。');
    return;
  }
  const dataToSend = { name: topicName.value };
  console.log('送信データ:', dataToSend);
  try {
    // 'name' フィールドを 'title' に変更
    await createTopic({ title: topicName.value });
    alert('テーマが正常に登録されました！');
    topicName.value = '';

    // 新規テーマが登録された後、テーマリストを再取得する
    // await fetchTopics(); 

    emit('topic-saved');
  } catch (error) {
    console.error("テーマの登録に失敗しました:", error);
    alert('テーマの登録に失敗しました。');
  }
};
</script>

<style scoped>
.topic-form {
  padding: 1.5rem;
  background-color: #f0f4f7;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-save {
  background-color: #4CAF50;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-save:hover {
  background-color: #45a049;
}
</style>