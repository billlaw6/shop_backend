import axios from 'axios'

let base = `http://localhost:8000`

// DjangoRestFramework自带登录
// export const authLogin = params => { return axios.post(`${base}/api-token-auth/login/`, params).then(res => res) }
// Django-rest-auth提供的登录
export const authLogin = params => { return axios.post(`${base}/rest-auth/login/`, params).then(res => res) }
export const authUser = params => { return axios.get(`${base}/rest-auth/user/`, params).then(res => res) }
export const authRegister = params => { return axios.post(`${base}/rest-auth/registration/`, params).then(res => res) }
export const authLogout = params => { return axios.post(`${base}/logout`, params).then(res => res) }
