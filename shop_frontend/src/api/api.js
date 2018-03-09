import axios from 'axios'

// let base = `http://localhost:8000`
let base = `http://123.56.115.20:80`

// DjangoRestFramework自带登录
// export const authLogin = params => { return axios.post(`${base}/api-token-auth/login/`, params).then(res => res) }
// Django-rest-auth提供的API
export const authLogin = params => { return axios.post(`${base}/rest-auth/login/`, params).then(res => res) }
export const authLogout = params => { return axios.post(`${base}/rest-auth/logout/`, params).then(res => res) }
export const authUser = params => { return axios.get(`${base}/rest-auth/user/`, params).then(res => res) }
export const authRegister = params => { return axios.post(`${base}/rest-auth/registration/`, params).then(res => res) }
export const authPassReset = params => { return axios.post(`${base}/rest-auth/password/reset/`, params).then(res => res) }
export const authPassResetConfirm = params => { return axios.post(`${base}/rest-auth/password/reset/confirm/`, params).then(res => res) }
export const authPassChange = params => { return axios.post(`${base}/rest-auth/password/change/`, params).then(res => res) }
export const authWeixinLogin = params => { return axios.post(`${base}/rest-auth/weixin/`, params).then(res => res) }
export const getCaptcha = params => { return axios.get(`${base}/get_captcha`, params).then(res => res) }
