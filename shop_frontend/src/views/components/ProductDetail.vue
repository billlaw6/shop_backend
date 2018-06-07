<template>
  <div>
    <div v-if="productDetail">
      <img :src='productDetail.image | mask_url'></img>
      <div class="product-name">{{ productDetail.name }}</div>
      <div class="product-price">{{ productDetail.price | currency }}</div>
      <div class="product-name">{{ productDetail.description }}</div>
    </div>
  </div>
</template>

<script>
  import { productDetail } from '../api/api'
  export default {
    name: 'ProductDetail',
    data () {
      return {
        productDetail: {}
      }
    },
    methods: {
      get_product_detail () {
        productDetail().then(
          (res) => {
            this.productDetail = res.data
          },
          (error) => {
            console.log('productDetail Error: ' + error)
          }
        ).catch((error) => {
          console.log('catched in productDetail:' + error)
        })
      }
    },
    filters: {
      mask_url: function (value) {
        if (!value) return ''
        value = value.toString()
        return value.replace('rest-api/products/shop_frontend/dist/', '')
      }
    },
    created () {
      // 组件创建完后获取数据，此时data已经被observed了
      this.get_product_detail(this.productId)
    },
    watch: {
      // 如果路由有变化，会再次执行该方法
      '$route': 'get_product_detail'
    }
  }
</script>

<style lang="stylus" scoped>

</style>
