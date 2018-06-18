<template>
  <div style="display:inline-block;padding:0 6px;">
    <Dropdown trigger="click" @on-click="setTheme">
      <a href="javascript:void(0)">
        <Icon :style="{marginTop: '-2px', verticalAlign: 'middle'}" color="#495060" :size="18" type="paintbucket"></Icon>
        <Icon type="arrow-down-b"></Icon>
      </a>
      <DropdownMenu slot="list">
        <DropdownItem v-for="(item, index) in themeList" :key="index" :name="item.name">
          <Row type="flex" justify="center" align="middle">
            <span style="margin-right:10px;"><Icon :size="20" :type="item.name.substr(0, 1) !== 'b' ? 'happy-outline' : 'happy'" :color="item.menu"/></span>
            <span><Icon :size="22" type="record" :color="item.element"/></span>
          </Row>
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  </div>
</template>

<script>
import Cookies from 'js-cookie'
import { mapMutations } from 'vuex'
import * as types from '@/vuex-store/types.js'
import config from '../../../../config/index.js'

export default {
  name: 'ThemeSwitch',
  data () {
    return {
      themeList: [
        {
          name: 'black_b',
          menu: '#495060',
          element: '#2d8cf0'
        },
        {
          name: 'light_r',
          menu: '#495060',
          element: '#e43e31'
        }
      ]
    }
  },
  methods: {
    ...mapMutations('app', {
      changeMenuTheme: types.CHANGE_MENU_THEME
    }),
    setTheme (themeFile) {
      let menuTheme = themeFile.substr(0, 1)
      let mainTheme = themeFile.substr(-1, 1)
      if (menuTheme === 'b') {
        // 黑色菜单
        this.changeMenuTheme('dark')
        menuTheme = 'dark'
      } else {
        menuTheme = 'light'
        menuTheme = 'light'
      }
      // let path = ''
      // let themeLink = document.querySelector('link[name="theme"]')
      let userName = Cookies.get('user')
      if (localStorage.theme) {
        let themeList = JSON.parse(localStorage.theme)
        let index = 0
        let hasThisUser = themeList.some((item, i) => {
          if (item.userName === userName) {
            index = i
            return true
          } else {
            return false
          }
        })
        if (hasThisUser) {
          themeList[index].mainTheme = mainTheme
          themeList[index].menuTheme = menuTheme
        } else {
          themeList.push({
            userName: userName,
            mainTheme: mainTheme,
            menuTheme: menuTheme
          })
        }
        localStorage.theme = JSON.stringify(themeList)
      } else {
        localStorage.theme = JSON.stringify([{
          userName: userName,
          mainTheme: mainTheme,
          menuTheme: menuTheme
        }])
      }
      let stylePath = ''
      if (config.dev) {
        stylePath = './src/views/components/main/theme-switch/theme/'
      } else {
        stylePath = 'dist/'
      }
      console.log(stylePath)
    }
  },
  created () {
    let path = ''
    if (config.dev) {
      path = './src/views/components/main/theme-switch/theme/'
    } else {
      path = 'dist/'
    }
    console.log(path)
    let name = Cookies.get('user')
    if (localStorage.theme) {
      let hasThisUser = JSON.parse(localStorage.theme).some(item => {
        if (item.userName === name) {
          this.changeMenuTheme(item.mainTheme)
          return true
        } else {
          return false
        }
      })
      if (!hasThisUser) {
        this.changeMenuTheme('dark')
        this.changeMenuTheme('b')
      }
    } else {
      this.changeMenuTheme('dark')
      this.changeMenuTheme('b')
    }
    // 根据用户设置主题
    if (this.$store.state.app.themeColor !== 'b') {
      // let stylesheetPath = path + this.$store.state.app.themeColor + '.css'
      // let themeLink = document.querySelector('link[name="theme"]')
      // themeLink.setAttribute('href', stylesheetPath)
    }
  }
}
</script>
