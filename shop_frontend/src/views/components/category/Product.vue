<template>
  <div class="product">
    <router-link :to="{ name:'detail', params: { productId: item.id }}">
      <img v-lazy="imageUrl" alt="product"></img><br/>
      <span class="name">{{ item.name }}</span>
      <span class="price">{{ item.price | currency }}</span>
    </router-link>
    <div class="product-operate">
      <Input class="amount" v-model="amount" size="large" :number="true">
        <span slot="prepend" v-on:click="amountDecrease"><Icon type="android-remove"></Icon></span>
        <span slot="append" v-on:click="amountIncrease"><Icon type="android-add"></Icon></span>
      </Input>
      <Button v-on:click="addToCart" type="primary">加入购物车</Button>
    </div>
  </div>
</template>

<script>
  import { mapState } from 'vuex'

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
      amountDecrease: function () {
        console.debug('amount decrease')
        if (this.amount > 0.2) {
          this.amount = parseFloat((this.amount - this.saleUnit).toFixed(this.decimals))
        }
      },
      amountIncrease: function () {
        console.debug('amount increase')
        if (parseFloat(this.amount) < 99) {
          this.amount = parseFloat((this.amount + this.saleUnit).toFixed(this.decimals))
        }
      },
      addToCart: function () {
        let _this = this
        console.debug('add to cart')
        _this.$store.dispatch('cart/addCartItem', {'item': _this.item, 'amount': _this.amount})
        _this.$Message.success({
          title: '加入购物车成功',
          content: '加入购物车成功'
        })
      }
    }
  }
</script>

<style lang="stylus" scoped>
  .product
    background-color: $background-color
    width: 100%
    img
      width: 100%
      display: flex
      overflow: hidden
    .name
      font-size: 1em
      font-weight: bold
      margin: 1vh 1vw 1vh 1vw
    .price
      font-size: 1.3em
      color: red
      margin: 1vh 1vw 1vh 1vw
  .product-operate
    .amount
      width: 30vw
      margin: 1vh 1vw 1vh 1vw
    button
      display: inline-block
      float: right
      margin: 1vh 1vw 1vh 1vw
</style>

