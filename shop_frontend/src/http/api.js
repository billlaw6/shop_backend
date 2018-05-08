import axios from 'axios'
import store from '@/vuex-store/index'
import router from '../router'

axios.defaults.baseURL = 'http://123.56.115.20'
axios.defaults.timeout = 5000
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
axios.defaults.headers.post['X-Requested-With'] = 'XMLHttpRequest'

// 请求拦截
axios.interceptors.request.use(function (config) {
  // 在发送请求之前做些什么
  // store.commit('SET_LOADING', true)
  // 如果有token,添加到请求报文 后台会根据该报文返回status
  if (store.state.login.token) {
    config.headers.Authorization = `token ${store.state.login.token}`
  }
  return config
}, function (error) {
  // 对请求错误做些什么
  window.alert('网络错误,请稍后再试')
  // store.commit('SET_LOADING', false)
  return Promise.reject(error)
})

// 如果本地有Token则每次请求都带上Token
axios.interceptors.request.use(
  config => {
    let accessToken = window.sessionStorage.accessToken
    if (accessToken) {
      // console.log('setting accessToken to: ' + accessToken)
      config.headers.Authorization = `Token ${accessToken}`
    } else {
      // console.log('No accessToken')
    }
    return config
  },
  err => {
    return Promise.reject(err)
  }
)

// 添加响应拦截器
axios.interceptors.response.use(function (response) {
  // 对响应数据做点什么
  // 加到时器主要是为了 展示Loading效果 项目中应去除
  setTimeout(() => {
    // store.commit('SET_LOADING', false)
  }, 300)
  return response
}, function (error) {
  // 对响应错误做点什么
  // store.commit('SET_LOADING', false)
  if (error.response) {
    if (error.response.status === 401) {
      // 如果返回401 即没有权限，跳到登录页重新登录
      // store.commit('CHANGE_TOKEN', 0)
      alert('请重新登录')
      router.replace({
        path: 'login',
        query: {redirect: router.currentRoute.fullPath}
      })
    }
  }
  return Promise.reject(error)
})

// 直接在一个文件里定义全部API更合理

export const authLogin = params => { return axios.post(`/get-token/login/`, params).then(res => res) }

export const getUserInfo = params => {
  console.log('getUserInfo')
}

export const getUserPermissions = params => {
  console.log('getUserPermissions')
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
