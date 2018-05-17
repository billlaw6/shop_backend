<template>
  <div class="products">
    Product
    <h1> {{ $route.params.id }} </h1>
    <product-detail></product-detail>
    <div class="product">
      <div class="picture">
        <img src="" alt="1">
        <img src="" alt="2">
        <img src="" alt="3">
      </div>
      <div class="description">
        <div></div>
      </div>
    </div>
    <div class="order">
      <Form ref="orderForm" :model="orderForm" :rules="orderFormDataRules">
        <FormItem prop="cell_phone">
          <Input size="large" type="text" v-model="orderForm.cell_phone" placeholder="注册使用的手机号" :autofocus=true>
            <span slot="prepend">0086</span>
          </Input>
        </FormItem>
        <captcha :height="40"></captcha>
        <FormItem prop="verify_code">
          <Row>
            <Col span="10">
              <Input size="large" type="text" v-model="orderForm.verify_code" placeholder="请输入短信验证码">
              </Input>
            </Col>
            <Col span="14">
              <timer-btn :second="6"></timer-btn>
            </Col>
          </Row>
        </FormItem>
        <FormItem>
          <Row>
            <Col span="8">
              <Button type="primary" @click="submitOrder">下单</Button>
            </Col>
          </Row>
        </FormItem>
      </Form>
    </div>
    <div class="sale-record"></div>
    <div class="comments"></div>
  </div>
</template>

<script>
  import TimerBtn from '../components/TimerBtn.vue'
  import Captcha from '../components/Captcha.vue'
  import ProductDetail from '../components/ProductDetail.vue'

  export default {
    components: {
      TimerBtn,
      Captcha,
      ProductDetail
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
