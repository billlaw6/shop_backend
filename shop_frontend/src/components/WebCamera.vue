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
      <Button type="primary" v-show="isShowImg" @click.native="resetPhoto">重新拍照</Button>
      <Button type="primary" v-show="!isShowImg" @click.native="stopPhoto">停止画面</Button>
      <Button type="primary" v-show="isShowImg" @click.native="savePhoto">保存</Button>
      <Button type="primary" v-show="!isShowImg" @click.native="photo">拍照</Button>
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
        // audioTrack: null,
        videoTrack: null
      }
    },
    methods: {
      initMedia () {
        let vm = this
        let mediaDevices = null
        // constraints 参数是一个包含了video 和 audio两个成员的MediaStreamConstraints 对象，用于说明请求的媒体类型。必须至少一个类型或者两个同时可以被指定。如果浏览器无法找到指定的媒体类型或者无法满足相对应的参数要求，那么返回的Promise对象就会处于rejected［失败］状态，NotFoundError作为rejected［失败］回调的参数。
        let constraints = {
          audio: true,
          video: {
            facingMode: 'user',
            width: {min: 320, ideal: 800, max: 1080},
            height: {min: 240, ideal: 600, max: 720}
          }
        }
        if (navigator.mediaDevices.getUserMedia) {
          // 最新标准API
          mediaDevices = navigator.mediaDevices.getUserMedia(constraints)
        } else if (navigator.webkitGetUserMedia) {
          // webkit内核浏览器
          mediaDevices = navigator.webkitGetUserMedia(constraints)
        } else if (navigator.mozGetUserMedia) {
          // Firefox浏览器
          mediaDevices = navigator.mozGetUserMedia(constraints)
        } else if (navigator.webkitGetUserMedia) {
          // 旧版API
          mediaDevices = navigator.getUserMedia(constraints)
        }
        if (mediaDevices === null) {
          // 正常情况下返回的是一个Promise
          alert('你的浏览器不支持访问用户媒体设备')
        } else {
          // 这个Promise成功后的回调函数带一个 MediaStream 对象作为其参数。
          mediaDevices.then(mediaStream => {
            let video = vm.$refs.video
            // MediaStream 接口是一个媒体内容的流.。一个流包含几个轨道，比如视频和音频轨道。
            if ('srcObject' in video) {
              // 新API
              // 程序自动从mediaStream中选择合适的track(audio, video)
              video.srcObject = mediaStream
            } else {
              // 老式API
              let compatibleURL = window.URL || window.webkitURL
              video.src = compatibleURL.createObjectURL(mediaStream) || mediaStream
            }
            video.onloadedmetadata = (e) => {
              video.play()
            }
            vm.video = video
            // vm.audioTrack = mediaStream.getTracks()[0]
            vm.videoTrack = mediaStream.getTracks()[1]
          }).catch(err => {
          // 这个Promise失败后的回调函数带一个DOMException对象作为其参数。
            console.log('err.message:' + err.name)
          })
        }
      },
      photo () {
        let vm = this
        let img = vm.$refs.img
        let canvas = vm.$refs.canvas
        let context = canvas.getContext('2d')
        let width = 800
        let height = 600
        canvas.width = width
        canvas.height = height
        img.height = height
        context.drawImage(vm.video, 0, 0, width, height)
        // HTMLCanvasElement.toDataURL() 方法返回一个包含图片展示的 data URI 。可以使用 type 参数其类型，默认为 PNG 格式。图片的分辨率为96dpi。
        vm.dataURL = canvas.toDataURL('image/png', 0.92)
        img.src = vm.dataURL
        vm.isShowImg = true
      },
      resetPhoto () {
        let vm = this
        vm.isShowImg = false
      },
      savePhoto () {
      // 从Canvas获取图片数据的核心思路是用canvas的toDataURL将Canvas的数据转换为base64位编码的PNG图像
        console.log(this.dataURL)
        this.$Message.success('已经保持了图片的:dataURL')
      },
      stopPhoto () {
        // this.audioTrack.stop()
        if (this.videoTrack !== null) {
          console.log('stop')
          console.log(this.videoTrack)
          // 执行就关闭浏览器，原因不明
          // this.videoTrack.stop()
        } else {
          console.log(this.videoTrack)
        }
      }
    },
    mounted () {
      this.initMedia()
    },
    destroyed () {
      let vm = this
      vm.stopPhoto()
    }
  }
</script>
