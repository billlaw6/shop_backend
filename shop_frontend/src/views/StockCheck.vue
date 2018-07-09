<template>
  <div>
    <Table ref="stockList" stripe :columns="stockColumns" :data="stockList">
      <div class="table-header" slot="header">
        <span style="text-align: center; font: 1.8em">当前库存</span>
      </div>
      <div class="table-footer" slot="footer">
        共计: <span>{{ total }}</span> 订单，合计: <span></span>
      </div>
    </Table>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import { searchStocks } from '@/http/api'

  export default{
    components: {
    },
    data: function () {
      return {
        total: 0,
        stockList: [],
        stockColumns: [
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
          },
          {
            title: this.$t('process'),
            key: 'action',
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'primary',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.handleProcessMoveRecord(params)
                  }
                }
              }, this.$t('toggle'))
            }
          }
        ]
      }
    },
    computed: {
      ...mapState('app', {
        currentDepartment: state => state.currentDepartment
      })
    },
    methods: {
      getStockData: function (department) {
        let params = {
          department: department
        }
        searchStocks(params).then((res) => {
          let { status, data, statusText } = res
          if (status !== 200) {
            console.log(statusText)
            console.log(data)
          } else {
            console.log('data:')
            console.log(data)
            this.total = data.count
            this.stockList = data.results
          }
        })
      }
    },
    mounted () {
      if (this.currentDepartment) {
        this.getStockData(this.currentDepartment)
      }
      this.getStockData('20001')
    }
  }
</script>

<style lang="stylus" scoped>
</style>
