<template lang="html">            
  <div class="service">           
    <ul>
      <li><i class="icon-ok"></i><span>自营品牌</span></li>
      <li><i class="icon-ok"></i><span>无忧退货</span></li>
      <li><i class="icon-ok"></i><span>48小时快速退款</span></li>
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
      display: -webkit-flex
      display: -ms-flex
      display: flex
      justify-content: space-around

      li
        display: -webkit-flex
        display: -ms-flex
        display: flex
        align-items: center
        padding: 3.3vw 0
        span
          i-font-size(font-size, 28)
          padding-left: 1vw
        i
          i-font-size(font-size, 36)
</style>
