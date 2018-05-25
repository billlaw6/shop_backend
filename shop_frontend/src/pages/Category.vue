<template>
  <div class="category">
    <index-header></index-header> 
    {{ pList.count }}
    {{ productListCount }}
    <div class="category">
     <ul class="product-list">
      <li v-for="item in pList.results" :key="item.id" class="product">
        <v-product :item="item"></v-product>
      </li>
     </ul>
    </div>
    <index-footer></index-footer> 
  </div>
</template>

<script>
  import IndexHeader from '@/components/common/IndexHeader.vue'
  import Product from '@/components/category/Product.vue'
  import IndexFooter from '@/components/common/IndexFooter.vue'
  import { getProducts } from '@/http/api'
  import { mapState, mapGetters, mapActions } from 'vuex'

  export default {
    components: {
      'index-header': IndexHeader,
      'v-product': Product,
      'index-footer': IndexFooter
    },
    data () {
      return {
        allData: ''
      }
    },
    computed: {
      // 模块命名空间写法一
      ...mapState('category', {
        'pList': state => state.productList
      }),
      // 模块命名空间写法一
      ...mapGetters('category', [
        'productListCount'
      ])
    },
    methods: {
      ...mapActions({
        setProductList: 'category/setProductList'
      })
    },
    beforeCreate () {
      let _this = this
      if (_this.productListCount) {
        console.debug('local products is empty')
      } else {
        getProducts().then((response) => {
          let _this = this
          console.debug('data gotton in Products:')
          console.debug(response.data)
          this.datas = response.data
          // 深拷贝，否则datas和mList相互影响
          this.mList = JSON.parse(JSON.stringify(response.data))
          _this.setProductList(this.mList).then(() => {
            console.debug('state product list set')
          })
        }).catch(function (error) {
          console.error(error)
        })
      }
    }
  }
</script>

<style lang="stylus" scoped>
  .category
    width: 100%
    height: 100%
    display: -webkit-box
    display: -ms-flexbox
    display: flex
    -webkit-box-orient: vertical
    -webkit-box-direction: normal
    -ms-flex-flow: column nowrap
    flex-flow: column nowrap
    .view
      width: 100%
      height:100%
      display: -webkit-box
      display: -ms-flexbox
      display: flex
  .product
    display: inline-block
    width: 30vw
    float: left
</style>
