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
import * as types from '@/vuex-store/types.js'
import config from '../../../../../config/index.js'

export default {
  name: 'themeSwitch',
  data () {
    return {
      themeList: [
        {
          name: 'black_b',
          menu: '#495060',
          element: '#2d8cf0'
        },
        {
          name: 'black_g',
          menu: '#495060',
          element: '#00a854'
        },
        {
          name: 'black_y',
          menu: '#495060',
          element: '#e96500'
        },
        {
          name: 'black_r',
          menu: '#495060',
          element: '#e43e31'
        },
        {
          name: 'light_b',
          menu: '#495060',
          element: '#2d8cf0'
        },
        {
          name: 'light_g',
          menu: '#495060',
          element: '#00a854'
        },
        {
          name: 'light_y',
          menu: '#495060',
          element: '#e96500'
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
    setTheme (themeFile) {
      let menuTheme = themeFile.substr(0, 1)
      let mainTheme = themeFile.substr(-1, 1)
      if (menuTheme === 'b') {
        // 黑色菜单
        this.$store.commit(types.CHANGE_MENU_THEME, 'dark')
        menuTheme = 'dark'
      } else {
        this.$store.commit(types.CHANGE_MENU_THEME, 'light')
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
    }
  },
  created () {
    let path = ''
    if (config.dev) {
      path = './src/views/components/main/theme-switch/theme/'
    } else {
      path = 'dist/'
    }
    let name = Cookies.get('user')
    if (localStorage.theme) {
      let hasThisUser = JSON.parse(localStorage.theme).some(item => {
        if (item.userName === name) {
          this.$store.commit(types.CHANGE_MENU_THEME, item.menuTheme)
          this.$store.commit(types.CHANGE_MAIN_THEME, item.mainTheme)
          return true
        } else {
          return false
        }
      })
      if (!hasThisUser) {
        this.$store.commit(types.CHANGE_MENU_THEME, 'dark')
        this.$store.commit(types.CHANGE_MAIN_THEME, 'b')
      }
    } else {
      this.$store.commit(types.CHANGE_MENU_THEME, 'dark')
      this.$store.commit(types.CHANGE_MAIN_THEME, 'b')
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
