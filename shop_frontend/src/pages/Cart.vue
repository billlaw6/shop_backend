<template lang="html">
    <div class="cart">
      <index-header></index-header>
      <Table :columns="cartListColumns" :data="cartList"></Table>
      <Row type="flex" justify="space-around" class="footer">
        <Col span="6" class="cart-list-sum">
          <span>共计{{ cartListCount }}种商品，合计{{ cartListSum | currency }}</span>
        </Col>
        <Col span="6" class="go-to-index">
          <router-link :to="{ name: 'index' }">
            <Icon type="ios-home" :size="24"></Icon>继续购物
          </router-link>
        </Col>
        <Col span="6" class="empty-cart">
          <div v-on:click="emptyCart">
            <Icon type="ios-cart" :size="24"></Icon>
            <span>清空购物车</span>
          </div>
        </Col>
        <Col span="6" class="empty-cart">
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
  import { mapState, mapGetters, mapActions } from 'vuex'

  export default {
    components: {
      'index-header': IndexHeader
    },
    data () {
      return {
        cartListColumns: [
          {
            title: '名称',
            key: 'name'
          },
          {
            title: '单价',
            key: 'price'
          },
          {
            title: '数量',
            key: 'amount'
          }
        ]
      }
    },
    computed: {
      ...mapState({
        // 大括号方式需要转成对象
        'loginStatus': state => state.loginStatus,
        // 为了能够使用 `this` 获取局部状态，必须使用常规函数
        'cartList' (state) {
          // console.debug(JSON.parse(window.localStorage.getItem('cartList')))
          if (state.cartList.length === 0 &&
              JSON.parse(window.localStorage.getItem('cartList')).length > 0) {
            console.debug('using localStorage cartList')
            this.$store.dispatch('copyCart', JSON.parse(window.localStorage.getItem('cartList')))
          }
          return state.cartList
        }
      }),
      ...mapGetters([
        'cartListCount',
        'cartListSum'
      ])
    },
    methods: {
      ...mapActions([
        'emptyCart'
      ]),
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
</style>
