<template lang="html">
  <section class="section1" v-if='section1'>
    <h1 class="section1-title">
      section1
      <i class="icon-right"></i>
    </h1>
    <ul class="section1-list">
      <li v-for="k in section1.list">
        <router-link :to="{name:'detail'}" :key="k.id">
          <img v-lazy="k.imgPath" alt="">
        </router-link>
      </li>
    </ul>
  <router-link :to="{ name: 'detail'}"  class="section1-banner">
    <img v-lazy="section1.banner" v-if='section1'>
  </router-link>
  </section>
</template>

<script>
  // import { Lazyload } from 'mint-ui'

  export default {
    props: ['section1']
  }
</script>

<style lang="stylus" scoped>
  @import '../../common/vars'
  .section1
    padding-top()
    .section1-title
      bordor-top()
      background-color: $background-color
      text-align: center
      padding: 4vw 0
      i-font-size(font-size, 40)
      color: $content-color
      position: relative
      i
        position: absolute
        right: 6vw
        top: 50%
        i-font-size(font-size, 56)
        i-font-size(margin-top, -16)
        &::before
          color: rgb(159, 159, 159)
    .section1-list
      display: -ms-flex
      display: -webkit-box
      display: -ms-flexbox
      display: flex
      -ms-flex-wrap: wrap
      flex-wrap: wrap
      -ms-flex-pack: distribute
      justify-content: space-around
      padding:0 2vw 4vw 2vw
      li
        width: 50%
        padding: 1vw
        -webkit-box-sizing: border-box
        box-sizing: border-box
        a,
        img
          width: 100%
          display: block

    .section1-banner
      display: block
      width: 100vw
      img
        width: 100%
        height: 24vw
</style>
