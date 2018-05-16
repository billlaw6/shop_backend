<template lang="html">
    <div class="cart">
      <index-header></index-header>
      <div class="filled-cart" v-if="cartList.length > 0">
        <Row v-for="item in cartList" :key="item.id" type="flex" justify="space-around" class="cart-list-product">
          <Col span="6" class="cart-list-image">
            <router-link :to="{ name:'detail', params: { productId: item.id }}">
              <img v-lazy="item.image" alt="product-image"></img>
              {{ item.image }}
            </router-link>
          </Col>
          <Col span="6" class="cart-list-description">
            {{ item.name }} {{ item.price | currency }}
          </Col>
          <Col span="6" class="cart-list-description">
            <Input v-model="item.amount" size="large" :number="true" :readonly="true">
              <span slot="prepend" v-on:click="decreaseCartItemAmount(item)"><Icon type="android-remove"></Icon></span>
              <span slot="append" v-on:click="increaseCartItemAmount(item)"><Icon type="android-add"></Icon></span>
            </Input>
          </Col>
          <Col span="6" class="cart-list-operate">
            <Icon type="android-delete"></Icon>删除
          </Col>
        </Row>

        <Row type="flex" justify="space-around" class="summary">
          <Col span="6" class="cart-list-sum">
            <span>共计{{ cartListCount }}种商品，合计{{ cartListSum | currency }}</span>
          </Col>
        </Row>
      </div>

      <div class="filled-cart" v-else>
        <Row>
          购物车中暂时没有商品
        </Row>
      </div>

      <Row type="flex" justify="space-around" class="footer">
        <Col span="8" class="go-to-index">
          <router-link :to="{ name: 'index' }">
            <Icon type="ios-home" :size="24"></Icon>继续购物
          </router-link>
        </Col>
        <Col span="8" class="empty-cart">
          <div v-on:click="emptyCart">
            <Icon type="ios-cart" :size="24"></Icon>
            <span>清空购物车</span>
          </div>
        </Col>
        <Col span="8" class="empty-cart">
          <div v-on:click="checkoutCart">
            <Icon type="ios-cart" :size="24"></Icon>
            <span>结算</span>
          </div>
        </Col>
      </Row>
    </div>
</template>

<script>
  import IndexHeader from '@/components/common/IndexHeader.vue'
  import ItemAmount from '@/components/common/ItemAmount.vue'
  import { mapState, mapGetters, mapActions } from 'vuex'

  export default {
    components: {
      'index-header': IndexHeader,
      'item-amount': ItemAmount
    },
    computed: {
      ...mapState({
        // 大括号方式需要转成对象
        'loginStatus': state => state.login.loginStatus,
        'cartList': state => state.cart.cartList
      }),
      ...mapGetters([
        // 模块命名空间写法一
        'cartListCount',
        'cartListSum'
      ])
    },
    methods: {
      // 模块命名空间写法二
      ...mapActions('cart', [
        'emptyCart',
        'setCartList',
        'addCartItem',
        'decreaseCartItemAmount',
        'increaseCartItemAmount'
      ]),
      resetCartList: function (newCartList) {
        console.debug('resetCartList')
        // cartList有任何改动（子元素的任何属性改变）都直接重置state的根元素cartList，以触发getters更新
        this.$store.dispatch('setCartList', newCartList)
      },
      checkoutCart: function (checkoutList) {
        console.debug('checkout cart')
        if (this.loginStatus) {
          console.debug('checking')
          this.$store.dispatch('emptyCart')
        } else {
          console.debug('redirecting')
          this.$router.push({ name: 'login' })
        }
      }
    },
    mounted () {
      console.debug('Cart.vue mounted')
    },
    beforeCreate () {
      console.log('Cart.vue creating')
      // window.localStorage.removeItem('cartList')
    }
  }
</script>

<style lang="stylus" scoped>
  .footer
    width: 100vw
    height: 10vh
    position: fixed
    bottom: 0.1vh
    div
      text-align: center
  .item-amount
    width: 30vw
</style>
