<template lang="html">
  <mt-header title="电商联盟">
    <router-link :to="{name:''}" slot="right">
      <mt-button icon="search"></mt-button>
    </router-link>
  </mt-header>
</template>

<script>
  export default {}
</script>

<style lang="stylus" scoped>
  @import '../../../common/vars'

  .mint-header
    padding: 6.8vw 4.8vw
    background-color: $background-color
    color: $content-color!important
    i-font-size(font-size, 40px)
</style>
