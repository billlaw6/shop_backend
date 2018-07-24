<template>
  <div class="customer-manage">
    <Row class="search-box">
      <Col span="8">
        <AutoComplete v-model="keyword" :placeholder="$t('localSearch')" icon="ios-Textsearch" :clearable="true">
          <Option v-for="option in aList" :value="option.username" :key="option.id">
            <span class="customer-name">{{ option.username }}</span>
            <span class="customer-price">{{ option.cell_phone }}</span>
            <span class="customer-price">{{ option.last_name }}</span>
            <span class="customer-price">{{ option.first_name }}</span>
          </Option>
        </AutoComplete>
      </Col>
      <Col span="3">
        <i-button type="primary" @click="getCustomerData(pageSize, pageNumber)">{{ $t('remoteSearch') }}</i-button>
      </Col>
      <Col span="4" push="9">
        <i-button type="primary" @click="showAddModal=true">{{ $t('addCustomer') }}</i-button>
       </Col>
    </Row>

    <Table ref="table" class="data-table" :loading="loadingStatus" :context="self" :data="aList" :columns="tableColumns" stripe></Table>

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

    <Modal v-model="showAddModal" title="添加客户" @on-ok="confirmAdd('addModelForm')" @on-cancel="cancelAdd('addModelForm')" >
      <Form ref="addModelForm" :model="addModel" :rules="ruleValidate" :label-width="100" enctype="multipart/form-data" accept-charset="utf-8">
        <Form-item :label="$t('username')" prop="username">
          <Input v-model="addModel.username" :placeholder="$t('username')"></Input>
          <ul v-for="error in addModelErrors.username">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('cell_phone')" prop="cell_phone">
          <Input v-model="addModel.cell_phone" :placeholder="$t('cell_phone')"></Input>
          <ul v-for="error in addModelErrors.cell_phone">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('last_name')" prop="last_name">
          <Input v-model="addModel.last_name" :placeholder="$t('last_name')"></Input>
          <ul v-for="error in addModelErrors.last_name">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('first_name')" prop="first_name">
          <Input v-model="addModel.first_name" :placeholder="$t('first_name')"></Input>
          <ul v-for="error in addModelErrors.first_name">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('email')" prop="email">
          <Input v-model="addModel.email" :placeholder="$t('email')"></Input>
          <ul v-for="error in addModelErrors.email">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
      </Form>
    </Modal>

    <Modal v-model="showEditModal" :title="$t('customerManage')" @on-ok="confirmEdit('editModelForm')" @on-cancel="cancelEdit('editModelForm')" >
      <Form ref="editModelForm" :model="editModel" :rules="ruleValidate" :label-width="100" enctype="multipart/form-data" accept-charset="utf-8">
        <Form-item :label="$t('username')" prop="username">
          <Input v-model="editModel.username" :placeholder="$t('username')"></Input>
          <ul v-for="error in editModelErrors.username">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('cell_phone')" prop="cell_phone">
          <Input v-model="editModel.cell_phone" :placeholder="$t('cell_phone')"></Input>
          <ul v-for="error in editModelErrors.cell_phone">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('last_name')" prop="last_name">
          <Input v-model="editModel.last_name" :placeholder="$t('last_name')"></Input>
          <ul v-for="error in editModelErrors.last_name">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('first_name')" prop="first_name">
          <Input v-model="editModel.first_name" :placeholder="$t('first_name')"></Input>
          <ul v-for="error in editModelErrors.first_name">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
        <Form-item :label="$t('email')" prop="email">
          <Input v-model="editModel.email" :placeholder="$t('email')"></Input>
          <ul v-for="error in editModelErrors.email">
            <li class="error">{{ error }}</li>
          </ul>
        </Form-item>
      </Form>
    </Modal>

  </div>
</template>

