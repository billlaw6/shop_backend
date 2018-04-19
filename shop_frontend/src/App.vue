<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style lang="stylus">
  @import './common/vars'
  body
    background-color: background-color
  #app
    font-family: font-family 
    color: color
    background-color: background-color
    title-color: title-color
    border-color: border-color
    shadow-color: shadow-color
    border-radius: border-radius
 
</style>
