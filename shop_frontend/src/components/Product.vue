<template>
  <div class="product">
    <div class="picture">
      <img src="../assets/1.jpg" alt="1">
    </div>
    <div class="description">
      <div>Adipisicing laboriosam veritatis quas minima maiores. Cum fugiat consequatur ex architecto minima. Sit deleniti sequi incidunt facere temporibus quidem recusandae voluptatum suscipit! Quod facere placeat odit suscipit deleniti molestiae ut aliquam dolore sint adipisci, vel. Fugiat laboriosam sunt aliquid facere!</div>
    </div>
  </div>
</template>

<script>
  import TimerBtn from '../components/TimerBtn.vue'
  import Captcha from '../components/Captcha.vue'

  export default {
    components: {
      TimerBtn,
      Captcha
    },
    data () {
      return {
        orderFormDataRules: {
          cell_phone: [
            { required: true, message: '请填写正确的手机号', trigger: 'blur' }
          ],
          captcha: [
            { required: true, message: '请证明您不是机器人', trigger: 'blur' },
            { type: 'string', min: 4, message: '验证码长度不小于4位', trigger: 'blur' }
          ],
          address: [
            { required: true, message: '请输入邮寄地址', trigger: 'blur' }
          ],
          verify_code: [
            { required: true, message: '请输入手机收到的验证码', trigger: 'blur' }
          ]
        },
        orderForm: {
          cell_phone: '',
          captcha: '',
          verify_code: '',
          address: ''
        }
      }
    },
    methods: {
      submitOrder () {
        console.log('submitOrder')
      }
    }
  }
</script>
