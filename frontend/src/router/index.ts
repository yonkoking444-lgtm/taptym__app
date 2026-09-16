import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../modules/listings/pages/Main.vue'),
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../modules/auth/pages/RegstrAuto.vue'),
    },
    {
      path: '/Other',
      name: 'other',
      component: () => import('../modules/listings/pages/Other.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/Main',
      name: 'Main',
      component: () => import('../modules/listings/pages/Main.vue'),
      props: false,
    },
    {
      path: '/SpareParts',
      name: 'SpareParts',
      component: () => import('../modules/listings/pages/Hous.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/Hous',
      redirect: '/SpareParts',
    },
    {
      path: '/Services',
      name: 'Services',
      component: () => import('../modules/listings/pages/Services.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/cardetail/:id',
      name: 'CarDetail',
      component: () => import('../modules/listings/pages/CarDetail.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/create',
      name: 'create',
      component: () => import('../modules/listings/pages/CreatePage.vue'),
      props: false,
      meta: { middleware: 'auth' },
    },
    {
      path: '/message',
      name: 'message',
      component: () => import('../modules/chat/pages/MessagePage.vue'),
      props: false,
      meta: { middleware: 'auth' },
    },
    {
      path: '/messageschat',
      name: 'messageschat',
      component: () => import('../modules/chat/pages/MessagesChat.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../modules/profile/pages/ProfilePage.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/profiledit',
      name: 'profiledit',
      component: () => import('../modules/profile/pages/ProfileEdit.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/my-items',
      name: 'my-items',
      component: () => import('../modules/listings/pages/MyItems.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/heshteg',
      name: 'heshteg',
      component: () => import('../modules/listings/pages/Heshteg.vue'),
    },
    {
      path: '/termsofuse',
      name: 'termsofuse',
      component: () => import('../modules/listings/pages/TermsofUse.vue'),
    },
    {
      path: '/privacypolicy',
      name: 'privacypolicy',
      component: () => import('../modules/listings/pages/PrivacyPolicy.vue'),
    },
    {
      path: '/pointpage',
      name: 'pointpage',
      component: () => import('../modules/listings/pages/PointPage.vue'),
    },
    {
      path: '/buyitems',
      name: 'buyitems',
      component: () => import('../modules/listings/pages/Buyitems.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/chair/:id',
      name: 'chairdetail',
      component: () => import('../modules/listings/pages/ChairDetail.vue'),
      props: false,
    },
    {
      path: '/Advertisements',
      name: 'Advertisements',
      component: () => import('../modules/listings/pages/Advertisements.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/ChairBuy',
      name: 'ChairBuy',
      component: () => import('../modules/listings/pages/ChairBuy.vue'),
      meta: { middleware: 'auth' },
    },
    {
      path: '/EditAdvertis',
      name: 'EditAdvertis',
      component: () => import('../modules/listings/pages/AdvertisEdit.vue'),
      meta: { middleware: 'auth' },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.middleware === 'auth' && !authStore.isAuthenticated) {
    next('/about')
    return
  }

  next()
})

export default router
