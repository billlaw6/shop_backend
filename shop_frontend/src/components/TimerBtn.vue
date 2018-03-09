<template>
  <button @click="run" :disabled="disabled || time > 0" :second="second">
    {{ text }}
  </button>
</template>

<script>
  export default {
    name: 'TimerBtn',
    props: {
      disabled: {
        type: Boolean,
        default: false
      },
      time: {
        type: Number,
        default: 0
      },
      second: {
        type: Number,
        default: 60
      }
    },
    methods: {
      run () {
        this.time = this.second
        this.timer()
      },
      timer () {
        if (this.time > 0) {
          this.time--
          setTimeout(this.timer, 1000)
        }
      }
    },
    computed: {
      text () {
        return this.time > 0 ? this.time + 's 后重新获取' : '获取验证码'
      }
    }
  }
</script>

<style lang="stylus" scoped>
</style>
