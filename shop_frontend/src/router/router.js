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
  name: 'error404',
  icon: 'error',
  title: {i18n: 'error404'},
  component: resolve => require(['@/views/Error404.vue'], resolve)
}

export const page403 = {
  path: '/403',
  name: 'error403',
  icon: 'error',
  title: {i18n: 'error403'},
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
  component: resolve => require(['@/views/ProductDetail.vue'], resolve)
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
    { path: 'ownspace', title: {i18n: 'ownspace'}, name: 'ownspaceIndex', meta: { requireAuth: true }, component: resolve => require(['@/views/User.vue'], resolve) },
    { path: 'message', title: {i18n: 'message'}, name: 'messageIndex', meta: { requireAuth: true }, component: resolve => require(['@/views/Protocal.vue'], resolve) }
  ]
}

// 作为Home组件的子页面展示并且在左侧菜单显示的路由写在appRouter里
// 全部router必须都有meta和children属性
export const appRouter = [
  {
    path: '/product-manage',
    icon: 'ios-grid-view',
    name: 'productManage',
    title: { i18n: 'productManage' },
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_product'
    },
    component: Home,
    children: [
      {
        path: 'list',
        icon: 'ios-grid-view',
        title: { i18n: 'productManage' },
        name: 'editProduct',
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
    name: 'orderManage',
    title: { i18n: 'orderManage' },
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_orderdetail'
    },
    component: Home,
    children: [
      {
        path: 'add',
        icon: 'compose',
        title: { i18n: 'addOrder' },
        name: 'addOrder',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/OrderAdd.vue'], resolve)
      },
      {
        path: 'edit',
        icon: 'edit',
        title: { i18n: 'editOrder' },
        name: 'editOrder',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/OrderManage.vue'], resolve)
      },
      {
        path: 'stats',
        icon: 'stats-bars',
        title: { i18n: 'statsOrder' },
        name: 'statsOrder',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/Error403.vue'], resolve)
      }
    ]
  },
  {
    path: '/stock-manage',
    icon: 'ios-list-outline',
    name: 'stockManage',
    title: { i18n: 'stockManage' },
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_orderdetail'
    },
    component: Home,
    children: [
      {
        path: 'stock',
        icon: 'compose',
        title: { i18n: 'addStockCheck' },
        name: 'addStockCheck',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/StockCheck.vue'], resolve)
      },
      {
        path: 'add',
        icon: 'compose',
        title: { i18n: 'addStockMoveRecord' },
        name: 'addStockMoveRecord',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/StockMoveRecordAdd.vue'], resolve)
      },
      {
        path: 'edit',
        icon: 'edit',
        title: { i18n: 'editStockMoveRecord' },
        name: 'editStockMoveOut',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/StockMoveRecordManage.vue'], resolve)
      },
      {
        path: 'stats',
        icon: 'stats-bars',
        title: { i18n: 'statsStockMoveRecord' },
        name: 'statsStockMoveRecord',
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
    icon: 'person',
    name: 'userManage',
    title: { i18n: 'userManage' },
    meta: {
      requireAuth: true,
      permission: 'sale_manage.add_orderdetail'
    },
    component: Home,
    children: [
      {
        path: 'index',
        icon: 'person-add',
        title: { i18n: 'userList' },
        name: 'userList',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/UserManage.vue'], resolve)
      },
      {
        path: 'index',
        icon: 'key',
        title: { i18n: 'permissionManage' },
        name: 'permissionManage',
        meta: {
          requireAuth: true,
          permission: 'sale_manage.add_orderdetail'
        },
        component: resolve => require(['@/views/PermissionManage.vue'], resolve)
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
