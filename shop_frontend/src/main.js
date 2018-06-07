// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import { router } from './router/index'
import store from '@/vuex-store/index'
import iView from 'iview'
import 'iview/dist/styles/iview.css'
import './assets/font-awesome-4.7.0/css/font-awesome.min.css' // 免费图标
import VueI18n from 'vue-i18n'
import VueLazyLoad from 'vue-lazyload'
import App from './App'

require('@/libs/filters') // 启用自定义过滤器
// require('@/http/mock') // 启用mock数据，只能放import语句后面

Vue.use(iView)
Vue.use(VueI18n)
Vue.use(VueLazyLoad, {
  error: '../../assets/logo.png',
  loading: '../../assets/logo.png'
})
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
  store
})
