<template>
  <div class="index">
    <index-header></index-header> 
    <v-service></v-service>
    <v-carousel v-bind:datas="datas"></v-carousel>
    <v-products v-bind:datas="datas"></v-products>
    <index-footer></index-footer> 
  </div>
</template>

<script>
  import IndexHeader from '@/components/common/IndexHeader.vue'
  import IndexFooter from '@/components/common/IndexFooter.vue'
  import Service from '@/components/index/Service.vue'
  import Products from '@/components/index/Products.vue'
  import Carousel from '@/components/index/Carousel.vue'
  // import { mapState } from 'vuex'

  export default {
    components: {
      'index-header': IndexHeader,
      'index-footer': IndexFooter,
      'v-service': Service,
      'v-products': Products,
      'v-carousel': Carousel
    },
    data () {
      return {
        datas: {},
        loading: true
      }
    },
    methods: {
    },
    beforeCreate () {
      console.log(this.datas)
      this.$api({
        method: 'get',
        url: '/rest-api/products/'
      }).then((response) => {
        console.log(response.data)
        this.datas = response.data
      }).catch(function (error) {
        window.alert(error)
      })
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../common/vars'
  .index
    width: 100%
    padding-bottom: 1vw
    background-color: $background-color
  .layout-logo
    background-color: red
</style>

