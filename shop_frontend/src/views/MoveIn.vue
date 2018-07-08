<template>
  <div>
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
        <Select 
          v-model="formInline.productInfo"
          filterable
          clearable
          >
          <!-- Select自带的filter过滤的是value值 -->
          <Option v-for="(option, index) in availableProducts"
            :value="option.id+'|'+option.name+'|'+option.py+'|'+option.sale_price"
            :key="index">
            <span>{{ option.name }}</span>
            <span style="margin-left: 5px; color:red">{{ option.sale_price | currency}}</span>
          </Option>
        </Select>
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
    <Form>
      <Form-item>
        <br/>
        <Button type="primary" size="small" @click="submitMoveRecord()">{{ $t('submitMoveRecord') }}</Button>
      </Form-item>
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
      return {
        ruleInline: {
          productInfo: [
            { required: true, message: this.$t('invalidProduct'), trigger: 'blur' }
          ]
          // move_amount: [
          //   { required: true, message: this.$t('invalidmove_amount'), trigger: 'blur' }
          // ]
        },
        formInline: {
          productInfo: '',
          move_amount: 0.1,
          batch_no: '',
          comment: ''
        },
        formInlineErrors: {},
        loadingProduct: false,
        moveRecordList: [],
        moveRecordListColumns: [
          {
            title: this.$t('product'),
            key: 'product_name',
            sortable: true
          },
          {
            title: this.$t('salePrice'),
            key: 'sale_price',
            sortable: true
          },
          {
            title: this.$t('moveAmount'),
            key: 'move_amount',
            sortable: true
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
        currentDepartment: state => state.currentDepartment
      }),
      ...mapState('stock', {
        moveRecordList: state => state.moveRecordList
      }),
      ...mapGetters('stock', [
        'moveRecordListCount',
        'moveRecordListSum'
      ]),
      total: function () {
        return this.moveRecordList.length
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
        emptyMoveRecordItem: 'emptyMoveRecordItem',
        setMoveRecordList: 'setMoveRecordList'
      }),
      addToList: function () {
        console.log(this.formInline)
        this.$refs['formInline'].validate((valid) => {
          if (valid) {
            console.log('valid')
            let payload = {}
            let product = this.formInline['productInfo'].split('|')
            this.formInline['product'] = product[0]
            this.formInline['product_name'] = product[1]
            this.formInline['sale_price'] = product[3]
            payload['item'] = JSON.parse(JSON.stringify(this.formInline))
            payload['move_amount'] = this.formInline.move_amount
            payload['batch_no'] = this.formInline.batch_no
            payload['comment'] = this.formInline.comment
            console.log(product)
            this.$store.dispatch('stock/addMoveRecordItem', payload)
          } else {
            this.$Message.error(this.$t('validateFailed'))
          }
        })
      },
      removeFromList: function (index) {
        this.removeMoveRecordItem(this.moveRecordList[index])
      },
      submitMoveRecord: function () {
        console.log('submitting move record')
        if (this.currentDepartment) {
          let params = {
            dept_in: this.currentDepartment,
            moveRecordList: this.moveRecordList
          }
          addMoveRecord(params).then((res) => {
            let { status, data, statusText } = res
            if (status !== 201) {
              this.$Message.error(this.$t('failed'))
            } else {
              console.log(data)
              console.log(statusText)
            }
          })
        } else {
          this.$Message.error(this.$t('invalideDeptIn'))
        }
      }
    },
    mounted () {
      // this.setProducts()
    }
  }
</script>

<style lang="stylus" scoped>
</style>
