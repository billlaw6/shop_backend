<template>
  <div class="layout">
    <Layout>
      <Header class="layout-header-bar">
        <Menu mode="horizontal" theme="primary" active-name="1" :accordion="true">
          <MenuItem name="logo">
            <div class="layout-logo">
              <img src="../assets/logo_top_baidu.png" alt="Logo">
            </div>
          </MenuItem>
          <MenuItem name="navToggle">
            <Icon @click.native="collapsedSider" :class="rotateIcon" type="navicon-round" size="46" style="vertical-align: middle"></Icon>
          </MenuItem>
          <!-- 对已登录用户显示用户信息 -->
          <div class="account-info">
            <template v-if="user">
              <MenuItem name="userInfo">
                <Dropdown trigger="click" placement="bottom-end" style="margin-left: 20px">
                  <a href="javascript:void(0)">
                    {{ user.username }}
                    <Avatar src="../assets/logo.png" alt="Logo"/>
                    <Icon type="arrow-down-b"></Icon>
                  </a>
                  <DropdownMenu slot="list">
                    <DropdownItem>修改密码</DropdownItem>
                    <DropdownItem v-on:click="logout">退出</DropdownItem>
                  </DropdownMenu>
                </Dropdown>
              </MenuItem>
              <MenuItem name="msgInfo">
                <Icon type="ios-navigate"></Icon>
                消息中心
              </MenuItem>
            </template>
            <template v-else>
              <MenuItem name="register">
                您好！
                <Icon type="person-add"></Icon>
                免费注册 
              </MenuItem>
              <MenuItem name="login">
                <Icon type="ios-play"></Icon>
                直接登录
              </MenuItem>
            </template>
          </div>
        </Menu>
      </Header>
      <Layout>
        <template v-show="user">
          <Sider ref="siderMenu" hide-trigger collapsible :collapsed-width="78" breakpoint="sm" v-model="isCollapsed">
            <Menu active-name="1-2" theme="light" width="auto" :open-names="['1']" :class="menuitemClasses">
              <Submenu name="1">
                <template slot="title">
                  <Icon type="ios-navigate"></Icon>
                  Item1
                </template>
                <MenuItem name="1-1">Option 1</MenuItem>
                <MenuItem name="1-2">Option 2</MenuItem>
                <MenuItem name="1-3">Option 3</MenuItem>
              </Submenu>
              <Submenu name="2">
                <template slot="title">
                  <Icon type="ios-keypad"></Icon>
                  Item 2
                </template>
                <MenuItem name="2-1">Option 1</MenuItem>
                <MenuItem name="2-2">Option 2</MenuItem>
              </Submenu>
              <Submenu name="3">
                <template slot="title">
                  <Icon type="ios-keypad"></Icon>
                  Item 3
                </template>
                <MenuItem name="3-1">Option 1</MenuItem>
                <MenuItem name="3-2">Option 2</MenuItem>
              </Submenu>
            </Menu>
          </Sider>
        </template>
        <Layout :style="{padding: '0 24px 24px'}">
          <Breadcrumb :style="{margin: '24px 0'}">
            <BreadcrumbItem> Elit?  </BreadcrumbItem>
            <BreadcrumbItem> Consectetur.  </BreadcrumbItem>
            <BreadcrumbItem> Consectetur?  </BreadcrumbItem>
          </Breadcrumb>
          <Content :style="{padding: '24px', minHeight: '280px', background: '#fff'}">
            <mavon-editor v-model="editorContent"/>
          </Content>
        </Layout>
      </Layout>
      <Footer class="layout-footer-center">2011-2016 &copy; TalkingData</Footer>
    </Layout>
  </div>
</template>

<script>
  import Navigation from '../components/Navigation.vue'
  import { mapState } from 'vuex'

  export default {
    components: {
      Navigation
    },
    data () {
      return {
        isCollapsed: false,
        editorContent: ''
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

