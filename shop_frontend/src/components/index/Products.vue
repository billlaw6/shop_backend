<template lang="html">
  <div class="product">
    <Row class="product-search">
      <Col span="10">
        <AutoComplete v-model="keyword" placeholder="搜" icon="ios-search" :clearable="true">
          <Option v-for="option in aList" :value="option.name" :key="option.id">
            <span class="product-name">{{ option.name }}</span>
            <span class="product-price">{{ option.price | currency }}</span>
          </Option>
        </AutoComplete>
      </Col>
      <Col span="4">
        <Button type="primary" @click="searchProduct">搜</Button>
      </Col>
    </Row>

    <Row class="product-list">
      <Col span="6" v-for="item in mList.results" :key="item.id">
        <router-link :to="{ name:'detail', params: { productId: item.id }}">
          <img v-lazy="item.image" alt="product"></img>
          <span>{{ item.name }}</span>
          <span>{{ item.price | currency }}</span>
        </router-link>
      </Col>
    </Row>
  </div>
</template>

<script>
  import { getProducts } from '../../http/api'

  export default {
    data () {
      return {
        keyword: '',
        datas: '',
        mList: ''
      }
    },
    computed: {
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
            } else if (item.description.toString().indexOf(this.keyword.toUpperCase()) !== -1) {
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
      // 使用computed属性替换autocomplete的filter-method
      // filterList (value, option) {
      //   // value确实为输入值，option为选项值
      //   console.log('value:' + value)
      //   // console.log('option')
      //   console.log(option)
      //   // if (option.name.toUpperCase().indexOf(value.toUpperCase()) !== -1) {
      //   //   return true
      //   // } else if (option.price.toString().indexOf(value) !== -1) {
      //   //   return true
      //   // } else {
      //   //   return false
      //   // }
      // },
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
            } else if (item.description.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else {
              return false
            }
          })
          this.mList.results = tmpArray1
          console.debug(this.keyword)
          console.debug(this.mList.results)
        }
      }
    },
    beforeCreate () {
      console.log('Products.vue creating')
      getProducts().then((response) => {
        console.debug('data gotton in Products:')
        console.debug(response.data)
        this.datas = response.data
        // 深拷贝，否则datas和mList相互影响
        this.mList = JSON.parse(JSON.stringify(response.data))
      }).catch(function (error) {
        console.error(error)
      })
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../../common/vars'

  .product
    margin: 1vh 1vw 1vh 1vw
  .product-search
    height: 12vh
    // background-color: red
    display: flex
    div
      vertical-align: middle
  .product-list, .ivu-row
    // background-color: red
    div,.ivu-col
      // background-color: red
      // background-color: red
      // 上右下左
      padding: 1vh 1vw 1vh 1vw
      a>img
        width: 100%
  .product-name
    font-weight: bold
  .product-price
    color: $primary-color 
    float: right
</style>
