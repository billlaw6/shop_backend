<template>
  <i-form ref="formPassResetConfirm" :model="formPassResetConfirm" :rules="passResetConfirmDataRules"  class="card-box">
    <Form-item class="formPassResetConfirm-title">
      <h3>修改密码</h3>
    </Form-item>

    <Form-item prop="new_password1">
      <i-input size="large" type="password" v-model="formPassResetConfirm.new_password1" placeholder="新密码">
        <Icon type="ios-lock-outline" slot="prepend"></Icon>
      </i-input>
    </Form-item>
    <Form-item prop="new_password2">
      <i-input size="large" type="password" v-model="formPassResetConfirm.new_password2" placeholder="新密码">
        <Icon type="ios-lock-outline" slot="prepend"></Icon>
      </i-input>
    </Form-item>
    <Form-item class="passreset-no-bottom">
      <Row >
        <i-col :xs="{ span: 8, offset: 6 }" >
          <i-button type="primary" @click="handleSubmit('formPassResetConfirm')">确认修改</i-button>
        </i-col>
      </Row>
    </Form-item>
  </i-form>
</template>

<script>
  import { authPassResetConfirm } from '../api/api'
  import { mapState, mapActions } from 'vuex'
  export default {
    data () {
      return {
        formPassResetConfirm: {
          old_password: '',
          new_password1: '',
          new_password2: ''
        },
        passResetConfirmDataRules: {
          old_password: [
            { required: true, message: '请填写原始密码', trigger: 'blur' }
          ],
          new_password1: [
            { required: true, message: '请填写新密码', trigger: 'blur' }
          ],
          new_password2: [
            { required: true, message: '请重复新密码', trigger: 'blur' }
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
            authPassResetConfirm(this.formPassResetConfirm).then((res) => {
              // console.log(res)
              let {data, status, statusText} = res
              console.log(data)
              if (status !== 200) {
                console.log(statusText)
                this.$Message.error('修改密码失败!')
              } else {
                // 跳转至用户目标页或默认页
                if (this.$route.query.redirect) {
                  this.$router.push(this.$route.query.redirect)
                } else {
                  this.$router.push({name: 'p404'})
                }
              }
            }, (error) => {
              console.log('Error in authPassResetConfirm: ' + error)
              this.$Message.error('修改密码失败!')
            }).catch((error) => {
              console.log('catched in authPassResetConfirm:' + error)
              this.$Message.error('修改密码失败!')
            })
          } else {
            this.$Message.error('表单验证失败!')
          }
        })
      },
      formPassResetConfirmChange (name) {
        // console.log('Change '+ name)
        this.$refs[name].resetFields()
      }
    },
    mounted () {
      console.log('PassResetConfirm mounted')
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
  .formPassResetConfirm-title {
    text-align: center
    font-seze: 28px
  }
  .formPassResetConfirm-title h3{
    font-size: 18px
  }
  .login-no-bottom {
    margin-bottom: 10px
  }
</style>
