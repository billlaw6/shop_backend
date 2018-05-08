// Root mutations
// 申明整个项目中存在的全部事件
// 使用常量替代 mutation 事件类型在各种 Flux 实现中是很常见的模式。这样可以使 linter 之类的工具发挥作用，同时把这些常量放在单独的文件中可以让你的代码合作者对整个 app 包含的 mutation 一目了然
export const SET_SITE_NAME = 'SET_SITE_NAME'

// module mutations
export const SET_ACCESS_TOKEN = 'login/SET_ACCESS_TOKEN'
export const SET_LOGIN_INFO = 'login/SET_LOGIN_INFO'
export const SET_LOGIN_STATUS = 'login/SET_LOGIN_STATUS'
export const SET_CURRENT_USER = 'login/SET_CURRENT_USER'

//
export const ADD_CART_ITEM = 'ADD_CART_ITEM'
export const SET_CART_ITEM_AMOUNT = 'SET_CART_ITEM_AMOUNT'
export const REMOVE_CART_ITEM = 'REMOVE_CART_ITEM'
export const COPY_CART = 'COPY_CART'
export const EMPTY_CART = 'EMPTY_CART'
