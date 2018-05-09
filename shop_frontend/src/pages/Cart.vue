<template lang="html">
    <div class="cart">
      <index-header></index-header>
      
      <!--
      <Table :columns="cartListColumns" :data="cartList"></Table>
      {{ cartList }}
      -->
      <Row v-for="item in cartList" :key="item.id" type="flex" justify="space-around" class="cart-list-product" v-if="cartList.length > 0">
        <Col span="6" class="cart-list-image">
          <img v-lazy="item.image" alt="product-image"></img>
        </Col>
        <Col span="6" class="cart-list-description">
          {{ item.name }} {{ item.sale_price }}
        </Col>
        <Col span="6" class="cart-list-description">
          <item-amount :item="item"></item-amount>
        </Col>
        <Col span="6" class="cart-list-operate">
          <Icon type="android-delete"></Icon>删除
        </Col>
      </Row>
      <Row v-else>
        购物车中暂时没有商品
      </Row>

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
  import ItemAmount from '@/components/common/ItemAmount.vue'
  import { mapState, mapGetters, mapActions } from 'vuex'

  export default {
    components: {
      'index-header': IndexHeader,
      'item-amount': ItemAmount
    },
    data () {
      return {
        // cartListColumns: [
        //   {
        //     title: '名称',
        //     key: 'name'
        //   },
        //   {
        //     title: '单价',
        //     key: 'price'
        //   },
        //   {
        //     title: '数量',
        //     key: 'amount'
        //   }
        // ]
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
              window.localStorage.getItem('cartList')) {
            console.debug('using localStorage cartList')
            this.$store.dispatch('copyCart', JSON.parse(window.localStorage.getItem('cartList')))
            return state.cartList
          } else {
            console.debug('using state cartList')
            return state.cartList
          }
          // 使用深度复制解决Input展示store变量无法直接修改的问题
          // return JSON.parse(JSON.stringify(state.cartList))
        }
      }),
      ...mapGetters([
        'cartListCount',
        'cartListSum'
      ])
    },
    methods: {
      ...mapActions([
        'emptyCart',
        'addCartItem',
        'setCartItemAmount'
      ]),
      amountDecrease: function (item) {
        console.debug('amount decrease')
        if (parseFloat(item.amount) > 0.1) {
          // 为了Input的prepend和append效果（只支持文本），在此麻烦点转换一下
          // item.amount = (parseFloat(item.amount) - 0.1).toFixed(2)
          this.$store.dispatch('addCartItem', {'item': item, 'amount': -0.1})
          // 手动刷新
          // this.cartList = state.cartList
          console.debug(item.amount)
        }
      },
      amountIncrease: function (item) {
        console.debug('amount increase')
        if (parseFloat(item.amount) < 10) {
          // toFixed返回的是string
          // item.amount = (parseFloat(item.amount) + 0.1).toFixed(2)
          this.$store.dispatch('addCartItem', {'item': item, 'amount': 0.1})
          // 手动刷新
          // this.cartList = state.cartList
          console.debug(item.amount)
        }
      },
      setAmount: function (item) {
        console.debug('enter amount')
        // 为了Input的prepend和append效果（只支持文本），在此麻烦点转换一下
        // item.amount = (parseFloat(item.amount) - 0.1).toFixed(2)
        this.$store.dispatch('setCartItemAmount', {'item': item, 'amount': item.amount})
        // 手动刷新
        // this.cartList = state.cartList
        console.debug(item.amount)
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
      // window.localStorage.removeItem('cartList')
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
</style>
