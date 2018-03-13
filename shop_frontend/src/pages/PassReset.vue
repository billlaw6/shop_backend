<template>
  <Row type="flex" justify="center" align="middle" class="code-row-bg">
    <Col span="12">
      <Tabs class="passResetTabs">
        <TabPane label="通过手机号找回">
          <Row>
            <Steps :current="1">
              <Step title="01" content="验证手机号"></Step>
              <Step title="02" content="重置密码"></Step>
            </Steps>
          </Row>
          <Row>
            <Form ref="formPhonePassReset" :model="formPhonePassReset" :rules="passPhoneResetDataRules"  class="card-box">
              <FormItem prop="cell_phone">
                <Input size="large" type="text" v-model="formPhonePassReset.cell_phone" placeholder="注册使用的手机号" :autofocus=true>
                  <span slot="prepend">0086</span>
                </Input>
              </FormItem>
              <FormItem prop="captcha">
                <Row>
                  <Col span='10'>
                    <Input size="large" type="text" v-model="formPhonePassReset.captcha" placeholder="请输入右侧字符">
                    </Input>
                  </Col>
                  <Col span='14'>
                    <captcha :height="40"></captcha>
                  </Col>
                </Row>
              </FormItem>
              <FormItem prop="verify_code">
                <Row>
                  <Col span='10'>
                    <Input size="large" type="text" v-model="formPhonePassReset.verify_code" placeholder="请输入短信验证码">
                    </Input>
                  </Col>
                  <Col span='14'>
                    <timer-btn :second="6"></timer-btn>
                  </Col>
                </Row>
              </FormItem>
              <FormItem>
                <Row>
                  <Col span="8">
                    <Button type="primary" @click="nextStep">下一步</Button>
                  </Col>
                </Row>
              </FormItem>
            </Form>
          </Row>
        </TabPane>
        <TabPane label="通过安全邮箱找回">
          <Row>
            <Steps :current="1">
              <Step title="01" content="验证安全邮箱"></Step>
              <Step title="02" content="点击校验邮件链接"></Step>
              <Step title="03" content="输入新密码"></Step>
            </Steps>
          </Row>
          <Row>
            <Form ref="formEmailPassReset" :model="formEmailPassReset" :rules="passEmailResetDataRules"  class="card-box">
              <FormItem prop="email">
                <Input size="large" type="email" v-model="formEmailPassReset.email" placeholder="安全邮箱" :autofocus=true>
                  <Icon type="ios-email-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <FormItem>
                <Button type="primary" @click="nextStep">下一步</Button>
              </FormItem>
            </Form>
          </Row>
        </TabPane>
      </Tabs>
    </Col>
  </Row>
</template>

<script>
  import { authPassReset } from '../api/api'
  import { mapState, mapActions } from 'vuex'
  import TimerBtn from '../components/TimerBtn.vue'
  import Captcha from '../components/Captcha.vue'
  export default {
    components: {
      TimerBtn,
      Captcha
    },
    data () {
      return {
        formEmailPassReset: {
          email: ''
        },
        passEmailResetDataRules: {
          email: [
            { required: true, message: '请填写安全邮箱地址', trigger: 'blur' }
          ]
        },
        formPhonePassReset: {
          cell_phone: '',
          captcha: '',
          verify_code: ''
        },
        passPhoneResetDataRules: {
          cell_phone: [
            { required: true, message: '请填写注册使用的手机号', trigger: 'blur' }
          ],
          captcha: [
            { required: true, message: '请填写右边图片字母', trigger: 'blur' }
          ],
          verify_code: [
            { required: true, message: '请填写手机收到的校验码', trigger: 'blur' }
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
        setUser: 'setUser'
      }),
      handleSubmit (name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            authPassReset(this.formPassReset).then((res) => {
              // console.log(res)
              let {data, status, statusText} = res
              console.log(data)
              if (status !== 200) {
                console.log(statusText)
                this.$Message.error('发送邮件失败!')
              } else {
                // 跳转至用户目标页或默认页
                if (this.$route.query.redirect) {
                  this.$router.push(this.$route.query.redirect)
                } else {
                  this.$router.push({name: 'p404'})
                }
              }
            }, (error) => {
              console.log('Error in authPassReset: ' + error)
              this.$Message.error('发送邮件失败!')
            }).catch((error) => {
              console.log('catched in authPassReset:' + error)
              this.$Message.error('发送邮件失败!')
            })
          } else {
            this.$Message.error('表单验证失败!')
          }
        })
      },
      formPassResetReset (name) {
        // console.log('Reset '+ name)
        this.$refs[name].resetFields()
      },
      nextStep () {
        console.log('next step')
        this.current = 2
      }
    },
    mounted () {
      console.log('PassReset mounted')
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
    /* border: 2px solid #8492A6;*/
  }

  .login-no-bottom {
    margin-bottom: 10px
  }
</style>
