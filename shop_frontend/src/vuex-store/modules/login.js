import * as types from '@/vuex-store/types'
import { authLogin, authLogout, getUserInfo, getUserPermissions } from '@/http/api'
import { router } from '@/router/index'

export default {
  // 如果希望你的模块具有更高的封装度和复用性，你可以通过添加 namespaced: true 的方式使其成为带命名空间的模块。当模块被注册后，它的所有 getter、action 及 mutation 都会自动根据模块注册的路径调整命名。
  namespaced: true,

  state: {
    accessToken: window.localStorage['accessToken'] ? JSON.parse(window.localStorage['accessToken']) : null,
    currentUser: window.localStorage['currentUser'] ? JSON.parse(window.localStorage['currentUser']) : null,
    // currentDepartment: null
    currentDepartment: window.localStorage['currentDepartment'] ? JSON.parse(window.localStorage['currentDepartment']) : null
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
        // console.debug('has username')
        return state.currentUser.username
      } else {
        // console.debug('no username')
        return null
      }
    }
  },

  // 对于模块内部的 mutation 和 getter，接收的第一个参数是模块的局部状态对象。
  // mutations 与 getters 类似，不同模块的 mutation 均可以通过 store.commit 直接触发。
  // mutations中如何访问rootState或rootGetters暂未找到资料
  mutations: {
    [types.SET_ACCESS_TOKEN] (state, accessToken, rootState, rootGetters) {
      // console.debug('login SET_ACCESS_TOKEN mutations')
      state.accessToken = accessToken
      // 同步更新localStorage内容，与state中从localStorage取值配合解决刷新页面state值丢失的问题
      window.localStorage.setItem('accessToken', JSON.stringify(state.accessToken))
    },

    [types.SET_CURRENT_USER] (state, currentUser, rootState, rootGetters) {
      // console.debug('login SET_CURRENT_USERmutations')
      state.currentUser = currentUser
      // 同步更新localStorage内容，与state中从localStorage取值配合解决刷新页面state值丢失的问题
      window.localStorage.setItem('currentUser', JSON.stringify(state.currentUser))
    },

    [types.SET_CURRENT_DEPARTMENT] (state, department) {
      state.currentDepartment = department
      if (department) {
        window.localStorage.currentDepartment = JSON.stringify(state.currentDepartment)
      }
    }
  },

  // 同样，对于模块内部的 action，局部状态通过 context.state 暴露出来，根节点状态则为 context.rootState
  actions: {
    'login': ({ dispatch, commit, rootState, rootGetters }, { username, password }) => {
      // console.debug('login with: ' + username + ' ' + password)
      window.localStorage.setItem('currentUser', null)
      commit(types.SET_LOADING, true, { root: true })
      authLogin({ username, password }).then((res) => {
        // console.debug(res)
        let {data, status} = res
        if (status !== 200) {
          return res
        } else {
          commit(types.SET_ACCESS_TOKEN, data.key)
          // 设置当前登录用户
          getUserInfo().then((res) => {
            // console.debug('getUserInfo: ')
            // console.debug(res)
            let {data, status} = res
            if (status !== 200) {
              // return res
            } else {
              // console.debug(data)
              // 此处需要转换成object
              let tmpUser = JSON.parse(data)
              // 设置当前登录用户权限
              getUserPermissions().then((res) => {
                let { data, status, statusText } = res
                if (status !== 200) {
                  console.debug('Error in getUserPermissions: ' + statusText)
                  // return res
                } else {
                  // console.error(data)
                  tmpUser.permissions = JSON.parse(data)
                  commit(types.SET_CURRENT_USER, tmpUser)
                  // console.error(tmpUser)
                  if (tmpUser.dept_belong.length > 0) {
                    commit(types.SET_CURRENT_DEPARTMENT, tmpUser.dept_belong[0])
                  }
                  if (tmpUser.is_staff) {
                    router.push({'name': 'dashboard'})
                  } else {
                    router.push({'name': 'user'})
                  }
                  return { 'status': 0, 'data': tmpUser }
                }
              }, (error) => {
                console.debug('Error in getUserPermissions: ' + error)
                // return { 'status': 1, 'data': error }
              }).catch((error) => {
                console.debug('catched in getUserPermissions:' + error)
                // return { 'status': 1, 'data': error }
              })
            }
          }, (error) => {
            console.debug('Error in getUserInfo: ')
            console.debug(error)
          }).catch((except) => {
            console.debug('catched in getUserInfo:' + except)
            console.debug(except)
            // return { 'status': 1, 'data': except }
          })
        }
      })
      // 调用root级的mutation
      commit(types.SET_LOADING, false, { root: true })
    },
    'logout': ({ dispatch, commit, rootState, rootGetters }) => {
      window.localStorage.setItem('currentUser', null)
      authLogout().then((res) => {
        // console.debug(res)
        let {status} = res
        // console.log(data)
        if (status !== 200) {
          return res
        } else {
          commit(types.SET_ACCESS_TOKEN, null)
          commit(types.SET_CURRENT_USER, null)
        }
      })
    },
    'setCurrentDepartment': ({ dispatch, commit, getters, rootGetters }, department) => {
      commit(types.SET_CURRENT_DEPARTMENT, department)
    }
  },

  modules: {
    // 模块里嵌套的模块会继承父模块的全名空间，除非在嵌套模块中也指定namespaced: true属性
  }
}
