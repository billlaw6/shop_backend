const Home = resolve => require(['@/views/Home.vue'], resolve)

// 不作为Home组件的子页面展示的页面单独写，如下
export const index = {
  path: '/',
  name: 'index',
  icon: 'earth',
  title: {i18n: 'index'},
  component: resolve => require(['@/views/Index.vue'], resolve)
}

export const loginRouter = {
  path: '/login',
  name: 'login',
  icon: 'earth',
  title: {i18n: 'login'},
  component: resolve => require(['@/views/Login.vue'], resolve)
}

export const page404 = {
  path: '/404',
  name: 'error-404',
  icon: 'error',
  title: {i18n: 'error-404'},
  component: resolve => require(['@/views/Error404.vue'], resolve)
}

export const page403 = {
  path: '/403',
  name: 'error-403',
  icon: 'error',
  title: {i18n: 'error-403'},
  component: resolve => require(['@/views/Error403.vue'], resolve)
}

export const category = {
  path: '/category/:categoryId',
  name: 'category',
  icon: 'earth',
  title: {i18n: 'category'},
  component: resolve => require(['@/views/Category.vue'], resolve)
}

export const detail = {
  path: '/detail/:productId',
  name: 'detail',
  icon: 'detail',
  title: {i18n: 'detail'},
  component: resolve => require(['@/views/Detail.vue'], resolve)
}

export const cart = {
  path: '/cart',
  name: 'cart',
  icon: 'cart',
  title: {i18n: 'cart'},
  component: resolve => require(['@/views/Cart.vue'], resolve)
}

export const user = {
  path: '/user',
  name: 'user',
  icon: 'user',
  title: {i18n: 'user'},
  component: resolve => require(['@/views/User.vue'], resolve),
  meta: {
    requireAuth: true
  }
}

// 作为Home组件的子页面展示但是不在左侧菜单显示的路由写在otherRouter里
// 如导航栏、消息栏等链接页面
export const otherRouter = {
  path: '/home',
  component: Home,
  meta: {
    requireAuth: true,
    permission: 'sale_manage.add_orderdetail'
  },
  children: [
    { path: '', title: {i18n: 'dashboard'}, name: 'dashboard', meta: { requireAuth: true }, component: resolve => require(['@/views/components/main/Dashboard.vue'], resolve) },
    { path: 'ownspace', title: {i18n: 'ownspace'}, name: 'ownspace_index', meta: { requireAuth: true }, component: resolve => require(['@/views/User.vue'], resolve) },
    { path: 'message', title: {i18n: 'message'}, name: 'message_index', meta: { requireAuth: true }, component: resolve => require(['@/views/Protocal.vue'], resolve) }
  ]
}

// 作为Home组件的子页面展示并且在左侧菜单显示的路由写在appRouter里
// 全部router必须都有meta和children属性
export const appRouter = [
  {
    path: '/product-manage',
    icon: 'ios-grid-view',
    name: 'product_manage',
    title: { i18n: 'product_manage' },
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_product'
    },
    component: Home,
    children: [
      {
        path: 'list',
        icon: 'ios-grid-view',
        title: { i18n: 'product_manage' },
        name: 'edit_product',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_product'
        },
        component: resolve => require(['@/views/ProductManage.vue'], resolve)
      }
    ]
  },
  {
    path: '/order-manage',
    icon: 'ios-list-outline',
    name: 'order_manage',
    title: { i18n: 'order_manage' },
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_orderdetail'
    },
    component: Home,
    children: [
      {
        path: 'edit',
        icon: 'edit',
        title: { i18n: 'edit_order' },
        name: 'edit_order',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/Error403.vue'], resolve)
      },
      {
        path: 'add',
        icon: 'compose',
        title: { i18n: 'add_order' },
        name: 'add_order',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/Error403.vue'], resolve)
      },
      {
        path: 'stats',
        icon: 'stats-bars',
        title: { i18n: 'stats_order' },
        name: 'stats_order',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/Error403.vue'], resolve)
      }
    ]
  },
  {
    path: '/user-manage',
    icon: 'key',
    name: 'user_manage',
    title: { i18n: 'user_manage' },
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_orderdetail'
    },
    component: Home,
    children: [
      {
        path: 'index',
        icon: 'key',
        title: { i18n: 'user_manage' },
        name: 'access_index',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/Error403.vue'], resolve)
      }
    ]
  },
  {
    path: '/international',
    icon: 'earth',
    title: {i18n: 'international'},
    name: 'international',
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_orderdetail'
    },
    component: Home,
    children: [
      {
        path: 'index',
        title: {i18n: 'international'},
        name: 'international_index',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/International.vue'], resolve)
      }
    ]
  },
  {
    path: '/component',
    icon: 'social-buffer',
    title: '组件',
    name: 'component',
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_orderdetail'
    },
    component: Home,
    children: [
      {
        path: 'text-editor',
        icon: 'compose',
        name: 'text-editor',
        title: '富文本编辑器',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/Error403.vue'], resolve)
      },
      {
        path: 'md-editor',
        icon: 'pound',
        name: 'md-editor',
        title: 'Markdown编辑器',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/Error403.vue'], resolve)
      },
      {
        path: 'image-editor',
        icon: 'crop',
        name: 'image-editor',
        title: '图片预览编辑',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/Error403.vue'], resolve)
      }
    ]
  },
  {
    path: '/form',
    icon: 'android-checkbox',
    name: 'form',
    title: '表单编辑',
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_orderdetail'
    },
    component: Home,
    children: [
      {
        path: 'artical',
        title: '文章发布',
        name: 'artical',
        icon: 'compose',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/Error403.vue'], resolve)
      }
    ]
  },
  {
    path: '/error-page',
    icon: 'android-sad',
    title: '错误页面',
    name: 'errorpage',
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_orderdetail'
    },
    component: Home,
    children: [
      {
        path: 'artical-publish',
        title: '错误页面',
        name: 'artical-publish',
        icon: 'compose',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/Error403.vue'], resolve)
      }
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
