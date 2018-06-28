<template lang="html">
  <div class="order">
    <Table ref="orderList" stripe :columns="orderListColumns" :data="orderListData">
      <div class="table-header" slot="header">
        订单列表
      </div>
      <div class="table-footer" slot="footer">
        共计: <span>{{ total }}</span> 订单，合计: <span></span>
      </div>
    </Table>

    <div style="margin: 10px; overflow: hidden">
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

    <Modal v-model="showOrderProcessModal" :title="$t('orderProcess')" @on-ok="confirmProcess('orderModelForm')" @on-cancel="cancelAdd('orderModelForm')" >
      <Form ref="processOrderForm" :model="orderModel" :rules="ruleOrderValidate"  label-position="left" inline>
        <Form-item :label="$t('customer')" prop="customer">
          <Input v-model="orderModel.buyer_name"></Input>
        </Form-item>
        <Form-item :label="$t('payment')" prop="payment">
          <AutoComplete v-model="orderModel.payment" :placeholder="$t('selectPayment')" icon="ios-search" 
            :clearable="true"
            @on-select="handlePaymentSelected"
          >
            <Option v-for="option in aPayment" :value="option.name" :key="option.id">
              <span class="product-name">{{ option.name }}</span>
            </Option>
          </AutoComplete>
          <ul v-for="error in orderErrors.payment">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('express')" prop="express">
          <AutoComplete v-model="orderModel.express" :placeholder="$t('selectExpress')" icon="ios-search" 
            :clearable="true"
            @on-select="handleExpressSelected"
          >
            <Option v-for="option in aExpress" :value="option.name" :key="option.id">
              <span class="product-name">{{ option.name }}</span>
            </Option>
          </AutoComplete>
          <ul v-for="error in orderErrors.express">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('expressNo')" prop="express_no">
          <Input v-model="orderModel.express_no" type="text"></Input>
          <ul v-for="error in orderErrors.express_no">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('comment')" prop="comment">
          <Input v-model="orderModel.comment" type="text"></Input>
          <ul v-for="error in orderErrors.comment">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item>
          <br/>
          <Button type="primary" size="large" @click="submitOrder"><Icon type="ios-download-outline"></Icon>{{ $t('submitOrder') }}</Button>
        </Form-item>
      </Form>
    </Modal>
    <br>
  </div>
</template>

<script>
  // import { mapState, mapActions } from 'vuex'
  import { getAllOrder, processOrder } from '@/http/api'

  export default {
    data: function () {
      return {
        keyword: '',
        dateRange: [new Date((new Date()).getFullYear(), (new Date()).getMonth(), (new Date()).getDate() - 2), new Date()],
        dateOptions: {
          shortcuts: [
            {
              text: '最近一周',
              value () {
                const end = new Date()
                const start = new Date()
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
                return [start, end]
              }
            },
            {
              text: '最近一个月',
              value () {
                const end = new Date()
                const start = new Date()
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
                return [start, end]
              }
            },
            {
              text: '最近三个月',
              value () {
                const end = new Date()
                const start = new Date()
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
                return [start, end]
              }
            }
          ]
        },
        orderListData: [],
        showOrderProcessModal: false,
        total: 0,
        orderModel: {},
        orderErrors: {},
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
                }}, param.row.order_no)
            }
          },
          {
            title: this.$t('buyer'),
            key: 'buyer_name',
            sortable: true
          },
          {
            title: this.$t('sumPrice'),
            key: 'sum_price',
            sortable: true
          },
          {
            title: this.$t('detail'),
            key: 'order_details',
            sortable: true,
            render: (h, params) => {
              let columns = [
                { title: this.$t('product'), key: 'product_name' },
                { title: this.$t('price'),
                  key: 'price',
                  render: (h, params) => {
                    return h('span', {
                      style: {
                        color: 'red'
                      }
                    }, params.row.price)
                  }
                },
                { title: this.$t('amount'), key: 'amount' }
              ]
              return h('Poptip', {
                props: {
                  trigger: 'hover',
                  title: '明细',
                  placement: 'bottom'
                }
              }, [
                h('Tag', params.row.order_details.length + '种商品'),
                h('div', {
                  slot: 'content',
                  style: {
                    width: '240px'
                  }
                }, [
                  h('Table', {
                    props: {
                      columns: columns,
                      data: params.row.order_details
                    }
                  }, 'table')
                ])
              ])
            }
          },
          {
            title: this.$t('createdBy'),
            key: 'created_by_name',
            sortable: true
          },
          {
            title: this.$t('createdAt'),
            key: 'created_at',
            sortable: true
          },
          {
            title: '操作',
            key: 'action',
            render: (h, params) => {
              let tagNames = ['nothing', 'enter', 'sent', 'checked']
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      // this.handleProcessOrder(params.row.id, params.row.status)
                      this.showOrderProcessModal = true
                    }
                  }
                }, this.$t(tagNames[params.row.status])),
                h('Button', {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.handleProcessOrder(params.row.id, 9)
                    }
                  }
                }, this.$t('trash'))
              ])
            }
          }
        ],
        pageNumber: 1,
        pageSize: 10
      }
    },
    computed: {
    },
    methods: {
      // 不能用箭头函数，里面的this作用域会不一样
      getOrderList: function (pageSize, pageNumber) {
        let paras = {
          // start: this.dateRange[0].getFullYear() + '-' + (this.dateRange[0].getMonth() - 1) + '-' + (this.dateRange[0].getDate() + 1),
          // end: this.dateRange[1].getFullYear() + '-' + (this.dateRange[1].getMonth() + 1) + '-' + (this.dateRange[1].getDate() + 1),
          keyword: this.keyword,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        getAllOrder(paras).then((res) => {
          let { data, status, statusText } = res
          if (status !== 200) {
            console.error('get Order failed:' + statusText)
          } else {
            this.total = data.count
            this.orderListData = data.results
          }
        }, (error) => {
          console.log('Error in getOrderList:' + error)
        })
      },
      changePage (value) {
        console.log(value)
        this.pageNumber = value
        this.getOrderList(this.pageSize, this.pageNumber)
      },
      changePageSize (value) {
        console.log(value)
        this.pageSize = value
        this.getOrderList(this.pageSize, this.pageNumber)
      },
      confirmProcess (name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            let orderModelSubmit = JSON.parse(JSON.stringify(this.orderModel))
            console.log(orderModelSubmit)
            processOrder(orderModelSubmit).then((res) => {
              let { data, status, statusText } = res
              if (status !== 203) {
                console.error('get Order failed:' + statusText)
              } else {
                console.log(data)
                this.$Message.success(this.$t('processSucceed'))
                this.getOrderList(this.pageSize, this.pageNumber)
              }
            }, (error) => {
              console.log('Error in getOrderList:' + error)
            })
          } else {
            this.$Message.error(this.$t('validateFailed'))
          }
        })
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
</style>
