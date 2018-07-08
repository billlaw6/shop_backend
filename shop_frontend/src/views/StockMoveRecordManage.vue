<template>
  <div>
    <Table ref="addedProduct" stripe :columns="moveRecordColumns" :data="moveRecordList">
      <div class="table-header" slot="header">
        待处理入出库
      </div>
      <div class="table-footer" slot="footer">
        共计: <span>{{ total }}</span> 订单，合计: <span></span>
      </div>
    </Table>
  </div>
</template>

<script>
  // import { mapState, mapGetters, mapActions } from 'vuex'
  import { getStockMoveRecord, processStockMoveRecord } from '@/http/api'

  export default{
    components: {
    },
    data: function () {
      return {
        total: 0,
        moveRecordList: [],
        moveRecordColumns: [
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
              }, this.$t('process'))
            }
          }
        ]
      }
    },
    computed: {
    },
    methods: {
      handleProcessMoveRecord: function (params) {
        console.log(params)
        let para = {
          id: params.row.id
        }
        processStockMoveRecord(para).then((res) => {
          let { status, data, statusText } = res
          if (status !== 203) {
            console.log(statusText)
          } else {
            console.log(data)
          }
        })
      }
    },
    mounted () {
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
    }
  }
</script>

<style lang="stylus" scoped>
</style>
