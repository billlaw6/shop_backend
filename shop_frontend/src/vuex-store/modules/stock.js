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
        tmpSum += item.price * item.moveAmount
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

    [types.SET_MOVE_RECORD_ITEM_AMOUNT] (state, {item, batchNo, moveAmount, comment}, rootState, rootGetters) {
      // 如果该品种已经存在，增加list中对应品种的moveAmount
      // 如果该品种不存在，增加list中对应品种及moveAmount
      let productIndex = -1
      // 直接修改state.moveRecordList中某元素item的moveAmount会出现切换页面最后添加的item不会触发getters重新计算的问题
      // 所以改成直接修改moveRecordList
      let tmpMoveRecordList = JSON.parse(JSON.stringify(state.moveRecordList))
      tmpMoveRecordList.forEach((el, index, array) => {
        if (el.id === item.id && el.batchNo === item.batchNo) {
          productIndex = index
        }
      })
      // console.debug('productIndex: ' + productIndex)
      if (productIndex === -1) {
        // console.debug('not existed')
        item['moveAmount'] = parseFloat(moveAmount.toFixed(state.decimals))
        item['comment'] = comment
        tmpMoveRecordList.push(item)
        state.moveRecordList = tmpMoveRecordList
        window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
      } else {
        // console.debug('existed')
        item['moveAmount'] = parseFloat(moveAmount.toFixed(state.decimals))
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
    [types.ADD_MOVE_RECORD_ITEM] (state, {item, moveAmount, batchNo, comment}, rootState, rootGetters) {
      let productIndex = -1
      state.moveRecordList.forEach((el, index, array) => {
        if (el.product.id === item.id && el.batchNo === batchNo) {
          productIndex = index
        }
      })
      if (productIndex === -1) {
        let newItem = {}
        newItem['product'] = item
        newItem['moveAmount'] = parseFloat(moveAmount.toFixed(state.decimals))
        newItem['batchNo'] = batchNo
        newItem['comment'] = comment
        state.moveRecordList.push(newItem)
        window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
      } else {
        state.moveRecordList[productIndex]['moveAmount'] += parseFloat(moveAmount.toFixed(state.decimals))
        // 允许更新备注
        state.moveRecordList[productIndex]['comment'] = comment
        window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
      }
    },

    [types.REMOVE_MOVE_RECORD_ITEM] (state, item, rootState, rootGetters) {
      let productIndex = -1
      state.moveRecordList.forEach((el, index, array) => {
        if (el.product.id === item.product.id && el.batchNo === item.batchNo) {
          productIndex = index
        }
      })
      if (productIndex !== -1) {
        state.moveRecordList.splice(productIndex, 1)
        window.localStorage.setItem('moveRecordList', JSON.stringify(state.moveRecordList))
      } else {
        console.error('列表中不存在此商品')
      }
    }
  },

  actions: {
    // 往列表中添加商品
    'addMoveRecordItem': ({ commit, state, getters, rootGetters }, { item, moveAmount, batchNo, comment }) => {
      commit(types.ADD_MOVE_RECORD_ITEM, { item, moveAmount, batchNo, comment })
      if (state.loginStatus) {
        console.debug('post moveRecordList to server')
      }
      console.debug('state.moveRecordList after commit add:')
    },

    'decreaseMoveRecordItemAmount': ({ commit, state, getters, rootState, rootGetters }, item) => {
      commit(types.SET_MOVE_RECORD_ITEM_AMOUNT, { 'item': item, 'moveAmount': item.moveAmount - rootState.saleUnit })
      if (state.loginStatus) {
        console.debug('post moveRecordList to server')
      }
      console.debug('state.moveRecordList after commit add:')
    },

    'increaseMoveRecordItemAmount': ({ commit, state, getters, rootState, rootGetters }, item) => {
      commit(types.SET_MOVE_RECORD_ITEM_AMOUNT, { 'item': item, 'moveAmount': item.moveAmount + rootState.saleUnit })
      if (state.loginStatus) {
        console.debug('post moveRecordList to server')
      }
      console.debug('state.moveRecordList after commit add:')
    },

    // 删除列表中某品种
    'removeMoveRecordItem': ({ commit, state }, item) => {
      commit(types.REMOVE_MOVE_RECORD_ITEM, item)
      // console.debug('state.moveRecordList after commit remove:')
      console.debug(state.moveRecordList)
      if (state.loginStatus) {
        console.debug('post moveRecordList to server')
      }
      console.debug('state.moveRecordList after commit add:')
    },

    // 清空列表
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
