import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RewindView from '../views/RewindView.vue'
import CalendarView from '../views/CalendarView.vue'
import InfographicView from '../views/InfographicView.vue'
import MasteryView from '../views/MasteryView.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/rewind/:riotId/:region',
      name: 'rewind',
      component: RewindView,
    },
    {
      path: '/rewind/:riotId/:region/calendar',
      name: 'calendar',
      component: CalendarView,
    },
    {
      path: '/rewind/:riotId/:region/infographic',
      name: 'infographic',
      component: InfographicView,
    },
    {
      path: '/rewind/:riotId/:region/mastery',
      name: 'mastery',
      component: MasteryView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
