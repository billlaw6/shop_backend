// 根级别的 mutation
import * as types from './mutation-types'

// Only one default export allowed per module.
export default {
  // 这是对象内方法的简化写法 es6
  // 全部展开是这样的 [types.SET_SITE_NAME]: (state, { sitename }) => {
  [types.SET_SITE_NAME] (state, { sitename }) {
    state.sitename = sitename
  }
}
