<template lang="html">
  <div class="products">
    <div class="product-search">
      <div class="search-box">
        <AutoComplete v-model="keyword" placeholder="搜" icon="ios-search" :clearable="true">
          <Option v-for="option in aList" :value="option.name" :key="option.id">
            <span class="product-name">{{ option.name }}</span>
            <span class="product-price">{{ option.price | currency }}</span>
          </Option>
        </AutoComplete>
      </div>
      <div class="search-button">
        <Button type="primary" @click="searchProduct">搜</Button>
      </div>
    </div>

    <ul class="product-list">
      <li class="product" v-for="item in mList.results" :key="item.id">
        <v-product :item="item"></v-product>
      </li>
    </ul>
  </div>
</template>

<script>
  import { getProducts } from '@/http/api'
  import { mapGetters, mapActions } from 'vuex'
  import Product from '@/views/components/category/Product.vue'

  export default {
    components: {
      'v-product': Product
    },
    data () {
      return {
        keyword: '',
        datas: '',
        mList: ''
      }
    },
    computed: {
      ...mapGetters('category', [
        'productListCount'
      ]),

      aList: function () {
        // 用于autocomplete
        if (Array.isArray(this.datas.results)) {
          // 深度拷贝方法
          let tmpArray = JSON.parse(JSON.stringify(this.datas.results))
          return tmpArray.filter((item, index, array) => {
            if (item.name.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return array.indexOf(item) === index
            } else if (item.price.toString().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else if (item.pinyin.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else if (item.py.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else if (item.description.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else {
              return false
            }
          })
        } else {
          return []
        }
      }
    },
    methods: {
      ...mapActions({
        setProductList: 'category/setProductList'
      }),

      searchProduct () {
        // 点击“搜”按钮时执行
        console.debug('搜')
        if (Array.isArray(this.datas.results)) {
          // 好像filter修改原值，filter以后相应数据没了，所以必须需要深拷贝
          console.debug(this.datas.results)
          let tmpArray = JSON.parse(JSON.stringify(this.datas.results))
          let tmpArray1 = tmpArray.filter((item, index, array) => {
            if (item.name.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else if (item.price.toString().indexOf(this.keyword) !== -1) {
              return true
            } else if (item.pinyin.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else if (item.py.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else if (item.description.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else {
              return false
            }
          })
          this.mList.results = tmpArray1
          // console.debug(this.keyword)
          // console.debug(this.mList.results)
        }
      }
    },
    beforeCreate () {
      console.log('Products.vue creating')
      getProducts().then((response) => {
        let _this = this
        console.debug('data gotton in Products:')
        console.debug(response.data)
        _this.datas = response.data
        // 深拷贝，否则datas和mList相互影响
        _this.mList = JSON.parse(JSON.stringify(response.data))
        _this.setProductList(_this.mList).then(() => {
          console.debug('state product list set')
        })
      }).catch(function (error) {
        console.error(error)
      })
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../../../common/vars'

  .products
    margin: 1vh 1vw 1vh 1vw
    // background-color: red
    background-color: $background-color
  .product-search
    width: 100%
    div.search-box
      width: 50%
      margin: 0.5vh 0.1vw 0.5vh 0.5vw
      display: inline-block
    div.search-button
      display: inline-block
      margin: 0.5vh 0.5vw 0.5vh 0.1vw
  .product-list
    background-color: $background-color
    .product
      // 上右下左
      display: inline-block
      border: solid 1px $border-color
      padding: 0.1vh 0.1vw 0.1vh 0.1vw
      // margin: 0.1vh 0.1vw 0.1vh 0.1vw
      overflow: hidden
      // background-color: red
      width: 48vw
      // float: left
</style>
