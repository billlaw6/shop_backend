<template lang="html">
  <div class="product">
    <!-- 不加v-if="datas.results"的话会出现未赋值前就访问，TypeError: undefined is not an object (evaluating 'this.datas.results.forEach') -->
    <!-- {{ m_list }}<br/> -->
    <AutoComplete
      v-model="keyword"
      :data="m_list"
      size="large"
      icon="ios-search"
      placeholder="搜索">
      <div class="demo-auto-complete-item">
        <Option v-for="item in m_list" :key="item.id" :value="item.name">
          <span class="demo-auto-complete-title">{{ item.name }}</span>
          <span class="demo-auto-complete-count">{{ item.price }}</span>
        </Option>
      </div>
    </AutoComplete>
    <Row class="product-list" v-if="datas.results">
      <Col span="6" v-for="k in m_list" :key="k.id">
        <router-link :to="{ name:'detail' }">
          <!-- 懒加载值不能用filter，否则加载不了图片 -->
          <img v-lazy="k.image" alt="">
          <span>{{ k.name }}</span>
          <span>{{ k.price | currency }}</span>
        </router-link>
      </Col>
    </Row>
  </div>
</template>

<script>
  export default {
    props: {
      datas: {
        type: Object,
        // 赋初始值防止报undefined错
        default: {}
      }
    },
    data () {
      return {
        keyword: ''
      }
    },
    computed: {
      // 此值不要一开始就用，否则会出现this.datas仍为undefined时导致的报错
      m_list: function () {
        // 好像filter修改原值，filter以后相应数据没了
        let tmpArray = this.datas.results
        let tmpArray1 = tmpArray.filter((item, index, array) => {
          // console.log(this.keyword)
          // console.log(item)
          if (item.name.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
            return true
          // price必须转换成string型
          } else if (item.price.toString().indexOf(this.keyword) !== -1) {
            return true
          // 好像加了description后效率太低
          // } else if (item.description.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
          //   return true
          } else {
            return false
          }
        })
        // 过滤后再mask URL
        tmpArray1.forEach((item, index, array) => {
          item['image'] = item['image'].replace('rest-api/products/shop_frontend/dist/', '')
        })
        return tmpArray1
      }
    },
    methods: {
      filterList (value, option) {
        // window.alert('serching')
        console.log(value)
        console.log(option)
        return option.toUpperCase().indexOf(value.toUpperCase()) !== -1
      }
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../../common/vars'

  .product
    // background-color: red
    div>div
      // background-color: red
      // 上右下左
      padding: 1vh 1vw 1vh 1vw
      a>img
        width: 100%
    // .demo-auto-complete-item
    //   padding: 4px 0
    //   border-bottom: 1px solid #F6F6F6
    
    // .demo-auto-complete-group
    //   font-size: 12px
    //   padding: 4px 6px
    
    // .demo-auto-complete-group span
    //   color: #666
    //   font-weight: bold
    
    // .demo-auto-complete-group a
    //   float: right
    
    // .demo-auto-complete-count
    //   float: right
    //   color: #999
    
    // .demo-auto-complete-more
    //   display: block
    //   margin: 0 auto
    //   padding: 4px
    //   text-align: center
    //   font-size: 12px
</style>
