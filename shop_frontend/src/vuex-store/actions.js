// 根级别的 action
// Action 类似于 mutation，不同在于：
//     Action 提交的是 mutation，而不是直接变更状态。
//     Action 可以包含任意异步操作。

// Action 函数接受一个与 store 实例具有相同方法和属性的 context 对象，因此你可以调用 context.commit 提交一个 mutation，或者通过 context.state 和 context.getters 来获取 state 和 getters。
// 当有好几个mutation要提交，尤其是多个mutation之间有先后顺序时，action是完美解决方案
// 将与localStorage同步放在mutations中，在更好保障同步的同时，还能把简单页面业务逻辑放在actions中
// 统一用action层作为store操作接口
import * as types from './types'

// 本案例使用ES2015的参数解构将context对象解构成了{ commit, state }，只取用context两个属性
// export const setSitename = (context, { sitename }) => {
export const setSitename = ({ commit, state }, sitename) => {
  console.log('set sitename action')
  commit(types.SET_SITE_NAME, sitename)
}

export const setLoading = ({ commit, state }, loading) => {
  console.debug('set loading action')
  commit(types.SET_SITE_NAME, loading)
}

// 往购物车中添加商品
export const addCartItem = ({ commit, state }, { item, amount }) => {
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
}

export const decreaseCartItemAmount = ({ commit, state }, item) => {
  commit(types.SET_CART_ITEM_AMOUNT, { 'item': item, 'amount': item.amount - state.saleUnit })
  if (state.loginStatus) {
    console.debug('post cartList to server')
  }
  console.debug('state.cartList after commit add:')
}

export const increaseCartItemAmount = ({ commit, state }, item) => {
  commit(types.SET_CART_ITEM_AMOUNT, { 'item': item, 'amount': item.amount + state.saleUnit })
  if (state.loginStatus) {
    console.debug('post cartList to server')
  }
  console.debug('state.cartList after commit add:')
}

// 删除购物车中某品种
export const removeCartItem = ({ commit, state }, item) => {
  commit(types.REMOVE_CART_ITEM, item)
  // console.debug('state.cartList after commit remove:')
  console.debug(state.cartList)
  if (state.loginStatus) {
    console.debug('post cartList to server')
  }
  console.debug('state.cartList after commit add:')
}

// 清空购物车
export const emptyCart = ({ commit, state }) => {
  commit(types.EMPTY_CART)
  console.debug('state.cartList after commit emptyCart:')
  // console.debug(state.cartList)
  if (state.loginStatus) {
    console.debug('post cartList to server')
  } else {
    console.debug('save cartList to localStorage')
  }
  console.debug('state.cartList after commit add:')
}

// 用于刷新类操作时将localStorage中的cartList同步到state中
export const setCartList = ({ commit, state }, cartList) => {
  commit(types.SET_CART_LIST, cartList)
  console.debug('state.cartList after commit setCartList:')
}
