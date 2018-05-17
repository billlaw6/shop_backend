<template lang="html">
  <!-- 不加v-if="datas.results"的话会出现未赋值前就访问-->
  <Row>
    <Col span="20" class="hot-product">
      <Carousel class="carousel" v-if="datas.results">
        <CarouselItem v-for="k in mList" :key="k.id" class="carousel-item">
          <router-link :to="{ name:'detail' }">
            <!-- 懒加载值不能用filter，否则加载不了图片 -->
            <img v-lazy="k.image" alt="">
          </router-link>
        </CarouselItem>
      </Carousel>
    </Col>
    <Col span="4" class="hot-product-desc">
      热销产品说明
    </Col>
  </Row>
</template>

<script>
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
        url: '/rest-api/hot-products/'
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
    // padding-bottom: 9vh
  .carousel
    height: inherit
    // background-color: green
    // .ivu-carousel-arrow
    //   height: 5vh
      // background-color: green
    // .ivu-carousel-list
    //   background-color: red
  // .carousel-item
  //   // background-color: red
    a > img
      height: inherit
      width: 100%
   .hot-product-desc
      background-color: green
</style>
