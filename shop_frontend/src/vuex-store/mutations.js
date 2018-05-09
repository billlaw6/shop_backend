// 根级别的 mutation
// 一条重要的原则就是要记住 mutation 必须是同步函数。
// 更改 Vuex 的 store 中的状态的唯一方法是提交 mutation。Vuex 中的 mutation 非常类似于事件：每个 mutation 都有一个字符串的 事件类型 (type) 和 一个 回调函数 (handler)。这个回调函数就是我们实际进行状态更改的地方，并且它会接受 state 作为第一个参数
// Only one default export allowed per module.
import * as types from './types'

export default {
  [types.SET_SITE_NAME] (state, { sitename }) {
    state.sitename = sitename
  },

  // 这是对象内方法的简化写法 es6
  [types.ADD_CART_ITEM] (state, {item, amount}) {
    // console.debug('mutation received item:')
    // console.debug(item)
    // console.debug('mutation received amount:')
    // console.debug(amount)
    // 如果该品种已经存在，不增加count，只增加list中对应品种的amount
    // 如果该品种不存在，增加count，增加list中对应品种及amount
    // indexOf函数只适合查元素自己，不能直接查值相等的复制元素
    // let productIndex = this.state.cartList.indexOf(item)
    let productIndex = -1
    this.state.cartList.forEach((el, index, array) => {
      console.debug('item.id:')
      console.debug(item.id)
      console.debug('el.id:')
      console.debug(el.id)
      if (el.id === item.id) {
        productIndex = index
      }
    })
    console.debug('productIndex: ' + productIndex)
    if (productIndex === -1) {
      console.debug('not existed')
      console.debug(typeof amount)
      if (typeof amount === 'string') {
        // toFixed()返回NumberObject的字符串表示
        // item['amount'] = parseFloat(amount).toFixed(2)
        item['amount'] = parseFloat(amount)
      } else {
        item['amount'] = amount
      }
      this.state.cartList.push(item)
    } else {
      console.debug('existed')
      console.debug(typeof amount)
      // 用Input属性时会传进来string
      if (typeof amount === 'string') {
        item['amount'] = parseFloat(item['amount']) + parseFloat(amount)
      } else {
        item['amount'] = parseFloat(item['amount']) + amount
      }
      this.state.cartList[productIndex] = item
    }
  },

  [types.SET_CART_ITEM_AMOUNT] (state, {item, amount}) {
    // console.debug('mutation received item:')
    // console.debug(item)
    // console.debug('mutation received amount:')
    // console.debug(amount)
    // 如果该品种已经存在，不增加count，只增加list中对应品种的amount
    // 如果该品种不存在，增加count，增加list中对应品种及amount
    let productIndex = -1
    this.state.cartList.forEach((el, index, array) => {
      console.debug(el)
      if (el.id === item.id) {
        productIndex = index
      }
    })
    console.debug('productIndex: ' + productIndex)
    if (productIndex === -1) {
      console.debug('not existed')
      console.debug(typeof amount)
      if (typeof amount === 'string') {
        item['amount'] = parseFloat(amount)
      } else {
        item['amount'] = amount
      }
      this.state.cartList.push(item)
    } else {
      console.debug('existed')
      console.debug(typeof amount)
      // 用Input属性时会传进来string
      if (typeof amount === 'string') {
        item['amount'] = parseFloat(amount)
      } else {
        item['amount'] = amount
      }
      this.state.cartList[productIndex] = item
    }
  },

  [types.COPY_CART] (state, cartList) {
    console.debug('mutation copy_cart received cartList:')
    console.debug(cartList)
    this.state.cartList = cartList
  },

  [types.EMPTY_CART] (state) {
    console.debug('empty cart in mutation')
    this.state.cartList = []
  }
}
