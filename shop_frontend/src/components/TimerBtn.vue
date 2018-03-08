<template>
  <button :disabled="disabled || time > 0" :second="6">
    {{ text }}
  </button>
</template>

<script>
  export default {
    name: 'TimerBtn',
    data () {
      return {
        second: 6,
        time: 0
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
