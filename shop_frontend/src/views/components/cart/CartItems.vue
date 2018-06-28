<template lang="html">
  <div class="cart">
    <Table ref="cartList" stripe :columns="cartListColumns" :data="cartList">
      <div class="table-header" slot="header">
        已添加商品列表
      </div>

      <div class="table-footer" slot="footer">
        共计: <span>{{ cartListCount }}</span> 种商品，合计: <span>{{ cartListSum | currency }}</span>

      </div>
    </Table>
    <br>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex'
  import { getDepartments } from '@/http/api'

  export default {
    data () {
      return {
        emptyConfirm: false,
        toDepartment: null,
        cartListColumns: [
          {
            title: '商品名称',
            key: 'name',
            sortable: true,
            render: (h, param) => {
              let toUrl = {name: 'detail', params: {productId: param.row.id}}
              return h('router-link',
                {props: {
                  to: toUrl
                }}, param.row.name)
            }
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
            sortable: true,
            render: (h, params) => {
              return h('span', params.row.amount.toFixed(this.decimals))
            }
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
              return h('span', (params.row.price * params.row.amount).toFixed(this.decimals))
            }
          },
          {
            title: '备注',
            key: 'comment',
            render: (h, params) => {
              return h('span', params.row.comment)
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
        cartList: state => state.cartList,
        decimals: state => state.decimals
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
