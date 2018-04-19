<template>
  <div class="layout">
    <Layout>
      <Header class="layout-header-bar">
      </Header>
      <Layout :style="{padding: '0 24px 24px'}">
        <Content :style="{padding: '24px', minHeight: '280px', background: '#fff'}">
          <img src="../assets/WechatIMG7.jpeg" alt="banner1">
          <img src="../assets/WechatIMG8.jpeg" alt="banner1">
          <vue-table></vue-table>
          <product-list></product-list>
        </Content>
      </Layout>
      <Footer class="layout-footer-center">2011-2016 &copy; TalkingData</Footer>
    </Layout>
  </div>
</template>

<script>
  import ProductList from '../components/ProductList.vue'
  import VueTable from '../components/VueTable.vue'
  import { mapState } from 'vuex'

  export default {
    components: {
      ProductList,
      VueTable
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
  @import '../common/vars'
  img
    width: 100%
    height: auto
</style>

