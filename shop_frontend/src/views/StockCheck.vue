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
      <FormItem :label="$t('product')" prop="product">
        <Select 
          v-model="formInline.product"
          filterable
          remote
          :remote-method="getRemoteProduct"
        >
          <Option v-for="(option, index) in filteredProductList" :value="option.id" :key="index">
            <span>{{ option.name }}</span>
            <span style="margin-left: 5px; color:red">{{ option.sale_price | currency}}</span>
          </Option>
        </Select>
        <ul v-for="error in formInlineErrors.product">
          <li class="error">{{ error }}</li>
        </ul>
      </FormItem>
      <FormItem :label="$t('amount')" prop="amount">
        <InputNumber :max="10000" :min="0.0" :step="0.1" v-model="formInline.amount"></InputNumber>
        <ul v-for="error in formInlineErrors.amount">
          <li class="error">{{ error }}</li>
        </ul>
      </FormItem>
      <FormItem :label="$t('batch_no')" prop="batch_no">
        <Input v-model="formInline.batch_no"></Input>
        <ul v-for="error in formInlineErrors.batch_no">
          <li class="error">{{ error }}</li>
        </ul>
      </FormItem>
      <FormItem :label="$t('comment')" prop="comment">
        <Input v-model="formInline.comment" type="text></Input>
        <ul v-for="error in formInlineErrors.comment">
          <li class="error">{{ error }}</li>
        </ul>
      </FormItem>
    </Form>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import { getStock } from '@/http/api'

  export default{
    components: {
    },
    data: function () {
      return {
        total: 0,
        filteredProductList: [],
        ruleInline: {
          product: [
            { required: true }
          ]
        },
        formInline: {
          product: ''
        },
        formInlineErrors: {},
        loadingProduct: false,
        addedProductColumns: [
          // {
          //   title: this.$t('orderNo'),
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
      addedProduct: function () {
        return window.localStorage['addedProduct'] ? JSON.parse(window.localStorage['addedProduct']) : []
      }
    },
    methods: {
      getRemoteProduct (query) {
        let tmpArray = JSON.parse(JSON.stringify(this.availableProducts))
        // console.log(query)
        if (query !== '') {
          this.loadingProduct = true
          this.filteredProductList = tmpArray.filter((item, index, array) => {
            // console.log(query)
            // console.log(item)
            if (item.name.toUpperCase().indexOf(query.toUpperCase()) !== -1) {
              return true
            } else if (item.pinyin.toUpperCase().indexOf(query.toUpperCase()) !== -1) {
              return true
            } else if (item.py.toUpperCase().indexOf(query.toUpperCase()) !== -1) {
              return true
            } else if (item.sale_price.toString().toUpperCase().indexOf(query.toUpperCase()) !== -1) {
              return true
            } else {
              return false
            }
          })
          this.loadingProduct = false
        } else {
          this.filteredProductList = tmpArray
        }
      },
      getDate (from, to, pageSize, pageNumber) {
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
      }
    }
  }
</script>

<style lang="stylus" scoped>
</style>
