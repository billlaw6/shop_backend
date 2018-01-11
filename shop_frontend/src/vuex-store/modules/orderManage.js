import * as types from '../mutation-types'
// 模块内部的 action、mutation、和 getter 现在仍然注册在全局命名空间——这样保证了多个模块能够响应同一 mutation 或 action。你可以通过添加前缀或后缀的方式隔离各模块，以避免名称冲突。

// initial state
const state = {
  merchandiseList: []
}

// getters
const getters = {
  // 对于模块内部的 getter，根节点状态会作为第三个参数
  getMerchandiseList (state, getters, rootState) {
    return state.merchandiseList
  }
}

// mutations
// 对于模块内部的 mutation 和 getter，接收的第一个参数是模块的局部状态。
// all mutations should be maped into mutation-types.js
// 没找到在module的mutation中修改rootState的方法
const mutations = {
  [types.SET_MERCHANDISE_LIST] (state, value) {
    state.merchandiseList = value
  }
}

// actions  state.store.commit
// 同样，对于模块内部的 action，context.state 是局部状态，根节点的状态是 context.rootState
const actions = {
  setMerchandiseList ({ state, commit, rootState }, value) {
    commit(types.SET_MERCHANDISE_LIST, value)
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
