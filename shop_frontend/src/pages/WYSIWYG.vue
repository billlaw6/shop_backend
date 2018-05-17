<template>
  <div id="wysiwyg">
    <froala :tag="'textarea'" :config="config" v-model="model"></froala>
  </div>
</template>

<script>
  import VueFroala from 'vue-froala-wysiwyg'
  export default {
    name: 'FroalaWysiwyg',
    data () {
      return {
        config: {
          events: {
            'froalaEditor.initialized': function () {
              console.log('froala wysiwyg initialized')
            }
          }
        },
        model: 'Edit Your Content Here!'
      }
    }
  }
</script>

<style lang="stylus" scoped>
</style>
