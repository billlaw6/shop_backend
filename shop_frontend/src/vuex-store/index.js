import Vue from 'vue'
import Vuex from 'vuex'
import createLogger from 'vuex/dist/logger'

import * as actions from './actions'
import * as getters from './getters'
import mutations from './mutations'
import login from './modules/login'
import orderManage from './modules/orderManage'

Vue.use(Vuex)

// rootState
const state = {
  sitename: '小蜗牛直销管理系统',
  baseUrl: 'http://localhost:8000',
  mediaRoot: 'http://localhost:8000/media/'
}

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  state,
  mutations,
  getters,
  actions,
  modules: {
    login: login,
    orderManage: orderManage
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
})
