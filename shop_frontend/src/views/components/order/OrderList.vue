<template lang="html">
  <div class="order">
    <Table ref="orderList" stripe :columns="orderListColumns" :data="orderList">
      <div class="table-header" slot="header">
        订单列表
      </div>
      <div class="table-footer" slot="footer">
        共计: <span>{{ total }}</span> 订单，合计: <span></span>
      </div>
    </Table>
    <div style="margin: 10px;overflow: hidden">
      <div style="float: right;">
        <Page :total="total" :current="pageNumber"
          show-sizer show-elevator show-total
          :page-size=pageSize
          :page-size-opts=[10,20,40,10000]
          @on-change="changePage" 
          @on-page-size-change="changePageSize"
        >
        </Page>
      </div>
    </div>
    <br>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'
  import { getAllOrder } from '@/http/api'

  export default {
    data () {
      return {
        keyword: '',
        dateRange: [new Date((new Date()).getFullYear(), (new Date()).getMonth(), (new Date()).getDate() - 2), new Date()],
        orderList: [],
        total: 0,
        orderListColumns: [
          {
            title: this.$t('orderNo'),
            key: 'order_no',
            sortable: true,
            render: (h, param) => {
              let toUrl = {name: 'order', params: {orderId: param.row.id}}
              return h('router-link',
                {props: {
                  to: toUrl
                }}, param.row.name)
            }
          },
          {
            title: this.$t('sumPrice'),
            key: 'sum_price',
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
        ],
        pageNumber: 0,
        pageSize: 10
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
      })
    },
    methods: {
      ...mapActions([
        'setDepartments'
      ]),
      // 模块命名空间写法二
      ...mapActions('cart', [
        'emptyCart'
      ]),
      getOrderList: (pageSize, pageNumber) => {
        let paras = {
          start: this.dateRange[0].getFullYear() + '-' + (this.dateRange[0].getMonth() + 1) + '-' + (this.dateRange[0].getDate() + 1),
          end: this.dateRange[1].getFullYear() + '-' + (this.dateRange[1].getMonth() + 1) + '-' + (this.dateRange[1].getDate() + 1),
          keyword: this.keyword,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        getAllOrder(paras).then((res) => {
          console.debug('get order')
          let { data, status, statusText } = res
          if (status !== 200) {
            console.log('get Order failed:' + statusText)
          } else {
            this.total = data.count
            this.orderList = data.results
          }
        }, (error) => {
          console.log('Error in getOrderList:' + error)
        })
      },
      changePage (pageNumber) {
        console.log(pageNumber)
        this.pageNumber = pageNumber
        this.getProduct(this.pageSize, this.pageNumber)
      },
      changePageSize (pageSize) {
        console.log(pageSize)
        this.pageSize = pageSize
        this.getProduct(this.pageSize, this.pageNumber)
      }
      checkoutCart: function (checkoutList) {
        console.debug('checkout cart')
        if (this.loginStatus) {
          console.debug('checking')
          this.$store.dispatch('emptyCart')
        } else {
          console.debug('redirecting')
          this.$router.push({ name: 'login' })
        }
      }
    },
    mounted () {
      console.debug('Cart.vue mounted')
      this.getOrderList(this.pageSize, this.pageNumber)
    },
    beforeCreate () {
      console.log('Cart.vue creating')
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
