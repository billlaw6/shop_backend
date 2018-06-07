<template>
  <div>
    <!-- 用于将非footer内容和footer分开 -->
    <div class="pusher"></div>
    <Row class="footer">
      <Col span="6" class="index" :class="{ active: selected==='index'}">
        <router-link :to="{ name: 'index' }">
          <Icon type="ios-home" :size="24"></Icon><br/>
          首页
        </router-link>
      </Col>
      <Col span="6" class="category" :class="{ active: selected==='category'}">
        <router-link :to="{ name: 'category', params: { categoryId: 1}}">
          <Icon type="ios-list" :size="24"></Icon><br/>
          分类 
        </router-link>
      </Col>
      <Col span="6">
        <router-link :to="{ name: 'cart' }" :class="{ active: selected==='cart'}">
          <Icon type="ios-cart" :size="24"></Icon><br/>
          购物车
        </router-link>
      </Col>
      <Col span="6">
        <router-link :to="{ name: 'user' }" :class="{ active: selected==='user'}">
          <Icon type="ios-person" :size="24"></Icon><br/>
          我的
        </router-link>
      </Col>
    </Row>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        selected: ''
      }
    },
    mounted () {
      // 获取当前路由名称，根据该名称给当前footer添加is-selected
      let rName = this.$route.name
      switch (rName) {
        case 'index':
          this.selected = 'index'
          break
        case 'category':
          this.selected = 'category'
          break
        case 'cart':
          this.selected = 'cart'
          break
        case 'user':
          this.selected = 'user'
          break
      }
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../../../common/vars'

  .pusher
    height: 14vh
  .footer
    height: 10vh
    width: 100vw
    position: fixed
    bottom: 0.1vh
    div
      text-align: center
      // color: green
  // 动态class属性绑定，当前路径字体用阴影表示
  .active
    text-shadow: 3px 3px 3px $primary-color
  // 同时active了多个，无法切换
  // .router-link-active
  //   text-shadow: 3px 3px 3px $primary-color
</style>
