import Vue from 'vue'
import Vuex from 'vuex'
import createLogger from 'vuex/dist/logger'

import * as actions from './actions'
import * as getters from './getters'
import mutations from './mutations'

import login from './modules/login'
import cart from './modules/cart'
// import detail from './modules/detail'
// import category from './modules/category'

Vue.use(Vuex)

// rootState
const state = {
  // 统一在此取值，整个APP任何页面都不用处理刷新后store内容丢失的问题了
  loading: window.localStorage['loading'] ? JSON.parse(window.localStorage['loading']) : true,
  sitename: window.localStorage['sitename'] ? JSON.parse(window.localStorage['sitename']) : null,
  saleUnit: window.localStorage['saleUnit'] ? JSON.parse(window.localStorage['saleUnit']) : 0.1,
  decimals: window.localStorage['decimals'] ? JSON.parse(window.localStorage['decimals']) : 2
}

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  state,
  mutations,
  getters,
  actions,
  // 在 Vuex 模块化中，state 是唯一会根据组合时模块的别名来添加层级的，后面的 getters、mutations 以及 actions 都是直接合并在 store 下。
  // 默认情况下，模块内部的 action、mutation 和 getter 是注册在全局命名空间的——这样使得多个模块能够对同一 mutation 或 action 作出响应。
  // 如果希望你的模块具有更高的封装度和复用性，你可以通过添加 namespaced: true 的方式使其成为带命名空间的模块。当模块被注册后，它的所有 getter、action 及 mutation 都会自动根据模块注册的路径调整命名。
  modules: {
    login: login,
    cart: cart
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
})
