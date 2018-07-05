<template>
  <div class="stockMoveRecord-manage">
    <!-- 已添加列表 -->
    <div class="move-record-items">
      <move-record-items>
      </move-record-items>
    </div>

    <!-- 录入框 -->
    <div class="cart-enter">
      <Form ref="addModelForm" :model="addModel" :rules="ruleAddValidate"  label-position="left" inline>
        <Form-item :label="$t('product')" prop="name">
          <AutoComplete v-model="addModel.name" :placeholder="$t('selectProduct')" icon="ios-search" 
            :clearable="true"
            @on-select="handleProductSelected"
          >
            <Option v-for="option in aList" :value="option.name" :key="option.id">
              <span class="product-name">{{ option.name }}</span>
              <span class="product-price">{{ option.sale_price | currency }}</span>
            </Option>
          </AutoComplete>
          <ul v-for="error in addModelErrors.name">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('amount')" prop="amount">
          <InputNumber :max="10000" :min="0.0" :step="0.1" v-model="addModel.amount"></InputNumber>
          <ul v-for="error in addModelErrors.amount">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('comment')" prop="comment">
          <Input v-model="addModel.comment" type="text"></Input>
          <ul v-for="error in addModelErrors.comment">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item>
          <br/>
          <Button type="primary" @click="addToCart()">{{ $t('addToCart') }}</Button>
        </Form-item>
      </Form>
      <br/>
    </div>

    <div class="stockMoveRecord-info">
      <Form ref="submitOrderForm" :model="stockMoveRecordModel" :rules="ruleOrderValidate"  label-position="left" inline>
        <Form-item :label="$t('dept_in')" prop="dept_in">
          <Select v-model="stockMoveRecordModel.dept_in">
            <Option v-for="option in otherDepartments" :value="option.code" :key="option.code">{{ option.name }}</Option>
          </Select>
          <ul v-for="error in stockMoveRecordErrors.dept_in">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('comment')" prop="comment">
          <Input v-model="stockMoveRecordModel.comment" type="text"></Input>
          <ul v-for="error in stockMoveRecordErrors.comment">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item>
          <br/>
          <Button type="primary" size="large" @click="submitMoveRecord"><Icon type="ios-download-outline"></Icon>{{ $t('submitMoveRecord') }}</Button>
        </Form-item>
      </Form>
    </div>
  </div>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  import { getProducts, getCustomers, getExpresses, getPayments, addOrder } from '@/http/api'
  import MoveRecordItems from '@/views/components/stock/MoveRecordItems.vue'

  export default {
    components: {
      'move-record-items': MoveRecordItems
    },
    data: function () {
      const validateProductName = (rule, value, callback) => {
        // console.log(value)
        if (!value) {
          callback(new Error(this.$t('noProductError')))
        } else {
          if (this.availableProducts.some((val, index, array) => val.name === value)) {
            console.log('name valide')
            callback()
          } else {
            console.log('name valide')
            callback(new Error(this.$t('invalidProductError')))
          }
        }
      }
      const validateAmount = (rule, value, callback) => {
        console.log(value)
        if (!value) {
          callback(new Error(this.$t('noAmountError')))
        } else {
          if (value === 0) {
            callback(new Error(this.$t('invalidAmountError')))
          } else {
            callback()
          }
        }
      }
      const validateCustomer = (rule, value, callback) => {
        console.log(value)
        if (!value) {
          callback(new Error(this.$t('noCustomerError')))
        } else {
          if (this.availableCustomers.some((val, index, array) => val.username === value)) {
            console.log('name valide')
            callback()
          } else {
            console.log('name invalide')
            callback(new Error(this.$t('invalidCustomerError')))
          }
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
        addModel: {
          name: '',
          amount: 0,
          comment: ''
        },
        ruleAddValidate: {
          name: [
            { validator: validateProductName, trigger: 'blur' }
          ],
          amount: [
            { validator: validateAmount, trigger: 'blur' }
          ]
        },
        addModelErrors: {},
        stockMoveRecordModel: {
          dept_in: '',
          customer: '',
          payment: '',
          express: '',
          express_no: ''
        },
        ruleOrderValidate: {
          customer: [
            { validator: validateCustomer, trigger: 'blur' }
          ],
          payment: [
            { validator: validatePayment, trigger: 'blur' }
          ]
        },
        stockMoveRecordErrors: {},
        addedProducts: [],
        total: 0,
        pageNumber: 1,
        pageSize: 100000,
        tableColumns: [
          {
            title: '名称',
            key: 'product.name',
            align: 'center',
            sortable: true
          },
          {
            title: '价格',
            key: 'sale_price',
            align: 'left',
            sortable: true,
            render: (h, params) => {
              return h(
                'span',
                params.row.sale_price
              )
            }
          },
          {
            title: '数量',
            key: 'amount',
            align: 'center',
            sortable: true,
            render: (h, params) => {
              return h('span', {
              }, Number(params.row.amount).toFixed(this.decimals))
            }
          },
          {
            title: '小计',
            key: 'itemSum',
            align: 'left',
            sortable: true,
            render: (h, params) => {
              return h('span', {
                props: {
                  color: 'red'
                }
              }, params.row.sale_price * params.row.amount)
            }
          },
          {
            title: '备注',
            key: 'comment',
            align: 'left',
            sortable: true
          },
          {
            title: '操作',
            key: 'action',
            width: 150,
            align: 'center',
            render: (h, params) => {
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
                    }
                  }
                }, '编辑'),
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
                      this.showDelete(params.index)
                    }
                  }
                }, '开/关')
              ])
            }
          }
        ]
      }
    },
    computed: {
      ...mapState('app', {
        'maxSize': state => state.maxSize,
        'availableExpresses': state => state.availableExpresses,
        'availableDepartments': state => state.availableDepartments,
        'availablePayments': state => state.availablePayemnts
      }),
      ...mapState('cart', {
        'cartList': state => state.cartList,
        'decimals': state => state.decimals
      }),
      ...mapGetters('cart', [
        'cartListCount',
        'cartListSum'
      ]),
      aList: function () {
        // 用于autocomplete
        if (Array.isArray(this.availableProducts)) {
          // 深度拷贝方法
          let tmpArray = JSON.parse(JSON.stringify(this.availableProducts))
          return tmpArray.filter((item, index, array) => {
            if (item.name.toUpperCase().indexOf(this.addModel.name.toUpperCase()) !== -1) {
              // return array.indexOf(item) === index
              return true
            } else if (item.price.toString().indexOf(this.addModel.name.toUpperCase()) !== -1) {
              return true
            } else if (item.pinyin.toUpperCase().indexOf(this.addModel.name.toUpperCase()) !== -1) {
              return true
            } else if (item.py.toUpperCase().indexOf(this.addModel.name.toUpperCase()) !== -1) {
              return true
            } else {
              return false
            }
          })
        } else {
          return []
        }
      },
      aCustomer: function () {
        // 用于autocomplete
        if (Array.isArray(this.availableCustomers)) {
          // 深度拷贝方法
          let tmpArray = JSON.parse(JSON.stringify(this.availableCustomers))
          return tmpArray.filter((item, index, array) => {
            if (item.username.toUpperCase().indexOf(this.stockMoveRecordModel.customer.toUpperCase()) !== -1) {
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
        if (Array.isArray(this.availableExpresses)) {
          // 深度拷贝方法
          let tmpArray = JSON.parse(JSON.stringify(this.availableExpresses))
          return tmpArray.filter((item, index, array) => {
            if (item.name.toUpperCase().indexOf(this.stockMoveRecordModel.express.toUpperCase()) !== -1) {
              return true
            } else if (item.pinyin.toUpperCase().indexOf(this.stockMoveRecordModel.express.toUpperCase()) !== -1) {
              return true
            } else if (item.py.toUpperCase().indexOf(this.stockMoveRecordModel.express.toUpperCase()) !== -1) {
              return true
            } else {
              return false
            }
          })
        } else {
          return []
        }
      },
      aPayment: function () {
        // 用于autocomplete
        if (Array.isArray(this.availablePayments)) {
          // 深度拷贝方法
          let tmpArray = JSON.parse(JSON.stringify(this.availablePayments))
          return tmpArray.filter((item, index, array) => {
            if (item.name.toUpperCase().indexOf(this.stockMoveRecordModel.payment.toUpperCase()) !== -1) {
              // return array.indexOf(item) === index
              return true
            } else if (item.pinyin.toUpperCase().indexOf(this.stockMoveRecordModel.payment.toUpperCase()) !== -1) {
              return true
            } else if (item.py.toUpperCase().indexOf(this.stockMoveRecordModel.payment.toUpperCase()) !== -1) {
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
      // 获取商品列表
      getProduct: function (pageSize, pageNumber) {
        let paras = {
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        getProducts(paras).then((res) => {
          let { data, status, statusText } = res
          if (status !== 200) {
            this.loginMessage = statusText
          } else {
            this.total = res.data.count
            this.availableProducts = data.results
          }
        }, (error) => {
          console.log('Error in getProducts: ' + error)
          this.$Message.error('获取商品列表失败!')
        }).catch((error) => {
          console.log('catched in getProducts:' + error)
          this.$Message.error('获取商品列表失败!')
        })
        this.loadingStatus = false
      },
      // 获取顾客列表
      getCustomer: function (pageSize, pageNumber) {
        let paras = {
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        getCustomers(paras).then((res) => {
          let { data, status, statusText } = res
          if (status !== 200) {
            this.loginMessage = statusText
          } else {
            this.total = res.data.count
            this.availableCustomers = data.results
          }
        }, (error) => {
          this.$Message.error(error)
        }).catch((error) => {
          this.$Message.error(error)
        })
        this.loadingStatus = false
      },
      // 获取快递列表
      getExpress: function (pageSize, pageNumber) {
        let paras = {
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        getExpresses(paras).then((res) => {
          let { data, status, statusText } = res
          if (status !== 200) {
            this.loginMessage = statusText
          } else {
            this.total = res.data.count
            this.availableExpresses = data.results
          }
        }, (error) => {
          this.$Message.error(error)
        }).catch((error) => {
          this.$Message.error(error)
        })
        this.loadingStatus = false
      },
      getPayment: function (pageSize, pageNumber) {
        let paras = {
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        getPayments(paras).then((res) => {
          let { data, status, statusText } = res
          if (status !== 200) {
            this.loginMessage = statusText
          } else {
            this.total = res.data.count
            this.availablePayments = data.results
          }
        }, (error) => {
          this.$Message.error(error)
        }).catch((error) => {
          this.$Message.error(error)
        })
        this.loadingStatus = false
      },
      handleProductSelected: function (value) {
        this.addModel.name = value
        console.log(this.availableProducts)
        let productList = JSON.parse(JSON.stringify(this.availableProducts))
        if (this.addModel.name.length > 0 && productList.length > 0) {
          let tmpProduct = productList.filter((val, index, array) => val.name === this.addModel.name)
          this.selectedProduct = tmpProduct[0]
        }
      },
      handleCustomerSelected: function (value) {
        if (value) {
          this.stockMoveRecordModel.customer = value
        }
        console.log(this.stockMoveRecordModel.customer)
        console.log(this.availableCustomers)
        let customerList = JSON.parse(JSON.stringify(this.availableCustomers))
        console.log(customerList)
        if (this.stockMoveRecordModel.customer.length > 0 && customerList.length > 0) {
          let tmpCustomer = customerList.filter((val, index, array) => val.username === this.stockMoveRecordModel.customer)
          this.selectedCustomer = tmpCustomer[0]
        }
      },
      handleExpressSelected: function (value) {
        this.stockMoveRecordModel.express = value
        console.log(this.stockMoveRecordModel.express)
        let expressList = JSON.parse(JSON.stringify(this.availableExpresses))
        if (this.stockMoveRecordModel.express.length > 0 && expressList.length > 0) {
          let tmpExpress = expressList.filter((val, index, array) => val.name === this.stockMoveRecordModel.express)
          this.selectedExpress = tmpExpress[0]
        }
      },
      handlePaymentSelected: function (value) {
        this.stockMoveRecordModel.payment = value
        console.log(this.stockMoveRecordModel.payment)
        let paymentList = JSON.parse(JSON.stringify(this.availablePayments))
        if (this.stockMoveRecordModel.payment.length > 0 && paymentList.length > 0) {
          let tmpPayment = paymentList.filter((val, index, array) => val.name === this.stockMoveRecordModel.payment)
          this.selectedPayment = tmpPayment[0]
        }
      },
      addToCart: function () {
        this.$refs['addModelForm'].validate((valid) => {
          console.log('addToCart validating')
          if (valid) {
            console.log('valid')
            this.$store.dispatch('cart/addCartItem', {'item': this.selectedProduct, 'amount': this.addModel.amount, 'comment': this.addModel.comment})
            this.$Message.success({
              title: '加入购物车成功',
              content: '加入购物车成功'
            })
          } else {
            console.log('invalid')
            this.$Message.error('Fail!')
          }
        })
      },
      submitOrder: function () {
        console.log('submitting')
        this.$refs['submitOrderForm'].validate((valid) => {
          console.log('submit Order validating')
          console.log(valid)
          if (valid) {
            let params = {
              customer: this.selectedCustomer,
              payment: this.selectedPayment,
              cartList: this.cartList,
              cartListCount: this.cartListCount,
              cartListSum: this.cartListSum.toFixed(this.decimals),
              express: this.selectedExpress,
              express_no: this.stockMoveRecordModel.express_no
            }
            addOrder(params).then((res) => {
              let { data, status, statusText } = res
              if (status !== 201) {
                console.log('submit stockMoveRecord fail:' + statusText)
              } else {
                this.total = res.data.count
                this.availableExpresses = data.results
              }
            }, (error) => {
              this.$Message.error(error)
            }).catch((error) => {
              this.$Message.error(error)
            })
          } else {
            console.log('invalid')
            this.$Message.error('Fail!')
          }
        })
      }
    },
    mounted () {
      this.getProduct(this.pageSize, this.pageNumber)
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus" scoped>
  @import '../common/vars'

  .move-record-items
    margin: 4px
  .cart-enter
    margin: 4px
  .stockMoveRecord-info
    margin: 4px
</style>