<template>
  <i-form ref="formPassReset" :model="formPassReset" :rules="passResetDataRules"  class="card-box">
    <Form-item class="formPassReset-title">
      <h3>重置密码</h3>
    </Form-item>

    <Form-item prop="email">
      <i-input size="large" type="email" v-model="formPassReset.email" placeholder="安全邮箱" :autofocus=true>
        <Icon type="ios-email-outline" slot="prepend"></Icon>
      </i-input>
    </Form-item>
    <Form-item class="passreset-no-bottom">
      <Row >
        <i-col :xs="{ span: 8, offset: 6 }" >
          <i-button type="primary" @click="handleSubmit('formPassReset')">确认发送邮件</i-button>
        </i-col>
      </Row>
    </Form-item>
  </i-form>
</template>

<script>
  import { authPassReset } from '../api/api'
  import { mapState, mapActions } from 'vuex'
  export default {
    data () {
      return {
        formPassReset: {
          email: ''
        },
        passResetDataRules: {
          email: [
            { required: true, message: '请填写安全邮箱地址', trigger: 'blur' }
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
    margin: 180px auto
    width: 400px
    /* border: 2px solid #8492A6;*/
  }

  .title {
    margin: 0px auto 40px auto
    text-align: center
    color: #505458
  }
  .formPassReset-title {
    text-align: center
    font-seze: 28px
  }
  .formPassReset-title h3{
    font-size: 18px
  }
  .login-no-bottom {
    margin-bottom: 10px
  }
</style>
