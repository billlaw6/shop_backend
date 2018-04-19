<template lang="html">
  <section class="section1" v-if='section1'>
    <h1 class="section1-title">
      section1
      <i class="icon-right"></i>
    </h1>
    <ul class="section1-list">
      <li v-for="k in section1.list">
        <router-link :to="{name:'详情页'}" :key="k.id">
          <img v-lazy="k.imgPath" alt="">
        </router-link>
      </li>
    </ul>
  <router-link :to="{ name: '详情页'}"  class="section1-banner">
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
</style>
