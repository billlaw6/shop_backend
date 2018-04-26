import Vue from 'vue'
import Router from 'vue-router'
const Index = resolve => require(['@/pages/Index.vue'], resolve)
const Detail = resolve => require(['@/pages/Detail.vue'], resolve)
const Cart = resolve => require(['@/pages/Cart.vue'], resolve)
const Category = resolve => require(['@/pages/Category.vue'], resolve)
const CategoryMain = resolve => require(['@/components/category/Main.vue'], resolve)
const User = resolve => require(['@/pages/User.vue'], resolve)
const Home = resolve => require(['@/pages/Home.vue'], resolve)
const Shop = resolve => require(['@/pages/Shop.vue'], resolve)
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
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'index',
      component: Index,
      meta: {
        hidden: false
      }
    },
    {
      path: '/detail',
      name: 'detail',
      component: Detail,
      meta: {
        hidden: false
      }
    },
    {
      path: '/category',
      name: 'category',
      component: Category,
      redirect: '/category/all',
      children: [{
        path: '/category/:tab',
        component: CategoryMain
      }],
      meta: {
        hidden: false
      }
    },
    {
      path: '/cart',
      name: 'cart',
      component: Cart,
      meta: {
        hidden: false
      }
    },
    {
      path: '/user',
      name: 'user',
      component: User
      // meta: {
      //   requireAuth: true,
      //   hidden: false
      // }
    },
    {
      path: '/home',
      name: 'home',
      component: Home,
      meta: {
        hidden: false
      }
    },
    {
      path: '/shop',
      name: 'shop',
      component: Shop,
      meta: {
        hidden: false
      }
    },
    {
      name: 'product',
      path: '/product/:id',
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
