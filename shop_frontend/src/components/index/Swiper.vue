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
  .swiper
    height: 500px
</style>
