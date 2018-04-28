<template>
  <!-- 在首页父组件发送http请求,后将数据通过props传递给子组件,可减少请求次数,减少服务器压力 -->
  <div class="index">
    <head>
      <title>欢迎光临正岩苔茶微官网</title>
    </head>
    <Carousel autoplay loop>
      <CarouselItem v-for="product in datas.results" >
        <div>
          <img src="product.image" :key="product.id"></img>
        </div>
      </CarouselItem>
    </Carousel>
  </div>
</template>

<script>
  import Header from '@/components/common/Header.vue'
  import Footer from '@/components/common/Footer.vue'
  // import { mapState } from 'vuex'

  export default {
    components: {
      'v-header': Header,
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
        method: 'get',
        url: '/rest-api/products/'
      }).then((response) => {
        console.log(response.data)
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

