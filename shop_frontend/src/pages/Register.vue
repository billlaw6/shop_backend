<template>
  <Row type="flex" justify="center" align="middle" class="code-row-bg">
    <Col span="7">
      <Tabs class="registerTabs">
        <TabPane label="手机号注册">
          <i-form class="card-box" ref="formRegister" :model="formRegister" :rules="registerDataRules">
            <Form-item class="register-no-bottom">
              <Row type="flex" justify="end" class="code-row-bg">
                  <i-button type="primary" @click="handleSubmit('formRegister')" :long="true">提交</i-button>
              </Row>
            </Form-item>
          </i-form>
        </TabPane>
        <TabPane label="用户名注册">
          <i-form class="card-box" ref="formRegister" :model="formRegister" :rules="registerDataRules">
            <Form-item prop="username">
              <i-input size="large" type="text" v-model="formRegister.username" placeholder="用户名" :autofocus="true">
                <Icon type="ios-person-outline" slot="prepend"></Icon>
              </i-input>
              </i-input>
              <li v-for="error in registerServerError.username">{{ error }}</li>
            </Form-item>
            <Form-item prop="password1">
              <i-input size="large" type="password" v-model="formRegister.password1" placeholder="密码">
                <Icon type="ios-locked-outline" slot="prepend"></Icon>
              </i-input>
            </Form-item>
            <Form-item prop="password2">
              <i-input size="large" type="password" v-model="formRegister.password2" placeholder="密码确认">
                <Icon type="ios-locked-outline" slot="prepend"></Icon>
              </i-input>
              <li v-for="error in registerServerError.password">{{ error }}</li>
            </Form-item>
            <Form-item prop="email">
              <i-input size="large" type="email" v-model="formRegister.email" placeholder="邮箱">
                <Icon type="ios-email-outline" slot="prepend"></Icon>
              </i-input>
              <li v-for="error in registerServerError.email">{{ error }}</li>
            </Form-item>
            <Form-item class="login-no-bottom">
              <Row type="flex" justify="space-between" class="code-row-bg">
                <i-col col="12" >
                  <Checkbox-group v-model="formRegister.remember">
                    <Checkbox label="记住密码" name="remember">
                      同意<router-link to="/protocal">"服务条款"</router-link>和<router-link to="/privacy">"隐私权相关政策"</router-link>
                    </Checkbox>
                  </Checkbox-group>
                </i-col>
              </Row>
            </Form-item>
            <Form-item class="register-no-bottom">
              <Row type="flex" justify="end" class="code-row-bg">
                  <i-button type="primary" @click="handleSubmit('formRegister')" :long="true">提交</i-button>
              </Row>
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
      已有账号：<br/>
      <router-link to="/login">直接登录<Icon type="forward"></Icon></router-link>
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
  import { authRegister, authUser } from '../api/api'
  import { mapState, mapActions } from 'vuex'
  import TimerBtn from '../components/TimerBtn.vue'
  export default {
    components: {
      TimerBtn
    },
    data () {
      return {
        formRegister: {
          username: 'liubin',
          password1: 'woaini2006',
          password2: 'woaini2006',
          email: 'bill_law6@163.com'
        },
        registerDataRules: {
          username: [
            { required: true, message: '请填写用户名', trigger: 'blur' }
          ],
          password1: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { type: 'string', min: 8, message: '密码长度不能小于8位', trigger: 'blur' }
          ],
          password2: [
            { required: true, message: '请再次输入密码', trigger: 'blur' },
            { type: 'string', min: 8, message: '密码长度不能小于8位', trigger: 'blur' }
          ],
          email: [
            { required: true, message: '请输入常用邮箱', trigger: 'blur' },
            { type: 'email', message: '请输入有效邮箱地址', trigger: 'blur' }
          ]
        },
        registerServerError: {
          username: '',
          password: '',
          email: ''
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
            authRegister(this.formRegister).then((res) => {
              console.log(res)
              let {data, status, statusText} = res
              if (status !== 201) {
                this.$Message.error('注册失败!')
              } else {
                console.log('Register OK, statusText: ' + statusText)
                window.sessionStorage.setItem('accessToken', data.key)
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
                  console.log(error.response)
                })
                // 跳转至用户目标页或默认页
                if (this.$route.query.redirect) {
                  this.$router.push(this.$route.query.redirect)
                } else {
                  this.$router.push({name: 'p404'})
                }
              }
            }, (error) => {
              console.log(error.response)
              let {data, status, statusText} = error.response
              this.registerServerError = data
              this.$Message.error('注册失败' + status + statusText)
            }).catch((error) => {
              console.log('catched in Register:' + error)
              this.$Message.error('注册失败')
            })
          } else {
            this.$Message.error('表单验证失败!')
          }
        })
      },
      formRegisterReset (name) {
        // console.log('Reset '+ name)
        this.$refs[name].resetFields()
      }
    },
    mounted () {
      // console.log('Mounted')
      this.registerServerError = {}
    }
  }
</script>

<style lang="stylus" scoped>
  .registerTabs
    width: 100%
    margin: 3px

  .card-box
    padding: 20px
    -webkit-border-radius: 5px
    border-radius: 5px
    -moz-border-radius: 5px
    background-clip: padding-box
    background-color: #F9FAFC
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
