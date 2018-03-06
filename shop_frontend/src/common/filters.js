import Vue from 'vue'

export const capitalize = Vue.filter('capitalize', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})

const digitsRE = /(\d{3})(?=\d)/g
export function currency (value, currency, decimals) {
  value = parseFloat(value)
  if (!isFinite(value) || (!value && value !== 0)) return ''
  currency = currency != null ? currency : '￥'
  decimals = decimals != null ? decimals : 2
  let stringified = Math.abs(value).toFixed(decimals)
  let _int = decimals ? stringified.slice(0, -1 - decimals) : stringified
  let i = _int.length % 3
  let head = i > 0 ? (_int.slice(0, i) + (_int.length > 3 ? ',' : '')) : ''
  let _float = decimals ? stringified.slice(-1 - decimals) : ''
  let sign = value < 0 ? '-' : ''
  return sign + currency + head + _int.slice(i).replace(digitsRE, '￥1,') + _float
}

export const formatSex = Vue.filter('formatSex', function (row, column) {
  return row.sex === 1 ? '男' : row.sex === 0 ? '女' : '未知'
})
