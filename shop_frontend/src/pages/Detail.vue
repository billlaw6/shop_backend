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
      <Col span="12">
        <Input class="amount" v-model="amount" size="large" :number="true">
          <span slot="prepend" v-on:click="amountDecrease"><Icon type="android-remove"></Icon></span>
          <span slot="append" v-on:click="amountIncrease"><Icon type="android-add"></Icon></span>
        </Input>
        <span>千克</span>
      </Col>
      <Col span="4" class="sum-price">
        <span>小计：{{ this.productDetail.price * this.amount | currency }}</span>
      </Col>
    </Row>

    <Tabs value="detail">
      <TabPane label="图片详情" name="detail-pictures">
        Pictures
      </TabPane>
      <TabPane label="文字详情" name="detail-description">
        Description
      </TabPane>
    </Tabs>

    <Row type="flex" justify="space-around" class="footer">
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
  import { getProductDetail } from '../http/api'
  import { mapState, mapActions } from 'vuex'

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
    computed: {
      ...mapState({
        // 大括号方式需要转成对象
        decimals: state => state.cart.decimals,
        cartList: state => state.cart.cartList
      })
    },
    methods: {
      // 带模块命名空间的写简约写法
      ...mapActions('cart', [
        // 中括号方式可直接映射，但只能同名映射
        'removeCartItem',
        'addCartItem'
      ]),
      amountDecrease: function () {
        console.debug('amount decrease')
        if (this.amount > 0.2) {
          this.amount = parseFloat((this.amount - 0.1).toFixed(this.decimals))
        }
      },
      amountIncrease: function () {
        console.debug('amount increase')
        if (parseFloat(this.amount) < 99) {
          // this.amount = parseFloat((this.amount + 0.1).toFixed(this.decimals))
          this.amount = parseFloat((this.amount + 0.1).toFixed(this.decimals))
        }
      },
      addToCart: function () {
        console.debug('add to cart')
        this.$store.dispatch('cart/addCartItem', {'item': this.productDetail, 'amount': this.amount})
        this.$Modal.success({
          title: '加入购物车成功',
          content: '加入购物车成功'
        })
      }
    },
    beforeCreate () {
      console.debug('Detail.vue creating')
      getProductDetail(this.$route.params.productId).then((response) => {
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
  .amount
    width: 30vw
  .footer
    // background-color: red
    height: 10vh
    width: 100vw
    position: fixed
    bottom: 0.1vh
    div
      text-align: center
      color: $primary-color
      // display: inline-block
      vertical-align: middle
      span
        color: red
</style>
