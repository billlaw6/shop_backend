<template>
  <Input v-model="locItem.amount" size="large" step="0.1" :number="true" :on-enter="setAmount" v-if="item">
    <span slot="prepend" v-on:click="amountDecrease(locItem)"><Icon type="android-remove"></Icon></span>
    <span slot="append" v-on:click="amountIncrease(locItem)"><Icon type="android-add"></Icon></span>
  </Input>
</template>

<script>
  import { mapActions } from 'vuex'

  export default {
    props: {
      item: {
        type: Object,
        default: {}
      }
    },
    // data () {
    //   return {
    //     'locItem': ''
    //   }
    // },
    // 计算属性还是会修改原值，会报
    // Error: [vuex] Do not mutate vuex store state outside mutation handlers.
    computed: {
      locItem: function () {
        return JSON.parse(JSON.stringify(this.item))
      }
    },
    methods: {
      ...mapActions([
        'addCartItem',
        'setCartItemAmount'
      ]),
      amountDecrease: function (item) {
        console.debug('amount decrease')
        if (parseFloat(item.amount) > 0.1) {
          // 为了Input的prepend和append效果（只支持文本），在此麻烦点转换一下
          // item.amount = (parseFloat(item.amount) - 0.1).toFixed(2)
          this.$store.dispatch('addCartItem', {'item': item, 'amount': -0.1})
          console.debug(item.amount)
        }
      },
      amountIncrease: function (item) {
        console.debug('amount increase')
        if (parseFloat(item.amount) < 10) {
          // toFixed返回的是string
          // item.amount = (parseFloat(item.amount) + 0.1).toFixed(2)
          this.$store.dispatch('addCartItem', {'item': item, 'amount': 0.1})
          console.debug(item.amount)
        }
      },
      setAmount: function (item) {
        console.debug('enter amount')
          // 为了Input的prepend和append效果（只支持文本），在此麻烦点转换一下
          // item.amount = (parseFloat(item.amount) - 0.1).toFixed(2)
        this.$store.dispatch('setCartItemAmount', {'item': item, 'amount': item.amount})
        console.debug(item.amount)
      }
    }
  }
</script>

    
