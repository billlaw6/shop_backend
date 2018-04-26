<template>
  <section class="section2" v-if='section2'>
    <div class="section2-list">
      <ul>
        <li v-for="k in section2.list" :key="k.id">
          <router-link :to="{name:'detail'}">
            <img v-lazy="k.imgPath">
          </router-link>
          <h2 class="section2-list-title ac">
            {{k.title}}
          </h2>
          <p class="section2-list-intro">
            {{k.intro}}
          </p>
          <p class="section2-list-price">
            ￥{{k.price}}
          </p>
        </li>
      </ul>
    </div>
    <router-link class="section2-banner" :to="{name:'detail'}">
      <img v-lazy="section2.banner">
    </router-link>
  </section>
</template>

<script>
  // import { Lazyload } from 'mint-ui'

  export default {
    props: ['section2']
  }
</script>

<style lang="stylus" scoped>
  @import '../../common/vars'

  .section2-list
    overflow-x: auto
    width: 100%
    padding-top()
    /*原生滑动*/
    -webkit-overflow-scrolling: touch
    >ul
      border-top()
      display: -ms-flex
      display: -webkit-box
      display: -ms-flexbox
      display: flex
      padding: 6vw
      width: 380%
      li
        margin-right: 10vw
        width: 26vw
        a, img
          display: block
          width: 100%

        h2, p
          overflow: hidden
          white-space: nowrap
          text-overflow: ellipsis
        h2
          i-front-size(font-size, 32)
          padding-top: 3vw
          color: $content-color

        p.section2-list-intro
          padding-top: 2vw
          i-front-size(font-size, 26)
          color: rgb(150, 150, 150)

        p.section2-list-price
          color: $title-color

  .section2-banner
    display: block
    width: 100vw
    img
      display: block
      height: 24vw
      width: 100%
</style>
