<template>
  <div>
    <Row>
      <Col span="6">
        <Date-picker v-model="dateRange" type="daterange" format="yyyy-MM-dd" :options="dateOptions" placement="bottom-start" placeholder="商品创建时间"></Date-picker>
      </Col>
      <Col span="8">
        <Input v-model="filter" icon="icon-search" placeholder="本地检索"></Input>
      </Col>
      <Col span="3">
        <i-button type="primary" @click="getProduct()">查询</i-button>
      </Col>
      <Col span="4" push="3">
        <i-button type="primary" @click="showAddModal=true">添加商品</i-button>
       </Col>
    </Row>

    <Table :context="self" :data="tableData" :columns="tableColumns" stripe bmerchandise></Table>
    <div style="margin: 10px;overflow: hidden">
      <div style="float: right;">
        <Page :total="total" :current="page" @on-change="changePage" show-total></Page>
      </div>
    </div>

    <Modal v-model="showAddModal" title="添加商品" @on-ok="confirmAdd('addModelForm')" @on-cancel="cancelAdd('addModelForm')" >
      <Form ref="addModelForm" :model="addModel" :rules="ruleValidate" :label-width="100">
        <Form-item label="名称" prop="name">
          <Input v-model="addModel.name" placeholder="名称"></Input>
        </Form-item>
        <Form-item label="拼音" prop="pinyin">
          <Input v-model="addModel.pinyin" placeholder="拼音"></Input>
        </Form-item>
        <Form-item label="品牌" prop="brand">
          <Input v-model="addModel.brand" placeholder="品牌"></Input>
        </Form-item>
        <Form-item label="售价" prop="price">
          <Input-number :max="10000" :min="1" :step="0.1" v-model="addModel.price"></Input-number>
        </Form-item>
        <Form-item label="原价" prop="old_price">
          <Input-number :max="10000" :min="1" :step="0.1" v-model="addModel.old_price"></Input-number>
        </Form-item>
        <Form-item prop="is_active">
          <Checkbox v-model="addModel.is_active">是否在售</Checkbox>
        </Form-item>
        <Form-item prop="is_bestseller">
          <Checkbox v-model="addModel.is_bestseller">是否热销</Checkbox>
        </Form-item>
        <Form-item prop="end_datetime">
          <Date-picker v-model="addModel.end_datetime" type="datetime" format="yyyy-MM-dd HH:mm:ss" placement="bottom-start" placeholder="促销结束时间"></Date-picker>
        </Form-item>
        <Form-item label="描述" prop="description">
          <Input v-model="addModel.description" type="textarea" placeholder="商品描述"></Input>
        </Form-item>
        <Form-item label="检索词" prop="meta_keywords">
          <Input v-model="addModel.meta_keywords" placeholder="检索词"></Input>
        </Form-item>
        <Form-item label="检索描述" prop="meta_description">
          <Input v-model="addModel.meta_description" type="textarea" placeholder="检索描述"></Input>
        </Form-item>
      </Form>
    </Modal>

    <Modal v-model="showEditModal" title="修改商品" @on-ok="confirmEdit('editModelForm')" @on-cancel="cancelEdit('editModelForm')" >
      <Form ref="editModelForm" :model="editModel" :rules="ruleValidate" :label-width="100">
        <Form-item label="名称" prop="name">
          <Input v-model="editModel.name" placeholder="名称"></Input>
        </Form-item>
        <Form-item label="拼音" prop="pinyin">
          <Input v-model="editModel.pinyin" placeholder="拼音"></Input>
        </Form-item>
        <Form-item label="品牌" prop="brand">
          <Input v-model="editModel.brand" placeholder="品牌"></Input>
        </Form-item>
        <Form-item label="售价" prop="price">
          <Input-number :max="10000" :min="1" :step="0.1" v-model="editModel.price"></Input-number>
        </Form-item>
        <Form-item label="原价" prop="old_price">
          <Input-number :max="10000" :min="1" :step="0.1" v-model="editModel.old_price"></Input-number>
        </Form-item>
        <Form-item prop="is_active">
          <Checkbox v-model="editModel.is_active">是否在售</Checkbox>
        </Form-item>
        <Form-item prop="is_bestseller">
          <Checkbox v-model="editModel.is_bestseller">是否热销</Checkbox>
        </Form-item>
        <Form-item prop="end_datetime">
          <Date-picker v-model="editModel.end_datetime" type="datetime" format="yyyy-MM-dd HH:mm:ss" placement="bottom-start" placeholder="促销结束时间"></Date-picker>
        </Form-item>
        <Form-item label="描述" prop="description">
          <Input v-model="editModel.description" type="textarea" placeholder="商品描述"></Input>
        </Form-item>
        <Form-item label="检索词" prop="meta_keywords">
          <Input v-model="editModel.meta_keywords" placeholder="检索词"></Input>
        </Form-item>
        <Form-item label="检索描述" prop="meta_description">
          <Input v-model="editModel.meta_description" type="textarea" placeholder="检索描述"></Input>
        </Form-item>
      </Form>
    </Modal>

    <Modal v-model="showDeleteModal" title="删除商品" @on-ok="confirmDelete('deleteModelForm')" @on-cancel="cancelDelete('deleteModelForm')" >
      <h3 class="warning-title">确认删除下面商品？</h3>
      <Form ref="deleteModelForm" :model="deleteModel" :label-width="100">
        <Form-item label="名称" prop="name">
          <Input v-model="deleteModel.name" placeholder="名称" :readonly=true></Input>
        </Form-item>
      </Form>
    </Modal>
  </div>
