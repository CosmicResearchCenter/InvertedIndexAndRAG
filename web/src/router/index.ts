import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
// import KnowledgeBaseManager from '../views/KnowledgeBaseManager/KnowledgeBaseManager.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/manager',
      name: 'manager',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/KnowledgeBaseListView.vue')
    },
    {
      path: '/manager/:id',
      name: 'knowledge-base',
      component: () => import('../views/KnowledgeBaseManager/KnowledgeBaseManager.vue')
    },
    {
      path: '/manager/:id/create',
      name: 'knowledge-base-create',
      component: () => import('../views/KnowledgeBaseManager/KnowledgeBaseCreate.vue')
    }
  ]
})

export default router
