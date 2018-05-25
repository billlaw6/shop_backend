<template>
  <div class="product">
    <img v-lazy="item.image" alt="product"></img><br/>
    <span>{{ item.name }}</span>
    <span>{{ item.price }}</span>
  </div>
</template>

<script>
  export default {
    props: {
      item: {
        type: Object,
        default: {}
      }
    },
    data () {
      return {
        locItem: ''
      }
    }
  }
</script>

<style language="stylus" scoped>
  .product
    font: 10px
</style>

