<template>
  <div class="index">
    <head><title>欢迎光临正岩苔茶微官网</title></head>
    <index-footer></index-footer> 
  </div>
</template>

<script>
  import IndexFooter from '@/components/common/IndexFooter.vue'
  // import { mapState } from 'vuex'

  export default {
    components: {
      'index-footer': IndexFooter
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
  .index
    width: 100%
    padding-bottom: 1vw
    background-color: $background-color
  .layout-logo
    background-color: red
</style>

