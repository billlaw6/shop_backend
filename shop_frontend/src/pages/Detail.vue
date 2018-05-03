<template lang="html">
  <div class="detail">
    <index-header></index-header> 
    Detail
  </div>
</template>

<script>
  import IndexHeader from '@/components/common/IndexHeader.vue'

  export default {
    components: {
      'index-header': IndexHeader
    },
    beforeCreate () {
      this.$store.dispatch('setDatas')
    }
  }
</script>

<style lang="stylus" scoped>
  .detail
    width: 100%
    padding-bottom: 14vw
</style>
