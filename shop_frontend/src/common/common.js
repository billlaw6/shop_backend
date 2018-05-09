const STORAGE_USER_KEY = 'STORAGE_USER_KEY'
// const STORAGE_CARTLIST_KEY = 'STORAGE_CARTLIST_KEY'
// const STORAGE_QUERYMYLIST_KEY = 'STORAGE_QUERYMYLIST_KEY'

export default {
  // 获取
  getLocal (key = STORAGE_USER_KEY) {
    // console.log('get local operation')
    return JSON.parse(window.localStorage.getItem(key))
  },
  // 设置用
  setLocal (res, key = STORAGE_USER_KEY, isSaveOldData = false) {
    // 第三个参数是true的话,会增加数据而不是重新设置,res必须是数组
    if (isSaveOldData) {
      if (this.getLocal(key)) {
        let oldData = this.getLocal(key)
        return window.localStorage.setItem(key, JSON.stringify(oldData.concat(res)))
      }
    }
    return window.localStorage.setItem(key, JSON.stringify(res))
  }
}

if (!Array.indexOf) {
  //IE6-8下自己编写回调函数执行的逻辑
  Array.prototype.indexOf = function (item) {
    context = context || window
    for (var i=0, len=this.length; i<len; i++) {
      if (this[i] === item) {
        return i
      }
    }
    return -1
  }
}

if (!Array.forEach) {
  //IE6-8下自己编写回调函数执行的逻辑
  Array.prototype.forEach = function (callback, context) {
    context = context || window
    for (var i=0, len=this.length; i<len; i++) {
      callback && callback.call(context, this[i], i, this)
    }
  }
}

if (!Array.map) {
  // IE6-8下自己编写回调函数执行的逻辑
  Array.prototype.forEach = function (callback, context) {
    context = context || window
    let newArray = []
    for (var i=0, len=this.length; i<len; i++) {
      if (typeof callback === 'function') {
        let var = callback.call(context, this[i], i, this)
        newArray[newArray.length] = val
      }
    }
  }
}
