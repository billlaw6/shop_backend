<template lang="html">
  <div class="wrap">
    <v-go-login></v-go-login>
    <ul class="something" v-if='carList'>
      <li v-for="(k,i) in carList">
          <div class="something-left" @click="toggle">
            <label class="true" :class="{false:!k.choseBool}">
              <input type="checkbox" v-model="k.choseBool">
            </label>
          </div>
          <div class="something-middle">
            <img :src="k.imgPath">
          </div>
          <div class="something-right">
            <p>{{k.title}}</p>
            <p style="color:rgb(199, 108, 28)"> {{k.col}} - {{k.size}}</p>
            <p>售价：{{k.price}}元</p>
            <div class="something-right-bottom" @click="cut(i)">
              <span></span>
            </div>
          </div>
      </li>
    </ul>
  </div>
</template>

<script>
  // 提示登录组件
  import GoLogin from '@/components/cart/GoLogin.vue'
  // import Util from '../../common/common'
  export default {
    components: {
      'v-go-login': GoLogin
    },
    computed: {
      carList () {
        return this.$store.state.detail.carList
      }
    },
    mounted () {
      // 初始化先获取购物车商品列表 否则 页面刷新出Bug
      if (this.$store.state.detail.carList === '') {
        this.$store.commit('RESET_CARLIST')
      }
    },
    methods: {
      cut (i) {
      // 点击垃圾桶，删除当前商品，这里用splice和filter都会bug,只能重置数组
        let newCarList = []
        for (let k = 0; k < this.carList.length; k++) {
          if (k !== i) {
            newCarList.push(this.carList[k])
          }
        }

        // 点击垃圾桶 把商品数量count-1
        this.$store.dispatch('setLocalCount', false)
        this.$store.dispatch('cutCarList', newCarList)
      },
      toggle () {
        setTimeout(() => {
          // 每点击一下都会改变choseBool的布尔值,所以要重置数组
          this.$store.dispatch('cutCarList', this.carList)
        }, 0)
      }
    }
  }
</script>

<style lang="stylus" scoped>
</style>
