<template>
  <i-form ref="formLogin" :model="formLogin" :rules="loginDataRules"  class="card-box">
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
      <Row type="flex" justify="space-between" class="code-row-bg">
        <i-col col="12" >
          <Checkbox-group v-model="formLogin.remember">
            <Checkbox label="记住密码" name="remember"></Checkbox>
          </Checkbox-group>
        </i-col>
        <i-col col="12" >
          <router-link to="/pass_reset">忘记密码?</router-link>
        </i-col>
      </Row>
    </Form-item>
    <Form-item class="login-no-bottom">
      <Row type="flex" justify="space-between" class="code-row-bg">
        <i-col span="12">
          <i-button type="primary" @click="handleSubmit('formLogin')">登录</i-button>
        </i-col>
        <i-col span="12">
          <router-link to="/register"><i-button type="primary">去注册</i-button></router-link>
        </i-col>
      </Row>
    </Form-item>
  </i-form>
</template>

<script>
  import { authLogin, authUser } from '../api/api'
  import { mapState, mapActions } from 'vuex'
  export default {
    data () {
      return {
        formLogin: {
          username: 'liubin',
          password: 'woaini2006',
          remember: []
        },
        loginDataRules: {
          username: [
            { required: true, message: '请填写用户名', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请填写密码', trigger: 'blur' },
            { type: 'string', min: 8, message: '密码长度不能小于8位', trigger: 'blur' }
          ]
        }
      }
    },
    computed: {
      ...mapState({
        loginStatus: state => state.login.loginStatus
      })
    },
    methods: {
      ...mapActions({
        setToken: 'setToken',
        setLoginStatus: 'setLoginStatus',
        setUser: 'setUser'
      }),
      handleSubmit (name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            // 清除旧的无效Token
            window.sessionStorage.removeItem('accessToken')
            authLogin(this.formLogin).then((res) => {
              // console.log(res)
              let {data, status, statusText} = res
              if (status !== 200) {
                console.log(statusText)
                this.$Message.error('用户名或密码错误!')
              } else {
                // window.sessionStorage.setItem('accessToken', data.token)
                window.sessionStorage.setItem('accessToken', data.key)
                // console.log('Login')
                // console.log(this.$route.query.redirect)
                // 登录成功，设置全局用户
                authUser().then((res) => {
                  console.log(res)
                  // window.sessionStorage.removeItem('user')
                  let {data, status} = res
                  if (status !== 200) {
                    this.$Message.error('获取用户信息失败!')
                  } else {
                    console.log(data)
                    this.$store.dispatch('setLoginStatus', true)
                    this.$store.dispatch('setUser', data)
                    window.sessionStorage.setItem('user', JSON.stringify(data))
                    console.log(data.username)
                  }
                }, (error) => {
                  console.log(error)
                })
                // 跳转至用户目标页或默认页
                if (this.$route.query.redirect) {
                  this.$router.push(this.$route.query.redirect)
                } else {
                  this.$router.push({name: 'p404'})
                }
              }
            }, (error) => {
              console.log('Error in authLogin: ' + error)
              this.$Message.error('用户名或密码错误')
            }).catch((error) => {
              console.log('catched in authLogin:' + error)
              this.$Message.error('用户名或密码错误')
            })
          } else {
            this.$Message.error('表单验证失败!')
          }
          if (this.formLogin.remember[0] === '记住密码') {
            window.sessionStorage.setItem('username', JSON.stringify(this.formLogin.username))
            window.sessionStorage.setItem('password', JSON.stringify(this.formLogin.password))
          } else {
            window.sessionStorage.removeItem('username')
            window.sessionStorage.removeItem('password')
          }
        })
      },
      formLoginReset (name) {
        // console.log('Reset '+ name)
        this.$refs[name].resetFields()
      }
    },
    mounted () {
      if (sessionStorage.getItem('username')) {
        this.formLogin.username = JSON.parse(sessionStorage.getItem('username'))
      } else {
        this.formLogin.username = ''
      }
      if (sessionStorage.getItem('password')) {
        this.formLogin.password = JSON.parse(sessionStorage.getItem('password'))
      } else {
        this.formLogin.password = ''
      }
    }
  }
</script>

<style lang="stylus" scoped>
  .card-box
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

  .title
    margin: 0px auto 40px auto
    text-align: center
    color: #505458
  .formLogin-title
    text-align: center
    font-seze: 28px
  .formLogin-title h3
    font-size: 18px
  .login-no-bottom
    margin-bottom: 10px
</style>
