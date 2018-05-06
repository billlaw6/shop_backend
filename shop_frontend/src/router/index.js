import Vue from 'vue'
import Router from 'vue-router'
const Index = resolve => require(['@/pages/Index.vue'], resolve)
const Category = resolve => require(['@/pages/Category.vue'], resolve)
const Detail = resolve => require(['@/pages/Detail.vue'], resolve)
// const Login = resolve => require(['@/pages/Login.vue'], resolve)

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
      path: '/category/:categoryId',
      name: 'category',
      component: Category,
      // redirect: '/category/all',
      // children: [{
      //   path: '/category/:tab',
      //   component: CategoryMain
      // }],
      meta: {
        hidden: false
      }
    },
    {
      path: '/detail/:productId',
      name: 'detail',
      component: Detail,
      meta: {
        hidden: false
      }
    }
    // {
    //   path: '/cart',
    //   name: 'cart',
    //   component: Cart,
    //   meta: {
    //     hidden: false
    //   }
    // },
    // {
    //   path: '/user',
    //   name: 'user',
    //   component: User,
    //   meta: {
    //     requireAuth: true,
    //     hidden: false
    //   }
    // },
    // {
    //   path: '/login',
    //   name: 'login',
    //   component: Login,
    //   meta: {
    //     hidden: false
    //   }
    // }
  ]
})
