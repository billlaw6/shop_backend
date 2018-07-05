import * as types from '../types'

export default {
  namespaced: true,

  state: {
    productList: window.localStorage['productList'] ? JSON.parse(window.localStorage['productList']) : []
  },

  getters: {
  },

  mutations: {
    [types.SET_PRODUCT_LIST] (state, productList, rootState, rootGetters) {
      state.productList = productList
      window.localStorage.setItem('productList', JSON.stringify(state.productList))
    }
  },

  actions: {
    'setProductList': ({ dispatch, commit, getters, rootGetters }, productList) => {
      // commit('someMutation', null, { root: true })  // 'someMutation'
      commit(types.SET_PRODUCT_LIST, productList)  // 'category/someMutation'
    }
  }
}
