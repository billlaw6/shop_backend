<template>
  <div class="stock-list">
    <Row class="search-box">
      <Col span="6">
        <Date-picker v-model="dateRange" type="daterange" format="yyyy-MM-dd" :options="dateOptions" placement="bottom-start" placeholder="订单创建时间"></Date-picker>
      </Col>
      <Col span="8">
        <AutoComplete v-model="keyword" 
          :placeholder="$t('localSearch')"
          icon="ios-search"
          :clearable="true">
          <Option v-for="option in aStockList" :value="option.product.name" :key="option.id">
            <span class="name">{{ option.product.name }}</span>
            <span class="name">{{ option.product.sale_price }}</span>
            <span class="name">{{ option.batch_no }}</span>
          </Option>
        </AutoComplete>
      </Col>
      <Col span="3">
        <i-button type="primary" @click="getStockData(pageSize, pageNumber)">{{ $t('remoteSearch') }}</i-button>
      </Col>
    </Row>

    <Table ref="stockList" stripe :columns="stockColumns" :data="stockList">
      <div class="table-header" slot="header">
        <span style="text-align: center; font: 1.8em">当前库存</span>
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
        keyword: '',
        dateRange: [new Date((new Date().getTime()) - 3 * 24 * 3600 * 1000), new Date((new Date().getTime()) + 2 * 24 * 3600 * 1000)],
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
        pageSize: 10,
        pageNumber: 1,
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
    // watch: {
    //   currentDepartment: function (value) {
    //     if (value) {
    //       this.getStockData(value)
    //     } else {
    //       console.log('no currentDepartment')
    //     }
    //   }
    // },
    computed: {
      ...mapState('login', {
        currentDepartment: state => state.currentDepartment
      }),
      aStockList: function () {
        if (Array.isArray(this.stockList)) {
          return this.stockList.filter((item, index, array) => {
            if (this.keyword) {
              if (item.product.name.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
                return array.indexOf(item) === index
              } else if (item.product.sale_price.toString().indexOf(this.keyword.toUpperCase()) !== -1) {
                return true
              } else if (item.product.pinyin.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
                return true
              } else if (item.product.py.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
                return true
              } else if (item.batch_no.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
                return true
              } else {
                return false
              }
            } else {
              return true
            }
          })
        } else {
          return []
        }
      }
    },
    methods: {
      getStockData: function (pageSize, pageNumber) {
        // GET请求不方便传对象
        let params = {
          start: this.dateRange[0].getFullYear() + '-' + (this.dateRange[0].getMonth() + 1) + '-' + (this.dateRange[0].getDate()),
          end: this.dateRange[1].getFullYear() + '-' + (this.dateRange[1].getMonth() + 1) + '-' + (this.dateRange[1].getDate()),
          keyword: this.keyword,
          department: this.currentDepartment.code,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        console.log(params)
        searchStocks(params).then((res) => {
          let { status, data, statusText } = res
          if (status !== 200) {
            console.log(statusText)
            console.log(data)
          } else {
            // console.log('data:')
            // console.log(data)
            this.total = data.count
            this.stockList = data.results
          }
        })
      },
      changePage (value) {
        console.log(value)
        this.pageNumber = value
        this.getStockData(this.pageSize, this.pageNumber)
      },
      changePageSize (value) {
        this.pageSize = value
        this.getStockData(this.pageSize, this.pageNumber)
      }
    },
    mounted () {
      if (this.currentDepartment) {
        this.getStockData(this.pageSize, this.pageNumber)
      } else {
        console.log('no currentDepartment')
      }
    }
  }
</script>

<style lang="stylus" scoped>
</style>
