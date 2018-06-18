<template lang="html">
  <div class="cart">
    <index-header></index-header>

    <Table ref="cartList" stripe :columns="cartListColumns" :data="cartList">
      <div class="table-header" slot="header">
        已添加商品列表
      </div>
      <div class="table-footer" slot="footer">
        共计: <span>{{ cartListCount }}</span> 种商品，合计: <span>{{ cartListSum | currency }}</span>
      </div>
    </Table>
    <br>

    <Tabs type="card">
      <TabPane label="操作">
        <Row type="flex" justify="end" class="code-row-bg">
          <Col :xs="{ span: 12 }" :lg="{ span: 6 }" class="empty-cart">
            <Button type="error" v-on:click="emptyConfirm=true">
              <Icon type="trash-a" :size="18"></Icon>
              <span>清空购物车</span>
            </Button>
            <Modal v-model="emptyConfirm" title="确认吗？" @on-ok="emptyCart">
              <p>确认删除全部商品？</p>
            </Modal>
          </Col>
          <Col :xs="{ span: 12 }" :lg="{ span: 6 }" class="checkout-cart" v-on:click="checkoutCart">
            <Button type="primary">
              <Icon type="ios-cart" :size="18"></Icon>
              <span>结算</span>
            </Button>
          </Col>
        </Row>
      </TabPane>
      <br>
      <TabPane label="店员操作" v-if="currentUser && currentUser.is_staff">
        <Row type="flex" justify="end" class="code-row-bg">
          <Col :xs="{ span: 12 }" :lg="{ span: 6 }" class="move-in-cart" v-on:click="checkoutCart">
            <Button type="primary">
              <Icon type="ios-download-outline" :size="18"></Icon>
              <span>采购入库</span>
            </Button>
          </Col>
          <Col :xs="{ span: 12 }" :lg="{ span: 6 }" class="move-out-cart" v-on:click="checkoutCart">
            <Icon type="ios-upload" :size="18"></Icon>
            <label for="toDepartment">
              <span>出库至</span>
            </label>
            <Select v-model="toDepartment" filterable id="toDepartment">
              <Option v-for="item in otherDepartments" :key="item.id" :value="item.id">{{ item.name }}</Option>
            </Select>
          </Col>
        </Row>
      </TabPane>
    </Tabs>

    <index-footer></index-footer> 
  </div>
</template>

<script>
  import IndexHeader from '@/views/components/common/IndexHeader.vue'
  import IndexFooter from '@/views/components/common/IndexFooter.vue'
  import CartItem from '@/views/components/cart/CartItem.vue'
  import { mapState, mapGetters, mapActions } from 'vuex'
  import { getDepartments } from '@/http/api'

  export default {
    components: {
      'index-header': IndexHeader,
      'index-footer': IndexFooter,
      'cart-item': CartItem
    },
    data () {
      return {
        emptyConfirm: false,
        toDepartment: null,
        cartListColumns: [
          {
            title: '商品名称',
            key: 'name',
            sortable: true
          },
          {
            title: '单价',
            key: 'price',
            sortable: true
          },
          {
            title: '减',
            key: 'decrease',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'warning',
                    size: 'small',
                    shape: 'circle'
                  },
                  on: {
                    click: () => {
                      this.decreaseCartItemAmount(params.row)
                    }
                  }
                }, '-')
              ])
            }
          },
          {
            title: '数量',
            key: 'amount',
            sortable: true
          },
          {
            title: '加',
            key: 'increase',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'warning',
                    size: 'small',
                    shape: 'circle'
                  },
                  on: {
                    click: () => {
                      this.increaseCartItemAmount(params.row)
                    }
                  }
                }, '+')
              ])
            }
          },
          {
            title: '小计',
            key: 'itemSum',
            render: (h, params) => {
              return h('span', (params.row.price * params.row.amount).toFixed(2))
            }
          },
          {
            title: '操作',
            key: 'action',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.removeCartItem(params.row)
                    }
                  }
                }, '删除')
              ])
            }
          }
        ]
      }
    },
    computed: {
      // 模块命名空间写法二
      ...mapState({
        loginStatus: state => state.login.loginStatus,
        currentUser: state => state.login.currentUser,
        otherDepartments: state => {
          // 尝试复制一下，防止修改state原值
          let tmpArray = JSON.parse(JSON.stringify(state.departments.results))
          if (state.login.currentUser) {
            // console.error(state.login.currentUser.department)
            let tmpArray1 = tmpArray.filter((item, index, array) => {
              // console.error(item.id)
              return item.id !== state.login.currentUser.department
            })
            return tmpArray1
          } else {
            console.error(state.login.currentUser)
            return tmpArray
          }
        }
      }),
      // 模块命名空间写法一
      ...mapState('cart', {
        cartList: state => state.cartList
      }),
      ...mapGetters('cart', [
        // 模块命名空间写法一
        'cartListCount',
        'cartListSum'
      ])
    },
    methods: {
      ...mapActions([
        'setDepartments'
      ]),
      // 模块命名空间写法二
      ...mapActions('cart', [
        'emptyCart',
        'setCartList',
        'removeCartItem',
        'resetCartList',
        'decreaseCartItemAmount',
        'increaseCartItemAmount'
      ]),
      checkoutCart: function (checkoutList) {
        console.debug('checkout cart')
        if (this.loginStatus) {
          console.debug('checking')
          this.$store.dispatch('emptyCart')
        } else {
          console.debug('redirecting')
          this.$router.push({ name: 'login' })
        }
      }
    },
    mounted () {
      console.debug('Cart.vue mounted')
    },
    beforeCreate () {
      // console.log('Cart.vue creating')
      getDepartments().then((response) => {
        let _this = this
        _this.setDepartments(response.data).then(() => {
          console.debug('state product list set')
        })
      }).catch(function (error) {
        console.error(error)
      })
    }
  }
</script>

<style lang="stylus" scoped>
  .cart-item
    border: 1px solid
  .footer
    width: 100vw
    height: 10vh
    div
      text-align: center
  .table-header
    font-size: 1.3em
    text-align: center
  .table-footer
    font-size: 1.2em
    margin: 1vh 3vw 6vh 1vw
    span
      color: red
</style>
