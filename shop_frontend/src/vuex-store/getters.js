// 根级别的 getter
// 有时候我们需要从 store 中的 state 中派生出一些状态
// Vuex 允许我们在 store 中定义“getter”（可以认为是 store 的计算属性）。就像计算属性一样，getter 的返回值会根据它的依赖被缓存起来，且只有当它的依赖值发生了改变才会被重新计算。
// 下面备注过时，现官方文档使用的就是箭头函数，并且将箭头函数修改成普通函数也没实时刷新
// 使用sitename测试时用箭头函数也实时刷新了。
// 官方建议在getter和computed里不使用箭头函数（可能是getter属性在页面不能实时刷新的原因）

export const debug = state => {
  return process.env.NODE_ENV !== 'production'
}

export const currentUser = state => {
  return state.login.currentUser
}
