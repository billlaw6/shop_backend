<template lang="html">
  <div class="detail">
    <index-header></index-header> 
    <Carousel autoplay>
      <CarouselItem v-for="item in productDetail.carouselImages" :key="item.order" class="carousel-item">
        <img v-lazy="item.image" alt="">
      </CarouselItem>
    </Carousel>

    <Row class="description">
      <Col span="16">
        <span class="product-name">{{ productDetail.name }}</span> 
      </Col>
      <Col span="8">
        <span class="product-price">{{ productDetail.price | currency }}</span>
      </Col>
    </Row>
    <Row class="operate">
      <span class="product-name">{{ productDetail.name }}</span> 
      <span class="product-price">{{ productDetail.price | currency }}</span>
    </Row>
    <Row class="footer">
      <Col span="2" class="amount-tag">
        <span>数量:</span>
      </Col>
      <Col span="3" class="amount">
        <Input v-model="amount" size="large" step="0.1">
          <span slot="prepend" v-on:click="amountDecrease"><Icon type="android-remove"></Icon></span>
          <span slot="append" v-on:click="amountIncrease"><Icon type="android-add"></Icon></span>
        </Input>
      </Col>
      <Col span="1" class="amount-unit">
        <span>千克</span>
      </Col>
      <Col span="1" class="sum-price">
        <span>{{ this.productDetail.price * this.amount | currency }}</span>
      </Col>
      <Col span="6" class="add-to-cart">
        <div v-on:click="addToCart">
          <Icon type="ios-cart" :size="24"></Icon>
          <span>加入购物车</span>
        </div>
      </Col>
    </Row>
  </div>
</template>

<script>
  import IndexHeader from '@/components/common/IndexHeader.vue'

  export default {
    components: {
      'index-header': IndexHeader
    },
    data () {
      return {
        productDetail: '',
        amount: 1
      }
    },
    methods: {
      amountDecrease: function () {
        console.debug('amount decrease')
        // 为了Input的prepend和append效果（只支持文本），在此麻烦点转换一下
        if (parseFloat(this.amount) > 0.1) {
          this.amount = (parseFloat(this.amount) - 0.1).toFixed(2)
        }
      },
      amountIncrease: function () {
        console.debug('amount decrease')
        if (parseFloat(this.amount) < 10) {
          this.amount = (parseFloat(this.amount) + 0.1).toFixed(2)
        }
      },
      addToCart: function () {
        console.debug('add to cart')
      }
    },
    beforeCreate () {
      console.debug('Detail.vue creating')
      this.$api({
        method: 'get',
        url: '/rest-api/products/' + this.$route.params.productId
      }).then((response) => {
        console.debug('data gotten in Detail:')
        console.debug(response.data)
        this.productDetail = response.data
      }).catch(function (error) {
        console.error(error)
      })
    }
  }
</script>

<style lang="stylus" scoped>
  .ivu-carousel
    img
      display: inline
      width: 100%
  .footer
    height: 10vh
    width: 100vw
    position: fixed
    bottom: 0.1vh
    display: inline
    div
      text-align: center
      color: $primary-color
      // display: inline-block
      vertical-align: middle
      span
        color: red
</style>
