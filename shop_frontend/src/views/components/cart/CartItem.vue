<template>
  <div class="product">
    <router-link :to="{ name:'detail', params: { productId: item.id }}">
      <!-- <img v-lazy="imageUrl" alt="product"></img> -->
      <span class="name">{{ item.name }}</span>
      <span class="price">{{ item.price | currency }}</span>
      <span class="sum-price"> 小计：{{ (item.amount * item.price).toFixed(2) | currency }}</span>
    </router-link>
    <div class="amount">
      <Input v-model="item.amount" size="large" :number="true" :readonly="true">
        <span slot="prepend" v-on:click="decreaseCartItemAmount(item)"><Icon type="android-remove"></Icon></span>
        <span slot="append" v-on:click="increaseCartItemAmount(item)"><Icon type="android-add"></Icon></span>
      </Input>
    </div>
    <Button v-on:click="removeCartItem(item)" type="error">
      <Icon type="android-delete"></Icon>&nbsp删除
    </Button>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    props: {
      item: {
        type: Object,
        default: {}
      }
    },
    data () {
      return {
        amount: 1
      }
    },
    computed: {
      ...mapState({
        // 大括号方式需要转成对象
        decimals: state => state.cart.decimals,
        saleUnit: state => state.saleUnit
      }),
      imageUrl: function () {
        return this.item['image'].replace('sale-manage/products/shop_frontend/dist/', '')
      }
    },
    methods: {
      ...mapActions('cart', [
        'emptyCart',
        'setCartList',
        'removeCartItem',
        'decreaseCartItemAmount',
        'increaseCartItemAmount'
      ])
    }
  }
</script>

<style lang="stylus" scoped>
  .product
    background-color: $background-color
    display: inline
    width: 100%
    border: solid 1px $border-color
    margin: 1vh 1vw 5vh 1vw
    img
      width: 100%
      display: flex
      overflow: hidden
    .name
      font-size: 1.2em
      font-weight: bold
      margin: 1vh 1vw 1vh 1vw
    .price, .sum-price
      font-size: 1.3em
      color: red
      margin: 1vh 1vw 1vh 1vw
    .amount
      width: 30vw
      margin: 1vh 1vw 1vh 1vw
    .ivu-btn
      margin: 1vh 1vw 1vh 1vw
</style>

