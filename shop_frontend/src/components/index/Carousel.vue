<template lang="html">
  <!-- 不加v-if="datas.results"的话会出现未赋值前就访问-->
  <Carousel class="hot-product" v-if="datas.results">
    <CarouselItem v-for="k in mList" :key="k.id">
      <router-link :to="{ name:'detail' }">
        <!-- 懒加载值不能用filter，否则加载不了图片 -->
        <img v-lazy="k.image" alt="">
      </router-link>
    </CarouselItem>
  </Carousel>
</template>

<script>
  // import { Lazyload } from 'mint-ui'

  export default {
    // props: {
    //   datas: {
    //     type: Object,
    //     default: {}
    //   }
    // },
    data () {
      return {
        datas: {}
      }
    },
    computed: {
      // 此值不要一开始就用，否则会出现this.datas仍为undefined时导致的报错
      mList: function () {
        this.datas.results.forEach((item, index, array) => {
          item['image'] = item['image'].replace('rest-api/products/shop_frontend/dist/', '')
        })
        return this.datas.results
      }
    },
    beforeCreate () {
      console.log('Carousel.vue creating')
      console.debug('datas before api:' + this.datas)
      this.$api({
        method: 'get',
        url: '/rest-api/products/'
      }).then((response) => {
        console.debug('data gotten in Carousel:')
        console.debug(response.data)
        this.datas = response.data
      }).catch(function (error) {
        console.error(error)
      })
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../../common/vars'

  .hot-product
    height: 50vh
  .ivu-carousel
    height: 100%
    // background-color: green
  .ivu-carousel-list
    height: 100%
  .ivu-carousel-item
    width: 100%
    position: relative
    // background-color: red
    div>a>img
      position: absolute
      height: 100%
      width: 100%
</style>
