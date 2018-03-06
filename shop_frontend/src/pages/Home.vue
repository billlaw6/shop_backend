<template>
  <div class="layout">
    <Layout>
      <Header class="layout-header-bar">
        <Menu mode="horizontal" theme="primary" active-name="1" :accordion=true>
          <Row>
            <Col span="6">
              <MenuItem name="navToggle">
                <Icon @click.native="collapsedSider" :class="rotateIcon" :style="{margin: '20px 20px 0'}" type="navicon-round" size="24"></Icon>
              </MenuItem>
            </Col>
            <Col span="6">
              <MenuItem name="logo">
                <div class="layout-logo"></div>
              </MenuItem>
            </Col>
            <Col span="12" class="layout-nav">
              <MenuItem name="userInfo">
                <Icon type="ios-person"></Icon>
                <Dropdown trigger="click" placement="bottom-end" style="margin-left: 20px">
                  <a href="javascript:void(0)">
                    <Avatar src="../assets/logo.png" alt="Logo"/>
                    <Icon type="arrow-down-b"></Icon>
                  </a>
                  <DropdownMenu slot="list">
                    <DropdownItem>修改密码</DropdownItem>
                    <DropdownItem>退出</DropdownItem>
                  </DropdownMenu>
                </Dropdown>
              </MenuItem>
              <MenuItem name="msgInfo">
                <Icon type="ios-navigate"></Icon>
                Item1
              </MenuItem>
            </Col>
          </Row>
        </Menu>
      </Header>
      <Layout>
        <Sider ref="sider" hide-trigger collapsible :collapsed-width="78" breakpoint="sm" v-model="isCollapsed">
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
        <Layout :style="{padding: '0 24px 24px'}">
          <Breadcrumb :style="{margin: '24px 0'}">
            <BreadcrumbItem> Elit?  </BreadcrumbItem>
            <BreadcrumbItem> Consectetur.  </BreadcrumbItem>
            <BreadcrumbItem> Consectetur?  </BreadcrumbItem>
          </Breadcrumb>
          <Content :style="{padding: '24px', minHeight: '280px', background: '#fff'}">
            Elit cumque libero sapiente debitis incidunt omnis? Atque maiores vel maxime laudantium eius omnis asperiores ab hic vero omnis. Aspernatur?
          </Content>
        </Layout>
      </Layout>
      <Footer class="layout-footer-center">2011-2016 &copy; TalkingData</Footer>
    </Layout>
  </div>
</template>

<script>
  import Navigation from '../components/Navigation.vue'
  export default {
    components: {
      Navigation
    },
    data () {
      return {
        isCollapsed: false,
        theme1: 'light',
        span_left: 5,
        span_right: 19
      }
    },
    computed: {
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
        this.$refs.sider.toggleCollapse()
      }
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../styles/vars'
  .layout
    border: 1px solid #d7dde4
    background: #f5f7f9
    position: relative
    border-radius: 4px
    overflow: hidden
    width: 100%
  .layout-header-bar
    // position: fixed
    width: 100%
    background-color: Primary
    // Menu宽度没占满，试调未解决，先用同一背景色处理
    // ul
    //   width: 100%
    //   background-color: green
  .layout-logo
    height: 30px
    background: #5b6270
    border-radius: 3px
    float: left
    position: relative
    top: 15px
    left: 20px
  .layout-nav
    margin: 0 auto
    // MenuItem渲染为li
    li 
      float: right
      position: relative
  .layout-footer-center
    text-align: center
</style>

