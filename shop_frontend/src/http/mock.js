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

// let getUserInfo = Mock.mock(`${base}/rest-auth/user/`, {
//   'pk|0-100': 0,
//   'username': '@name',
//   'email': '@email',
//   'first_name': '@name',
//   'last_name': '@name'
// })

let getUserInfo = Mock.mock(`${base}/user_manage/user_info/`, 'get', {
  'id|0-100': 0,
  'username': '@name',
  'first_name': '@first',
  'last_name': '@last',
  'email': '@email',
  'is_staff': Random.boolean(),
  'is_superuser': Random.boolean()
})
// let perms = ['dict_manage.change_payment', 'user_manage.change_shopuser', 'dict_manage.change_orderstatus', 'admin.change_logentry', 'dict_manage.change_category', 'oauth2_provider.change_accesstoken', 'verify_utils.change_captcharecord', 'oauth2_provider.change_grant', 'contenttypes.add_contenttype', 'auth.change_group', 'auth.add_group', 'oauth2_provider.change_application', 'account.change_emailaddress', 'dict_manage.change_product', 'verify_utils.delete_verifycoderecord', 'oauth2_provider.add_grant', 'sessions.add_session', 'dict_manage.add_orderstatus', 'social_django.delete_nonce', 'social_django.change_usersocialauth', 'dict_manage.delete_orderstatus', 'social_django.delete_code', 'account.delete_emailconfirmation', 'admin.add_logentry', 'social_django.add_nonce', 'verify_utils.add_verifycoderecord', 'user_manage.add_shopuser', 'dict_manage.change_productpicture', 'user_manage.change_group', 'dict_manage.delete_express', 'sites.delete_site', 'social_django.add_usersocialauth', 'authtoken.delete_token', 'weixin.change_apiaccesstoken', 'dict_manage.add_product', 'verify_utils.delete_captcharecord', 'dict_manage.add_category', 'social_django.add_association', 'sessions.delete_session', 'admin.delete_logentry', 'dict_manage.delete_location', 'dict_manage.add_payment', 'social_django.add_partial', 'authtoken.change_token', 'oauth2_provider.delete_grant', 'account.change_emailconfirmation', 'dict_manage.delete_categorytag', 'dict_manage.add_express', 'verify_utils.add_captcharecord', 'dict_manage.change_express', 'user_manage.change_membership', 'social_django.delete_usersocialauth', 'dict_manage.delete_product', 'user_manage.delete_shopuser', 'oauth2_provider.add_accesstoken', 'account.delete_emailaddress', 'contenttypes.delete_contenttype', 'dict_manage.add_location', 'social_django.delete_partial', 'account.add_emailconfirmation', 'oauth2_provider.delete_accesstoken', 'auth.delete_group', 'dict_manage.change_location', 'dict_manage.delete_productpicture', 'sites.add_site', 'social_django.change_association', 'auth.change_permission', 'account.add_emailaddress', 'dict_manage.delete_category', 'oauth2_provider.add_application', 'user_manage.delete_membership', 'social_django.add_code', 'social_django.delete_association', 'authtoken.add_token', 'user_manage.add_membership', 'auth.delete_permission', 'sessions.change_session', 'verify_utils.change_verifycoderecord', 'oauth2_provider.add_refreshtoken', 'auth.add_permission', 'oauth2_provider.delete_application', 'sites.change_site', 'social_django.change_nonce', 'dict_manage.change_categorytag', 'social_django.change_partial', 'weixin.add_apiaccesstoken', 'weixin.delete_apiaccesstoken', 'dict_manage.delete_payment', 'oauth2_provider.delete_refreshtoken', 'user_manage.add_group', 'oauth2_provider.change_refreshtoken', 'dict_manage.add_productpicture', 'contenttypes.change_contenttype', 'dict_manage.add_categorytag', 'social_django.change_code', 'user_manage.delete_group']
let perms = ['dict_manage.change_payment', 'user_manage.change_shopuser']
let getUserPerms = Mock.mock(`${base}/user_manage/user_perms/`, 'get', {
  'data|2': perms
})

export { hotProducts, products, productDetail, authLogin, authLogout, getUserInfo, getUserPerms }
