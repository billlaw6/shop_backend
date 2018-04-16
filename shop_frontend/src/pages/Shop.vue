<template>
  <div class="layout">
    <Layout>
      <Header class="layout-header-bar">
      </Header>
      <Layout :style="{padding: '0 24px 24px'}">
        <Content :style="{padding: '24px', minHeight: '280px', background: '#fff'}">
          <product-list></product-list>
        </Content>
      </Layout>
      <Footer class="layout-footer-center">2011-2016 &copy; TalkingData</Footer>
    </Layout>
  </div>
</template>

<script>
  import ProductList from '../components/ProductList.vue'
  import { mapState } from 'vuex'

  export default {
    components: {
      ProductList
    },
    data () {
      return {
        isCollapsed: false
      }
    },
    computed: {
      ...mapState({
        user: state => state.login.user
      }),
      rotateIcon () {
        return [
          'menu-icon',
          this.isCollapsed ? 'rotate-icon' : ''
        ]
      },
      menuitemClasses () {
        return [
          'menu-item',
          this.isCollapsed ? 'collapsed-menu' : ''
        ]
      }
    },
    methods: {
      collapsedSider () {
        // toggleCollapse为iView Sider组件的方法
        this.$refs.siderMenu.toggleCollapse()
      },
      logout (event) {
        console.log(event)
        this.$store.dispatch('setUser', null)
      }
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../styles/vars'
  .layout
    border: 1px solid #d7dde4
    background: Primary
    position: relative
    border-radius: 4px
    overflow: hidden
    width: 100%
  .layout-header-bar
    background-color: Primary
  .layout-logo
    border-radius: 3px
    float: left
    position: relative
    img
      vertical-align: middle
  .account-info
    float: right
    position: relative
  .layout-footer-center
    text-align: center
</style>

