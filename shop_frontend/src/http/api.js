// 直接在一个文件里定义全部API更合理
import axios from 'axios'
import store from '@/vuex-store/index'
// import * as types from '@/vuex-store/types'
import { router } from '@/router/index'

// axios.defaults.baseURL = 'http://123.56.115.20'
// axios.defaults.baseURL = 'http://127.0.0.1:8081'
axios.defaults.timeout = 5000
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
axios.defaults.headers.post['X-Requested-With'] = 'XMLHttpRequest'

// 添加请求拦截器
// 如果本地有Token则每次请求都带上Token
axios.interceptors.request.use(
  // 请求之前做的事
  config => {
    if (store.state.login.accessToken) {
      config.headers.Authorization = 'Token ' + store.state.login.accessToken
    }
    return config
  },
  // 请求错误处理
  err => {
    return Promise.reject(err)
  }
)

// 添加响应拦截器
// 如果Token过期导致401错误，测清空本地Token再登录
axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.error(error.response)
    if (error.response.status === 401) {
      // 如果Token过期等原因导致401错误，测清空本地Token再登录
      // store.commit(types.SET_ACCESS_TOKEN, null)
      store.commit('login/SET_ACCESS_TOKEN', null)
      // this.$Message(this.$t('loginPlease'))
      router.replace({
        name: 'login',
        query: {redirect: router.currentRoute.fullPath}
      })
    } else {
      console.error(error.response.status)
    }
    return Promise.reject(error)
  }
)

export const authUser = params => { return axios.get(`/rest-auth/user/`, {params: params}).then(res => res) }

export const authRegister = params => { return axios.post(`/rest-auth/registration/`, params).then(res => res) }

export const authPassReset = params => { return axios.post(`/rest-auth/password/reset/`, params).then(res => res) }

export const authPassResetConfirm = params => { return axios.post(`/rest-auth/password/reset/confirm/`, params).then(res => res) }

export const authPassChange = params => { return axios.post(`/rest-auth/password/change/`, params).then(res => res) }

export const authWeixinLogin = params => { return axios.post(`/rest-auth/weixin/`, params).then(res => res) }

export const getCaptcha = params => { return axios.get(`/utils/get-captcha`, {params: params}).then(res => res) }

// 微信公众号相关API
export const weixinUserList = params => { return axios.post(`/weixin/user-list/`, params).then(res => res) }

export const weixinUserInfo = params => { return axios.post(`/weixin/user-info/`, params).then(res => res) }

export const weixinBatchUserInfo = params => { return axios.post(`/weixin/batch-user-info/`, params).then(res => res) }

export const getDepartments = params => {
  return axios.get(`/user-manage/departments/`, {params: params}).then(res => res)
}

export const getAllOrder = params => {
  return axios.get(`/sale-manage/orders/`, {params: params}).then(res => res)
}

export const getOrderInfo = params => {
  return axios.get(`/sale-manage/orders/${params}/`).then(res => res)
}

export const processOrder = params => {
  return axios.post(`/sale-manage/order/process/`, params).then(res => res)
}

export const toggleOrderDetail = params => {
  return axios.post(`/sale-manage/order-detail/toggle/`, params).then(res => res)
}

export const authLogin = params => {
  // http://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html
  // 提交username, email, password，返回Token Object's key.
  return axios.post(`/rest-auth/login/`, params).then(res => res)
}

export const authLogout = params => {
  // http://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html
  return axios.post(`/rest-auth/logout/`, params).then(res => res)
}

export const getUserInfo = params => {
  return axios.get(`/user-manage/user-info/`, {params: params}).then(res => res)
}

export const getUserPermissions = params => {
  return axios.get(`/user-manage/user-perms/`, {params: params}).then(res => res)
}

export const getCustomers = params => {
  // rest自带的，有limit和offset两参数
  return axios.get(`/user-manage/users/`, {params: params}).then(res => res)
}

export const getExpresses = params => {
  // rest自带的，有limit和offset两参数
  return axios.get(`/sale-manage/expresses/`, {params: params}).then(res => res)
}

export const getPayments = params => {
  // rest自带的，有limit和offset两参数
  return axios.get(`/sale-manage/payments/`, {params: params}).then(res => res)
}

export const getLocations = params => {
  // rest自带的，有limit和offset两参数
  return axios.get(`/user-manage/locations/`, {params: params}).then(res => res)
}

export const getProducts = params => {
  // rest自带的，有limit和offset两参数
  return axios.get(`/sale-manage/products/`, {params: params}).then(res => res)
}

export const searchProducts = params => {
  // params参数可含 keyword, limit, offset
  return axios.get(`/sale-manage/product/search/`, {params: params}).then(res => res)
}

export const getProductDetail = params => { return axios.get(`/sale-manage/products/${params}`).then(res => res) }

export const addProduct = params => {
  return axios.post(`/sale-manage/product/`, params).then(res => res)
}

export const createProduct = params => {
  return axios.post(`/sale-manage/product/create/`, params).then(res => res)
}

export const toggleProduct = params => {
  return axios.post(`/sale-manage/product/toggle/`, params).then(res => res)
}

export const updateProduct = params => {
  return axios.post(`/sale-manage/product/update/`, params).then(res => res)
}

export const getHotProducts = params => {
  return axios.get(`/sale-manage/hot-products/`, {params: params}).then(res => res)
}

export const addOrder = params => {
  return axios.post(`/sale-manage/order/add/`, params).then(res => res)
}

export const addMoveRecord = params => {
  return axios.post(`/sale-manage/move-record/add/`, params).then(res => res)
}

export const processStockMoveRecord = params => {
  return axios.post(`/sale-manage/move-record/process/`, params).then(res => res)
}

// export const getStockMoveRecord = params => {
//   return axios.get(`/sale-manage/move-records/`, {params: params}).then(res => res)
// }

export const getStockMoveRecord = params => {
  return axios.get(`/sale-manage/move-record/search/`, {params: params}).then(res => res)
}

export const getStocks = params => {
  return axios.get(`/sale-manage/stock/`, {params: params}).then(res => res)
}

export const searchStocks = params => {
  return axios.get(`/sale-manage/stock/search/`, {params: params}).then(res => res)
}

export const searchCustomers = params => {
  return axios.get(`/user-manage/customer/search/`, {params: params}).then(res => res)
}

export const addCustomer = params => {
  return axios.post(`/user-manage/customer/`, params).then(res => res)
}

export const createCustomer = params => {
  return axios.post(`/user-manage/customer/create/`, params).then(res => res)
}

export const toggleCustomer = params => {
  return axios.post(`/user-manage/customer/toggle/`, params).then(res => res)
}

export const updateCustomer = params => {
  return axios.post(`/user-manage/customer/update/`, params).then(res => res)
}
