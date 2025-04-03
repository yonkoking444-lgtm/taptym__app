import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Main.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/RegstrAuto.vue'),
    },
    {
      path: '/Other',
      name: 'other',
      component: () => import('../views/Other.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/Main',
      name: 'Main',
      component: () => import('../views/Main.vue'),
      props: false,
      
    },
    {
      path: '/Hous',
      name: 'Hous',
      component: () => import('../views/Hous.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/Services',
      name: 'Services',
      component: () => import('../views/Services.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/cardetail/:id', 
      name: 'CarDetail',
      component: () => import('../views/CarDetail.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/create', 
      name: 'create',
      component: () => import('../views/CreatePage.vue'),
      props: false,
      meta: { middleware: 'auth' },
    },    
    {
      path: '/message', 
      name: 'message',
      component: () => import('../views/MessagePage.vue'),
      props: false,
      meta: { middleware: 'auth' },
    },    
    {
      path: '/messageschat',
      name: 'messageschat',
      component: () => import('../views/MessagesChat.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfilePage.vue'),
    },
    {
      path: '/profiledit',
      name: 'profiledit',
      component: () => import('../views/ProfileEdit.vue'),
    },
    {
      path: '/heshteg',
      name: 'heshteg',
      component: () => import('../views/Heshteg.vue'),
      
    },
    {
      path: '/termsofuse',
      name: 'termsofuse',
      component: () => import('../views/TermsofUse.vue'),
    
    },
    {
      path: '/privacypolicy',
      name: 'privacypolicy',
      component: () => import('../views/PrivacyPolicy.vue'),
    },
    {
      path: '/pointpage',
      name: 'pointpage',
      component: () => import('../views/PointPage.vue'),
    },
    {
      path: '/buyitems',
      name: 'buyitems',
      component: () => import('../views/Buyitems.vue'),
      meta: { middleware: 'auth' },

    },
    {
      path: '/chair/:id',
      name: 'chairdetail',
      component: () => import('../views/ChairDetail.vue'),
      props: false,
    },    
    {
      path: '/Advertisements',
      name: 'Advertisements',
      component: () => import('../views/Advertisements.vue'),
      meta: { middleware: 'auth' },
      
    },    
    {
      path: '/ChairBuy',
      name: 'ChairBuy',
      component: () => import('../views/ChairBuy.vue'),
      meta: { middleware: 'auth' },
    },    
    {
      path: '/EditAdvertis',
      name: 'EditAdvertis',
      component: () => import('../views/AdvertisEdit.vue'),
      meta: { middleware: 'auth' },
    }
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('users')
  if (to.meta.middleware === 'auth' && !isAuthenticated) {
    next('/') 
  } else {
    next()
  }
})


export default router
