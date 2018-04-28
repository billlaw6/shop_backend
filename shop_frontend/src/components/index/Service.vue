<template lang="html">            
  <div class="service">           
    <ul>
      <li><i class="fa fa-check-circle-o"></i><span>自营品牌</span></li>
      <li><i class="fa fa-check-circle-o"></i><span>无忧退货</span></li>
      <li><i class="fa fa-check-circle-o"></i><span>48小时快速退款</span></li>
    </ul>
  </div>
</template> 

<script>
  export default {
  }
</script>

<style lang="stylus" scoped>
  @import '../../common/vars'
  .service
    border-bottom()
    ul
      i-vendor-value(display, flex)
      justify-content: space-around
      li
        i-vendor-value(display, flex)
        align-items: center
        padding: 1.3vw 0
        span
          i-font-size(font-size, 28)
          padding-left: 1vw
        i
          i-font-size(font-size, 36)
          color: $checked-color
</style>
