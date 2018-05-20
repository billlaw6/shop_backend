import * as types from '../types'

export default {
  namespaced: true,

  state: {
    // 直接修改cartList能触发state相关的getters重新计算，但修改cartList中某元素的某属性好像不会触发
    cartList: window.localStorage['cartList'] ? JSON.parse(window.localStorage['cartList']) : [],
    decimals: window.localStorage['decimals'] ? JSON.parse(window.localStorage['decimals']) : 2
  },

  // 对于模块内部的 mutation 和 getter，接收的第一个参数是模块的局部状态对象。
  getters: {
    'cartListCount': (state, getters, rootState, rootGetters) => { return state.cartList.length },
    'cartListSum': (state, getters, rootState, rootGetters) => {
      let tmpSum = 0.0
      // 直接修改cartList能触发state相关的getters重新计算，但修改cartList中某元素的某属性好像不会触发
      state.cartList.forEach((item, index) => {
        console.debug(item.price)
        console.debug(item.amount)
        tmpSum += item.price * item.amount
      })
      return tmpSum
    }
  },

  // 对于模块内部的 mutation 和 getter，接收的第一个参数是模块的局部状态对象。
  // mutations中如何访问rootState或rootGetters暂未找到资料
  mutations: {
    [types.SET_CART_LIST] (state, cartList, rootState, rootGetters) {
      console.debug('mutation copy_cart received cartList:')
      console.debug(cartList)
      state.cartList = cartList
      window.localStorage.setItem('cartList', JSON.stringify(state.cartList))
    },

    [types.SET_CART_ITEM_AMOUNT] (state, {item, amount}, rootState, rootGetters) {
      // 如果该品种已经存在，增加list中对应品种的amount
      // 如果该品种不存在，增加list中对应品种及amount
      let productIndex = -1
      // 直接修改state.cartList中某元素item的amount会出现切换页面最后添加的item不会触发getters重新计算的问题
      // 所以改成直接修改cartList
      let tmpCartList = JSON.parse(JSON.stringify(state.cartList))
      tmpCartList.forEach((el, index, array) => {
        // console.debug(el)
        if (el.id === item.id) {
          productIndex = index
        }
      })
      console.debug('productIndex: ' + productIndex)
      if (productIndex === -1) {
        // console.debug('not existed')
        item['amount'] = parseFloat(amount.toFixed(state.decimals))
        tmpCartList.push(item)
        state.cartList = tmpCartList
        window.localStorage.setItem('cartList', JSON.stringify(state.cartList))
      } else {
        // console.debug('existed')
        item['amount'] = parseFloat(amount.toFixed(state.decimals))
        tmpCartList[productIndex] = item
        state.cartList = tmpCartList
        window.localStorage.setItem('cartList', JSON.stringify(state.cartList))
      }
    },

    [types.EMPTY_CART] (state, rootState, rootGetters) {
      console.debug('empty cart in mutation')
      state.cartList = []
      window.localStorage.setItem('cartList', JSON.stringify(state.cartList))
    },

    // 这是对象内方法的简化写法 es6
    [types.ADD_CART_ITEM] (state, {item, amount}, rootState, rootGetters) {
      // console.debug('mutation received item:')
      // console.debug(item)
      // console.debug('mutation received amount:')
      // console.debug(amount)
      // 如果该品种已经存在，不增加count，只增加list中对应品种的amount
      // 如果该品种不存在，增加count，增加list中对应品种及amount
      // indexOf函数只适合查元素自己，不能直接查值相等的复制元素
      // let productIndex = state.cartList.indexOf(item)
      let productIndex = -1
      state.cartList.forEach((el, index, array) => {
        if (el.id === item.id) {
          productIndex = index
        }
      })
      // console.debug('productIndex: ' + productIndex)
      if (productIndex === -1) {
        // console.debug('not existed')
        // console.debug(typeof amount)
        item['amount'] = parseFloat(amount.toFixed(state.decimals))
        state.cartList.push(item)
        window.localStorage.setItem('cartList', JSON.stringify(state.cartList))
      } else {
        // console.debug('existed')
        // console.debug(typeof amount)
        item['amount'] = parseFloat(amount.toFixed(state.decimals))
        state.cartList[productIndex] = item
        window.localStorage.setItem('cartList', JSON.stringify(state.cartList))
      }
    }
  },

  // 同样，对于模块内部的 action，局部状态通过 context.state 暴露出来，根节点状态则为 context.rootState
  // 如果你希望使用全局 state 和 getter，rootState 和 rootGetter 会作为第三和第四参数传入 getter，也会通过 context 对象的属性传入 action。
  // 若需要在全局命名空间内分发 action 或提交 mutation，将 { root: true } 作为第三参数传给 dispatch 或 commit 即可。
  actions: {
    // 在这个模块中， dispatch 和 commit 也被局部化了
    // 他们可以接受 `root` 属性以访问根 dispatch 或 commit
    'testAction': ({ dispatch, commit, getters, rootGetters }) => {
      dispatch('someAction')  // 'cart/someAction'
      dispatch('someAction', null, { root: true })  // 'someAction'
      commit('someMutation')  // 'cart/someMutation'
      commit('someMutation', null, { root: true })  // 'someMutation'
    },

    // 往购物车中添加商品
    'addCartItem': ({ commit, state, getters, rootGetters }, { item, amount }) => {
      // console.debug('action received item:')
      // console.debug(item)
      // console.debug('action received amount:')
      // console.debug(amount)
      commit(types.ADD_CART_ITEM, { item, amount })
      // sessionStorage仅在当前会话下有效，关闭页面或浏览器后被清除。
      // localStorage生命周期是永久
      // 每次更新购物车后对未登录的用户将购物车信息存放本地一份，这样刷新页面时信息可从本地取
      // 每次更新购物车后对已登录的用户将购物车信息提交服务器，这样刷新页面时信息可从服务器取
      if (state.loginStatus) {
        console.debug('post cartList to server')
      }
      console.debug('state.cartList after commit add:')
    },

    'decreaseCartItemAmount': ({ commit, state, getters, rootState, rootGetters }, item) => {
      commit(types.SET_CART_ITEM_AMOUNT, { 'item': item, 'amount': item.amount - rootState.saleUnit })
      if (state.loginStatus) {
        console.debug('post cartList to server')
      }
      console.debug('state.cartList after commit add:')
    },

    'increaseCartItemAmount': ({ commit, state, getters, rootState, rootGetters }, item) => {
      commit(types.SET_CART_ITEM_AMOUNT, { 'item': item, 'amount': item.amount + rootState.saleUnit })
      if (state.loginStatus) {
        console.debug('post cartList to server')
      }
      console.debug('state.cartList after commit add:')
    },

    // 删除购物车中某品种
    'removeCartItem': ({ commit, state }, item) => {
      commit(types.REMOVE_CART_ITEM, item)
      // console.debug('state.cartList after commit remove:')
      console.debug(state.cartList)
      if (state.loginStatus) {
        console.debug('post cartList to server')
      }
      console.debug('state.cartList after commit add:')
    },

    // 清空购物车
    'emptyCart': ({ commit, state }) => {
      commit(types.EMPTY_CART)
      console.debug('state.cartList after commit emptyCart:')
      // console.debug(state.cartList)
      if (state.loginStatus) {
        console.debug('post cartList to server')
      } else {
        console.debug('save cartList to localStorage')
      }
      console.debug('state.cartList after commit add:')
    },

    // 用于刷新类操作时将localStorage中的cartList同步到state中
    'setCartList': ({ commit, state }, cartList) => {
      commit(types.SET_CART_LIST, cartList)
      console.debug('state.cartList after commit setCartList:')
    }
  }
}
