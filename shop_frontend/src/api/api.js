import axios from 'axios'

let base = `http://localhost:8000`

export const authLogin = params => { return axios.post(`${base}/get-token/login/`, params).then(res => res) }
export const authLogout = params => { return axios.post(`${base}/logout`, params).then(res => res) }
