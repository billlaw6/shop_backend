<template>
  <div class="move-record-process">
    <Row class="search-box">
      <Col span="6">
        <Date-picker v-model="dateRange" type="daterange" format="yyyy-MM-dd" :options="dateOptions" placement="bottom-start" placeholder="订单创建时间"></Date-picker>
      </Col>
      <Col span="8">
        <AutoComplete v-model="keyword" 
          :placeholder="$t('localSearch')"
          icon="ios-search"
          :clearable="true">
          <Option v-for="option in aStockMoveRecord" :value="option.page_no" :key="option.id">
            <span class="name">{{ option.page_no.substring(0, 4) }}</span>
            <span class="product-name">{{ option.product_name }}</span>
            <span class="sale-price">{{ option.sale_price | currency }}</span>
          </Option>
        </AutoComplete>
      </Col>
      <Col span="3">
        <i-button type="primary" @click="handleRemoteSearch()">{{ $t('remoteSearch') }}</i-button>
      </Col>
    </Row>

    <Table ref="addedProduct" stripe :columns="moveRecordColumns" :data="aStockMoveRecord">
      <div class="table-header" slot="header">
        待处理入出库
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
  import { getStockMoveRecord, processStockMoveRecord } from '@/http/api'

  export default{
    components: {
    },
    data: function () {
      return {
        total: 0,
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
        pageNumber: 1,
        pageSize: 10,
        moveRecordList: [],
        moveRecordColumns: [
          {
            title: this.$t('pageNo'),
            key: 'page_no',
            sortable: true,
            render: (h, param) => {
              return h('span', param.row.page_no.substring(0, 4))
            }
          },
          {
            title: this.$t('deptOut'),
            key: 'dept_out_name',
            sortable: true
          },
          {
            title: this.$t('deptIn'),
            key: 'dept_in_name',
            sortable: true
          },
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
            title: this.$t('process'),
            key: 'action',
            render: (h, params) => {
              let process = 'process'
              if (params.row.dept_in_name === this.currentDepartment.name) {
                process = 'confirmMoveIn'
              } else if (params.row.dept_out_name === this.currentDepartment.name) {
                process = 'confirmMoveOut'
              }
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
              }, this.$t(process))
            }
          }
        ]
      }
    },
    computed: {
      ...mapState('login', {
        currentDepartment: state => state.currentDepartment
      }),
      aStockMoveRecord: function () {
        return this.moveRecordList.filter((item, index, array) => {
          // console.log(item.product_name)
          // console.log(this.keyword)
          if (this.keyword) {
            if (item.page_no.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else if (item.product_name.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else if (item.product_py.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else if (item.dept_in_name.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
              return true
            } else if (item.dept_out_name.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
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
      handleProcessMoveRecord: function (params) {
        let para = {
          id: params.row.id,
          currentDept: this.currentDepartment
        }
        console.log(para)
        processStockMoveRecord(para).then((res) => {
          let { status, data, statusText } = res
          if (status !== 203) {
            console.log(statusText)
          } else {
            console.log(data)
          }
        })
      },
      getStockMoveRecordData (pageSize, pageNumber) {
        let paras = {
          start: this.dateRange[0].getFullYear() + '-' + (this.dateRange[0].getMonth()) + '-' + (this.dateRange[0].getDate() + 1),
          end: this.dateRange[1].getFullYear() + '-' + (this.dateRange[1].getMonth() + 1) + '-' + (this.dateRange[1].getDate() + 1),
          keyword: this.keyword,
          department: this.currentDepartment,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        console.log(paras)
        getStockMoveRecord().then((res) => {
          let { status, data, statusText } = res
          if (status !== 200) {
            console.log(statusText)
            console.log(data)
          } else {
            console.log(data)
            this.total = data.count
            this.moveRecordList = data.results
          }
        })
      },
      changePage (value) {
        this.pageNumber = value
        this.getStockMoveRecordData(this.pageSize, this.pageNumber)
      },
      changePageSize (value) {
        this.pageSize = value
        this.getStockMoveRecordData(this.pageSize, this.pageNumber)
      }
    },
    mounted () {
      this.getStockMoveRecordData(this.pageSize, this.pageNumber)
    }
  }
</script>

<style lang="stylus" scoped>
</style>
