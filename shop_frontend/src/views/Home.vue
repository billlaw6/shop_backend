<template>
  <div class="layout">  
    <Layout>
      <Sider ref="side-menu" hide-trigger collapsible :collapsed-width="78" v-model="shrink">
        <shrinkable-menu :shrink="shrink" @on-change="handleSubmenuChange" :theme="menuTheme" :before-push="beforePush"           
          :open-names="openedSubmenuArr"      
          :menu-list="menuList">              
          <div slot="top" class="logo-con">   
            <img v-show="!shrink"  src="../assets/images/logo.jpg" key="max-logo" />
            <img v-show="shrink" src="../assets/images/logo-min.jpg" key="min-logo" />
          </div>    
        </shrinkable-menu>
      </Sider>

      <Layout>
        <Header :style="{padding: 0}" class="layout-header-bar">
          <Icon @click.native="toggleClick" :class="rotateIcon" :style="{margin: '20px 20px 0'}" type="navicon-round" size="24"></Icon>
          <div class="header-middle-con">
            <div class="main-breadcrumb">
            </div>
          </div>
        </Header>

        <Content>
          <div class="single-page-con" :style="{left: shrink?'10vw':'25vw'}">
            <div class="single-page">
              <keep-alive :include="cachePage">
                <router-view></router-view>
              </keep-alive>
            </div>
          </div>
        </Content>

        <Footer>
        </Footer>
      </Layout>
    </Layout>
  </div>
</template>

<script>
  // import Cookies from 'js-cookie'
  import { mapState, mapMutations } from 'vuex'
  import * as types from '@/vuex-store/types'
  import ShrinkableMenu from '@/views/components/main/shrinkable-menu/ShrinkableMenu.vue'
  
  export default {
    components: {
      ShrinkableMenu
    },
    data () {
      return {
        shrink: false,
        userName: '',
        isFullScreen: false
      }
    },
    computed: {
      ...mapState('app', {
        'openedSubmenuArr': state => state.openedSubmenuArr,
        'menuList': state => state.menuList,
        'pageTagsList': state => state.pageTagsList,
        'currentPath': state => state.currentPath,
        'lang': state => state.lang,
        'menuTheme': state => state.menuTheme,
        'cachePage': state => state.cachePage,
        'msgCount': state => state.messageCount
      }),
      avatorPath () {
        return localStorage.avatorImgPath
      }
    },
    methods: {
      ...mapMutations('app', {
        setMessageCount: types.SET_MESSAGE_COUNT,
        setTagList: types.SET_TAG_LIST,
        updateMenuList: types.UPDATE_MENU_LIST,
        changeMenuTheme: types.CHANGE_MENU_THEME,
        changeMainTheme: types.CHANGE_MAIN_THEME,
        setCurrentPageName: types.SET_CURRENT_PAGENAME,
        addOpenSubmenu: types.ADD_OPEN_SUBMENU
      }),
      // ...mapActions({
      //   setMessageCount: 'app/setMessageCount'
      // }),
      toggleClick () {
        this.shrink = !this.shrink
        // 直接commit需要自己写module name前缀
        // 不直接commit，统一由mapMutations转换成本地函数，方便管理
        // this.$store.commit('app/SET_MESSAGE_COUNT', 3)
        this.setMessageCount(3)
      },
      beforePush () {
        return true
      },
      handleSubmenuChange () {
        console.log('submenu changed')
      }
    },
    watch: {
      '$route' (to) {
        this.setCurrentPageName(to.name)
        // let pathArr = util.setCurrentPath(this, to.name)
        // if (pathArr.length > 2) {
        //   this.$store.commit(types.ADD_OPEN_SUBMENU, pathArr[1].name)
        // }
        localStorage.currentPageName = to.name
      },
      lang () {
        // util.setCurrentPath(this, this.$route.name) // 在切换语言时用于刷新面包屑
      },
      openedSubmenuArr () {
        setTimeout(() => {
          this.scrollBarResize()
        }, 300)
      }
    },
    mounted () {
      this.updateMenuList()
    },
    created () {
    },
    dispatch () {
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../common/vars'
  
  .layout-header-bar
    background-color: $background-color
  .logo-con
    img
      width: 100%
      height: 100%
</style>
