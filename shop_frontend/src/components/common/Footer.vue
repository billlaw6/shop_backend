<template lang="html">
  <!-- gotoRouter:点击后路由跳转到与id名相同的route.name所对应的路径 -->
  <footer class="footer" @click.stop='gotoRouter'>
    <mt-tabbar v-model="selected" fixed>
    <mt-tab-item id="index">
      <i slot="icon" class="icon-index"></i>
        首页 
    </mt-tab-item>
    <mt-tab-item id="category">
      <i slot="icon" class="icon-category"></i>
        分类
    </mt-tab-item>
    <mt-tab-item id="cart">
      <i slot="icon" class="icon-car"></i>
        购物车
    </mt-tab-item>
    <mt-tab-item id="user">
      <i class="fa fa-user-o fa-2x"></i>
        我的
    </mt-tab-item>
  </mt-tabbar>
  </footer>
</template>

<script>
  export default {
    methods: {
      gotoRouter () {
        this.$router.push({
          name: this.selected
        })
      }
    },
    data () {
      return {
        // 对应mt-tab-item 的id值
        selected: ''
      }
    },
    mounted () {
      // 获取当前路由名称，根据该名称给当前footer添加is-selected
      let Rname = this.$route.name
      switch (Rname) {
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
  @import '../../common/vars'
  @import '../../assets/index/style.css'

  .mint-tab-item-label:hover
    color:#333
    .mint-tabbar
      background-color: #fff
      background-image: none
      box-shadow: 0 0 2.2vw 0 hsla(0, 6%, 50%, .13)
      -webkit-box-shadow: 0 0 2.2vw 0 hsla(0, 6%, 50%, .13)
      .is-selected
        color: $content-color
        background-color: $background-color
        i
          &::before
            color: $content-color
      i
        i-font-size(font-size, 42)
</style>
