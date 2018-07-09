import {otherRouter, appRouter} from '@/router/router'
import * as types from '@/vuex-store/types'
// import Cookies from 'js-cookie'
import i18Locales from '@/locale/locale'
import Vue from 'vue'

import { getPayments, getDepartments, getExpresses, getLocations } from '@/http/api'

const app = {
  namespaced: true,

  state: {
    cachePage: window.localStorage['cachePage'] ? JSON.parse(window.localStorage['cachePage']) : [],
    lang: '',
    currentDepartment: '',
    // currentDepartment: window.localStorage['currentDepartment'] ? JSON.parse(window.localStorage['currentDepartment']) : null,
    pageSize: 10, // 默认取数时每次获取行数，转成limit参数发送给服务器
    isFullScreen: false,
    maxSize: 1024, // 单位kb
    openedSubmenuArr: window.localStorage['openedSubmenuArr'] ? JSON.parse(window.localStorage['openedSubmenuArr']) : [], // 要展开的菜单数组
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
    dontCache: ['text-editor', 'artical-publish'], // 在这里定义你不想要缓存的页面的name属性值(参见路由配置router.js)
    availablePayments: window.localStorage['availablePayments'] ? JSON.parse(window.localStorage['availablePayments']) : [],
    availableExpresses: window.localStorage['availableExpresses'] ? JSON.parse(window.localStorage['availableExpresses']) : [],
    availableDepartments: window.localStorage['availableDepartments'] ? JSON.parse(window.localStorage['availableDepartments']) : [],
    availableLocations: window.localStorage['availableLocations'] ? JSON.parse(window.localStorage['availableLocations']) : []
  },

  getters: {
    'currentUser': (state, getters, rootState, rootGetters) => { return rootState.login.currentUser },
    'langList': () => { return i18Locales }
  },

  mutations: {
    [types.SET_TAG_LIST] (state, list) {
      state.tagList.push(...list)
    },
    [types.UPDATE_MENU_LIST] (state, menuList) {
      state.menuList = menuList
    },
    [types.CHANGE_MENU_THEME] (state, theme) {
      state.menuTheme = theme
    },
    [types.CHANGE_MAIN_THEME] (state, mainTheme) {
      state.themeColor = mainTheme
    },
    [types.ADD_OPENED_SUBMENU] (state, name) {
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
      if (window.localStorage.cachePage) {
        state.cachePage = JSON.parse(window.localStorage.cachePage)
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
      window.localStorage.pageOpenedList = JSON.stringify(state.pageOpenedList)
    },
    [types.CLEAR_ALL_TAGS] (state) {
      state.pageOpenedList.splice(1)
      state.cachePage.length = 0
      window.localStorage.pageOpenedList = JSON.stringify(state.pageOpenedList)
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
      window.localStorage.pageOpenedList = JSON.stringify(state.pageOpenedList)
    },
    [types.SET_OPENED_LIST] (state) {
      state.pageOpenedList = window.localStorage.pageOpenedList ? JSON.parse(window.localStorage.pageOpenedList) : [otherRouter.children[0]]
    },
    [types.SET_CURRENT_PATH] (state, pathArr) {
      state.currentPath = pathArr
    },
    [types.SET_CURRENT_PAGENAME] (state, name) {
      state.currentPageName = name
    },
    [types.SET_AVATOR] (state, path) {
      window.localStorage.avatorImgPath = path
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
      window.localStorage.pageOpenedList = JSON.stringify(state.pageOpenedList)
    },
    [types.SET_CURRENT_DEPARTMENT] (state, department) {
      state.currentDepartment = department
      // window.localStorage.currentDepartment = JSON.stringify(state.currentDepartment)
    },
    [types.SET_PRODUCTS] (state, param) {
      state.availableProducts = param
      window.localStorage.availableProducts = JSON.stringify(state.availableProducts)
    },
    [types.SET_PAYMENTS] (state, param) {
      state.availablePayments = param
      window.localStorage.availablePayments = JSON.stringify(state.availablePayments)
    },
    [types.SET_DEPARTMENTS] (state, param) {
      state.availableDepartments = param
      window.localStorage.availableDepartments = JSON.stringify(state.availableDepartments)
    },
    [types.SET_EXPRESSES] (state, param) {
      state.availableExpresses = param
      window.localStorage.availableExpresses = JSON.stringify(state.availableExpresses)
    },
    [types.SET_LOCATIONS] (state, param) {
      state.availableLocations = param
      window.localStorage.availableLocations = JSON.stringify(state.availableLocations)
    }
  },

  actions: {
    'setMessageCount': ({ dispatch, commit, getters, rootGetters }, count) => {
      commit(types.SET_MESSAGE_COUNT, count)
    },
    'setCurrentDepartment': ({ dispatch, commit, getters, rootGetters }, department) => {
      commit(types.SET_CURRENT_DEPARTMENT, department)
    },
    // 用actions中的rootGetters绕开mutations中取不到rootState的问题
    'updateMenuList': ({ dispatch, commit, getters, rootGetters }, count) => {
      let tmpMenuList = []
      appRouter.forEach((item, index) => {
        if (item.meta.permission !== undefined) {
          if (rootGetters.currentUser) {
            // 如果已登录，继续判断用户权限
            if (rootGetters.currentUser.permissions.some((val, index, array) => val === item.meta.permission)) {
              // 如果有权限，显示相应router至菜单中并搜索子项和判断子项权限
              // console.error(item.children)
              if (item.children === undefined) {
                // console.error('no child')
                tmpMenuList.push(item)
              } else {
                let tmpItem = JSON.parse(JSON.stringify(item))
                let childrenArr = []
                childrenArr = item.children.filter((child, index, array) => {
                  if (child.meta.permission !== undefined) {
                    if (rootGetters.currentUser.permissions.some((val, index, array) => val === child.meta.permission)) {
                      return child
                    }
                  } else {
                    return child
                  }
                })
                // console.error('childrenArr:')
                // console.error(childrenArr)
                tmpItem.children = childrenArr
                tmpMenuList.push(tmpItem)
                // console.error(tmpMenuList)
              }
            }
          } else {
            // 需要权限又没登录时不显示
          }
        } else {
          // 父项不需要权限，要继续判断子项
          // console.error('no permission required')
          if (item.children === undefined) {
            tmpMenuList.push(item)
          } else {
            let tmpItem = JSON.parse(JSON.stringify(item))
            let childrenArr = []
            childrenArr = item.children.filter((child, index, array) => {
              if (child.meta.permission !== undefined) {
                if (rootGetters.currentUser.permissions.some((val, index, array) => val === child.meta.permission)) {
                  return child
                }
              } else {
                return child
              }
            })
            // console.error('childrenArr:')
            // console.error(childrenArr)
            tmpItem.children = childrenArr
            tmpMenuList.push(tmpItem)
            // console.error(tmpMenuList)
          }
        }
      })
      commit(types.UPDATE_MENU_LIST, tmpMenuList)
    },
    'setPayments': ({ dispatch, commit, getters, rootGetters }) => {
      getPayments().then((res) => {
        let { data, status, statusText } = res
        if (status !== 200) {
          console.log('Error in getPayments:' + statusText)
        } else {
          commit(types.SET_PAYMENTS, data.results)
        }
      }, (error) => {
        console.log('Error in getPayments:' + error)
      })
    },
    'setDepartments': ({ dispatch, commit, getters, rootGetters }) => {
      getDepartments().then((res) => {
        let { data, status, statusText } = res
        if (status !== 200) {
          console.log('Error in getDepartments:' + statusText)
        } else {
          commit(types.SET_DEPARTMENTS, data.results)
        }
      }, (error) => {
        console.log('Error in getDepartments:' + error)
      })
    },
    'setExpresses': ({ dispatch, commit, getters, rootGetters }) => {
      getExpresses().then((res) => {
        let { data, status, statusText } = res
        if (status !== 200) {
          console.log('Error in getExpresses:' + statusText)
        } else {
          commit(types.SET_EXPRESSES, data.results)
        }
      }, (error) => {
        console.log('Error in getExpresses:' + error)
      })
    },
    'setLocations': ({ dispatch, commit, getters, rootGetters }) => {
      getLocations().then((res) => {
        let { data, status, statusText } = res
        if (status !== 200) {
          console.log('Error in getLocations:' + statusText)
        } else {
          commit(types.SET_LOCATIONS, data.results)
        }
      }, (error) => {
        console.log('Error in getLocations:' + error)
      })
    }
  }
}

export default app
