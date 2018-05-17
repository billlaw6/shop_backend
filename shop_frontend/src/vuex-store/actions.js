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
