<template>
  <div class="index">
    <index-header></index-header> 
    <v-service></v-service>
    <!-- <v-carousel></v-carousel> -->
    <v-products></v-products>
    <v-divider></v-divider>
    <index-footer></index-footer> 
  </div>
</template>

<script>
  import IndexHeader from '@/views/components/common/IndexHeader.vue'
  import IndexFooter from '@/views/components/common/IndexFooter.vue'
  import Divider from '@/views/components/common/Divider.vue'
  import Service from '@/views/components/index/Service.vue'
  import Products from '@/views/components/index/Products.vue'
  import Carousel from '@/views/components/index/Carousel.vue'
  // import { mapState } from 'vuex'

  export default {
    components: {
      'index-header': IndexHeader,
      'index-footer': IndexFooter,
      'v-divider': Divider,
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
    created () {
      console.debug('Index.vue created')
    },
    mounted () {
      console.debug('Index.vue mounted')
    },
    nextTick () {
      console.debug('nextTick')
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

