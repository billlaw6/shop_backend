<template>
  <div>
    <div>
      <div class="web-camera">
        <div class="border" v-if="!isShowImg">
          <span class="top_left"></span>
          <span class="top_right"></span>
          <span class="bottom_left"></span>
          <span class="bottom_right"></span>
        </div>
        <video ref="video"></video>
        <img ref="img" class="img" v-show="isShowImg">
      </div>
      <canvas ref="canvas" class="canvas" v-show="false"></canvas>
    </div>
    <div class="button_group">
      <button v-show="isShowImg" title="重新拍照" @click.native="resetPhoto"/>
      <button v-show="isShowImg" title="拍照" @click.native="surePhoto"/>
      <button v-show="!isShowImg" title="拍照" @click.native="photo" />
    </div>
  </div>
</template>

<script>
  export default {
    name: 'WebCamera',
    data () {
      return {
        video: null,
        isShowImg: false,
        dataURL: null,
        track: null
      }
    },
    methods: {
      initPhoto () {
        let vm = this
        let mediaDevices = null
        let containers = {
          audio: true,
          video: {
            facingMode: 'user',
            width: {min: 300, ideal: 800, max: 1920},
            height: {min: 400, ideal: 800, max: 1920}
          }
        }
        if (navigator.mediaDevices.getUserMedia) {
          // 最新标准API
          mediaDevices = navigator.mediaDevices.getUserMedia(containers)
        } else if (navigator.webkitGetUserMedia) {
          // webkit内核浏览器
          mediaDevices = navigator.webkitGetUserMedia(containers)
        } else if (navigator.mozGetUserMedia) {
          // Firefox浏览器
          mediaDevices = navigator.mozGetUserMedia(containers)
        } else if (navigator.webkitGetUserMedia) {
          // 旧版API
          mediaDevices = navigator.getUserMedia(containers)
        }
        if (mediaDevices === null) {
          alert('你的浏览器不支持访问用户媒体设备')
        } else {
          mediaDevices.then(mediaStream => {
            let video = vm.$refs.video
            let compatibleURL = window.URL || window.webkitURL
            video.src = compatibleURL.createObjectURL(mediaStream)
            video.onloadedmetadata = (e) => {
              video.play()
            }
            vm.video = video
            vm.track = mediaStream.getTracks()[0]
          }).catch(err => {
            console.log('err.message:' + err.name)
          })
        }
      },
      photo () {
        let vm = this
        let dataURL = null
        let img = vm.$refs.img
        let canvas = vm.$refs.canvas
        let context = canvas.getContext('2d')
        let width = 300
        let height = 400
        canvas.width = width
        canvas.height = height
        img.height = height
        context.drawImage(vm.video, 0, 0, width, height)
        dataURL = canvas.toDataURL('image/png')
        img.src = dataURL
        vm.isShowImg = true
      },
      resetPhoto () {
        let vm = this
        vm.isShowImg = false
      },
      surePhoto () {
        console.log(this.dataURL)
        this.$Message.success('已经保持了图片的:dataURL')
      },
      stopPhoto () {
        this.track.stop()
      }
    },
    mounted () {
      this.initPhoto()
    },
    destroyed () {
      let vm = this
      vm.stopPhoto()
    }
  }
</script>
