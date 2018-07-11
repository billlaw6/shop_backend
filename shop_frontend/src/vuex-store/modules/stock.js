import * as types from '@/vuex-store/types'

export default {
  namespaced: true,

  state: {
    // 直接修改moveRecordList能触发state相关的getters重新计算，但修改moveRecordList中某元素的某属性好像不会触发
    moveRecordList: window.localStorage['moveRecordList'] ? JSON.parse(window.localStorage['moveRecordList']) : [],
    decimals: window.localStorage['decimals'] ? JSON.parse(window.localStorage['decimals']) : 2
  },

  // 对于模块内部的 mutation 和 getter，接收的第一个参数是模块的局部状态对象。
  getters: {
    'moveRecordListCount': (state, getters, rootState, rootGetters) => { return state.moveRecordList.length },
    'moveRecordListSum': (state, getters, rootState, rootGetters) => {
      let tmpSum = 0.0
      // 直接修改moveRecordList能触发state相关的getters重新计算，但修改moveRecordList中某元素的某属性好像不会触发
      state.moveRecordList.forEach((item, index) => {
        tmpSum += item.price * item.amount
      })
      return tmpSum
    }
  },

  // 对于模块内部的 mutation 和 getter，接收的第一个参数是模块的局部状态对象。
  // mutations中如何访问rootState或rootGetters暂未找到资料
  mutations: {
    [types.SET_MOVE_RECORD_LIST] (state, moveRecordList, rootState, rootGetters) {
      state.moveRecordList = moveRecordList
      window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
    },

    [types.SET_MOVE_RECORD_ITEM_AMOUNT] (state, {item, batch_no, amount, comment}, rootState, rootGetters) {
      // 如果该品种已经存在，增加list中对应品种的amount
      // 如果该品种不存在，增加list中对应品种及amount
      let productIndex = -1
      // 直接修改state.moveRecordList中某元素item的amount会出现切换页面最后添加的item不会触发getters重新计算的问题
      // 所以改成直接修改moveRecordList
      let tmpMoveRecordList = JSON.parse(JSON.stringify(state.moveRecordList))
      tmpMoveRecordList.forEach((el, index, array) => {
        if (el.id === item.id && el.batch_no === item.batch_no) {
          productIndex = index
        }
      })
      // console.debug('productIndex: ' + productIndex)
      if (productIndex === -1) {
        // console.debug('not existed')
        item['amount'] = parseFloat(amount.toFixed(state.decimals))
        item['comment'] = comment
        tmpMoveRecordList.push(item)
        state.moveRecordList = tmpMoveRecordList
        window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
      } else {
        // console.debug('existed')
        item['amount'] = parseFloat(amount.toFixed(state.decimals))
        item['comment'] = comment
        tmpMoveRecordList[productIndex] = item
        state.moveRecordList = tmpMoveRecordList
        window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
      }
    },

    [types.EMPTY_MOVE_RECORD] (state, rootState, rootGetters) {
      state.moveRecordList = []
      window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
    },

    // 这是对象内方法的简化写法 es6
    [types.ADD_MOVE_RECORD_ITEM] (state, {item, amount, batch_no, comment}, rootState, rootGetters) {
      let productIndex = -1
      state.moveRecordList.forEach((el, index, array) => {
        if (el.id === item.id && el.batch_no === item.batch_no) {
          productIndex = index
        }
      })
      if (productIndex === -1) {
        item['amount'] = parseFloat(amount.toFixed(state.decimals))
        item['comment'] = comment
        state.moveRecordList.push(item)
        window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
      } else {
        console.debug(state.moveRecordList[productIndex]['amount'])
        console.debug(parseFloat(amount.toFixed(state.decimals)))
        console.debug(state.decimals)
        state.moveRecordList[productIndex]['amount'] += parseFloat(amount.toFixed(state.decimals))
        state.moveRecordList[productIndex]['comment'] = comment
        window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
      }
    },

    [types.REMOVE_MOVE_RECORD_ITEM] (state, item, rootState, rootGetters) {
      let productIndex = -1
      state.moveRecordList.forEach((el, index, array) => {
        if (el.id === item.id && el.batch_no === item.batch_no) {
          productIndex = index
        }
      })
      if (productIndex !== -1) {
        state.moveRecordList.splice(productIndex, 1)
        window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
      } else {
        console.error('购物车中不存在此商品')
      }
    }
  },

  actions: {
    // 往购物车中添加商品
    'addMoveRecordItem': ({ commit, state, getters, rootGetters }, { item, amount, batch_no, comment }) => {
      commit(types.ADD_MOVE_RECORD_ITEM, { item, amount, batch_no, comment })
      if (state.loginStatus) {
        console.debug('post moveRecordList to server')
      }
      console.debug('state.moveRecordList after commit add:')
    },

    'decreaseMoveRecordItemAmount': ({ commit, state, getters, rootState, rootGetters }, item) => {
      commit(types.SET_MOVE_RECORD_ITEM_AMOUNT, { 'item': item, 'amount': item.amount - rootState.saleUnit })
      if (state.loginStatus) {
        console.debug('post moveRecordList to server')
      }
      console.debug('state.moveRecordList after commit add:')
    },

    'increaseMoveRecordItemAmount': ({ commit, state, getters, rootState, rootGetters }, item) => {
      commit(types.SET_MOVE_RECORD_ITEM_AMOUNT, { 'item': item, 'amount': item.amount + rootState.saleUnit })
      if (state.loginStatus) {
        console.debug('post moveRecordList to server')
      }
      console.debug('state.moveRecordList after commit add:')
    },

    // 删除购物车中某品种
    'removeMoveRecordItem': ({ commit, state }, item) => {
      commit(types.REMOVE_MOVE_RECORD_ITEM, item)
      // console.debug('state.moveRecordList after commit remove:')
      console.debug(state.moveRecordList)
      if (state.loginStatus) {
        console.debug('post moveRecordList to server')
      }
      console.debug('state.moveRecordList after commit add:')
    },

    // 清空购物车
    'emptyMoveRecord': ({ commit, state }) => {
      commit(types.EMPTY_MOVE_RECORD)
      console.debug('state.moveRecordList after commit emptyMoveRecord:')
      // console.debug(state.moveRecordList)
      if (state.loginStatus) {
        console.debug('post moveRecordList to server')
      } else {
        console.debug('save moveRecordList to localStorage')
      }
      console.debug('state.moveRecordList after commit add:')
    },

    // 用于刷新类操作时将localStorage中的moveRecordList同步到state中
    'setMoveRecordList': ({ commit, state }, moveRecordList) => {
      commit(types.SET_MOVE_RECORD_LIST, moveRecordList)
      console.debug('state.moveRecordList after commit setMoveRecordList:')
    }
  }
}
