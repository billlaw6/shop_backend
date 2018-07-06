<template>
  <div>
    <Table ref="addedProduct" stripe :columns="addedProductColumns" :data="addedProduct">
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
      <FormItem :label="$t('amount')" prop="amount">
        <InputNumber :max="10000" :min="0.0" :step="0.1" v-model="formInline.amount"></InputNumber>
        <ul v-if="formInlineErrors.amount" v-for="error in formInlineErrors.amount">
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
        <Button type="primary" @click="addToList()">{{ $t('addToList') }}</Button>
      </Form-item>
    </Form>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'
  import { getStock } from '@/http/api'

  export default{
    components: {
    },
    data: function () {
      return {
        ruleInline: {
          productInfo: [
            { required: true }
          ]
        },
        formInline: {
          productInfo: '',
          amount: 0,
          batch_no: '',
          comment: ''
        },
        formInlineErrors: {},
        loadingProduct: false,
        addedProduct: [],
        addedProductColumns: [
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
            title: this.$t('amount'),
            key: 'amount',
            sortable: true
          },
          {
            title: this.$t('batchNo'),
            key: 'batch_no',
            sortable: true
          }
          // {
          //   title: this.$t('product'),
          //   key: 'product',
          //   sortable: true,
          //   render: (h, param) => {
          //     let toUrl = {name: 'order', params: {orderId: param.row.id}}
          //     return h('router-link', {
          //       props: {
          //         to: toUrl
          //       }
          //     }, param.row.name)
          //   }
          // }
        ]
      }
    },
    computed: {
      ...mapState('app', {
        availableProducts: state => state.availableProducts
      }),
      total: function () {
        return this.addedProduct.length
      }
    },
    methods: {
      ...mapActions('app', {
        setProducts: 'setProducts'
      }),
      getStockDate: function (from, to, pageSize, pageNumber) {
        let params = {
          from: from,
          to: to,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        getStock(params).then((res) => {
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
      },
      addToList () {
        // console.log(this.formInline)
        this.$refs['formInline'].validate((valid) => {
          if (valid) {
            console.log('valid')
            let product = this.formInline['productInfo'].split('|')
            // console.log(product)
            this.formInline['product'] = product[0]
            this.formInline['product_name'] = product[1]
            this.formInline['sale_price'] = product[3]
            this.addedProduct.push(this.formInline)
            console.log(this.addedProduct)
          } else {
            this.$Message.error(this.$t('validateFailed'))
          }
        })
      }
    },
    mounted () {
      this.setProducts()
    }
  }
</script>

<style lang="stylus" scoped>
</style>
