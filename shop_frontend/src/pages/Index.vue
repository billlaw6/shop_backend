<template>
  <!-- 在首页父组件发送http请求,后将数据通过props传递给子组件,可减少请求次数,减少服务器压力 -->
  <div class="index">
    <head>
      <title>欢迎光临正岩苔茶微官网</title>
    </head>
    <v-header></v-header>
    <v-swiper :swiperData="datas.swiper"></v-swiper>
    <v-service></v-service>
    <v-section1 :section1="datas.section1"></v-section1>
  </div>
</template>

<script>
  import Header from '../components/index/Header.vue'
  import Swiper from '../components/index/Swiper.vue'
  import Service from '../components/index/Service.vue'
  import Section1 from '../components/index/Section1.vue'
  // import { mapState } from 'vuex'

  export default {
    components: {
      'v-header': Header,
      'v-swiper': Swiper,
      'v-service': Service,
      'v-section1': Section1
    },
    data () {
      return {
        datas: '',
        loading: true
      }
    },
    beforeCreate () {
      console.log('getting data')
      this.$api({
        method: 'post',
        url: '/index'
      }).then((response) => {
        console.log('response.data')
        this.datas = response.data
      }).catch(function (error) {
        window.alert(error)
      })
    },
    methods: {
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../common/vars'
  .index
    width: 100%
    padding-bottom: 14vw
    background-color: $background-color
</style>

