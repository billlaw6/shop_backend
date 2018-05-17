import Mock from 'mockjs'
let Random = Mock.Random
let base = `http://123.56.115.20`
let hotProducts = Mock.mock(`${base}/rest-api/hot-products/`, {
  'count|1-100': 1,
  'results|4-10': [{
    'id|+1': 1, // 属性值1用来确定类型
    'name': '@name',
    'pinyin|4': 'pinyin',
    'price|99-9999': 100,
    'sale_price|99-9999': 100,
    'py|4': 'py',
    'image': Random.image('400x100', '#dec4e0', '#333', 'png', ''),
    'description': Random.paragraph()
  }]
})

let products = Mock.mock(`${base}/rest-api/products/`, {
  'count|1-100': 1,
  'results|80-100': [{
    'id|+1': 1, // 属性值1用来确定类型
    'name': '@name',
    'pinyin|4': 'pinyin',
    'price|99-9999': 100,
    'sale_price|99-9999': 100,
    'py|4': 'py',
    'image': Random.image('200x200', '#dec4e0', '#333', 'png', ''),
    'description': Random.paragraph()
  }]
})

// 好像不带域名也匹配拦截得挺好
let productDetail = Mock.mock(/\/rest-api\/products\/\d/, {
  'id|1-1000': 1,
  'name': '@name',
  'pinyin|4': 'pinyin',
  'price|99-9999': 100,
  'sale_price|99-9999': 100,
  'carouselImages|3-5': [{
    'order|+1': 1, // 属性值1用来确定类型
    'image': Random.image('800x100', '#dec4e0', '#333', 'png', ''),
    'description': Random.paragraph()
  }],
  'detailImages|3-5': [{
    'order|+1': 1, // 属性值1用来确定类型
    'image': Random.image('800x100', '#dec4e0', '#333', 'png', ''),
    'description': Random.paragraph()
  }]
})

let authLogin = Mock.mock(`${base}/rest-auth/login/`, {
  'key': 1
})

let authLogout = Mock.mock(`${base}/rest-auth/logout/`, {
  'key': 0
})

let getUserInfo = Mock.mock(`${base}/rest-auth/user/`, {
  'pk|0-100': 0,
  'username': '@name',
  'email': '@email',
  'first_name': '@name',
  'last_name': '@name'
})

export { hotProducts, products, productDetail, authLogin, authLogout, getUserInfo }
