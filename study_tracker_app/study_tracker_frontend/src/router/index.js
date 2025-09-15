// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue'; 

const routes = [
  {
    path: '/', 
    name: 'home',
    component: HomeView // HomeViewを割り当てる
  },
  // 他のルート定義...
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;