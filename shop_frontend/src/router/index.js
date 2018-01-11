import Vue from 'vue'
import Router from 'vue-router'
const Login = resolve => require(['@/pages/Login.vue'], resolve)
const p401 = resolve => require(['@/pages/401.vue'], resolve)
const p404 = resolve => require(['@/pages/404.vue'], resolve)

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/401',
      name: 'p401',
      component: p401
    },
    {
      path: '/404',
      name: 'p404',
      component: p404
    }
  ]
})
