<template lang="html">
  <div class="detail">
    <Row class="description">
      <Col span="16">
        <span class="order-name">{{ orderInfo.order_no}}</span> 
      </Col>
      <Col span="8">
        <span class="order-price">{{ orderInfo.sum_price | currency }}</span>
      </Col>
    </Row>

    <Table ref="orderDetail" stripe :columns="orderDetailColumns" :data="orderInfo.order_details">
      <div class="table-header" slot="header">
        订单列表
      </div>
      <div class="table-footer" slot="footer">
        共计: <span>{{ total }}</span> 订单，合计: <span></span>
      </div>
    </Table>


    <Tabs value="detail">
      <TabPane label="图片详情" name="detail-pictures">
        Pictures
      </TabPane>
      <TabPane label="文字详情" name="detail-description">
        Description
      </TabPane>
    </Tabs>

  </div>
</template>

<script>
  import { getOrderInfo } from '../http/api'
  import { mapState, mapActions } from 'vuex'

  export default {
    components: {
    },
    data () {
      return {
        orderInfo: {},
        orderDetail: [],
        amount: null,
        orderDetailColumns: [
          {
            title: this.$t('product'),
            key: 'product_name'
          },
          {
            title: this.$t('price'),
            key: 'price'
          },
          {
            title: this.$t('amount'),
            key: 'amount'
          }
        ]
      }
    },
    computed: {
      ...mapState({
        // 大括号方式需要转成对象
        decimals: state => state.cart.decimals
      })
    },
    methods: {
      ...mapActions('cart', [
        // 中括号方式可直接映射，但只能同名映射
        'removeCartItem',
        'addCartItem'
      ])
    },
    beforeCreate () {
      console.debug('Detail.vue creating')
    },
    mounted () {
      getOrderInfo(this.$route.params.orderId).then((response) => {
        console.debug('data gotten in Detail:')
        console.debug(response.data)
        this.orderInfo = response.data
      }).catch(function (error) {
        console.error(error)
      })
    }
  }
</script>

<style lang="stylus" scoped>
</style>
