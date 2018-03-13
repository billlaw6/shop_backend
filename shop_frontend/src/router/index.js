import Vue from 'vue'
import Router from 'vue-router'
const Home = resolve => require(['@/pages/Home.vue'], resolve)
const Product = resolve => require(['@/pages/Product.vue'], resolve)
const Login = resolve => require(['@/pages/Login.vue'], resolve)
const OauthLogin = resolve => require(['@/pages/OauthLogin.vue'], resolve)
const Register = resolve => require(['@/pages/Register.vue'], resolve)
const PassReset = resolve => require(['@/pages/PassReset.vue'], resolve)
const PassResetConfirm = resolve => require(['@/pages/PassResetConfirm.vue'], resolve)
const PassChange = resolve => require(['@/pages/PassChange.vue'], resolve)
const Privacy = resolve => require(['@/pages/Privacy.vue'], resolve)
const Protocal = resolve => require(['@/pages/Protocal.vue'], resolve)
const p401 = resolve => require(['@/pages/401.vue'], resolve)
const p404 = resolve => require(['@/pages/404.vue'], resolve)

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'home',
      component: Home,
      meta: {
        hidden: false
      }
    },
    {
      path: '/product',
      name: 'product',
      component: Product,
      meta: {
        hidden: false
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: {
        hidden: false
      }
    },
    {
      path: '/oauthLogin',
      name: 'oauthLogin',
      component: OauthLogin,
      meta: {
        hidden: false
      }
    },
    {
      path: '/pass_reset',
      name: 'pass_reset',
      component: PassReset,
      meta: {
        hidden: false
      }
    },
    {
      path: '/pass_reset_confirm',
      name: 'pass_reset_confirm',
      component: PassResetConfirm,
      meta: {
        hidden: false
      }
    },
    {
      path: '/password_change',
      name: 'pass_change',
      component: PassChange,
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
      path: '/protocal',
      name: 'Protocal',
      component: Protocal,
      meta: {
        hidden: false
      }
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: Privacy,
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
