<template>
  <header class="index-header">
    <head><title>欢迎光临正岩苔茶微官网</title></head>
    <Row>
      <Col span="6">
        <router-link :to="{ name: 'index' }">
          <img src="../../assets/logo.png" alt="Logo" class="logo"></img>
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
    height: 9vh
    width: 100vw
    top: 1vh
    div
      height: 100%
      vertical-align: middle
      // background-color: red
      .logo
        height: 100%
        margin-left: 6px
        // absolute才会限制在父级div下面
        position: absolute
</style>

