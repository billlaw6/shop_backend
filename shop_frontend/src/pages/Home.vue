<template>
  <div class="layout">
    <head>
      <title>欢迎光临正岩苔茶微官网</title>
    </head>
    <Layout>
      <Layout :style="{padding: '0 24px 24px'}">
        <Content :style="{padding: '24px', minHeight: '280px', background: '#fff'}">

        <h1>User List</h1>
        <weixin-user-list next_openid=''></weixin-user-list> 
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
</style>

