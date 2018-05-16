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
  modules: {
    login: login,
    cart: cart
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
})
