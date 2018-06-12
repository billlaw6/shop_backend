import {otherRouter, appRouter} from '@/router/router'
import * as types from '@/vuex-store/types'
// import Cookies from 'js-cookie'
import Vue from 'vue'

const app = {
  namespaced: true,

  state: {
    cachePage: [],
    lang: '',
    isFullScreen: false,
    openedSubmenuArr: [], // 要展开的菜单数组
    menuTheme: 'dark', // 主题
    themeColor: '',
    pageOpenedList: [{
      title: '首页',
      path: '',
      name: 'home_index'
    }],
    currentPageName: '',
    currentPath: [
      {
        title: '首页',
        path: '',
        name: 'home_index'
      }
    ], // 面包屑数组
    menuList: [],
    routers: [
      otherRouter,
      ...appRouter
    ],
    tagList: [...otherRouter.children],
    messageCount: 0,
    dontCache: ['text-editor', 'artical-publish'] // 在这里定义你不想要缓存的页面的name属性值(参见路由配置router.js)
  },

  mutations: {
    [types.SET_TAG_LIST] (state, list) {
      state.tagList.push(...list)
    },
    [types.UPDATE_MENU_LIST] (state) {
      // let accessCode = parseInt(Cookies.get('access'))
      let menuList = []
      appRouter.forEach((item, index) => {
        if (item.access !== undefined) {
        } else {
          if (item.children.length === 1) {
            menuList.push(item)
          } else {
            let len = menuList.push(item)
            let childrenArr = []
            childrenArr = item.children.filter(child => {
              if (child.access !== undefined) {
              } else {
                return child
              }
            })
            if (childrenArr === undefined || childrenArr.length === 0) {
              menuList.splice(len - 1, 1)
            } else {
              let handledItem = JSON.parse(JSON.stringify(menuList[len - 1]))
              handledItem.children = childrenArr
              menuList.splice(len - 1, 1, handledItem)
            }
          }
        }
      })
      state.menuList = menuList
    },
    [types.CHANGE_MENU_THEME] (state, theme) {
      state.menuTheme = theme
    },
    [types.CHANGE_MAIN_THEME] (state, mainTheme) {
      state.themeColor = mainTheme
    },
    [types.ADD_OPEN_SUBMENU] (state, name) {
      let hasThisName = false
      let isEmpty = false
      if (name.length === 0) {
        isEmpty = true
      }
      if (state.openedSubmenuArr.indexOf(name) > -1) {
        hasThisName = true
      }
      if (!hasThisName && !isEmpty) {
        state.openedSubmenuArr.push(name)
      }
    },
    [types.CLOSE_PAGE] (state, name) {
      state.cachePage.forEach((item, index) => {
        if (item === name) {
          state.cachePage.splice(index, 1)
        }
      })
    },
    [types.INIT_CACHE_PAGE] (state) {
      if (localStorage.cachePage) {
        state.cachePage = JSON.parse(localStorage.cachePage)
      }
    },
    [types.REMOVE_TAG] (state, name) {
      state.pageOpenedList.map((item, index) => {
        if (item.name === name) {
          state.pageOpenedList.splice(index, 1)
        }
      })
    },
    [types.PAGE_OPENED_LIST] (state, get) {
      let openedPage = state.pageOpenedList[get.index]
      if (get.argu) {
        openedPage.argu = get.argu
      }
      if (get.query) {
        openedPage.query = get.query
      }
      state.pageOpenedList.splice(get.index, 1, openedPage)
      localStorage.pageOpenedList = JSON.stringify(state.pageOpenedList)
    },
    [types.CLEAR_ALL_TAGS] (state) {
      state.pageOpenedList.splice(1)
      state.cachePage.length = 0
      localStorage.pageOpenedList = JSON.stringify(state.pageOpenedList)
    },
    [types.CLEAR_OTHER_TAGS] (state, vm) {
      let currentName = vm.$route.name
      let currentIndex = 0
      state.pageOpenedList.forEach((item, index) => {
        if (item.name === currentName) {
          currentIndex = index
        }
      })
      if (currentIndex === 0) {
        state.pageOpenedList.splice(1)
      } else {
        state.pageOpenedList.splice(currentIndex + 1)
        state.pageOpenedList.splice(1, currentIndex - 1)
      }
      let newCachepage = state.cachePage.filter(item => {
        return item === currentName
      })
      state.cachePage = newCachepage
      localStorage.pageOpenedList = JSON.stringify(state.pageOpenedList)
    },
    [types.SET_OPENED_LIST] (state) {
      state.pageOpenedList = localStorage.pageOpenedList ? JSON.parse(localStorage.pageOpenedList) : [otherRouter.children[0]]
    },
    [types.SET_CURRENT_PATH] (state, pathArr) {
      state.currentPath = pathArr
    },
    [types.SET_CURRENT_PAGENAME] (state, name) {
      state.currentPageName = name
    },
    [types.SET_AVATOR] (state, path) {
      localStorage.avatorImgPath = path
    },
    [types.SWITCH_LANG] (state, lang) {
      state.lang = lang
      Vue.config.lang = lang
    },
    [types.CLEAR_OPENED_SUBMENU] (state) {
      state.openedSubmenuArr.length = 0
    },
    [types.SET_MESSAGE_COUNT] (state, count) {
      state.messageCount = count
    },
    [types.INCREATE_TAG] (state, tagObj) {
      state.pageOpenedList.push(tagObj)
      localStorage.pageOpenedList = JSON.stringify(state.pageOpenedList)
    }
  },

  actions: {
    'setMessageCount': ({ dispatch, commit, getters, rootGetters }, count) => {
      commit(types.SET_MESSAGE_COUNT, count)
    }
  }
}

export default app
