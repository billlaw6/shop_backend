<template lang="html">
  <div class="order">
    <Row>
      <Col span="6">
        <Date-picker v-model="dateRange" type="daterange" format="yyyy-MM-dd" :options="dateOptions" placement="bottom-start" placeholder="订单创建时间"></Date-picker>
      </Col>
      <Col span="8">
        <AutoComplete v-model="keyword" :placeholder="$t('localSearch')" icon="ios-search" :clearable="true">
          <Option v-for="option in aList" :value="option.order_no" :key="option.order_no">
            <span class="name">{{ option.order_no}}</span>
            <span class="sum_price">{{ option.buyer_name }}</span>
            <span class="sum_price">{{ option.sum_price | currency }}</span>
          </Option>
        </AutoComplete>
      </Col>
      <Col span="3">
        <i-button type="primary" @click="handleRemoteSearch()">{{ $t('remoteSearch') }}</i-button>
      </Col>
      <Col span="4" push="3">
        <i-button type="primary" @click="">{{ $t('addOrder') }}</i-button>
       </Col>
    </Row>

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

    <Modal v-model="showOrderProcessModal" :title="$t('orderProcess')" @on-ok="confirmProcess('processOrderForm')" @on-cancel="cancelProcess('orderModelForm')" >
      <Form ref="processOrderForm" :model="orderModel" :rules="ruleOrderValidate"  label-position="left" inline>
        <Form-item :label="$t('express')" prop="express">
          <AutoComplete v-model="orderModel.express" :placeholder="$t('selectExpress')" icon="ios-search" 
            :clearable="true"
            @on-select="handleExpressSelected"
          >
            <Option v-for="option in aExpress" :value="option.name" :key="option.code">
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
        <Form-item :label="$t('payment')" prop="payment">
          <Select v-model="orderModel.payment">
            <Option v-for="item in availablePayments" :value="item.code" :key="item.code">{{ item.name }}</Option>
          </Select>
          <ul v-for="error in orderErrors.payment">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('comment')" prop="comment">
          <Input v-model="orderModel.comment" type="text"></Input>
          <ul v-for="error in orderErrors.comment">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <div style="display: none">
          <Input v-model="orderModel.order_no"></Input>
          <Input v-model="orderModel.status"></Input>
        </div>
      </Form>
    </Modal>
    <br>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import { getAllOrder, processOrder } from '@/http/api'

  export default {
    data: function () {
      const validateExpress = (rule, value, callback) => {
        if (value) {
          if (this.availableExpresses.some((val, index, array) => val.name === value)) {
            console.log('name valide')
            callback()
          } else {
            console.log('name invalide')
            callback(new Error(this.$t('invalidExpressError')))
          }
        } else {
          callback()
        }
      }
      const validatePayment = (rule, value, callback) => {
        if (!value) {
          callback()
        } else {
          if (this.availablePayments.some((val, index, array) => val.name === value)) {
            console.log('name valide')
            callback()
          } else {
            console.log('name invalide')
            callback(new Error(this.$t('invalidPaymentError')))
          }
        }
      }
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
        orderModel: {
          express: '',
          payment: '',
          payment_no: '',
          comment: '',
          order_no: '',
          status: ''
        },
        orderErrors: {},
        ruleOrderValidate: {
          express: [
            { validator: validateExpress, trigger: 'blur' }
          ],
          payement: [
            { validator: validatePayment, trigger: 'blur' }
          ]
        },
        orderListColumns: [
          {
            title: this.$t('orderNo'),
            key: 'order_no',
            sortable: true,
            render: (h, param) => {
              let toUrl = {name: 'order', params: {orderNo: param.row.order_no}}
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
            title: this.$t('status'),
            key: 'status',
            sortable: true,
            align: 'center',
            filters: [
              {
                label: this.$t('cart'),
                value: 'cart'
              },
              {
                label: this.$t('order'),
                value: 'order'
              },
              {
                label: this.$t('sent'),
                value: 'sent'
              },
              {
                label: this.$t('checked'),
                value: 'checked'
              }
            ],
            filterMultiple: true,
            filterMethod (value, row) {
              // 比较时注意变量类型
              return row.status === value
            },
            render: (h, params) => {
              return h('span', this.$t(params.row.status))
              // }, params.row.status)
            }
          },
          {
            title: '操作',
            key: 'action',
            render: (h, params) => {
              // let tagNames = ['nothing', 'enter', 'sent', 'checked']
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.showEdit(params.index)
                      // this.orderModel = this.orderListData[index]
                      // this.showOrderProcessModal = true
                    }
                  }
                }, this.$t('process')),
                h('Button', {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
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
        pageSize: 10,
        selectedPayment: {},
        selectedExpress: {}
      }
    },
    computed: {
      ...mapState('app', {
        'availableExpresses': state => state.availableExpresses,
        'availableDepartments': state => state.availableDepartments,
        'availablePayments': state => state.availablePayments
      }),
      aList: function () {
        // 用于autocomplete
        if (Array.isArray(this.orderListData)) {
          // 深度拷贝方法
          let tmpArray = JSON.parse(JSON.stringify(this.orderListData))
          return tmpArray.filter((item, index, array) => {
            if (item.order_no.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return array.indexOf(item) === index
            } else if (item.sum_price.toString().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else {
              return false
            }
          })
        } else {
          return []
        }
      },
      aExpress: function () {
        // 用于autocomplete
        // console.error(this.availableExpresses)
        if (Array.isArray(this.availableExpresses)) {
          // 深度拷贝方法
          let tmpArray = JSON.parse(JSON.stringify(this.availableExpresses))
          // console.error(tmpArray)
          return tmpArray.filter((item, index, array) => {
            if (item.name.toUpperCase().indexOf(this.orderModel.express.toUpperCase()) !== -1) {
              return true
            } else if (item.pinyin.toUpperCase().indexOf(this.orderModel.express.toUpperCase()) !== -1) {
              return true
            } else if (item.py.toUpperCase().indexOf(this.orderModel.express.toUpperCase()) !== -1) {
              return true
            } else {
              return false
            }
          })
        } else {
          return []
        }
      }
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
      handleRemoteSearch (pageSize, pageNumber) {
        let paras = {
          start: this.dateRange[0].getFullYear() + '-' + (this.dateRange[0].getMonth() + 1) + '-' + (this.dateRange[0].getDate() + 1),
          end: this.dateRange[1].getFullYear() + '-' + (this.dateRange[1].getMonth() + 1) + '-' + (this.dateRange[1].getDate() + 1),
          keyword: this.keyword,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        this.getOrderList(paras).then((res) => {
          let { data, status, statusText } = res
          if (status !== 200) {
            this.loginMessage = statusText
          } else {
            this.$Loading.finish()
            this.total = res.data.count
            this.tableData = data.results
          }
        }, (error) => {
          console.log('Error in getProducts: ' + error)
          this.$Message.error('获取商品列表失败!')
        }).catch((error) => {
          console.log('catched in getProducts:' + error)
          this.$Message.error('获取商品列表失败!')
        })
      },
      showEdit (index) {
        this.showOrderProcessModal = true
        // console.error(this.orderListData[index].express)
        if (this.orderListData[index].express === null) {
          this.orderListData[index].express = ''
        }
        // console.error(this.orderListData[index].express.toUpperCase())
        // console.error(this.orderListData[index].payment)
        if (this.orderListData[index].payment === null) {
          this.orderListData[index].payment = ''
        }
        // console.error(this.orderListData[index].payment.toUpperCase())
        this.orderModel = this.orderListData[index]
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
      },
      cancelProcess (name) {
        this.$Message.warning(this.$t('canceled'))
      },
      handleExpressSelected: function (value) {
        this.orderModel.express = value
        console.log(this.orderModel.express)
        let expressList = JSON.parse(JSON.stringify(this.availableExpresses))
        if (this.orderModel.express.length > 0 && expressList.length > 0) {
          let tmpExpress = expressList.filter((val, index, array) => val.name === this.orderModel.express)
          this.selectedExpress = tmpExpress[0]
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
</style>
