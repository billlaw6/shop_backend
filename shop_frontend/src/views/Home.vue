<template>
  <div class="layout"> 
    <Layout>
      <Sider ref="side-menu" hide-trigger collapsible :collapsed-width="78" v-model="shrink">
        <shrinkable-menu 
          :shrink="shrink" 
          @on-change="handleSubmenuChange" 
          :theme="menuTheme" 
          :before-push="beforePush"          
          :open-names="openedSubmenuArr"     
          :menu-list="menuList"
        >             
          <div slot="top" class="logo-con">  
            <router-link :to="{ name: 'dashboard' }">
              <img v-show="!shrink"  src="../assets/images/logo.jpg" key="max-logo" />
              <img v-show="shrink" src="../assets/images/logo-min.jpg" key="min-logo" />
            </router-link>
          </div>   
        </shrinkable-menu>
      </Sider>

      <Layout>
        <Header :style="{padding: 0}" class="layout-header-bar">
          <Menu mode="horizontal" active-name="breadcrumb" theme="light">
            <div class="toggle-icon">
              <Icon @click.native="toggleClick" :class="rotateIcon" :style="{margin: '20px 20px 0'}" type="navicon-round" size="30"></Icon>
            </div>
            <div class="header-middle">
              <MenuItem name="breadcrumb">
                <breadcrumb-nav :currentPath="currentPath"></breadcrumb-nav>
              </MenuItem>
            </div>
            <div class="header-right">
              <MenuItem name="fullscreen">
                <full-screen v-model="isFullScreen" @on-change="fullscreenChange"></full-screen>
              </MenuItem>
              <MenuItem name="message-tip">
                <message-tip v-model="msgCount"></message-tip>
              </MenuItem>
              <!--
              {{ currentDepartment }}
              <MenuItem name="theme-switch">
                <theme-switch></theme-switch>
              </MenuItem>
              -->
              <MenuItem v-if="currentUser.dept_belong" name="current-dept">
                <AutoComplete v-model="currDeptName"
                  :placeholder="$t('selectDepartment')"
                  @on-select="handleCurrentDeptChange"
                  >
                  <Option v-for="item in currentUser.dept_belong" :value="item.name" :key="item.code">{{ item.name }}</Option>
                </AutoComplete>
              </MenuItem>
              <div class="user-dropdown-menu">
                <Row type="flex" justify="end" align="middle" class="user-dropdown-innercon">
                  <Dropdown transfer trigger="click" @on-click="handleClickUserDropdown">
                    <a href="javascript:void(0)">
                      <span class="main-user-name">{{ currentUser.username }}</span>
                      <Icon type="arrow-down-b"></Icon>
                    </a>
                    <DropdownMenu slot="list">
                      <DropdownItem name="ownSpace">{{ $t('ownSpace') }}</DropdownItem>
                      <DropdownItem name="logout" divided>{{ $t('logout') }}</DropdownItem>
                    </DropdownMenu>
                  </Dropdown>
                  <Avatar :src="avatorPath" style="background: #619fe7;margin-left: 10px;"></Avatar>
                </Row>
              </div>
            </div>
          </Menu>
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
  import { mapState, mapMutations, mapActions } from 'vuex'
  import * as types from '@/vuex-store/types'
  import ShrinkableMenu from '@/views/components/main/shrinkable-menu/ShrinkableMenu.vue'
  import BreadcrumbNav from '@/views/components/main/BreadcrumbNav.vue'
  import FullScreen from '@/views/components/main/FullScreen.vue'
  import MessageTip from '@/views/components/main/MessageTip.vue'
  import ThemeSwitch from '@/views/components/main/ThemeSwitch.vue'
  import LockScreen from '@/views/components/main/lockscreen/LockScreen.vue'

  export default {
    components: {
      ShrinkableMenu,
      BreadcrumbNav,
      FullScreen,
      MessageTip,
      ThemeSwitch,
      LockScreen
    },
    data () {
      return {
        shrink: false,
        userName: '',
        currDeptName: '',
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
      ...mapState('login', {
        'currentUser': state => state.currentUser,
        'currentDepartment': state => state.currentDepartment
      }),
      rotateIcon () {
        return [
          'menu-icon',
          this.shrink ? 'rotate-icon' : ''
        ]
      },
      avatorPath () {
        return localStorage.avatorImgPath
      }
    },
    methods: {
      ...mapMutations('app', {
        setMessageCount: types.SET_MESSAGE_COUNT,
        setTagList: types.SET_TAG_LIST,
        changeMenuTheme: types.CHANGE_MENU_THEME,
        changeMainTheme: types.CHANGE_MAIN_THEME,
        addOpenedSubmenu: types.ADD_OPENED_SUBMENU,
        clearOpenedSubmenu: types.CLEAR_OPENED_SUBMENU
      }),
      ...mapActions('login', {
        logout: 'logout',
        setCurrentDepartment: 'setCurrentDepartment'
      }),
      ...mapActions('app', {
        updateMenuList: 'updateMenuList',
        setCurrentPageName: 'setCurrentPageName',
        setProducts: 'setProducts',
        setPayments: 'setPayments',
        setDepartments: 'setDepartments',
        setExpresses: 'setExpresses',
        setLocations: 'setLocations'
      }),
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
      handleSubmenuChange (name) {
        console.log('submenu changed to:' + name)
      },
      fullscreenChange (isFullScreen) {
        console.log(isFullScreen)
      },
      handleClickUserDropdown (name) {
        if (name === 'ownSpace') {
          // util.openNewPage(this, 'ownspace_index')
          this.$router.push({
            name: 'ownspace_index'
          })
        } else if (name === 'logout') {
          // 退出登录
          this.logout()
          this.clearOpenedSubmenu()
          this.$router.push({
            name: 'login'
          })
        }
      },
      handleCurrentDeptChange (value) {
        // filter() 方法创建一个新的数组，新数组中的元素是通过检查指定数组中符合条件的所有元素。
        // console.log(value)
        let current = this.currentUser.dept_belong.filter((val, index, array) => {
          return val.name === value
        })
        // console.log(current)
        if (current.length > 0) {
          this.setCurrentDepartment(current[0])
        } else {
          // 编辑内容时value为undefined，所以将它修改回原值。
          this.$Message.error(this.$t('invalidDepartment'))
          this.currDeptName = this.currentDepartment.name
        }
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
      this.currDeptName = this.currentDepartment.name
      // 全局通用的一些数据取一次共用，省得各页面分别取，减少网络请求
      this.setProducts()
      this.setPayments()
      this.setDepartments()
      this.setExpresses()
      this.setLocations()
    },
    created () {
      // window.localStorage.clear()
    },
    dispatch () {
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../common/vars'

  .layout
    border: 1px solid $border-color
    background: $background-color
    position: relative
    border-radius: 4px
    overflow: hidden
  .logo-con
    img
      width: 100%
      height: 100%
  .menu-icon
    transition: all .3s
  .rotate-icon
    transform: rotate(-90deg)
  .layout-header-bar
    background-color: $background-color
    box-shadow: 0 1px 1px rgba(0,0,0,.1)
  .toggle-icon
    float: left
    position: relative
    bottom: 6px
  .header-middle
    display: inline-block
  .header-right
    display: inline-block
    float: right
  .user-dropdown-menu
    display: inline-block
</style>