<script>
  // import { mapState } from 'vuex'
  import { searchCustomers, createCustomer, updateCustomer } from '@/http/api'

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
          username: '',
          first_name: '',
          last_name: '',
          cell_phone: '',
          email: ''
        },
        addModelErrors: {},
        editModel: {
          username: '',
          first_name: '',
          last_name: '',
          cell_phone: '',
          email: ''
        },
        editModelErrors: {},
        ruleValidate: {
          username: [
            { required: true, message: '名字必须的哦', trigger: 'blur' }
          ],
          first_name: [
            { min: 1, message: '至少一个字吧', trigger: 'blur' }
          ],
          last_name: [
            { min: 1, message: '至少一个字吧', trigger: 'blur' }
          ],
          cell_phone: [
            { required: true, message: '留个电话吧', trigger: 'blur' }
          ]
        },
        self: this,
        tableData: [],
        total: 0,
        pageNumber: 1,
        pageSize: 10,
        tableColumns: [
          {
            title: '用户名',
            key: 'username',
            align: 'center',
            sortable: true
          },
          {
            title: this.$t('last_name'),
            key: 'last_name',
            align: 'left'
          },
          {
            title: this.$t('first_name'),
            key: 'first_name',
            align: 'left'
          },
          {
            title: this.$t('action'),
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
                }, this.$t('edit'))
              ])
            }
          }
        ]
      }
    },
    computed: {
      aList: function () {
        // 用于autocomplete
        if (Array.isArray(this.tableData)) {
          return this.tableData.filter((item, index, array) => {
            if (this.keyword) {
              if (item.username.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
                return array.indexOf(item) === index
              } else if (item.last_name.toString().indexOf(this.keyword.toUpperCase()) !== -1) {
                return true
              } else if (item.first_name.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
                return true
              } else if (item.cell_phone.toUpperCase().indexOf(this.keyword.toUpperCase()) !== -1) {
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
        this.editModel = this.aList[index]
      },
      // 获取客户列表
      getCustomerData: function (pageSize, pageNumber) {
        this.loadingStatus = true
        let paras = {
          start: this.dateRange[0].getFullYear() + '-' + (this.dateRange[0].getMonth() + 1) + '-' + (this.dateRange[0].getDate()),
          end: this.dateRange[1].getFullYear() + '-' + (this.dateRange[1].getMonth() + 1) + '-' + (this.dateRange[1].getDate()),
          keyword: this.keyword,
          limit: pageSize,
          offset: (pageNumber - 1) * pageSize
        }
        // console.log(paras)
        searchCustomers(paras).then((res) => {
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
          console.log('Error in searchCustomers: ' + error)
          this.$Message.error('获取客户列表失败!')
        }).catch((error) => {
          console.log('catched in searchCustomers:' + error)
          this.$Message.error('获取客户列表失败!')
        })
        this.loadingStatus = false
      },
      changePage (pageNumber) {
        console.log(pageNumber)
        this.pageNumber = pageNumber
        this.getCustomerData(this.pageSize, this.pageNumber)
      },
      changePageSize (pageSize) {
        console.log(pageSize)
        this.pageSize = pageSize
        this.getCustomerData(this.pageSize, this.pageNumber)
      },
      exportData (type) {
        if (type === 1) {
          this.$refs.table.exportCsv({
            filename: 'CustomerList' + new Date()
          })
        } else if (type === 2) {
          this.$refs.table.exportCsv({
            filename: 'CustomerList_sorted_filtered' + new Date(),
            original: false
          })
        } else if (type === 3) {
          this.$refs.table.exportCsv({
            filename: 'CustomerList_customed' + new Date(),
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
      // 增加客户
      confirmAdd: function (name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            // 坑，注意javascript的浅复制，使用JSON实现深复制
            this.addModelErrors = {}
            let addModelSubmit = JSON.stringify(this.addModel)
            addModelSubmit = JSON.parse(addModelSubmit)
            // console.log(addModelSubmit)
            createCustomer(addModelSubmit).then((res) => {
              let { data, status, statusText } = res
              if (status !== 201) {
                this.loginMessage = statusText
                // console.log(data.detail)
                this.addModelErrors = data
                this.$Message.error('添加客户失败!')
                this.showAddModel = true
              } else {
                console.log(data)
                this.$Message.success('添加客户成功!')
                // this.showAddModel = false
                // 更新客户列表
                this.getCustomerData(this.pageSize, this.pageNumber)
              }
            }, (error) => {
              console.log('Error in addCustomer: ' + error)
              this.$Message.error('添加客户失败!')
            }).catch((error) => {
              console.log('Exception in addCustomer: ' + error)
              this.$Message.error('添加客户失败!')
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
      // 修改客户
      confirmEdit: function (name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            // 用这个办法实现深复制
            this.editModelErrors = {}
            let editModelSubmit = JSON.parse(JSON.stringify(this.editModel))
            // console.log(editModelSubmit)
            updateCustomer(editModelSubmit).then((res) => {
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
                this.$Message.success('修改客户成功!')
                this.getCustomerData(this.pageSize, this.pageNumber)
              }
            }, (error) => {
              console.log('Error in editCustomer: ' + error)
              this.$Message.error('修改客户失败!')
            }).catch((error) => {
              console.log('catched in editCustomer:' + error)
              this.$Message.error('修改客户失败!')
            })
          } else {
            this.$Message.error('客户信息校验失败!')
          }
        })
      },
      handleReset (name) {
        this.$refs[name].resetFields()
      },
      handleFormatError: function () {
        this.$Message.error(this.$t('format_error'))
      }
    },
    mounted () {
      this.getCustomerData(this.pageSize, this.pageNumber)
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus" scoped>
  @import '../common/vars'
  .search-box
    margin: 6px
  .customer-manage
    margin: 6px
  .data-table
    margin: 6px
  .customer-image
    width: 100%
    height: 100%
  .warning-title
    color: $warning-color
    text-align: center
</style>
