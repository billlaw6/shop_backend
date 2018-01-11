// 根级别的 action
import * as types from './mutation-types'

// Action 函数接受一个与 store 实例具有相同方法和属性的 context 对象，因此你可以调用 context.commit 提交一个 mutation，或者通过 context.state 和 context.getters 来获取 state 和 getters。
export const setSitename = ({ commit, state }, { sitename }) => {
  commit(types.SET_SITE_NAME, { sitename })
  console.log(state.sitename)
}

