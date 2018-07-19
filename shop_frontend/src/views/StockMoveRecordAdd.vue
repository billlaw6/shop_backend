<template>
  <div class="stock-move-in">
    <Table ref="moveRecordList" stripe :columns="moveRecordListColumns" :data="moveRecordList">
      <div class="table-header" slot="header">
        已添加商品
      </div>
      <div class="table-footer" slot="footer">
        共计: <span>{{ total }}</span> 订单，合计: <span></span>
      </div>
    </Table>

    <Form ref="formInline" :model="formInline" :rules="ruleInline" inline>
      <FormItem :label="$t('product')" prop="productInfo">
        <AutoComplete v-model="formInline.productInfo"
          :placeholder="$t('selectProduct')"
          icon="ios-search" 
          :clearable="true"
          @on-select="handleProductSelected">
          <Option v-for="option in aProduct" :value="option.name" :key="option.id">
            <span class="product-name">{{ option.name }}</span>
            <span class="product-price">{{ option.sale_price | currency }}</span>
          </Option>
        </AutoComplete>
        <ul v-if="formInlineErrors.productInfo" v-for="error in formInlineErrors.productInfo">
          <li class="error">{{ error }}</li>
        </ul>
      </FormItem>
      <FormItem :label="$t('moveAmount')" prop="move_amount">
        <InputNumber :max="10000" :min="0.1" :step="0.1" v-model="formInline.move_amount"></InputNumber>
        <ul v-if="formInlineErrors.move_amount" v-for="error in formInlineErrors.move_amount">
          <li class="error">{{ error }}</li>
        </ul>
      </FormItem>
      <FormItem :label="$t('batchNo')" prop="batch_no">
        <Input v-model="formInline.batch_no"></Input>
        <ul v-if="formInlineErrors.batch_no" v-for="error in formInlineErrors.batch_no">
          <li class="error">{{ error }}</li>
        </ul>
      </FormItem>
      <FormItem :label="$t('comment')" prop="comment">
        <Input v-model="formInline.comment" type="text"></Input>
        <ul v-if="formInlineErrors.comment" v-for="error in formInlineErrors.comment">
          <li class="error">{{ error }}</li>
        </ul>
      </FormItem>
      <Form-item>
        <br/>
        <Button type="primary" size="small" @click="addToList()">{{ $t('addToList') }}</Button>
      </Form-item>
    </Form>

    <Form ref="formInlineSubmit" :model="formInlineSubmit" :rules="ruleInlineSubmit" inline>
      <Tabs>
        <TabPane v-if="currentDepartment.level===1" :label="$t('moveIn')" icon="">
          <Form-item>
            <br/>
            <Button type="primary" size="large" @click="submitMoveIn()">{{ $t('submitMoveIn') }}</Button>
          </Form-item>
        </TabPane>
        <TabPane :label="$t('moveOut')" icon="">
          <FormItem :label="$t('toDepartment')" prop="toDepartment">
            <AutoComplete v-model="formInlineSubmit.toDept"
              :placeholder="$t('selectToDept')"
              icon="ios-search" 
              :clearable="true"
              @on-select="handleToDeptSelected">
              <Option v-for="option in otherDepartments" :value="option.name" :key="option.code">
                <span class="product-name">{{ option.name }}</span>
              </Option>
            </AutoComplete>
          </FormItem>
          <Form-item>
            <br/>
            <Button type="primary" size="large" @click="submitMoveOut()">{{ $t('submitMoveOut') }}</Button>
          </Form-item>
        </TabPane>
      </Tabs>
    </Form>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex'
  import { addMoveRecord } from '@/http/api'

  export default{
    components: {
    },
    data: function () {
      const validateProductName = (rule, value, callback) => {
        if (!value) {
          callback(new Error(this.$t('noProductError')))
        } else {
          if (this.availableProducts.filter((val, index, array) => val.name === value).length > 0) {
            callback()
          } else {
            callback(new Error(this.$t('invalidProductError')))
          }
        }
      }
      const validateToDepartmentName = (rule, value, callback) => {
        if (!value) {
          callback(new Error(this.$t('noDepartmentError')))
        } else {
          if (this.otherDepartments.filter((val, index, array) => val.name === value).length > 0) {
            callback()
          } else {
            callback(new Error(this.$t('invalidDepartmentError')))
          }
        }
      }
      const validateMoveAmount = (rule, value, callback) => {
        if (!value) {
          callback(new Error(this.$t('noMoveAmountError')))
        } else {
          if (value >= 0.1 && value < 1000) {
            callback()
          } else {
            callback(new Error(this.$t('invalidMoveAmountError')))
          }
        }
      }
      return {
        selectedProduct: null,
        selectedToDept: null,
        ruleInline: {
          productInfo: [
            { validator: validateProductName, trigger: 'blur' },
            { required: true, message: this.$t('invalidProduct'), trigger: 'blur' }
          ],
          move_amount: [
            // 此两项合并使用时输入了数字也报空
            // { type: 'number', message: this.$t('invalideNumber'), trigger: 'blur' },
            // { required: true, message: this.$t('invalidmove_amount'), trigger: 'blur' }
            // 建议解决方案：Input设为text型，判断空使用系统自带的，判断数字自定义方法。
            { validator: validateMoveAmount, trigger: 'blur' }
          ]
        },
        ruleInlineSubmit: {
          toDept: [
            { validator: validateToDepartmentName, trigger: 'blur' }
          ]
        },
        formInline: {
          productInfo: '',
          move_amount: 0.0,
          batch_no: '',
          comment: ''
        },
        formInlineErrors: {},
        formInlineSubmit: {
          toDept: ''
        },
        loadingProduct: false,
        moveRecordListColumns: [
          {
            title: this.$t('product'),
            key: 'product.name',
            sortable: true,
            render: (h, params) => {
              return h('span', params.row.product.name)
            }
          },
          {
            title: this.$t('salePrice'),
            key: 'sale_price',
            sortable: true,
            render: (h, params) => {
              return h('span', parseFloat(params.row.product.sale_price).toFixed(this.decimals))
            }
          },
          {
            title: this.$t('moveAmount'),
            key: 'move_amount',
            sortable: true,
            render: (h, params) => {
              return h('span', params.row.moveAmount.toFixed(this.decimals))
            }
          },
          {
            title: this.$t('batchNo'),
            key: 'batch_no',
            sortable: true
          },
          {
            title: '操作',
            key: 'action',
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.removeFromList(params.index)
                  }
                }
              }, this.$t('remove'))
            }
          }
        ]
      }
    },
    computed: {
      ...mapState('app', {
        availableProducts: state => state.availableProducts,
        availableDepartments: state => state.availableDepartments
      }),
      ...mapState('login', {
        currentDepartment: state => state.currentDepartment
      }),
      ...mapState('stock', {
        moveRecordList: state => state.moveRecordList,
        decimals: state => state.decimals
      }),
      ...mapGetters('stock', [
        'moveRecordListCount',
        'moveRecordListSum'
      ]),
      otherDepartments: function () {
        // console.log(this.availableDepartments)
        // console.log(this.currentDepartment)
        if (this.availableDepartments.length > 0 && this.currentDepartment) {
          return this.availableDepartments.filter((item, index, array) => {
            if (this.currentDepartment.code === item.code) {
              return false
            } else {
              if (this.formInlineSubmit.toDept) {
                if (item.name.toUpperCase().indexOf(this.formInlineSubmit.toDept.toUpperCase()) !== -1) {
                  return true
                } else if (item.pinyin.toUpperCase().indexOf(this.formInlineSubmit.toDept.toUpperCase()) !== -1) {
                  return true
                } else if (item.py.toUpperCase().indexOf(this.formInlineSubmit.toDept.toUpperCase()) !== -1) {
                  return true
                } else {
                  return false
                }
              } else {
                return true
              }
            }
          })
        } else {
          return this.availableDepartments
        }
      },
      total: function () {
        return this.moveRecordList.length
      },
      aProduct: function () {
        return this.availableProducts.filter((item, index, array) => {
          if (this.formInline.productInfo) {
            if (item.name.toUpperCase().indexOf(this.formInline.productInfo.toUpperCase()) !== -1) {
              return true
            } else if (item.sale_price.toString().indexOf(this.formInline.productInfo.toUpperCase()) !== -1) {
              return true
            } else if (item.pinyin.toUpperCase().indexOf(this.formInline.productInfo.toUpperCase()) !== -1) {
              return true
            } else if (item.py.toUpperCase().indexOf(this.formInline.productInfo.toUpperCase()) !== -1) {
              return true
            } else {
              return false
            }
          } else {
            return true
          }
        })
      }
    },
    methods: {
      ...mapActions('app', {
        setProducts: 'setProducts',
        setCurrentDepartment: 'setCurrentDepartment'
      }),
      ...mapActions('stock', {
        addMoveRecordItem: 'addMoveRecordItem',
        removeMoveRecordItem: 'removeMoveRecordItem',
        emptyMoveRecord: 'emptyMoveRecord',
        setMoveRecordList: 'setMoveRecordList'
      }),
      handleProductSelected: function (value) {
        this.formInline.productInfo = value
        if (value) {
          if (this.formInline.productInfo.length > 0 && this.availableProducts.length > 0) {
            let tmpProduct = this.availableProducts.filter((val, index, array) => val.name === this.formInline.productInfo)
            this.selectedProduct = tmpProduct[0]
          } else {
            this.$Message.error('invalideProduct')
          }
        }
      },
      addToList: function () {
        this.$refs['formInline'].validate((valid) => {
          if (valid) {
            // 参数名对应不上时会直接不执行
            this.$store.dispatch('stock/addMoveRecordItem',
              { item: this.selectedProduct,
                moveAmount: this.formInline.move_amount,
                batchNo: this.formInline.batch_no,
                comment: this.formInline.comment
              })
          } else {
            this.$Message.error(this.$t('validateFailed'))
          }
        })
      },
      removeFromList: function (index) {
        this.removeMoveRecordItem(this.moveRecordList[index])
      },
      handleToDeptSelected: function (value) {
        this.formInlineSubmit.toDept = value
        if (value) {
          if (this.formInlineSubmit.toDept.length > 0 && this.otherDepartments.length > 0) {
            let tmpDepartment = this.otherDepartments.filter((val, index, array) => val.name === this.formInlineSubmit.toDept)
            this.selectedToDept = tmpDepartment[0]
          } else {
            this.$Message.error('invalideToDept')
          }
        }
      },
      submitMoveIn: function () {
        if (this.currentDepartment && this.moveRecordList.length > 0) {
          let params = {
            deptIn: this.currentDepartment,
            moveRecordList: this.moveRecordList
          }
          addMoveRecord(params).then((res) => {
            // let { status, data, statusText } = res
            let { status } = res
            if (status === 201) {
              // console.log(data)
              // console.log(statusText)
              this.$Message.success(this.$t('submitSucceed'))
              this.emptyMoveRecord()
            } else {
              this.$Message.error(this.$t('failed'))
            }
          })
        } else {
          this.$Message.error(this.$t('请先录入商品'))
        }
      },
      submitMoveOut: function () {
        if (this.currentDepartment && this.moveRecordList.length > 0) {
          let params = {
            deptOut: this.currentDepartment,
            deptIn: this.selectedToDept,
            moveRecordList: this.moveRecordList
          }
          addMoveRecord(params).then((res) => {
            // let { status, data, statusText } = res
            let { status } = res
            if (status === 201) {
              // console.log(data)
              // console.log(statusText)
              this.$Message.success(this.$t('submitSucceed'))
              this.emptyMoveRecord()
            } else {
              this.$Message.error(this.$t('failed'))
            }
          })
        } else {
          this.$Message.error(this.$t('请先录入商品'))
        }
      }
    },
    mounted () {
      // this.emptyMoveRecord()
    }
  }
</script>

<style lang="stylus" scoped>
  @import '../common/vars'
  .stock-move-in
    margin: 6px
</style>
