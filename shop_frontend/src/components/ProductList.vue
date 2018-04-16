<template>
  <div>
    <Row>
      <Col v-for="(product, index) in productList.results" :key="index" span="12">
        <router-link :to='"/product/"+product.id'>
          <img :src='product.image | mask_url'></img>
          <div class="product-name">{{ product.name }}</div>
        </router-link>
        <div class="product-price">{{ product.price | currency }}</div>
      </Col>
    </Row>
  </div>
</template>

<script>
  import { productList } from '../api/api'
  export default {
    name: 'ProductList',
    data () {
      return {
        productList: {}
      }
    },
    methods: {
      get_product_list () {
        productList().then(
          (res) => {
            this.productList = res.data
          },
          (error) => {
            console.log('productList Error: ' + error)
          }
        ).catch((error) => {
          console.log('catched in productList:' + error)
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
    mounted () {
      this.get_product_list(this.openid)
    }
  }
</script>

<style lang="stylus" scoped>

</style>
