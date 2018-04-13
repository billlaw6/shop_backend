<template>
  <div>
    UserList
    <div>{{userList.count}}</div>
    <div>{{userList.total}}</div>
    <div>{{userList.data}}</div>
    <div>{{userList.next_openid}}</div>
    <Table :columns="columns" :data="data" size="small" ref="table"></Table>
    <br>
    <Button type="primary" size="large" @click="exportData(1)"><Icon type="iso-download-outline"></Icon>Export source data</Button>
    <Button type="primary" size="large" @click="exportData(2)"><Icon type="iso-download-outline"></Icon>Export sorting and filtered data</Button>
    <Button type="primary" size="large" @click="exportData(3)"><Icon type="iso-download-outline"></Icon>Export custom data</Button>
  </div>
</template>

<script>
  import { weixinUserList, weixinBatchUserInfo } from '../api/api'

  export default {
    name: 'WeixinUserList',
    props: {
      next_openid: {
        type: String,
        required: true,
        default: ''
      }
    },
    data () {
      return {
        userList: {},
        columns: [
          {
            'title': '国家',
            'key': 'country',
            'fixed': 'left',
            'width': 200
          },
          {
            'title': '省',
            'key': 'province',
            'fixed': 'left',
            'sortable': true,
            'width': 200,
            filters: [
              {
                label: '北京',
                value: '北京'
              }
            ]
          },
          {
            'title': '城市',
            'key': 'city',
            'fixed': 'left',
            'sortable': true,
            'width': 200
          },
          {
            'title': '昵称',
            'key': 'nickname',
            'fixed': 'left',
            'sortable': true,
            'width': 200
          },
          {
            'title': '性别',
            'key': 'sex',
            'fixed': 'left',
            'sortable': true,
            'width': 200,
            filters: [
              {
                label: '男',
                value: '1'
              },
              {
                label: '女',
                value: '2'
              }
            ],
            filterMultiple: false,
            filterMethod (value, row) {
              // 比较时注意变量类型
              if (value === '1') {
                return row.sex === 1
              } else if (value === '2') {
                return row.sex === 2
              }
            }
          }
        ],
        data: []
      }
    },
    methods: {
      get_user_list () {
        let data = { 'next_openid': this.next_openid }
        console.log(data)
        weixinUserList(data).then(
          (res) => {
            this.userList = res.data
            weixinBatchUserInfo(this.userList).then(
              (res) => {
                console.log(res)
                this.data = res.data.user_info_list
              },
              (error) => {
                console.log(error)
              }
            ).catch((error) => {
              console.log('catched in weixinBatchUserInfo: ' + error)
            })
          },
          (error) => {
            console.log('weixinUserList Error: ' + error)
          }
        ).catch((error) => {
          console.log('catched in weixinUserList:' + error)
        })
      },
      exportData (type) {
        if (type === 1) {
          this.$refs.table.exportCsv({
            filename: 'The original data'
          })
        } else if (type === 2) {
          this.$refs.table.exportCsv({
            filename: 'Sorting and filtering data',
            original: false
          })
        } else if (type === 3) {
          this.$refs.table.exportCsv({
            filename: 'Custom data',
            columns: this.columns.filter((col, index) => index < 4),
            data: this.data.filter((data, index) => index < 4)
          })
        }
      }
    },
    mounted () {
      this.get_user_list(this.next_openid)
    }
  }
</script>

<style lang="stylus" scoped>
</style>
