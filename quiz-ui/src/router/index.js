import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import NewQuizPage from '@/views/NewQuizPage.vue'
import QuestionManager from '@/views/QuestionManager.vue'
import ScorePage from '@/views/ScorePage.vue'
import Admin from '@/views/Admin.vue'
import QuestionList from '@/views/QuestionList.vue'
import QuestionEdition from '@/views/QuestionEdition.vue';
import QuestionCreate from '@/views/QuestionCreate.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/admin/question/add',
      name: 'QuestionCreate',
      component: QuestionCreate
      
    },

    {
      path: '/admin',
      name: "Admin",
      component: Admin 
    },
    {
      path: '/admin/questionlist',
      name: "QuestionList",
      component: QuestionList 
    },
    {
      path: '/admin/question/edit/:questionId',
      name: 'QuestionEdition',
      component: QuestionEdition,
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
