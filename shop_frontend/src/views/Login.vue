<template>
  <i-form ref="formLogin" :model="formLogin" :rules="formLoginRules"  class="card-box">
    <Form-item class="formLogin-title">
      <h3>系统登录</h3>
    </Form-item>

    <Form-item prop="username">
      <i-input size="large" type="text" v-model="formLogin.username" placeholder="用户名" :autofocus=true>
        <Icon type="ios-person-outline" slot="prepend"></Icon>
      </i-input>
    </Form-item>
    <Form-item prop="password">
      <i-input size="large"  type="password" v-model="formLogin.password" placeholder="密码">
        <Icon type="ios-locked-outline" slot="prepend"></Icon>
      </i-input>
    </Form-item>
    <Form-item class="login-no-bottom">
      <Checkbox-group v-model="formLogin.remember">
        <Checkbox label="记住密码" name="remember"></Checkbox>
      </Checkbox-group>
    </Form-item>
    <Form-item class="login-no-bottom">
      <Row >
        <i-col :xs="{ span: 4, offset: 6 }" >
          <i-button type="primary" @click="handleSubmit('formLogin')">登录</i-button>
        </i-col>
        <i-col :xs="{ span: 4, offset: 6 }">
          <i-button  type="primary" @click="formLoginReset('formLogin')">重置</i-button>
        </i-col>
      </Row>
    </Form-item>
  </i-form>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex'

  export default {
    data () {
      return {
        formLogin: {
          username: 'liubin',
          password: 'liubin123456',
          remember: []
        },
        formLoginRules: {
          username: [
            { required: true, message: '请填写用户名', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请填写密码', trigger: 'blur' },
            { type: 'string', min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
          ]
        }
      }
    },
    computed: {
      // 模块命名空间写法一
      ...mapState('login', {
        'cUser': state => state.currentUser
      }),
      // 模块命名空间写法一
      ...mapGetters('login', [
        'loginStatus',
        'username'
      ])
    },
    methods: {
      // 模块命名空间写法二
      ...mapActions({
        setAccessToken: 'login/setAccessToken',
        login: 'login/login'
      }),
      handleSubmit (name) {
        let _this = this
        _this.$refs[name].validate((valid) => {
          if (valid) {
            // 清除过期的accessToken，错误的accessToken会报401未授权错误，更新数据库时测出来的
            window.localStorage.removeItem('accessToken')
            // this.$store.dispatch('login/login', this.formLogin)
            // console.error(this.$store.state.login.currentUser)
            _this.login(_this.formLogin).then(() => {
              // 箭头函数里的this会自动带入上下文的
              // 常规函数则需要使用bind传入this
              // console.error(this.cUser)
              // if (_this.cUser.is_staff) {
              //   _this.$router.push({'name': 'home'})
              // } else {
              //   _this.$router.push({'name': 'user'})
              // }
            // 常规函数使用bind传入this
            // }.bind(_this))
            })
          } else {
            _this.$Message.error('表单验证失败!')
          }
          if (_this.formLogin.remember[0] === '记住密码') {
            window.localStorage.setItem('username', JSON.stringify(_this.formLogin.username))
            window.localStorage.setItem('password', JSON.stringify(_this.formLogin.password))
          } else {
            window.localStorage.removeItem('username')
            window.localStorage.removeItem('password')
          }
        })
      },
      formLoginReset (name) {
        let _this = this
        _this.$refs[name].resetFields()
      }
    },
    mounted () {
      if (localStorage.getItem('username')) {
        this.formLogin.username = JSON.parse(localStorage.getItem('username'))
      }
      if (localStorage.getItem('password')) {
        this.formLogin.password = JSON.parse(localStorage.getItem('password'))
      }
    }
  }
</script>

<style lang="stylus" scoped>
  .card-box {
    padding: 20px
    /*box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);*/
    -webkit-border-radius: 5px
    border-radius: 5px
    -moz-border-radius: 5px
    background-clip: padding-box
    margin-bottom: 20px
    background-color: #F9FAFC
    margin: 180px auto
    width: 400px
    /* border: 2px solid #8492A6;*/
  }

  .title {
    margin: 0px auto 40px auto
    text-align: center
    color: #505458
  }
  .formLogin-title {
    text-align: center
    font-seze: 28px
  }
  .formLogin-title h3{
    font-size: 18px
  }
  .login-no-bottom {
    margin-bottom: 10px
  }
</style>
