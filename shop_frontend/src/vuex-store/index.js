import Vue from 'vue'
import Vuex from 'vuex'
import createLogger from 'vuex/dist/logger'

import * as actions from './actions'
import * as getters from './getters'
import mutations from './mutations'

import login from './modules/login'
// import detail from './modules/detail'
// import category from './modules/category'

Vue.use(Vuex)

// rootState
const state = {
  sitename: '',
  loginStatus: false,
  baseUrl: 'http://localhost:8000',
  mediaRoot: 'http://localhost:8000/media/',
  cartList: []
}

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  state,
  mutations,
  getters,
  actions,
  modules: {
    login: login
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
})
