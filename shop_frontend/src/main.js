// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import iView from 'iview'
// import 'iview/dist/styles/iviews.css'
import '../node_modules/.2.8.0@iview/dist/styles/iview.css'
import store from './vuex-store/index'
import axios from 'axios'
import App from './App'

Vue.use(iView)

// 如果本地有Token则每次请求都带上Token
axios.interceptors.request.use(
  config => {
    let accessToken = window.sessionStorage.accessToken
    if (accessToken) {
      console.log('setting accessToken to: ' + accessToken)
      config.headers.Authorization = `Token ${accessToken}`
    } else {
      console.log('No accessToken')
    }
    return config
  },
  err => {
    return Promise.reject(err)
  }
)

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

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
  store
})
