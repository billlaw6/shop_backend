<template>            
  <Row class="service">           
    <Col span="8"><Icon type="checkmark"></Icon><span>自营品牌</span></Col>
    <Col span="8"><Icon type="checkmark"></Icon><span>无忧退货</span></Col>
    <Col span="8"><Icon type="checkmark"></Icon><span>48小时快速退款</span></Col>
  </Row>
</template> 

<script>
  export default {
  }
</script>

<style lang="stylus" scoped>
  @import '../../common/vars'

  .service
    border-bottom()
    i-font-size(font-size, 23)
    color: $checked-color
  .ivu-col
    text-align: center
    i
      margin: 1vh 1vw 1vh 1vw
</style>
