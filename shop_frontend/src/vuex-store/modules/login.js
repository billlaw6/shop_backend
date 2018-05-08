import * as types from '../types'
const state = {
  token: 0
}

const mutations = {
  [types.SET_ACCESS_TOKEN] (state, token) {
    state.token = token
  }
}

export default {
  state,
  mutations
}
