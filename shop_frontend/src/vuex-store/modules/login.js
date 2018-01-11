import * as types from '../mutation-types'
// 模块内部的 action、mutation、和 getter 现在仍然注册在全局命名空间——这样保证了多个模块能够响应同一 mutation 或 action。你可以通过添加前缀或后缀的方式隔离各模块，以避免名称冲突。

// initial state
const state = {
  accessToken: null,
  loginStatus: false,
  user: null,
  permissions: null
}

// getters
const getters = {
  // 对于模块内部的 getter，根节点状态会作为第三个参数
  loginStatus (state, getters, rootState) {
    return state.loginStatus
  },
  permissions (state, getters, rootState) {
    return state.permissions
  }
}

// mutations
// 对于模块内部的 mutation 和 getter，接收的第一个参数是模块的局部状态。
// all mutations should be maped into mutation-types.js
// 没找到在module的mutation中修改rootState的方法
const mutations = {
  [types.SET_ACCESS_TOKEN] (state, accessToken) {
    state.accessToken = accessToken
  },
  [types.SET_LOGIN_STATUS] (state, value) {
    state.loginStatus = value
  },
  [types.SET_CURRENT_USER] (state, user) {
    state.user = user
  },
  [types.SET_USER_PERMISSIONS] (state, permissions) {
    state.permissions = permissions
  }
}

// actions  state.store.commit
// 同样，对于模块内部的 action，context.state 是局部状态，根节点的状态是 context.rootState
const actions = {
  setToken ({ state, commit, rootState }, accessToken) {
    commit(types.SET_ACCESS_TOKEN, accessToken)
  },
  setLoginStatus ({ state, commit, rootState }, value) {
    commit(types.SET_LOGIN_STATUS, value)
  },
  setUser ({ state, commit, rootState }, user) {
    commit(types.SET_CURRENT_USER, user)
  },
  setPermissions ({ state, commit, rootState }, permissions) {
    commit(types.SET_USER_PERMISSIONS, permissions)
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
