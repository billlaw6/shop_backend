// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import iView from 'iview'
// import 'iview/dist/styles/iviews.css'
import store from './vuex-store/index'
import axios from 'axios'
import App from './App'

Vue.use(iView)

axios.interceptors.request.use(
  config => {
    let accessToken = window.sessionStorage.accessToken
    if (accessToken) {
      // console.log('setting accessToken to: ' + accessToken)
      config.headers.Authorization = `Token ${accessToken}`
    } else {
      // console.log('No accessToken')
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
  let user = JSON.parse(window.sessionStorage.getItem('user'))
  let permissions = JSON.parse(window.sessionStorage.getItem('permissions'))
  if (to.matched.some(record => record.meta.requireAuth)) {
    if (accessToken && user) {
      if (to.meta.permission === 'undefined') {
        // console.log(permissions.some(to.meta.permission))
        next()
      } else if (permissions.some(record => record.codename === to.meta.permission)) {
        // console.log('Has permission')
        next()
      } else {
        console.log('Lack of permission')
        // next({ path: from.path })
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
