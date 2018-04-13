<template>
  <div class="layout">
    <link rel="prefetch" href="http://123.56.115.20:8080/#/login">
    <Layout>
      <Header class="layout-header-bar">
        <Menu mode="horizontal" theme="primary" active-name="1" :accordion="true">
          <MenuItem name="logo">
            <div class="layout-logo">
              <Icon type="home"></Icon>主页
            </div>
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
      <Layout :style="{padding: '0 24px 24px'}">
        <Content :style="{padding: '24px', minHeight: '280px', background: '#fff'}">
        <weixin-user-info openid='oxpwht2d0SuyiTBqUSBHojho6Tn8'></weixin-user-info> 
        <h1>User List</h1>
        <weixin-user-list next_openid=''></weixin-user-list> 
        <!--
          <Carousel v-model="value2" 
                  :height="setting.height"
                  :loop="setting.loop"
                  :autoplay="setting.autoplay"
                  :autoplay-speed="setting.autoplaySpeed"
                  :dots="setting.dots"
                  :radius-dot="setting.radiusDot"
                  :trigger="setting.trigger"
                  :arrow="setting.arrow"
                  :easing="setting.easing">
            <CarouselItem>
              <div class="demo-carousel">
                <img src="../assets/1.jpg" alt="1">
              </div>
            </CarouselItem>
            <CarouselItem>
              <div class="demo-carousel">
                <img src="../assets/2.jpg" alt="2">
              </div>
            </CarouselItem>
            <CarouselItem>
              <div class="demo-carousel">
                <img src="../assets/3.jpg" alt="3">
              </div>
            </CarouselItem>
          </Carousel>
         -->
          <article>
            <h1>Consectetur eaque ex ipsam soluta?</h1>
            Dolor eveniet quisquam quidem vitae autem, aliquid delectus, rem fuga aspernatur quaerat molestias alias molestiae! Ab rem temporibus expedita illo fugiat eos non. Neque ipsum quam nam sed in incidunt!
          </article>
          <!--
          <web-camera></web-camera>
          -->
        </Content>
      </Layout>
      <Footer class="layout-footer-center">2011-2016 &copy; TalkingData</Footer>
    </Layout>
  </div>
</template>

<script>
  import WebCamera from '../components/WebCamera.vue'
  import WeixinUserInfo from '../components/WeixinUserInfo.vue'
  import WeixinUserList from '../components/WeixinUserList.vue'
  import { mapState } from 'vuex'

  export default {
    components: {
      WebCamera,
      WeixinUserInfo,
      WeixinUserList
    },
    data () {
      return {
        isCollapsed: false,
        editorContent: '',
        value2: 0,
        setting: {
          height: 'auto',
          loop: true,
          autoplay: true,
          autoplaySpeed: 2000,
          dots: 'inside',
          radiusDot: false,
          trigger: 'click',
          arrow: 'hover',
          easing: 'ease'
        }
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

