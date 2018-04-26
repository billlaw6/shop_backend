<template lang="html">
    <div class="cart">
      <!-- slot分发内容 让子组件混合父组件的内容 -->
      <v-header>
        <h1 slot="title">购物车</h1>
      </v-header>
      <!-- 根据购物车是否有商品加载不同的组件 -->
      <v-loaded v-if="count"></v-loaded>
      <v-empty v-else></v-empty>
      <v-footer></v-footer>
    </div>
</template>

<script>
import Header from '@/components/common/Header.vue'
import Empty from '@/components/cart/Empty.vue'
import Loaded from '@/components/cart/Loaded.vue'
import Footer from '@/components/cart/Footer.vue'

export default {
  components: {
    'v-header': Header,
    'v-empty': Empty,
    'v-loaded': Loaded,
    'v-footer': Footer
  },

  computed: {
    count () {
      return this.$store.state.detail.count
    }
  },
  mounted () {
    // 防止刷新页面数据为空
    if (this.$store.state.detail.count === '') {
      this.$store.commit('RESET_COUNT')
    }
  }
}
</script>

<style lang="stylus" scoped>
.cart {
  width: 100%
  padding-bottom: 14vw
}
</style>
