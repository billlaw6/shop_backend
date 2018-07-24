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
        <i-button type="primary" @click="getStockMoveRecordData(pageSize, pageNumber)">{{ $t('remoteSearch') }}</i-button>
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

    <Button type="primary" size="large" @click="exportData(3)"><Icon type="ios-download-outline"></Icon>{{ $t('exportCustomedData') }}</Button>

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
            title: this.$t('status'),
            key: 'status',
            filterMultiple: true,
            filterMethod (value, row) {
              // 比较时注意变量类型
              if (value === true) {
                return row.is_active === true
              } else if (value === false) {
                return row.is_active === false
              }
            },
            render: (h, params) => {
              let statusTag = ''
              if (params.row.dept_in_name === this.currentDepartment.name &&
                params.row.status === 0 && /^0\d{4}/.test(params.row.dept_in)) {
                statusTag = 'toMoveIn'
              } else if (params.row.dept_in_name === this.currentDepartment.name &&
                params.row.status === 1 && /^0\d{4}/.test(params.row.dept_out)) {
                statusTag = 'toCheck'
              } else if (params.row.dept_in_name === this.currentDepartment.name &&
                params.row.status === 1 && !/^0\d{4}/.test(params.row.dept_out)) {
                statusTag = 'toBeReceived'
              } else if (params.row.dept_in_name === this.currentDepartment.name &&
                params.row.status === 2 && /^0\d{4}/.test(params.row.dept_out)) {
                statusTag = 'beChecked'
              } else if (params.row.dept_in_name === this.currentDepartment.name &&
                params.row.status === 2 && !/^0\d{4}/.test(params.row.dept_out)) {
                statusTag = 'beReceived'
              } else if (params.row.dept_out_name === this.currentDepartment.name &&
                params.row.status === 0) {
                statusTag = 'toMoveOut'
              } else if (params.row.dept_out_name === this.currentDepartment.name &&
                params.row.status === 1) {
                statusTag = 'toBeReceived'
              }
              return h('span', {
                style: {
                  marginRight: '5px'
                }
              // }, this.$t(statusTag) + params.row.status)
              }, this.$t(statusTag))
            }
          },
          {
            title: this.$t('process'),
            key: 'action',
            render: (h, params) => {
              let process = 'process'
              if (params.row.dept_in_name === this.currentDepartment.name &&
                params.row.status === 0) {
                process = 'confirmMoveIn'
              } else if (params.row.dept_in_name === this.currentDepartment.name &&
                params.row.status === 1 && /^0\d{4}/.test(params.row.dept_out)) {
                process = 'confirmCheck'
              } else if (params.row.dept_in_name === this.currentDepartment.name &&
                params.row.status === 1 && !/^0\d{4}/.test(params.row.dept_out)) {
                process = 'confirmReceive'
              } else if (params.row.dept_out_name === this.currentDepartment.name &&
                params.row.status === 0) {
                process = 'confirmMoveOut'
              } else if (params.row.dept_out_name === this.currentDepartment.name &&
                params.row.status === 1) {
                process = 'process'
              }
              let disabled = (process === 'process')
              return h('Button', {
                props: {
                  type: 'primary',
                  disabled: disabled,
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
        if (this.moveRecordList) {
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
        } else {
          return []
        }
      }
    },
    watch: {
      currentDepartment: function (newVal, oldVal) {
        console.log(newVal.code)
        this.getStockMoveRecordData(this.pageSize, this.pageNumber)
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
          if (status === 201) {
            console.log(data)
            this.$Message.success(this.$t('processSucceed'))
            this.$Message.success(this.$t('newStockCreated'))
            this.getStockMoveRecordData(this.pageSize, this.pageNumber)
          } else if (status === 203) {
            console.log(data)
            this.$Message.success(this.$t('processSucceed'))
            this.getStockMoveRecordData(this.pageSize, this.pageNumber)
          } else {
            console.log(statusText)
            this.$Message.error(this.$t('processFailed'))
          }
        })
      },
      getStockMoveRecordData: function (pageSize, pageNumber) {
        let paras = {
          start: this.dateRange[0].getFullYear() + '-' + (this.dateRange[0].getMonth() + 1) + '-' + (this.dateRange[0].getDate()),
          end: this.dateRange[1].getFullYear() + '-' + (this.dateRange[1].getMonth() + 1) + '-' + (this.dateRange[1].getDate()),
          keyword: this.keyword,
          department: this.currentDepartment.code,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        getStockMoveRecord(paras).then((res) => {
          console.log(res)
          let { status, data, statusText } = res
          if (status !== 200) {
            console.log(statusText)
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
      },
      exportData (type) {
        if (type === 1) {
          this.$refs.table.exportCsv({
            filename: 'List' + new Date()
          })
        } else if (type === 2) {
          this.$refs.table.exportCsv({
            filename: 'List_sorted_filtered' + new Date(),
            original: false
          })
        } else if (type === 3) {
          this.$refs.table.exportCsv({
            filename: 'List_customed' + new Date(),
            columns: this.tableColumns.filter((col, index) => index < 4),
            data: this.aStockMoveRecord.filter((data, index) => index < 10)
          })
        }
      }
    },
    mounted () {
      this.getStockMoveRecordData(this.pageSize, this.pageNumber)
    }
  }
</script>

<style lang="stylus" scoped>
</style>
