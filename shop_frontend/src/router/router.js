const Home = resolve => require(['@/views/Home.vue'], resolve)

// 不作为Home组件的子页面展示的页面单独写，如下
export const index = {
  path: '/',
  name: 'index',
  meta: {
    title: 'Index - 主页',
    requireAuth: false
  },
  component: resolve => require(['@/views/Index.vue'], resolve)
}

export const loginRouter = {
  path: '/login',
  name: 'login',
  meta: {
    title: 'Login - 登录'
  },
  component: resolve => require(['@/views/Login.vue'], resolve)
}

export const page404 = {
  path: '/404',
  name: 'error-404',
  meta: {
    title: '404-页面不存在'
  },
  component: resolve => require(['@/views/Error404.vue'], resolve)
}

export const page403 = {
  path: '/403',
  meta: {
    title: '403-权限不足'
  },
  name: 'error-403',
  component: resolve => require(['@/views/Error403.vue'], resolve)
}

export const category = {
  path: '/category/:categoryId',
  meta: {
    title: '分类商品'
  },
  name: 'category',
  component: resolve => require(['@/views/Category.vue'], resolve)
}

export const detail = {
  path: '/detail/:productId',
  meta: {
    title: '商品详情'
  },
  name: 'detail',
  component: resolve => require(['@/views/Detail.vue'], resolve)
}

export const cart = {
  path: '/cart',
  meta: {
    title: '购物车'
  },
  name: 'cart',
  component: resolve => require(['@/views/Cart.vue'], resolve)
}

export const user = {
  path: '/user',
  meta: {
    title: '个人中心'
  },
  name: 'user',
  component: resolve => require(['@/views/User.vue'], resolve)
}

// 作为Home组件的子页面展示但是不在左侧菜单显示的路由写在otherRouter里
export const otherRouter = {
  path: '/home',
  name: 'otherRouter',
  // redirect: '/home',
  component: Home,
  children: [
    { path: 'ownspace', title: '个人中心', name: 'ownspace_index', component: resolve => require(['@/views/User.vue'], resolve) },
    { path: 'order/:order_id', title: '订单详情', name: 'order-info', component: resolve => require(['@/views/Protocal.vue'], resolve) }, // 用于展示动态路由
    { path: 'message', title: '消息中心', name: 'message_index', component: resolve => require(['@/views/Protocal.vue'], resolve) }
  ]
}

// 作为Home组件的子页面展示并且在左侧菜单显示的路由写在appRouter里
export const appRouter = [
  {
    path: '/access',
    icon: 'key',
    name: 'access',
    title: '权限管理',
    component: Home,
    children: [
      { path: 'index', title: '权限管理', name: 'access_index', component: resolve => require(['@/views/Error403.vue'], resolve) }
    ]
  },
  {
    path: '/international',
    icon: 'earth',
    title: {i18n: 'international'},
    name: 'international',
    component: Home,
    children: [
      { path: 'index', title: {i18n: 'international'}, name: 'international_index', component: resolve => require(['@/views/International.vue'], resolve) }
    ]
  },
  {
    path: '/component',
    icon: 'social-buffer',
    name: 'component',
    title: '组件',
    component: Home,
    children: [
      {
        path: 'text-editor',
        icon: 'compose',
        name: 'text-editor',
        title: '富文本编辑器',
        component: resolve => require(['@/views/Error403.vue'], resolve)
      },
      {
        path: 'md-editor',
        icon: 'pound',
        name: 'md-editor',
        title: 'Markdown编辑器',
        component: resolve => require(['@/views/Error403.vue'], resolve)
      },
      {
        path: 'image-editor',
        icon: 'crop',
        name: 'image-editor',
        title: '图片预览编辑',
        component: resolve => require(['@/views/Error403.vue'], resolve)
      }
    ]
  },
  {
    path: '/form',
    icon: 'android-checkbox',
    name: 'form',
    title: '表单编辑',
    component: Home,
    children: [
      { path: 'artical-publish', title: '文章发布', name: 'artical-publish', icon: 'compose', component: resolve => require(['@/views/Error403.vue'], resolve) },
      { path: 'workflow', title: '工作流', name: 'workflow', icon: 'arrow-swap', component: resolve => require(['@/views/Error403.vue'], resolve) }
    ]
  },
  {
    path: '/error-page',
    icon: 'android-sad',
    title: '错误页面',
    name: 'errorpage',
    component: Home,
    children: [
      { path: 'index', title: '错误页面', name: 'errorpage_index', component: resolve => require(['@/views/Error403.vue'], resolve) }
    ]
  }
]

// 所有上面定义的路由都要写在下面的routers里
export const routers = [
  index,
  loginRouter,
  otherRouter,
  ...appRouter,
  category,
  detail,
  cart,
  user,
  page403,
  page404
]
