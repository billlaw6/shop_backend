<template>
  <Input v-model="locItem.amount" size="large" step="0.1" :number="true" @on-enter="setAmount(locItem)" v-if="locItem">
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
    data () {
      return {
        locItem: ''
      }
    },
    // 计算属性还是会修改原值，会报
    // Error: [vuex] Do not mutate vuex store state outside mutation handlers.
    // computed: {
    //   locItem: {
    //     get: function () {
    //       // return this.item
    //       return JSON.parse(JSON.stringify(this.item))
    //     },
    //     // 后期可尝试自定义set避免上述报错
    //     set: function (newValue) {
    //       console.log(newValue)
    //     }
    //   }
    // },
    methods: {
      ...mapActions([
        'addCartItem',
        'setCartItemAmount'
      ]),
      amountDecrease: function (curItem) {
        console.debug('amount decrease')
        if (parseFloat(curItem.amount) > 0.2) {
          // 为了Input的prepend和append效果（只支持文本），在此麻烦点转换一下
          // item.amount = (parseFloat(item.amount) - 0.1).toFixed(2)
          // console.log('begin')
          // console.log('curItem: ' + curItem.amount)
          this.$store.dispatch('addCartItem', {'item': curItem, 'amount': -0.1})
          // 看action后父组件传入的item是否更新
          // console.log('this.item: ')
          // console.log(this.item)
          // 看action后computed的locItem是否更新
          // console.log('this.locItem: ')
          // console.log(this.locItem)
          // this.item没及时刷新，重新获取无用
          // this.curItem = JSON.parse(JSON.stringify(this.item))
          // console.log('end')
          // 测试发现item没有实时更新，页面刷新操作才会。不知道如何主动触发组件重建
          // console.log('this.item.amount: ' + this.item.amount)
          // this.$nextTick(function () {
          //   console.log('nextTick')
          //   curItem = JSON.parse(JSON.stringify(this.item))
          // })
          // console.log(this.item.amount)
        }
      },
      amountIncrease: function (curItem) {
        console.debug('amount decrease')
        if (parseFloat(curItem.amount) < 9.9) {
          this.$store.dispatch('addCartItem', {'item': curItem, 'amount': 0.1})
        }
      },
      setAmount: function (curItem) {
        // console.debug('setAmount')
        // console.debug(curItem)
        this.$store.dispatch('setCartItemAmount', {'item': curItem, 'amount': curItem.amount})
      }
    },
    mounted () {
      this.locItem = JSON.parse(JSON.stringify(this.item))
    }
  }
</script>

    
