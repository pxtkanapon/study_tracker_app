// api/api.js
import axios from 'axios';

/**
 * @const {string} BASE_URL - バックエンドAPIのベースURL。
 * 開発環境のIPアドレスに合わせて変更してください。
 */
const BASE_URL = 'http://192.168.0.9:8000/api/';

/**
 * Axiosインスタンスを作成。
 * 共通のベースURLを設定し、リクエストとレスポンスの処理を簡素化します。
 */
const api = axios.create({
  baseURL: BASE_URL,
});

/**
 * 学習記録のリストをバックエンドから取得します。
 * @async
 * @returns {Promise<Object>} 学習記録のデータを含むPromise。
 */
export const getRecords = () => {
  return api.get('records/');
};

/**
 * 新しい学習記録をバックエンドに登録します。
 * @async
 * @param {Object} record - 登録する学習記録データ。
 * @returns {Promise<Object>} 登録された学習記録のデータを含むPromise。
 */
export const createRecord = (record) => {
  return api.post('records/', record);
};

/**
 * 既存の学習記録をバックエンドで更新します。
 * @async
 * @param {Object} record - 更新する学習記録データ（idを含む）。
 * @returns {Promise<Object>} 更新された学習記録のデータを含むPromise。
 */
export const updateRecord = (record) => {
  return api.patch(`records/${record.id}/`, record);
};

/**
 * **学習記録をバックエンドで削除します。**
 * @async
 * @param {number} id - 削除する学習記録のID。
 * @returns {Promise<Object>} 削除操作のレスポンスを含むPromise。
 */
export const deleteRecord = (id) => {
  return api.delete(`records/${id}/`);
};

/**
 * 学習テーマのリストをバックエンドから取得します。
 * @async
 * @returns {Promise<Object>} 学習テーマのデータを含むPromise。
 */
export const getTopics = () => {
  return api.get('topics/');
};

/**
 * 新しい学習テーマをバックエンドに登録します。
 * @async
 * @param {Object} topic - 登録する学習テーマデータ（例: { title: '新しいテーマ' }）。
 * @returns {Promise<Object>} 登録された学習テーマのデータを含むPromise。
 */
export const createTopic = (topic) => {
  return api.post('topics/', topic);
};

/**
 * 既存の学習テーマをバックエンドで更新します。
 * @async
 * @param {Object} topic - 更新する学習テーマデータ（idとtitleを含む）。
 * @returns {Promise<Object>} 更新された学習テーマのデータを含むPromise。
 */
export const updateTopic = (topic) => {
  return api.patch(`topics/${topic.id}/`, topic);
};