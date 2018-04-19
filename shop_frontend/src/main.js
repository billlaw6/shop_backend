// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
// import mavonEditor from 'mavon-editor'
// import '../node_modules/mavon-editor/dist/css/index.css'
import store from './vuex-store/index'
import api from '@/http/api.js'       // 基于axios的http请求
import Mint from 'mint-ui' // 饿了么移动端开源UI框架
import 'mint-ui/lib/style.css'
import App from './App'

require('@/http/mock') // 启用mock数据，只能放import语句后面

Vue.use(Mint)
Vue.config.productionTip = false
Vue.prototype.$api = api // this.$api即是http里的api

router.beforeEach((to, from, next) => {
  // 判断该路由是否需要登录权限
  let accessToken = window.sessionStorage.getItem('accessToken')
  // window.sessionStorage.removeItem('user')
  let user = JSON.parse(window.sessionStorage.getItem('user'))
  let permissions = JSON.parse(window.sessionStorage.getItem('permissions'))
  if (to.matched.some(record => record.meta.requireAuth)) {
    // console.log('page require Authorization here')
    if (accessToken && user) {
      if (to.meta.permission === 'undefined') {
        console.log(permissions.some(to.meta.permission))
        next()
      } else if (permissions.some(record => record.codename === to.meta.permission)) {
        console.log('Has permission')
        next()
      } else {
        console.log('Lack of permission')
        next({ path: from.path })
      }
    } else {
      next({
        name: 'login',
        query: { redirect: to.fullPath }
      })
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
