// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import store from '@/vuex-store/index'
// import api from '@/http/api.js'       // 基于axios的http请求
// import Mint from 'mint-ui' // 饿了么移动端开源UI框架
// import 'mint-ui/lib/style.css'
import iView from 'iview'
import 'iview/dist/styles/iview.css'
import './assets/font-awesome-4.7.0/css/font-awesome.min.css' // 免费图标
import VueLazyLoad from 'vue-lazyload'
import App from './App'

require('@/common/filters') // 启用自定义过滤器
require('@/http/mock') // 启用mock数据，只能放import语句后面

// Vue.use(Mint)
Vue.use(iView)
Vue.use(VueLazyLoad, {
  error: '../../assets/logo.png',
  loading: '../../assets/logo.png'
})
Vue.config.productionTip = false
// Vue.prototype.$api = api // this.$api即是http里的api

router.beforeEach((to, from, next) => {
  let currentUser = JSON.parse(window.localStorage.getItem('currentUser'))
  // 判断该路由是否需要登录权限
  if (to.meta.requireAuth) {
    console.log('page require Authorization here')
    // 如果目标URL有权限控制，则继续判断用户权限
    if (to.meta.permission) {
      if (currentUser.permissions !== undefined) {
        // console.error(currentUser.permissions.data)
        // console.error(Boolean(to.meta.permission))
        if (to.meta.permission && currentUser.permissions.data.some((item, index, array) => item === to.meta.permission)) {
          console.log('Has permission')
          next()
        } else {
          console.log('Lack of permission')
          next({ path: from.path })
        }
      } else {
        // 用户权限为空，跳转回去
        console.log('Lack of permission')
        next({ path: from.path })
      }
    // 目标URL权限为空，则直接进入
    } else {
      next()
    }
  } else {
    next()
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
  store
})
