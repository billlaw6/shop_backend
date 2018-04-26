<template>            
  <mt-swipe class="swiper" :auto="4000" v-if='swiperData'>
    <mt-swipe-item v-for="k in swiperData" :key="k.id">
        <img :src="k.imgPath">
    </mt-swipe-item>            
  </mt-swipe>
</template>                       

<script>
  export default {
    props: ['swiperData']
  }
</script>

<style lang="stylus" scoped>
  @import '../../common/vars'
  .mint-swipe
    width: 100%
    height: 50vw
    a, img
      display: block
      width: 100%
      height: 100%
</style>
