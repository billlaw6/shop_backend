<template>
  <div>
    <div>{{userInfo.country}}</div>
    <div>{{userInfo.province}}</div>
    <div>{{userInfo.city}}</div>
    <div>{{userInfo.sex}}</div>
    <div>{{userInfo.nickname}}</div>
    <img :src='userInfo.headimgurl'></img>
  </div>
</template>

<script>
  import { weixinUserInfo } from '../api/api'
  export default {
    name: 'WeixinUserInfo',
    props: {
      openid: {
        type: String,
        required: true,
        default: ''
      }
    },
    data () {
      return {
        userInfo: {}
      }
    },
    methods: {
      get_user_info () {
        let data = { 'openid': this.openid }
        console.log(data)
        weixinUserInfo(data).then(
          (res) => {
            this.userInfo = res.data
          },
          (error) => {
            console.log('weixinUserInfo Error: ' + error)
          }
        ).catch((error) => {
          console.log('catched in weixinUserInfo:' + error)
        })
      }
    },
    mounted () {
      this.get_user_info(this.openid)
    }
  }
</script>

<style lang="stylus" scoped>
</style>
