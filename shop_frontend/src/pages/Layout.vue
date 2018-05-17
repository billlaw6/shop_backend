<template>
  <div class="layout">
    <head><title>欢迎光临正岩苔茶微官网</title></head>
    <Layout>
      <Header>
        <Menu mode="horizontal" theme="dark" active-name="1">
          <div class="layout-logo"></div>
          <div class="layout-nav">
            <MenuItem name="1">
              <Icon type="ios-navigate"></Icon>
              Item 1
            </MenuItem>
            <MenuItem name="2">
              <Icon type="ios-keypad"></Icon>
              Item 2
            </MenuItem>
            <MenuItem name="3">
              <Icon type="ios-analytics"></Icon>
              Item 3
            </MenuItem>
            <MenuItem name="4">
              <Icon type="ios-paper"></Icon>
              Item 4
            </MenuItem>
          </div>
        </Menu>
      </Header>
      <Content>
        <v-product-list></v-product-list>
        <Carousel autoplay loop>
          <CarouselItem v-for="product in datas.results" :key="product.id">
            <div>
              <img :src="product.image | maskImageUrl"></img>
            </div>
          </CarouselItem>
        </Carousel>
      </Content>
      <Footer class="layout-footer-center">2011-2016 &copy; TalkingData</Footer>
    </Layout>
  </div>
</template>

<script>
  import Header from '@/components/common/Header.vue'
  import ProductList from '@/components/ProductList.vue'
  import Footer from '@/components/common/Footer.vue'
  // import { mapState } from 'vuex'

  export default {
    components: {
      'v-header': Header,
      'v-product-list': ProductList,
      'v-footer': Footer
    },
    data () {
      return {
        datas: '',
        loading: true
      }
    },
    beforeCreate () {
      console.log('getting data')
      this.$api({
        method: 'get',
        url: '/rest-api/products/'
      }).then((response) => {
        console.log(response.data)
        this.datas = response.data
      }).catch(function (error) {
        window.alert(error)
      })
    },
    methods: {
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../common/vars'
  .layout
    width: 100%
    padding-bottom: 1vw
    background-color: $background-color
  .layout-logo
    background-color: red
</style>