</template>

<script>
  import { getProducts, addProduct, updateProduct } from '@/http/api'
  export default {
    data: function () {
      return {
        merchandiseList: [],
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
        filter: '',
        showAddModal: false,
        showEditModal: false,
        showDeleteModal: false,
        addModel: {
          name: '',
          pinyin: '',
          brand: '',
          price: 0.0,
          old_price: 0.0,
          is_active: false,
          is_bestseller: false,
          end_datetime: '2017-06-18T03:02:20Z',
          description: '',
          meta_keywords: '',
          meta_description: ''
        },
        editModel: {
          name: '',
          pinyin: '',
          brand: '',
          price: 0.0,
          old_price: 0.0,
          is_active: false,
          is_bestseller: false,
          end_datetime: '',
          description: '',
          meta_keywords: '',
          meta_description: ''
        },
        deleteModel: {
          name: ''
        },
        ruleValidate: {
          name: [
            { required: true, message: '给商品取个名字吧', trigger: 'blur' },
            { type: 'string', min: 2, message: '多赐几个字嘛', trigger: 'blur' }
          ],
          pinyin: [
            { required: true, trigger: 'blur' },
            { type: 'string', trigger: 'blur' }
          ],
          brand: [
            { required: false, trigger: 'blur' },
            { type: 'string', trigger: 'blur' }
          ],
          price: [
            { required: true, type: 'number', min: 0, max: 10000, message: '介是几个钱？', trigger: 'blur' }
          ],
          old_price: [
            { required: false, type: 'number', min: 0, max: 10000, message: '介是几个钱？', trigger: 'blur' }
          ],
          is_active: [
            { required: true, type: 'boolean', trigger: 'blur' }
          ],
          is_bestseller: [
            { required: true, type: 'boolean', trigger: 'blur' }
          ],
          description: [
            { required: false, message: '不描述一下商品吗？', trigger: 'blur' }
          ],
          meta_keywords: [
            { required: false, message: '添加搜索关键词？', trigger: 'blur' }
          ],
          meta_description: [
            { required: false, message: '添加搜索关键描述？', trigger: 'blur' }
          ]
        },
        self: this,
        tableData: [],
        total: 0,
        page: 1,
        tableColumns: [
          {
            type: 'selection',
            width: 60,
            align: 'center'
          },
          {
            title: '名称',
            key: 'name',
            align: 'center',
            sortable: true
          },
          {
            title: '价格',
            key: 'price',
            align: 'left',
            sortable: true
          },
          {
            title: '是否在售',
            key: 'is_active',
            align: 'center',
            sortable: true
          },
          {
            title: '促销结束时间',
            key: 'end_datetime',
            align: 'left',
            sortable: true
          },
          {
            title: '创建人',
            key: 'owner',
            align: 'center',
            sortable: true
          },
          {
            title: '创建时间',
            key: 'created_at',
            align: 'left',
            sortable: true
          },
          {
            title: '操作',
            key: 'action',
            width: 150,
            align: 'center',
            render (row, column, index) {
              return `<i-button type="primary" size="small" @click="showEdit (${index})">查看</i-button> <i-button type="error" size="small" @click="showDelete (${index})">删除</i-button>`
            }
          }
        ]
      }
    },
    computed: {
    },
    methods: {
      showEdit (index) {
        this.showEditModal = true
        this.editModel = this.tableData[index]
        // console.log(this.editModel)
        this.editModel.old_price = Number(this.editModel.old_price)
        this.editModel.price = Number(this.editModel.price)
      },
      showDelete (index) {
        this.showDeleteModal = true
        this.deleteModel = this.tableData[index]
      },
      cancelDelete (index) {
        this.showDeleteModal = false
        this.$Message.info('点击了取消')
      },
      // 获取商品列表
      getProduct: function () {
        let para = {
          start: this.dateRange[0].getFullYear() + '-' + (this.dateRange[0].getMonth() + 1) + '-' + (this.dateRange[0].getDate() + 1),
          end: this.dateRange[1].getFullYear() + '-' + (this.dateRange[1].getMonth() + 1) + '-' + (this.dateRange[1].getDate() + 1),
          filter: this.filter,
          page: this.page
        }
        this.$Loading.start()
        getProducts(para).then((res) => {
          let { data, status, statusText } = res
          if (status !== 200) {
            this.loginMessage = statusText
          } else {
            this.$Loading.finish()
            this.total = res.data.count
            this.tableData = data.results
          }
        }, (error) => {
          console.log('Error in getProducts: ' + error)
          this.$Message.error('获取商品列表失败!')
        }).catch((error) => {
          console.log('catched in getProducts:' + error)
          this.$Message.error('获取商品列表失败!')
        })
      },
      changePage (row) {
        console.log(row)
        this.page = row
        this.getProduct()
      },

      // 撤销添加
      cancelAdd () {
        this.showAddModel = false
        this.$Message.info('点击了取消')
      },

      // 增加商品
      confirmAdd: function (name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            // 坑，注意javascript的浅复制，使用JSON实现深复制
            let addModelSubmit = JSON.stringify(this.addModel)
            addModelSubmit = JSON.parse(addModelSubmit)
            // console.log(addModelSubmit)
            addProduct(addModelSubmit).then((res) => {
              let { data, status, statusText } = res
              if (status !== 201) {
                this.loginMessage = statusText
                // console.log(data.detail)
                this.$Message.error('添加商品失败!')
              } else {
                console.log(data)
                this.$Message.success('添加商品成功!')
                this.showAddModel = false
                // 更新商品列表
                this.getProduct()
              }
            }, (error) => {
              console.log('Error in addProduct: ' + error)
              this.$Message.error('添加商品失败!')
            }).catch((error) => {
              console.log('Exception in addProduct: ' + error)
              this.$Message.error('添加商品失败!')
            })
          } else {
            console.log(this.$refs[name].errors)
            console.log(this.addModel)
            this.$Message.error('表单验证失败!')
          }
        })
      },

      // 撤销修改
      cancelEdit () {
        this.showEditModel = false
        this.$Message.info('点击了取消')
      },
      // 修改商品
      confirmEdit: function (name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            // 用这个办法实现深复制
            let editModelSubmit = JSON.stringify(this.editModel)
            editModelSubmit = JSON.parse(editModelSubmit)
            console.log(editModelSubmit)
            updateProduct(editModelSubmit).then((res) => {
              let { data, status, statusText } = res
              if (status !== 200) {
                console.log(statusText)
                this.$Message.error(status)
              } else {
                data.old_price = Number(data.old_price)
                data.price = Number(data.price)
                this.editModel = data
                console.log(this.editModel)
                this.$Message.success('修改商品成功!')
                this.getProduct()
              }
            }, (error) => {
              console.log('Error in editProduct: ' + error)
              this.$Message.error('修改商品失败!')
            }).catch((error) => {
              console.log('catched in editProduct:' + error)
              this.$Message.error('修改商品失败!')
            })
          } else {
            this.$Message.error('商品信息校验失败!')
          }
        })
      },
      // 删除商品
      confirmDelete: function (name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            console.log('deleting')
            let deleteModelSubmit = JSON.stringify(this.deleteModel)
            deleteModelSubmit = JSON.parse(deleteModelSubmit)
            deleteModelSubmit.status = 7
            updateProduct(deleteModelSubmit).then((res) => {
              let { data, status, statusText } = res
              if (status !== 200) {
                console.log(statusText)
                this.$Message.error(status)
              } else {
                console.log(data)
                this.$Message.success('删除商品成功!')
                this.getProduct()
              }
            }, (error) => {
              console.log('Error in deleteProduct: ' + error)
              this.$Message.error('删除商品失败!')
            }).catch((error) => {
              console.log('catched in deleteProduct:' + error)
              this.$Message.error('删除商品失败!')
            })
          } else {
            this.$Message.error('商品信息校验失败!')
          }
        })
      },
      handleReset (name) {
        this.$refs[name].resetFields()
      }
    },
    mounted () {
      this.getProduct()
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus" scoped>
  @import '../common/vars'
  .warning-title
    color: warning-color
    text-align: center
</style>
