// 根级别的 getter
// 有时候我们需要从 store 中的 state 中派生出一些状态

export const debug = state => {
  return process.env.NODE_ENV !== 'production'
}

export const user = state => {
  return state.login.user
}

export const username = state => {
  if (state.login.user !== null) {
    console.log('has username')
    return state.login.user.username
  } else {
    console.log('no username')
    return null
  }
}

export const cartListCount = state => {
  return state.cartList.length
}

export const cartListSum = state => {
  let tmpSum = 0.0
  state.cartList.forEach(function (item, index) {
    console.debug(item.price)
    console.debug(item.amount)
    tmpSum += item.price * item.amount
  })
  return tmpSum
}
