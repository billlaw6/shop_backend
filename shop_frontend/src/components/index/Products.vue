<template lang="html">
  <div class="product">
    <!-- 不加v-if="datas.results"的话会出现未赋值前就访问-->
    <Row class="product-search">
      <Col span="10">
        <AutoComplete v-model="keyword" :data="testData" :filter-method="filterList">
        </AutoComplete>
      </Col>
      <Col span="4">
        <Button type="primary" @click="searchProduct">搜</Button>
      </Col>
    </Row>

    <!-- {{ mList }}<br/> -->
    <Row class="product-list">
      <Col span="6" v-for="item in mList.results" :key="item.id">
        <div><img v-lazy="item.image" alt="product"></img></div>
        <span>{{ item.name }}</span>
        <span>{{ item.price | currency }}</span>
      </Col>
    </Row>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        testData: ['laskdjfl', 'lskdjlllsd', 'kjljjkdkaa'],
        keyword: '',
        datas: '',
        mList: ''
      }
    },
    computed: {
    },
    methods: {
      filterList (value, option) {
        // value确实为输入值，option为选项值
        // console.log('value:' + value)
        // console.log('option')
        // console.log(option)
        // return option.name.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1
        return option.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1
      },
      searchProduct () {
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
      this.$api({
        method: 'get',
        url: '/rest-api/products/'
      }).then((response) => {
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

  .search
    height: 12vh
    background-color: red
    display: flex
    div
      vertical-align: middle
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
