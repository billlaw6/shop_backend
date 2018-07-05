// 申明整个项目中存在的全部事件
// 使用常量替代 mutation 事件类型在各种 Flux 实现中是很常见的模式。这样可以使 linter 之类的工具发挥作用，同时把这些常量放在单独的文件中可以让你的代码合作者对整个 app 包含的 mutation 一目了然

// Root mutations
export const SET_SITE_NAME = 'SET_SITE_NAME'
export const SET_DEPARTMENTS = 'SET_DEPARTMENTS'
export const SET_LOADING = 'SET_LOADING'

// module mutations
// modules/login.js
export const SET_ACCESS_TOKEN = 'SET_ACCESS_TOKEN'
export const SET_CURRENT_USER = 'SET_CURRENT_USER'

// modules/category.js
export const SET_PRODUCT_LIST = 'SET_PRODUCT_LIST'

// modules/cart.js
export const ADD_CART_ITEM = 'ADD_CART_ITEM'
export const SET_CART_ITEM_AMOUNT = 'SET_CART_ITEM_AMOUNT'
export const REMOVE_CART_ITEM = 'REMOVE_CART_ITEM'
export const SET_CART_LIST = 'SET_CART_LIST'
export const EMPTY_CART = 'EMPTY_CART'

// modules/app.js
// actions中commit时会自动加上 'app/'
// VUE组件中commit时用types不方便，需要手动添加 'app/'前缀
export const SET_TAG_LIST = 'SET_TAG_LIST'
export const UPDATE_MENU_LIST = 'UPDATE_MENU_LIST'
export const CHANGE_MENU_THEME = 'CHANGE_MENU_THEME'
export const CHANGE_MAIN_THEME = 'CHANGE_MAIN_THEME'
export const ADD_OPENED_SUBMENU = 'ADD_OPENED_SUBMENU'
export const CLOSE_PAGE = 'CLOSE_PAGE'
export const INIT_CACHE_PAGE = 'INIT_CACHE_PAGE'
export const REMOVE_TAG = 'REMOVE_TAG'
export const PAGE_OPENED_LIST = 'PAGE_OPENED_LIST'
export const CLEAR_ALL_TAGS = 'CLEAR_ALL_TAGS'
export const CLEAR_OTHER_TAGS = 'CLEAR_OTHER_TAGS'
export const SET_OPENED_LIST = 'SET_OPENED_LIST'
export const SET_CURRENT_PATH = 'SET_CURRENT_PATH'
export const SET_CURRENT_PAGENAME = 'SET_CURRENT_PAGENAME'
export const SET_AVATOR = 'SET_CURRENT_AVATOR'
export const SWITCH_LANG = 'SWITCH_LANG'
export const CLEAR_OPENED_SUBMENU = 'CLEAR_OPENED_SUBMENU'
export const SET_MESSAGE_COUNT = 'SET_MESSAGE_COUNT'
export const INCREATE_TAG = 'INCREATE_TAG'
export const SET_PRODUCTS = 'SET_PRODUCTS'
export const SET_PAYMENTS = 'SET_PAYMENTS'
export const SET_EXPRESSES = 'SET_EXPRESSES'
export const SET_LOCATIONS = 'SET_LOCATIONS'
