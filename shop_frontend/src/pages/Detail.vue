<template lang="html">
  <div class="detail">
    <v-swipe></v-swipe>
    <v-choose></v-choose>
    <v-content></v-content>
    <v-baseline></v-baseline>
    <v-footer></v-footer>
  </div>
</template>

<script>
  import Swipe from '@/components/detail/Swipe.vue'
  import Choose from '@/components/detail/Choose.vue'
  import Content from '@/components/detail/Content.vue'
  import Footer from '@/components/detail/Footer.vue'
  import Baseline from '@/components/common/Baseline.vue'

  export default {
    components: {
      'v-swipe': Swipe,
      'v-choose': Choose,
      'v-content': Content,
      'v-footer': Footer,
      'v-baseline': Baseline
    },

    beforeCreate () {
      this.$store.dispatch('setDatas')
    }
  }
</script>

<style lang="stylus" scoped>
  .detail
    width: 100%
    padding-bottom: 14vw
</style>
