import Vue from 'vue'
import Router from 'vue-router'
// import {routers, appRouter, otherRouter} from './router'
import {routers} from './router'

Vue.use(Router)

const RouterConfig = {
  mode: 'history',
  routes: routers
}

export const router = new Router(RouterConfig)

router.beforeEach((to, from, next) => {
  let currentUser = JSON.parse(window.localStorage.getItem('currentUser'))
  // 判断该路由是否需要登录权限
  if (to.meta.requireAuth) {
    console.log('page require Authorization here')
    // 如果目标URL有权限控制，则继续判断用户权限
    // console.error(to.meta.permission)
    if (to.meta.permission) {
      // console.error('page require permission: ' + to.meta.permission)
      // console.error(currentUser)
      if (currentUser && currentUser.permissions) {
        // console.error(Boolean(to.meta.permission))
        if (to.meta.permission && currentUser.permissions.some((item, index, array) => item === to.meta.permission)) {
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
