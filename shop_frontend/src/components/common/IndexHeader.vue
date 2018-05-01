<template>
  <header class="index-header">
    <Row>
      <Col span="6" class="index">
        <router-link to="">
          <i class=""></i>
          首页
        </router-link>
      </Col>
      <Col span="6" class="category">
        <router-link to="">
          <i class=""></i>
          分类 
        </router-link>
      </Col>
      <Col span="6">
        <router-link to="cart">
          <i class=""></i>
          购物车
        </router-link>
      </Col>
      <Col span="6">
        <router-link to="user">
          <i class=""></i>
          我的
        </router-link>
      </Col>
    </Row>
  </header>
</template>

<script>
  export default {
  }
</script>

<style lang="stylus" scoped>
  @import '../../common/vars'
  
  .index-header
    width: 100vw
    position: fixed
    bottom: 0
    header
      width: 100%
      div>div>a
        i-vendor-value(display, flex)
        color: red

</style>

