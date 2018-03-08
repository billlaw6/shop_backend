<template>
  <Row type="flex" justify="center" align="middle" class="code-row-bg">
    <Col span="7">
      <Tabs class="loginTabs">
        <TabPane label="密码登录">
          <i-form ref="formLogin" :model="formLogin" :rules="loginDataRules"  class="card-box">
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
                <i-col col="12" pull="2" >
                  <router-link to="/pass_reset">忘记密码?</router-link>
                </i-col>
              </Row>
            </Form-item>
            <Form-item class="login-no-bottom">
              <i-button type="primary" @click="handleSubmit('formLogin')" :long="true">登录</i-button>
            </Form-item>
          </i-form>
        </TabPane>
        <TabPane label="验证码登录">
          <i-form ref="formLogin" :model="formLogin" :rules="loginDataRules"  class="card-box">
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
                <i-col col="12" pull="2" >
                  <router-link to="/pass_reset">忘记密码?</router-link>
                </i-col>
              </Row>
            </Form-item>
            <Form-item class="login-no-bottom">
              <i-button type="primary" @click="handleSubmit('formLogin')" :long="true">登录</i-button>
            </Form-item>
          </i-form>
        </TabPane>
      </Tabs>
    </Col>
    <Col span="1" class="vertical-divider">
      <!--<hr/>-->
      或
    </Col>
    <Col span="5">
      还没有账号：<br/>
      <router-link to="/register">立即注册<Icon type="forward"></Icon></router-link>
      <br/><br/><br/><br/><br/>
      使用以下账号直接登录：<br/>
      <Row type="flex" justify="space-between" class="code-row-bg">
        <i-col span="8">
          <Icon src="../assets/weibo.png" size="10"></Icon>
          <a href="http://123.56.115.20/auth/login/weixin">微信</a>
        </i-col>
        <i-col span="8">
          <a href="http://123.56.115.20/auth/login/weibo">微博</a>
        </i-col>
        <i-col span="8">
          <a href="http://123.56.115.20/auth/login/github">GITHUB</a>
        </i-col>
      </Row>
    </Col>
  </Row>
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
  .loginTabs
    width: 100%
    margin: 3px
  .card-box
    padding: 20px
    /*box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);*/
    -webkit-border-radius: 5px
    border-radius: 5px
    -moz-border-radius: 5px
    background-clip: padding-box
    margin-bottom: 20px
    background-color: #F9FAFC
    margin: 18px auto
    width: auto
    /* border: 2px solid #8492A6;*/

  .login-no-bottom
    margin-bottom: 10px

  .vertical-divider
    text-align: center
    hr
      width: 2px
      height: 100px
      display: inline-block
</style>
