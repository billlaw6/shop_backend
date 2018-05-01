import Vue from 'vue'

// Vue已经自带
// const capitalize = Vue.filter('capitalize', function (value) {
//   if (!value) return ''
//   value = value.toString()
//   return value.charAt(0).toUpperCase() + value.slice(1)
// })

// const digitsRE = /(\d{3})(?=\d)/g
// export function currency (value, currency, decimals) {
//   value = parseFloat(value)
//   if (!isFinite(value) || (!value && value !== 0)) return ''
//   currency = currency != null ? currency : '￥'
//   decimals = decimals != null ? decimals : 2
//   let stringified = Math.abs(value).toFixed(decimals)
//   let _int = decimals ? stringified.slice(0, -1 - decimals) : stringified
//   let i = _int.length % 3
//   let head = i > 0 ? (_int.slice(0, i) + (_int.length > 3 ? ',' : '')) : ''
//   let _float = decimals ? stringified.slice(-1 - decimals) : ''
//   let sign = value < 0 ? '-' : ''
//   return sign + currency + head + _int.slice(i).replace(digitsRE, '￥1,') + _float
// }

const formatSex = Vue.filter('formatSex', function (row, column) {
  return row.sex === 1 ? '男' : row.sex === 0 ? '女' : '未知'
})

const maskImageUrl = Vue.filter('maskImageUrl', function (data) {
  // console.error(typeof data)
  if (typeof data === 'string') {
    // console.log('string')
    return data.replace('rest-api/products/shop_frontend/dist/', '')
  } else if (typeof data === 'object') {
    // console.log('object')
    // 处理[{},{},...]型数据
    if (data instanceof Array) {
      data.forEach((item, index, array) => {
        item['image'] = item['image'].replace('rest-api/products/shop_frontend/dist/', '')
        // for (let p in item) {
        //   item[p] = item[p].replace('rest-api/products/shop_frontend/dist/', '')
        // }
      })
      return data
    }
  }
})

export default { formatSex, maskImageUrl }
