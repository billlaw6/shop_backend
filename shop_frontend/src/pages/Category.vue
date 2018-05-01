<template>
  <div class="category">
    <index-footer></index-footer> 
  </div>
</template>

<script>
  import IndexFooter from '@/components/common/IndexFooter.vue'
  export default {
    components: {
      'index-footer': IndexFooter
    },
    data () {
      return {
        allData: ''
      }
    },
    created () {
      this.$api({
        method: 'post',
        url: '/category'
      }).then((res) => {
        this.allData = res.data
      }).catch((error) => {
        console.log(error)
      })
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
</style>
