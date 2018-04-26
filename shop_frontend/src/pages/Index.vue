<template>
  <!-- 在首页父组件发送http请求,后将数据通过props传递给子组件,可减少请求次数,减少服务器压力 -->
  <div class="index">
    <head>
      <title>欢迎光临正岩苔茶微官网</title>
    </head>
    <v-header></v-header>
    <v-swipe :swiperData="datas.swipe"></v-swipe>
    <v-service></v-service>
    <v-section1 :section1="datas.section1"></v-section1>
    <v-section2 :section2="datas.section2"></v-section2>
    <v-section3 :section3="datas.section3"></v-section3>
    <v-section4 :section4="datas.section4"></v-section4>
    <v-baseline></v-baseline>
    <v-footer></v-footer>
  </div>
</template>

<script>
  import Header from '@/components/index/Header.vue'
  import Swipe from '@/components/index/Swipe.vue'
  import Service from '@/components/index/Service.vue'
  import Section1 from '../components/index/Section1.vue'
  import Section2 from '../components/index/Section2.vue'
  import Section3 from '../components/index/Section3.vue'
  import Section4 from '../components/index/Section4.vue'
  import Baseline from '../components/common/Baseline.vue'
  import Footer from '../components/common/Footer.vue'
  // import { mapState } from 'vuex'

  export default {
    components: {
      'v-header': Header,
      'v-swipe': Swipe,
      'v-service': Service,
      'v-section1': Section1,
      'v-section2': Section2,
      'v-section3': Section3,
      'v-section4': Section4,
      'v-baseline': Baseline,
      'v-footer': Footer
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

