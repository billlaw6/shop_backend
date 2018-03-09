<template>
  <div :class="captcha" >
    <img :src="image_data" alt="CAPTCHA" @click="getCaptcha" :length="length" :width="width" :height="height" :fontsize="fontsize">
  </div>
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
          img: null,
          code: null
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
