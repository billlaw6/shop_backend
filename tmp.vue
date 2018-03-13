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
      if (navigator.mediaDevices.getUserMedia || navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia) {
        initPhoto () {
          let vm = this
          let mediaDevices = navigator.mediaDevices.getUserMedia({ audio: false, video: {width: 300, height: 400 }})
          this.getUserMedia({
            video: {width: 480, height:320}
          }, success, error)
        } else {
          alert("你的浏览器不支持访问用户媒体设备")
        }
      },
      getUserMedia (constrains, success, error) {
        if (navigator.mediaDevices.getUserMedia) {
          // 最新标准API
          navigator.mediaDevices.getUserMedia(constrains).then(success).catch(error)
        } else if (navigator.webkitGetUserMedia) {
          // webkit内核浏览器
          navigator.webkitGetUserMedia(constrains).then(success).catch(error)
        } else if (navigator.mozGetUserMedia) {
          // Firefox浏览器
          navigator.mozGetUserMedia(constrains).then(success).catch(error)
        } else if (navigator.webkitGetUserMedia) {
          // 旧版API
          navigator.getUserMedia(constrains).then(success).catch(error)
        }
      },
      success (stream) {
        // 兼容webkit内核浏览器
        let compatibleURL = window.URL || window.webkitURL
        // 将视频流设置为video元素的源
        video.src = compatibleURL.createObjectURL(stream)
        // 播放视频
        video.play()
      },

      error (error) {
        console.log("访问用户媒体设备失败：", error.name, error.message)
      },

      drawImage () {
        context.drawImage(video, 0, 0, 480, 320)
      }

    }, 
    mounted () {
      this.initPhoto()
    }
    }
  }
</script>
