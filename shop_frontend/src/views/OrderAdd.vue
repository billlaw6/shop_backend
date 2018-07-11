<template>
  <div class="order-manage">
    <!-- 已添加列表 -->
    <div class="cart-items">
      <cart-items>
      </cart-items>
    </div>

    <!-- 录入框 -->
    <div class="cart-enter">
      <Form ref="addModelForm" :model="addModel" :rules="ruleAddValidate"  label-position="left" inline>
        <Form-item :label="$t('product')" prop="name">
          <AutoComplete v-model="addModel.name" :placeholder="$t('selectProduct')" icon="ios-search" 
            :clearable="true"
            @on-select="handleProductSelected">
            <Option v-for="option in aProduct" :value="option.product.name" :key="option.id">
              <span class="product-name">{{ option.product.name }}</span>
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

    <div class="order-info">
      <Form ref="submitOrderForm" :model="orderModel" :rules="ruleOrderValidate"  label-position="left" inline>
        <Form-item :label="$t('customer')" prop="customer">
          <AutoComplete v-model="orderModel.customer" :placeholder="$t('selectCustomer')" icon="ios-search" 
            :clearable="true"
            @on-select="handleCustomerSelected"
          >
            <Option v-for="option in aCustomer" :value="option.username" :key="option.id">
              <span class="product-name">{{ option.username }}</span>
              <span class="product-price">{{ option.last_name }}</span>
              <span class="product-price">{{ option.first_name }}</span>
            </Option>
          </AutoComplete>
          <ul v-for="error in orderErrors.customer">
            <li class="error">{{ error }}</li>
          </ul>
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
        <Form-item style="display: none" prop="cartListLength">
          <InputNumber v-model="orderModel.cartListLength" type="text"></InputNumber>
        </Form-item>
        <Form-item>
          <br/>
          <Button type="primary" size="large" @click="submitOrder"><Icon type="ios-download-outline"></Icon>{{ $t('submitOrder') }}</Button>
        </Form-item>
      </Form>
    </div>
  </div>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  import { searchStocks, getCustomers, getExpresses, getPayments, addOrder } from '@/http/api'
  import CartItems from '@/views/components/cart/CartItems.vue'

  export default {
    components: {
      'cart-items': CartItems
    },
    data: function () {
      const validateProductName = (rule, value, callback) => {
        if (!value) {
          callback(new Error(this.$t('noProductError')))
        } else {
          if (this.availableProducts.filter((val, index, array) => val.product.name === value).length > 0) {
            callback()
          } else {
            callback(new Error(this.$t('invalidProductError')))
          }
        }
      }
      const validateAmount = (rule, value, callback) => {
        // console.log(value)
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
        // console.log(value)
        if (!value) {
          callback(new Error(this.$t('noCustomerError')))
        } else {
          if (this.availableCustomers.some((val, index, array) => val.username === value)) {
            // console.log('name valide')
            callback()
          } else {
            // console.log('name invalide')
            callback(new Error(this.$t('invalidCustomerError')))
          }
        }
      }
      const validatePayment = (rule, value, callback) => {
        if (!value) {
          callback()
        } else {
          if (this.availablePayments.some((val, index, array) => val.name === value)) {
            // console.log('name valide')
            callback()
          } else {
            // console.log('name invalide')
            callback(new Error(this.$t('invalidPaymentError')))
          }
        }
      }
      const validateCartListLength = (rule, value, callback) => {
        if (this.cartList.length === 0) {
          callback(new Error(this.$t('invalidCartListLengthError')))
        }
      }
      return {
        availableProducts: [],
        selectedProduct: null,
        availableCustomers: [],
        availablePayments: [],
        availableExpresses: [],
        selectedCustomer: null,
        addModel: {
          name: '', // 绑定以后没有选项时会被赋值成undefined
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
        orderModel: {
          customer: '',
          payment: '',
          express: '',
          express_no: '',
          cartListLength: 0
        },
        ruleOrderValidate: {
          customer: [
            { validator: validateCustomer, trigger: 'blur' }
          ],
          payment: [
            { validator: validatePayment, trigger: 'blur' }
          ],
          cartListLength: [
            { validator: validateCartListLength, trigger: 'blur' }
            // { type: 'number', message: this.$t('invalideNumber'), trigger: 'blur' },
            // { min: 1, message: this.$t('invalideNumber'), trigger: 'blur' }
          ]
        },
        orderErrors: {},
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
              }, (Number(params.row.sale_price) * Number(params.row.amount)).foFixed(this.decimals))
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
        'currentDepartment': state => state.currentDepartment
        // 'availableDepartments': state => state.availableDepartments,
        // 'availablePayments': state => state.availablePayemnts
      }),
      ...mapState('login', {
        'currentDepartment': state => state.currentDepartment
      }),
      ...mapState('cart', {
        'cartList': state => state.cartList,
        'decimals': state => state.decimals
      }),
      ...mapGetters('cart', [
        'cartListCount',
        'cartListSum'
      ]),
      aProduct: function () {
        // filter, concat, slice方法会生成亲的数组
        // 手工敲入的字母会被赋值给addModel.name
        // console.log('aProduct')
        // 使用删除修改选择的内容时会触发两次aProduc计算，
        // 一次addModel.name值为undefined，一次为空字符串
        // console.log(this.addModel.name)
        return this.availableProducts.filter((item, index, array) => {
          if (this.addModel.name) {
            if (item.product.name.toUpperCase().indexOf(this.addModel.name.toUpperCase()) !== -1) {
              return true
            } else if (item.product.sale_price.toString().indexOf(this.addModel.name.toUpperCase()) !== -1) {
              return true
            } else if (item.product.pinyin.toUpperCase().indexOf(this.addModel.name.toUpperCase()) !== -1) {
              return true
            } else if (item.product.py.toUpperCase().indexOf(this.addModel.name.toUpperCase()) !== -1) {
              return true
            } else {
              return false
            }
          } else {
            return true
          }
        })
      },
      aCustomer: function () {
        // 用于autocomplete
        if (Array.isArray(this.availableCustomers)) {
          // 深度拷贝方法
          return this.availableCustomers.filter((item, index, array) => {
            // 删除选择项内容时，对应的值会被赋值成undefined
            if (this.addModel.customer) {
              if (item.username.toUpperCase().indexOf(this.orderModel.customer.toUpperCase()) !== -1) {
                return true
              } else {
                return false
              }
            } else {
              return true
            }
          })
        } else {
          return this.availableCustomers
        }
      },
      aExpress: function () {
        // 用于autocomplete
        if (Array.isArray(this.availableExpresses)) {
          // filter不修改原array
          return this.availableExpresses.filter((item, index, array) => {
            if (this.addModel.express) {
              if (item.name.toUpperCase().indexOf(this.orderModel.express.toUpperCase()) !== -1) {
                return true
              } else if (item.pinyin.toUpperCase().indexOf(this.orderModel.express.toUpperCase()) !== -1) {
                return true
              } else if (item.py.toUpperCase().indexOf(this.orderModel.express.toUpperCase()) !== -1) {
                return true
              } else {
                return false
              }
            } else {
              return true
            }
          })
        } else {
          return this.availableExpresses
        }
      },
      aPayment: function () {
        // 用于autocomplete
        if (Array.isArray(this.availablePayments)) {
          // 深度拷贝方法
          return this.availablePayments.filter((item, index, array) => {
            if (this.orderModel.payment) {
              if (item.name.toUpperCase().indexOf(this.orderModel.payment.toUpperCase()) !== -1) {
                return true
              } else if (item.pinyin.toUpperCase().indexOf(this.orderModel.payment.toUpperCase()) !== -1) {
                return true
              } else if (item.py.toUpperCase().indexOf(this.orderModel.payment.toUpperCase()) !== -1) {
                return true
              } else {
                return false
              }
            } else {
              return true
            }
          })
        } else {
          return this.availablePayments
        }
      }
    },
    watch: {
      currentDepartment () {
        this.getStockData(this.pageSize, this.pageNumber)
      }
    },
    methods: {
      // 获取商品列表
      getStockData: function (pageSize, pageNumber) {
        let paras = {
          department: this.currentDepartment.code,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        searchStocks(paras).then((res) => {
          let { data, status, statusText } = res
          if (status !== 200) {
            this.loginMessage = statusText
          } else {
            // console.log(data)
            this.total = res.data.count
            this.availableProducts = data.results
          }
        }, (error) => {
          console.log('Error in getStockDatas: ' + error)
          this.$Message.error('获取商品列表失败!')
        }).catch((error) => {
          console.log('catched in getStockDatas:' + error)
          this.$Message.error('获取商品列表失败!')
        })
        this.loadingStatus = false
      },
      // 获取顾客列表
      getCustomerData: function (pageSize, pageNumber) {
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
      getExpressData: function (pageSize, pageNumber) {
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
      getPaymentData: function (pageSize, pageNumber) {
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
        // console.log('handleProductSelected')
        this.addModel.name = value
        if (value) {
          if (this.addModel.name.length > 0 && this.availableProducts.length > 0) {
            let tmpProduct = this.availableProducts.filter((val, index, array) => val.product.name === this.addModel.name)
            this.selectedProduct = tmpProduct[0].product
          } else {
            this.$Message.error('invalideProduct')
          }
        }
      },
      handleCustomerSelected: function (value) {
        this.orderModel.customer = value
        if (value) {
          if (this.orderModel.customer.length > 0 && this.availableCustomers.length > 0) {
            let tmpCustomer = this.availableCustomers.filter((val, index, array) => val.username === this.orderModel.customer)
            this.selectedCustomer = tmpCustomer[0]
          } else {
            this.$Message.error('invalideCustomer')
          }
        }
      },
      handleExpressSelected: function (value) {
        this.orderModel.express = value
        if (value) {
          if (this.orderModel.express.length > 0 && this.availableExpresses.length > 0) {
            let tmpExpress = this.availableExpresses.filter((val, index, array) => val.name === this.orderModel.express)
            this.selectedExpress = tmpExpress[0]
          } else {
            this.$Message.error('invalideExpresses')
          }
        }
      },
      handlePaymentSelected: function (value) {
        this.orderModel.payment = value
        if (value) {
          if (this.orderModel.payment.length > 0 && this.availablePayments.length > 0) {
            let tmpPayment = this.availablePayments.filter((val, index, array) => val.name === this.orderModel.payment)
            this.selectedPayment = tmpPayment[0]
          } else {
            this.$Message.error('invalidePayment')
          }
        }
      },
      addToCart: function () {
        this.$refs['addModelForm'].validate((valid) => {
          // console.log('addToCart validating')
          if (valid) {
            // console.log('valid')
            this.$store.dispatch('cart/addCartItem', {'item': this.selectedProduct, 'amount': this.addModel.amount, 'comment': this.addModel.comment})
            this.$Message.success({
              title: '加入购物车成功',
              content: '加入购物车成功'
            })
          } else {
            console.log('invalid')
            this.$Message.error(this.$t('invalideOrder'))
          }
        })
      },
      submitOrder: function () {
        // console.log('submitting')
        this.$refs['submitOrderForm'].validate((valid) => {
          // console.log('submit Order validating')
          // console.log(valid)
          if (valid) {
            let params = {
              customer: this.selectedCustomer,
              payment: this.selectedPayment,
              cartList: this.cartList,
              cartListCount: this.cartListCount,
              cartListSum: this.cartListSum.toFixed(this.decimals),
              express: this.selectedExpress,
              express_no: this.orderModel.express_no
            }
            addOrder(params).then((res) => {
              let { data, status, statusText } = res
              if (status !== 201) {
                console.log('submit order fail:' + statusText)
              } else {
                // console.log(data)
                let message = data.order_no.substring(0, 4) + this.$t('orderAddedSucceed')
                this.$Message.success({
                  title: this.$t('orderAddedSucceed'),
                  content: message
                })
                this.$store.dispatch('cart/emptyCart')
              }
            }, (error) => {
              this.$Message.error(error)
            }).catch((error) => {
              this.$Message.error(error)
            })
          } else {
            // console.log('invalid')
            this.$Message.error(this.$t('invalideOrder'))
          }
        })
      }
    },
    mounted () {
      this.getStockData(this.pageSize, this.pageNumber)
      this.getCustomerData(this.pageSize, this.pageNumber)
      this.getExpressData(this.pageSize, this.pageNumber)
      this.getPaymentData(this.pageSize, this.pageNumber)
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus" scoped>
  @import '../common/vars'

  .cart-items
    margin: 4px
  .cart-enter
    margin: 4px
  .order-info
    margin: 4px
</style>
