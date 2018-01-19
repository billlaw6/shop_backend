import Vue from 'vue'
import Router from 'vue-router'
const Login = resolve => require(['@/pages/Login.vue'], resolve)
const Register = resolve => require(['@/pages/Register.vue'], resolve)
const p401 = resolve => require(['@/pages/401.vue'], resolve)
const p404 = resolve => require(['@/pages/404.vue'], resolve)

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: {
        hidden: false
      }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: {
        hidden: false
      }
    },
    {
      path: '/401',
      name: 'p401',
      component: p401,
      meta: {
        requireAuth: true,
        permission: 'add_group',
        iconCls: 'ios-star',
        leaf: true,
        menu_name: '商品管理',
        hidden: false
      }
    },
    {
      path: '/404',
      name: 'p404',
      component: p404,
      meta: {
        requireAuth: false,
        permission: 'add_group',
        iconCls: 'ios-star',
        leaf: true,
        menu_name: '商品管理',
        hidden: false
      }
    }
  ]
})
