// 直接在一个文件里定义全部API更合理
//
import axios from 'axios'
import store from '@/vuex-store/index'
import * as types from '@/vuex-store/types'
import router from '@/router/index'

axios.defaults.baseURL = 'http://123.56.115.20'
axios.defaults.timeout = 5000
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
axios.defaults.headers.post['X-Requested-With'] = 'XMLHttpRequest'

// 添加响应拦截器
// 如果本地有Token则每次请求都带上Token
axios.interceptors.request.use(
  config => {
    if (store.state.login.accessToken) {
      console.debug('setting accessToken to: ' + store.state.login.accessToken)
      config.headers.Authorization = 'Token ' + store.state.login.accessToken
    } else {
      console.debug('No accessToken')
    }
    return config
  },
  err => {
    console.debug(err)
    if (err.response) {
      if (err.response.status === 401) {
        // 如果返回401 即没有权限，跳到登录页重新登录
        store.commit(types.SET_ACCESS_TOKEN, null)
        alert('请重新登录')
        router.replace({
          path: 'login',
          query: {redirect: router.currentRoute.fullPath}
        })
      }
      return Promise.reject(err)
    }
  }
)

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
  console.debug('getUserInfo')
  return axios.get(`/rest-auth/user/`, params).then(res => res)
}

export const getUserPermissions = params => {
  console.debug('getUserPermissions')
  return axios.get(`/rest-auth/user/`, params).then(res => res)
}

export const getProducts = params => {
  return axios.get(`/rest-api/products/`).then(res => res)
}

export const getHotProducts = params => {
  return axios.get(`/rest-api/hot-products/`).then(res => res)
}

export const getProductDetail = params => {
  let productId = params
  return axios.get(`/rest-api/products/${productId}`).then(res => res)
}
