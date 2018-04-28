<template lang="html">
  <section class="product" v-if='product_list'>
    <ul class="product-list">
      <li v-for="k in m_product_list">
        <router-link :to="{ name:'detail' }" :key="k.id">
          <!-- 懒加载值不能用filter，否则加载不了图片 -->
          <img v-lazy="k.image" alt="">
        </router-link>
      </li>
    </ul>
    <router-link :to="{ name: 'detail'}"  class="product-banner">
      <img v-lazy="product_list.banner" v-if='product_list'>
    </router-link>
  </section>
</template>

<script>
  // import { Lazyload } from 'mint-ui'

  export default {
    props: ['product_list'],
    computed: {
      m_product_list: function () {
        this.product_list.forEach((item, index, array) => {
          item['image'] = item['image'].replace('rest-api/products/shop_frontend/dist/', '')
        })
        return this.product_list
      }
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../../common/vars'
  .product
    padding-top()
    .product-list-title
      bordor-top()
      background-color: $background-color
      text-align: center
      padding: 4vw 0
      i-font-size(font-size, 40)
      color: $content-color
      position: relative
      i
        position: absolute
        right: 6vw
        top: 50%
        i-font-size(font-size, 56)
        i-font-size(margin-top, -16)
        &::before
          color: rgb(159, 159, 159)
    .product-list
      display: -ms-flex
      display: -webkit-box
      display: -ms-flexbox
      display: flex
      -ms-flex-wrap: wrap
      flex-wrap: wrap
      -ms-flex-pack: distribute
      justify-content: space-around
      width: 100vw
      overflow: hidden
      /* 上 右 下 左 */
      padding: 2vw 2vw 2vw 0vw
      li
        float: left
        line-height: 40px
        display: inline
        height: auto
        word-break: break-all
        word-wrap: break-word
        padding: 1vw

        a,img[lazy=loading]
          width: 50px
          height: 50px
          display: block
    .product-banner
      display: block
      width: 100vw
      img
        width: 100%
        height: 24vw
</style>
