<template lang="html">
  <div class="stock-move-record">
    <Table ref="moveRecordList" stripe :columns="moveRecordListColumns" :data="moveRecordList">
      <div class="table-header" slot="header">
        已添加商品列表
      </div>

      <div class="table-footer" slot="footer">
        共计: <span>{{ moveRecordListCount }}</span> 种商品，合计: <span>{{ moveRecordListSum | currency }}</span>

      </div>
    </Table>
    <br>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex'
  import { getStockMoveRecord } from '@/http/api'

  export default {
    props: {
      currentDept: {
        type: Object,
        default: null
      }
    },
    data () {
      return {
        pageSize: 10,
        pageNumber: 1,
        moveRecordList: [],
        moveRecordListColumns: [
          {
            title: 'page_no',
            key: 'page_no',
            sortable: true
          },
          {
            title: '商品名称',
            key: 'name',
            sortable: true,
            render: (h, param) => {
              let toUrl = {name: 'detail', params: {productId: param.row.id}}
              return h('router-link',
                {props: {
                  to: toUrl
                }}, param.row.name)
            }
          },
          {
            title: '单价',
            key: 'price',
            sortable: true
          },
          {
            title: this.$t('batch_no'),
            key: 'price',
            sortable: true
          },
          {
            title: '数量',
            key: 'amount',
            sortable: true,
            render: (h, params) => {
              return h('span', params.row.amount.toFixed(this.decimals))
            }
          },
          {
            title: '小计',
            key: 'itemSum',
            render: (h, params) => {
              return h('span', (params.row.price * params.row.amount).toFixed(this.decimals))
            }
          },
          {
            title: '备注',
            key: 'comment',
            render: (h, params) => {
              return h('span', params.row.comment)
            }
          },
          {
            title: '操作',
            key: 'action',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.removeCartItem(params.row)
                    }
                  }
                }, '删除')
              ])
            }
          }
        ]
      }
    },
    computed: {
      // 模块命名空间写法二
      ...mapState({
        otherDepartments: state => {
          // 尝试复制一下，防止修改state原值
          let tmpArray = JSON.parse(JSON.stringify(state.departments.results))
          if (state.login.currentUser) {
            // console.error(state.login.currentUser.department)
            let tmpArray1 = tmpArray.filter((item, index, array) => {
              // console.error(item.id)
              return item.id !== state.login.currentUser.department
            })
            return tmpArray1
          } else {
            console.error(state.login.currentUser)
            return tmpArray
          }
        }
      }),
      // 模块命名空间写法一
      ...mapState('cart', {
        decimals: state => state.decimals
      }),
      ...mapGetters('cart', [
        // 模块命名空间写法一
        'moveRecordListCount',
        'moveRecordListSum'
      ])
    },
    methods: {
      ...mapActions([
        'setDepartments'
      ]),
      // 模块命名空间写法二
      ...mapActions('cart', [
        'emptyCart',
        'setCartList',
        'removeCartItem',
        'resetCartList',
        'decreaseCartItemAmount',
        'increaseCartItemAmount'
      ]),
      getData (department, pageSize, pageNumber) {
        let params = {
          department: department,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        getStockMoveRecord(params).then((res) => {
          let { data, status, statusText } = res
          if (status !== 200) {
            console.log('get moveRecord failed:' + statusText)
          } else {
            this.total = data.count
            this.moveRecordList = data.results
          }
        }, (error) => {
          console.error(error)
        })
      }
    },
    mounted () {
      this.getData(this.currentDept, this.pageSize, this.pageNumber)
    },
    beforeCreate () {
    }
  }
</script>

<style lang="stylus" scoped>
  .cart-item
    border: 1px solid
  .footer
    width: 100vw
    height: 10vh
    div
      text-align: center
  .table-header
    font-size: 1.3em
    text-align: center
  .table-footer
    font-size: 1.2em
    margin: 1vh 3vw 6vh 1vw
    span
      color: red
</style>
