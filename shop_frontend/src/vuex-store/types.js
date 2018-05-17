// 申明整个项目中存在的全部事件
// 使用常量替代 mutation 事件类型在各种 Flux 实现中是很常见的模式。这样可以使 linter 之类的工具发挥作用，同时把这些常量放在单独的文件中可以让你的代码合作者对整个 app 包含的 mutation 一目了然

// Root mutations
export const SET_SITE_NAME = 'SET_SITE_NAME'
export const SET_LOADING = 'SET_LOADING'

// module mutations
// modules/login.js
export const SET_ACCESS_TOKEN = 'SET_ACCESS_TOKEN'
export const SET_CURRENT_USER = 'SET_CURRENT_USER'

// modules/cart.js
export const ADD_CART_ITEM = 'ADD_CART_ITEM'
export const SET_CART_ITEM_AMOUNT = 'SET_CART_ITEM_AMOUNT'
export const REMOVE_CART_ITEM = 'REMOVE_CART_ITEM'
export const SET_CART_LIST = 'SET_CART_LIST'
export const EMPTY_CART = 'EMPTY_CART'
