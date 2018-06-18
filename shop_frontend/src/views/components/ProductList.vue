<template>
  <div>
    <Input size="large" type="text" v-model="keyword" placeholder="搜索" :autofocus=true></Input>
    <div @click="sort_by_price_desc()">按价格降序</div>
    <div @click="sort_by_price_asce()">按价格升序</div>
    <div @click="sort_by_online_desc()">按上架时间</div>
    <Row>
      <Col v-for="(product, index) in productList.results" :key="index" span="12">
        <router-link :to='"/product/"+product.id'>
          <img :src='product.image | maskImageUrl'></img>
          <div class="product-name">{{ product.name }}</div>
        </router-link>
        <div class="product-price">{{ product.price | currency }}</div>
        <div class="updated_at">{{ product.updated_at.replace('T', ' ').slice(0, 16) }}</div>
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
      },
      sort_by_price_desc () {
        return this.productList.results.sort(function (a, b) {
          return b.price - a.price
        })
      },
      sort_by_price_asce () {
        return this.productList.results.sort(function (a, b) {
          return a.price - b.price
        })
      },
      sort_by_online_desc () {
        return this.productList.results.sort(function (a, b) {
          return Date.parse(b.updated_at) - Date.parse(a.updated_at)
        })
      }
    },
    mounted () {
      this.get_product_list(this.openid)
    }
  }
</script>

<style lang="stylus" scoped>
</style>
