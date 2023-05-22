import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import NewQuizPage from '@/views/NewQuizPage.vue'
import QuestionManager from '@/views/QuestionManager.vue'
import ScorePage from '@/views/ScorePage.vue'
import Admin from '@/views/Admin.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/admin',
      name: "Admin",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: Admin 
    },
    {
      path: "/start-new-quiz-page",
      name: "NewQuizPage",
      component: NewQuizPage
    },
    {
      path: "/questions",
      name: "Questions",
      component: QuestionManager
    },
    {
      path: "/score",
      name: "Score",
      component: ScorePage
    },
  ]
})

export default router
