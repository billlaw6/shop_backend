import * as types from '../types'
import { authLogin, getUserInfo, getUserPermissions } from '@/http/api'

export default {
  // 如果希望你的模块具有更高的封装度和复用性，你可以通过添加 namespaced: true 的方式使其成为带命名空间的模块。当模块被注册后，它的所有 getter、action 及 mutation 都会自动根据模块注册的路径调整命名。
  namespaced: true,

  state: {
    accessToken: window.localStorage['accessToken'] ? JSON.parse(window.localStorage['accessToken']) : null,
    currentUser: window.localStorage['currentUser'] ? JSON.parse(window.localStorage['currentUser']) : null
  },

  // 对于模块内部的 mutation 和 getters，接收的第一个参数是模块的局部状态对象。
  // 由于 getters 不区分模块，所以不同模块中的 getters 如果重名，Vuex 会报出 'duplicate getter key: [重复的getter名]' 错误。
  getters: {
    // 如果你希望使用全局 state 和 getter，rootState 和 rootGetter 会作为第三和第四参数传入 getter，也会通过 context 对象的属性传入 action。
    'loginStatus': (state, getters, rootState, rootGetter) => {
      if (state.currentUser) {
        return true
      } else {
        return false
      }
    },
    'username': (state, getters, rootState, rootGetter) => {
      if (state.currentUser !== null) {
        console.log('has username')
        return state.currentUser.username
      } else {
        console.log('no username')
        return null
      }
    }
  },

  // 对于模块内部的 mutation 和 getter，接收的第一个参数是模块的局部状态对象。
  // mutations 与 getters 类似，不同模块的 mutation 均可以通过 store.commit 直接触发。
  mutations: {
    [types.SET_ACCESS_TOKEN] (state, accessToken, rootState, rootGetters) {
      console.debug('login SET_ACCESS_TOKEN mutations')
      state.accessToken = accessToken
      // 同步更新localStorage内容，与state中从localStorage取值配合解决刷新页面state值丢失的问题
      window.localStorage.setItem('accessToken', JSON.stringify(state.accessToken))
    },

    [types.SET_CURRENT_USER] (state, currentUser, rootState, rootGetters) {
      console.debug('login SET_CURRENT_USERmutations')
      state.currentUser = currentUser
      // 同步更新localStorage内容，与state中从localStorage取值配合解决刷新页面state值丢失的问题
      window.localStorage.setItem('currentUser', JSON.stringify(state.currentUser))
    }
  },

  // 同样，对于模块内部的 action，局部状态通过 context.state 暴露出来，根节点状态则为 context.rootState
  actions: {
    'login': ({ dispatch, commit, rootState, rootGetters }, { username, password }) => {
      // console.debug('login with: ' + username + ' ' + password)
      commit(types.SET_LOADING, true, { root: true })
      authLogin({ username, password }).then((res) => {
        console.debug(res)
        let {data, status} = res
        if (status !== 200) {
          return res
        } else {
          commit(types.SET_ACCESS_TOKEN, data.key)
          // 设置当前登录用户
          getUserInfo().then((res) => {
            console.log('getUserInfo: ')
            console.log(res)
            let {data, status} = res
            if (status !== 200) {
              return res
            } else {
              console.log(data)
              let tmpUser = data
              // 设置当前登录用户权限
              getUserPermissions().then((res) => {
                let { data, status, statusText } = res
                if (status !== 200) {
                  console.log('Error in getUserPermissions: ' + statusText)
                  return res
                } else {
                  console.log(data)
                  tmpUser['permissions'] = data
                  commit(types.SET_CURRENT_USER, tmpUser)
                  return { 'status': 0, 'data': tmpUser }
                }
              }, (error) => {
                console.log('Error in getUserPermissions: ' + error)
                return { 'status': 1, 'data': error }
              }).catch((error) => {
                console.log('catched in getUserPermissions:' + error)
                return { 'status': 1, 'data': error }
              })
            }
          }, (error) => {
            console.log('Error in getUserInfo: ')
            console.debug(error)
            return { 'status': 1, 'data': error }
          }).catch((except) => {
            console.log('catched in getUserInfo:' + except)
            console.debug(except)
            return { 'status': 1, 'data': except }
          })
        }
      })
      commit(types.SET_LOADING, false, { root: true })
    }
  },

  modules: {
    // 模块里嵌套的模块会继承父模块的全名空间，除非在嵌套模块中也指定namespaced: true属性
  }
}
