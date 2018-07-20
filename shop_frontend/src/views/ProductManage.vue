<template>
  <div class="product-manage">
    <Row class="search-box">
      <Col span="8">
        <AutoComplete v-model="keyword" :placeholder="$t('localSearch')" icon="ios-Textsearch" :clearable="true">
          <Option v-for="option in aList" :value="option.name" :key="option.id">
            <span class="product-name">{{ option.name }}</span>
            <span class="product-price">{{ option.sale_price | currency }}</span>
          </Option>
        </AutoComplete>
      </Col>
      <Col span="3">
        <i-button type="primary" @click="getProductData(pageSize, pageNumber)">{{ $t('remoteSearch') }}</i-button>
      </Col>
      <Col span="4" push="9">
        <i-button type="primary" @click="showAddModal=true">{{ $t('addProduct') }}</i-button>
       </Col>
    </Row>

    <Table ref="table" class="data-table" :loading="loadingStatus" :context="self" :data="aList" :columns="tableColumns" stripe></Table>
    <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon>{{ $t('exportSourceData') }}</Button>
    <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon>{{ $t('exportSortedOrFilteredData') }}</Button>
    <Button type="primary" size="large" @click="exportData(3)"><Icon type="ios-download-outline"></Icon>{{ $t('exportCustomedData') }}</Button>
    <div style="margin: 10px;overflow: hidden">
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

    <Modal v-model="showAddModal" title="添加商品" @on-ok="confirmAdd('addModelForm')" @on-cancel="cancelAdd('addModelForm')" >
      <Form ref="addModelForm" :model="addModel" :rules="ruleValidate" :label-width="100" enctype="multipart/form-data" accept-charset="utf-8">
        <Form-item label="名称" prop="name">
          <Input v-model="addModel.name" placeholder="名称"></Input>
          <ul v-for="error in addModelErrors.name">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item label="品牌" prop="brand">
          <Input v-model="addModel.brand" placeholder="品牌"></Input>
          <ul v-for="error in addModelErrors.brand">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item label="售价" prop="sale_price">
          <InputNumber :max="10000" :min="1" :step="0.1" v-model="addModel.sale_price"></InputNumber>
          <ul v-for="error in addModelErrors.sale_price">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item label="原价" prop="price">
          <InputNumber :max="10000" :min="1" :step="0.1" v-model="addModel.price"></InputNumber>
          <ul v-for="error in addModelErrors.price">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item label="图片" prop="image">
          <Upload
            ref="addModelUpload"
            action="http://123.56.115.20/sale-manage/product/create/"
            :headers="headers"
            :data = "addModel"
            :format="['jpg', 'png', 'jpeg', 'gif', 'bmp', 'svg']"
            :on-format-error="handleFormatError"
            :max-size="maxSize"
            :on-exceeded-size="handleExceededSize"
            :before-upload="handleAddFileUploaded"
            :on-success="handleAddFileUploadSuccess"
          >
            <div v-if="uploadedFile">
              <span>选择了图片：{{ uploadedFile.name }}</span>
            </div>
            <span>选择图片上传</span>
            <Button type="ghost" icon="ios-cloud-upload-outline">上传文件</Button>
            <ul v-for="error in addModelErrors.image">
              <li class="error">{{ error }}</li>
            </ul>
          </Upload>
        </Form-item>
        <Form-item prop="is_active">
          <Checkbox v-model="addModel.is_active">是否在售</Checkbox>
          <ul v-for="error in addModelErrors.is_active">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item prop="is_bestseller">
          <Checkbox v-model="addModel.is_bestseller">是否热销</Checkbox>
          <ul v-for="error in addModelErrors.is_bestseller">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item label="描述" prop="description">
          <Input v-model="addModel.description" type="textarea" placeholder="商品描述"></Input>
          <ul v-for="error in addModelErrors.description">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item label="检索词" prop="meta_keywords">
          <Input v-model="addModel.meta_keywords" placeholder="检索词"></Input>
          <ul v-for="error in addModelErrors.meta_keywords">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item label="检索描述" prop="meta_description">
          <Input v-model="addModel.meta_description" type="textarea" placeholder="检索描述"></Input>
          <ul v-for="error in addModelErrors.meta_description">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
      </Form>
    </Modal>

    <Modal v-model="showEditModal" title="修改商品" @on-ok="confirmEdit('editModelForm')" @on-cancel="cancelEdit('editModelForm')" >
      <Form ref="editModelForm" :model="editModel" :rules="ruleValidate" :label-width="100">
        <Form-item label="名称" prop="name">
          <Input v-model="editModel.name" placeholder="名称"></Input>
        </Form-item>
        <Form-item label="品牌" prop="brand">
          <Input v-model="editModel.brand" placeholder="品牌"></Input>
        </Form-item>
        <Form-item label="售价" prop="sale_price">
          <InputNumber :max="10000" :min="1" :step="0.1" v-model="editModel.sale_price"></InputNumber>
        </Form-item>
        <Form-item label="原价" prop="price">
          <InputNumber :max="10000" :min="1" :step="0.1" v-model="editModel.price"></InputNumber>
        </Form-item>
        <Form-item label="图片" prop="image">
          <template v-if="editModel.image">
            <img class="product-image" :src="editModel.image.replace('sale-manage/products/shop_frontend/dist/', '')" alt="商品图片"/>
          </template>
          <Upload
            ref="editModelUpload"
            action="http://123.56.115.20/sale-manage/product/update/"
            :headers="headers"
            :data = "editModel"
            :format="['jpg', 'png', 'jpeg', 'gif', 'bmp', 'svg']"
            :on-format-error="handleFormatError"
            :max-size="maxSize"
            :on-exceeded-size="handleExceededSize"
            :before-upload="handleEditFileUploaded"
            :on-success="handleEditFileUploadSuccess"
          >
            <div v-if="uploadedFile">
              <span>选择了图片：{{ uploadedFile.name }}</span>
            </div>
            <span>选择图片上传</span>
            <Button type="ghost" icon="ios-cloud-upload-outline">上传文件</Button>
          </Upload>
        </Form-item>
        <Form-item prop="is_active">
          <Checkbox v-model="editModel.is_active">是否在售</Checkbox>
        </Form-item>
        <Form-item prop="is_bestseller">
          <Checkbox v-model="editModel.is_bestseller">是否热销</Checkbox>
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

    <Modal v-model="showDeleteModal" title="删除商品" @on-ok="confirmToggle('deleteModelForm')" @on-cancel="cancelDelete('deleteModelForm')" >
      <h3 class="warning-title">确认要开关商品？</h3>
      <Form ref="deleteModelForm" :model="deleteModel" :label-width="100">
        <Form-item label="名称" prop="name">
          <Input v-model="deleteModel.name" placeholder="名称" :readonly=true></Input>
        </Form-item>
        <Form-item label="售价" prop="sale_price">
          <InputNumber :max="10000" :min="1" :step="0.1" v-model="editModel.sale_price" :readonly=true></InputNumber>
        </Form-item>
        <Form-item label="原价" prop="price">
          <InputNumber :max="10000" :min="1" :step="0.1" v-model="editModel.price" :readonly=true></InputNumber>
        </Form-item>
      </Form>
    </Modal>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import { searchProducts, createProduct, updateProduct, toggleProduct } from '@/http/api'

  export default {
    data: function () {
      return {
        uploadedFile: null,
        loadingStatus: false,
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
        keyword: '',
        showAddModal: false,
        showEditModal: false,
        showDeleteModal: false,
        addModel: {
          name: '',
          brand: '',
          effective_month: 0,
          sale_price: 0.0,
          price: 0.0,
          is_active: false,
          is_bestseller: false,
          end_datetime: '2017-06-18T03:02:20Z',
          description: '',
          meta_keywords: '',
          meta_description: ''
        },
        addModelErrors: {},
        editModel: {
          name: '',
          brand: '',
          effective_month: 0,
          sale_price: 0.0,
          price: 0.0,
          is_active: false,
          is_bestseller: false,
          end_datetime: '',
          description: '',
          meta_keywords: '',
          meta_description: ''
        },
        editModelErrors: {},
        deleteModel: {
          name: '',
          sale_price: 0
        },
        ruleValidate: {
          name: [
            { required: true, message: '给商品取个名字吧', trigger: 'blur' },
            { type: 'string', min: 2, message: '多赐几个字嘛', trigger: 'blur' }
          ],
          brand: [
            { required: false, trigger: 'blur' },
            { type: 'string', trigger: 'blur' }
          ],
          sale_price: [
            { required: true, type: 'number', min: 0, max: 10000, message: '介是几个钱？', trigger: 'blur' }
          ],
          price: [
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
        pageNumber: 1,
        pageSize: 10,
        tableColumns: [
          {
            title: '名称',
            key: 'name',
            align: 'center',
            sortable: true
          },
          {
            title: '价格',
            key: 'sale_price',
            align: 'left',
            sortable: true,
            render: (h, params) => {
              return h(
                'span',
                // {
                //   style: {
                //     color: 'red'
                //   }
                // },
                params.row.sale_price
              )
            }
          },
          {
            title: '是否在售',
            key: 'is_active',
            align: 'center',
            sortable: true,
            filters: [
              {
                label: '停售',
                value: false
              },
              {
                label: '在售',
                value: true
              }
            ],
            filterMultiple: false,
            filterMethod (value, row) {
              // 比较时注意变量类型
              if (value === true) {
                return row.is_active === true
              } else if (value === false) {
                return row.is_active === false
              }
            },
            render: (h, params) => {
              let color = params.row.is_active ? 'green' : 'red'
              let text = params.row.is_active ? '在售' : '停售'
              return h('Tag', {
                props: {
                  type: 'dot',
                  color: color
                }
              }, text)
            }
          },
          {
            title: '描述',
            key: 'description',
            align: 'left',
            sortable: true
          },
          {
            title: '操作',
            key: 'action',
            width: 150,
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.showEdit(params.index)
                    }
                  }
                }, this.$t('edit')),
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.showDelete(params.index)
                    }
                  }
                }, this.$t('toggle'))
              ])
            }
          }
        ]
      }
    },
    computed: {
      ...mapState('app', {
        'maxSize': state => state.maxSize
      }),
      ...mapState('login', {
        'accessToken': state => state.accessToken
      }),
      // 图片上传时直接发起HTTP请求，所以需要单独设置
      headers: function () {
        let tmp = {}
        tmp['Authorization'] = 'Token ' + this.accessToken
        return tmp
      },
      aList: function () {
        // 用于autocomplete
        if (Array.isArray(this.tableData)) {
          return this.tableData.filter((item, index, array) => {
            if (this.keyword) {
              if (item.name.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
                return array.indexOf(item) === index
              } else if (item.sale_price.toString().indexOf(this.keyword.toUpperCase()) !== -1) {
                return true
              } else if (item.pinyin.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
                return true
              } else if (item.py.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
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
      showEdit (index) {
        this.showEditModal = true
        // this.editModel = this.tableData[index]
        this.editModel = this.aList[index]
        // Django-restful-framework将decimal转出来就已经是string类型
        this.editModel.sale_price = Number(this.editModel.sale_price)
        this.editModel.price = Number(this.editModel.price)
        // console.error(this.editModel)
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
      getProductData: function (pageSize, pageNumber) {
        this.loadingStatus = true
        let paras = {
          start: this.dateRange[0].getFullYear() + '-' + (this.dateRange[0].getMonth() + 1) + '-' + (this.dateRange[0].getDate()),
          end: this.dateRange[1].getFullYear() + '-' + (this.dateRange[1].getMonth() + 1) + '-' + (this.dateRange[1].getDate()),
          keyword: this.keyword,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        // console.log(paras)
        searchProducts(paras).then((res) => {
          let { data, status, statusText } = res
          if (status !== 200) {
            this.loginMessage = statusText
          } else {
            console.log(data)
            this.$Loading.finish()
            this.total = res.data.count
            this.tableData = data.results
          }
        }, (error) => {
          console.log('Error in searchProducts: ' + error)
          this.$Message.error('获取商品列表失败!')
        }).catch((error) => {
          console.log('catched in searchProducts:' + error)
          this.$Message.error('获取商品列表失败!')
        })
        this.loadingStatus = false
      },
      changePage (pageNumber) {
        console.log(pageNumber)
        this.pageNumber = pageNumber
        this.getProductData(this.pageSize, this.pageNumber)
      },
      changePageSize (pageSize) {
        console.log(pageSize)
        this.pageSize = pageSize
        this.getProductData(this.pageSize, this.pageNumber)
      },
      exportData (type) {
        if (type === 1) {
          this.$refs.table.exportCsv({
            filename: 'ProductList' + new Date()
          })
        } else if (type === 2) {
          this.$refs.table.exportCsv({
            filename: 'ProductList_sorted_filtered' + new Date(),
            original: false
          })
        } else if (type === 3) {
          this.$refs.table.exportCsv({
            filename: 'ProductList_customed' + new Date(),
            columns: this.tableColumns.filter((col, index) => index < 4),
            data: this.aList.filter((data, index) => index < 10)
          })
        }
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
            this.addModelErrors = {}
            let addModelSubmit = JSON.stringify(this.addModel)
            addModelSubmit = JSON.parse(addModelSubmit)
            // console.log(addModelSubmit)
            createProduct(addModelSubmit).then((res) => {
              let { data, status, statusText } = res
              if (status !== 201) {
                this.loginMessage = statusText
                // console.log(data.detail)
                this.addModelErrors = data
                this.$Message.error('添加商品失败!')
                this.showAddModel = true
              } else {
                console.log(data)
                this.$Message.success('添加商品成功!')
                // this.showAddModel = false
                // 更新商品列表
                this.getProductData(this.pageSize, this.pageNumber)
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
            this.editModelErrors = {}
            let editModelSubmit = JSON.parse(JSON.stringify(this.editModel))
            // console.log(editModelSubmit)
            updateProduct(editModelSubmit).then((res) => {
              let { data, status, statusText } = res
              if (status !== 201) {
                console.log(statusText)
                this.editModelErrors = data
                this.$Message.error(status)
                this.showEditModel = true
              } else {
                data.sale_price = Number(data.sale_price)
                data.price = Number(data.price)
                console.log(data)
                // this.editModel = JSON.parse(data)
                // this.editModel = data
                // this.showEditModel = false
                this.$Message.success('修改商品成功!')
                this.getProductData(this.pageSize, this.pageNumber)
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
      // 开关商品
      confirmToggle: function (name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            let deleteModelSubmit = JSON.stringify(this.deleteModel)
            deleteModelSubmit = JSON.parse(deleteModelSubmit)
            toggleProduct(deleteModelSubmit).then((res) => {
              let { status, statusText } = res
              if (status !== 201) {
                this.$Message.error(statusText)
              } else {
                this.$Message.success('开关商品成功!')
                this.getProductData(this.pageSize, this.pageNumber)
              }
            }, (error) => {
              console.log('Error in deleteProduct: ' + error)
              this.$Message.error('开关商品失败!')
            }).catch((error) => {
              console.log('catched in deleteProduct:' + error)
              this.$Message.error('开关商品失败!')
            })
          } else {
            this.$Message.error('商品信息校验失败!')
          }
        })
      },
      handleReset (name) {
        this.$refs[name].resetFields()
      },
      handleFormatError: function () {
        this.$Message.error(this.$t('format_error'))
      },
      handleExceededSize: function () {
        this.$Message.error(this.$t('exceeded_size_error'))
      },
      handleAddFileUploaded: function (file) {
        this.uploadedFile = file
        this.addModel['file'] = this.uploadedFile
        this.$refs.addModelUpload.clearFiles()
        this.getProductData(this.pageSize, this.pageNumber)
      },
      handleAddFileUploadSuccess: function (response, file, fileList) {
        console.log('file uploaded successfully')
        this.$refs.addModelUpload.clearFiles()
        this.getProductData(this.pageSize, this.pageNumber)
        this.$Message.success('修改商品成功!')
      },
      handleEditFileUploaded: function (file) {
        this.uploadedFile = file
        this.editModel['file'] = this.uploadedFile
        this.$refs.addModelUpload.clearFiles()
        this.$refs.editModelUpload.clearFiles()
        this.getProductData(this.pageSize, this.pageNumber)
      },
      handleEditFileUploadSuccess: function (response, file, fileList) {
        console.log('file uploaded successfully')
        this.$refs.editModelUpload.clearFiles()
        this.getProductData(this.pageSize, this.pageNumber)
        this.$Message.success('修改商品成功!')
      }
    },
    mounted () {
      this.getProductData(this.pageSize, this.pageNumber)
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus" scoped>
  @import '../common/vars'
  .search-box
    margin: 6px
  .product-manage
    margin: 6px
  .data-table
    margin: 6px
  .product-image
    width: 100%
    height: 100%
  .warning-title
    color: $warning-color
    text-align: center
</style>
