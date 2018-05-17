// 根级别的 mutation
// 一条重要的原则就是要记住 mutation 必须是同步函数。
// 更改 Vuex 的 store 中的状态的唯一方法是提交 mutation。Vuex 中的 mutation 非常类似于事件：每个 mutation 都有一个字符串的 事件类型 (type) 和 一个 回调函数 (handler)。这个回调函数就是我们实际进行状态更改的地方，并且它会接受 state 作为第一个参数
// Only one default export allowed per module.
//
// vuex，getters只执行了一次，数据更新getters的数据没有更新
// 建议自己好好看一下 vuex 官方文档吧， mutation 改变的是 state 的一个属性， 不是直接改变 state 本身的
// 感觉题主最后给出的解决方案很含糊啊，而且经测试好像不行的，我是这样解决的：
// 在文件顶部先引用vue，mutaions里面这样写，Vue.set(state,'messageList',res.data.messageList);通过这种方式就可以触发getters的更新
// 我刚刚也遇见这个问题
// 在motation里面的触发方法里面不能直接使用state赋值的方式
// 需要使用Vue.set(state.data, type, value)即可触发状态更新
import * as types from './types'

export default {
  // 在ES6中，把属性名用[]括起来，则括号中就可以引用提前定义的变量。
  [types.SET_SITE_NAME] (state, sitename) {
    state.sitename = sitename
    // 此写法才会触发getters的更新？
    // 否，根本原因在于是否修改的是state根元素
    // Vue.set(state, 'sitename', state.sitename + state.sitename)
    // 同步更新localStorage内容，与state中从localStorage取值配合解决刷新页面state值丢失的问题
    window.localStorage.setItem('sitename', JSON.stringify(state.sitename))
  },

  [types.SET_LOADING] (state, loading) {
    state.loading = loading
    // 此写法才会触发getters的更新？
    window.localStorage.setItem('loading', JSON.stringify(state.loading))
  }
}
