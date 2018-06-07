<template>
  <FormItem prop="verify_code">
    <Row>
      <div :class="captcha" >
        <Col span="12">
          <Input size="large" type="text" v-model="captcha.code" placeholder="验证码"></Input>
        </Col>
        <Col span="12">
          <img :src="image_data" alt="CAPTCHA" @click="getCaptcha" :length="length" :width="width" :height="height" :fontsize="fontsize">
        </Col>
      </div>
    </Row>
  </FormItem>
</template>

<script>
  import { getCaptcha } from '../api/api'
  export default {
    name: 'Captcha',
    props: {
      length: {
        type: Number,
        default: 4
      },
      width: {
        type: Number,
        default: 100
      },
      height: {
        type: Number,
        default: 40
      },
      fontsize: {
        type: Number,
        default: 35
      }
    },
    data () {
      return {
        captcha_paras: {
          length: this.length,
          width: this.width,
          height: this.height,
          fontsize: this.fontsize
        },
        captcha: {
          img: '',
          code: ''
        }
      }
    },
    computed: {
      image_data () {
        return 'data:image/jpeg;base64,' + this.captcha.img
      }
    },
    methods: {
      getCaptcha () {
        console.log('getCaptcha')
        getCaptcha(this.captcha_paras).then((res) => {
          let {data, status, statusText} = res
          console.log(data, status, statusText)
          this.captcha = data
        }, (error) => {
          console.log(error)
        }).catch((error) => {
          console.log(error)
        })
      },
      validateCaptcha (code) {
        console.log('validate')
      }
    },
    mounted () {
      this.getCaptcha()
    }
  }
</script>

<style lang="stylus" scoped>
</style>
