webpackJsonp([15],{"66Dm":function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=r("3SZ7"),a=r.n(s),o=r("34v0"),n=r.n(o),i=r("EcfS"),l=r("m4jk"),d={data:function(){var e=this;return{keyword:"",dateRange:[new Date((new Date).getTime()-2592e5),new Date((new Date).getTime()+1728e5)],dateOptions:{shortcuts:[{text:"最近一周",value:function(){var e=new Date,t=new Date;return t.setTime(t.getTime()-6048e5),[t,e]}},{text:"最近一个月",value:function(){var e=new Date,t=new Date;return t.setTime(t.getTime()-2592e6),[t,e]}},{text:"最近三个月",value:function(){var e=new Date,t=new Date;return t.setTime(t.getTime()-7776e6),[t,e]}}]},orderListData:[],showOrderProcessModal:!1,total:0,orderModel:{express:"",payment:"",payment_no:"",comment:"",order_no:"",status:""},orderErrors:{},ruleOrderValidate:{express:[{validator:function(t,r,s){r?e.availableExpresses.some(function(e,t,s){return e.name===r})?s():s(new Error(e.$t("invalidExpressError"))):s()},trigger:"blur"}],payement:[{validator:function(t,r,s){r?s(new Error(e.$t("noPaymentError"))):e.availablePayments.some(function(e,t,s){return e.name===r})?s():s(new Error(e.$t("invalidPaymentError")))},trigger:"blur"}]},orderListColumns:[{title:this.$t("orderNo"),key:"order_no",sortable:!0,render:function(e,t){return e("span",t.row.order_no.substring(0,4))}},{title:this.$t("department"),key:"department_name",sortable:!0},{title:this.$t("buyer"),key:"buyer_name",sortable:!0},{title:this.$t("sumPrice"),key:"sum_price",sortable:!0},{title:this.$t("detail"),key:"order_details",sortable:!0,render:function(t,r){var s=[{title:e.$t("product"),key:"product_name"},{title:e.$t("sale_price"),key:"sale_price",render:function(e,t){return e("span",{style:{color:"red"}},t.row.sale_price)}},{title:e.$t("amount"),key:"amount"}];return t("Poptip",{props:{trigger:"hover",title:"明细",placement:"bottom"}},[t("Tag",r.row.order_details.length+"种商品"),t("div",{slot:"content",style:{width:"240px"}},[t("Table",{props:{columns:s,data:r.row.order_details}},"table")])])}},{title:this.$t("createdBy"),key:"created_by_name",sortable:!0},{title:this.$t("createdAt"),key:"created_at",sortable:!0},{title:this.$t("status"),key:"status",sortable:!0,align:"center",filters:[{label:this.$t("cart"),value:"cart"},{label:this.$t("order"),value:"order"},{label:this.$t("sent"),value:"sent"},{label:this.$t("checked"),value:"checked"}],filterMultiple:!0,filterMethod:function(e,t){return t.status===e},render:function(t,r){return t("span",e.$t(r.row.status))}},{title:"操作",key:"action",render:function(t,r){return t("div",[t("Button",{props:{type:"primary",size:"small"},style:{marginRight:"5px"},on:{click:function(){e.showEdit(r.index)}}},e.$t("process")),t("Button",{props:{type:"error",size:"small"},style:{marginRight:"5px"},on:{click:function(){var t={order_no:r.row.order_no,status:"trashed"};Object(l.s)(t),e.getOrderList(e.pageSize,e.pageNumber)}}},e.$t("trash"))])}}],pageNumber:1,pageSize:10,selectedPayment:{},selectedExpress:{}}},computed:n()({},Object(i.e)("app",{availableExpresses:function(e){return e.availableExpresses},availableDepartments:function(e){return e.availableDepartments},availablePayments:function(e){return e.availablePayments}}),{aList:function(){var e=this;return Array.isArray(this.orderListData)?this.orderListData.filter(function(t,r,s){return-1!==t.order_no.toUpperCase().indexOf(e.keyword.toUpperCase())?s.indexOf(t)===r:-1!==t.sum_price.toString().indexOf(e.keyword.toUpperCase())}):[]},aExpress:function(){var e=this;return Array.isArray(this.availableExpresses)?this.availableExpresses.filter(function(t,r,s){return!e.orderModel.express||(-1!==t.name.toUpperCase().indexOf(e.orderModel.express.toUpperCase())||(-1!==t.pinyin.toUpperCase().indexOf(e.orderModel.express.toUpperCase())||-1!==t.py.toUpperCase().indexOf(e.orderModel.express.toUpperCase())))}):[]},aPayment:function(){var e=this;return console.log(this.orderModel.payment),Array.isArray(this.availablePayments)?this.availablePayments.filter(function(t,r,s){return!e.orderModel.payment||(-1!==t.name.toUpperCase().indexOf(e.orderModel.payment.toUpperCase())||(-1!==t.pinyin.toUpperCase().indexOf(e.orderModel.payment.toUpperCase())||-1!==t.py.toUpperCase().indexOf(e.orderModel.payment.toUpperCase())))}):[]}}),methods:{getOrderList:function(e,t){var r=this,s={start:this.dateRange[0].getFullYear()+"-"+(this.dateRange[0].getMonth()+1)+"-"+this.dateRange[0].getDate(),end:this.dateRange[1].getFullYear()+"-"+(this.dateRange[1].getMonth()+1)+"-"+this.dateRange[1].getDate(),keyword:this.keyword,limit:e,offset:(t-1)*e};Object(l.g)(s).then(function(e){var t=e.data,s=e.status,a=e.statusText;200!==s?console.error("get Order failed:"+a):(r.total=t.count,r.orderListData=t.results)},function(e){console.log("Error in getOrderList:"+e)})},changePage:function(e){console.log(e),this.pageNumber=e,this.getOrderList(this.pageSize,this.pageNumber)},changePageSize:function(e){this.pageSize=e,this.getOrderList(this.pageSize,this.pageNumber)},showEdit:function(e){this.showOrderProcessModal=!0,null===this.orderListData[e].express?this.orderListData[e].express="":this.orderListData[e].express=this.orderListData[e].express_name,null===this.orderListData[e].payment?this.orderListData[e].payment="":this.orderListData[e].payment=this.orderListData[e].payment_name,this.orderModel=this.aList[e]},confirmProcess:function(e){var t=this;this.$refs[e].validate(function(e){if(e){var r=JSON.parse(a()(t.orderModel));r.payment=t.selectedPayment.code,r.express=t.selectedExpress.code,console.log(r),Object(l.s)(r).then(function(e){console.error(e);var r=e.data,s=e.status,a=e.statusText;204===s?t.$Message.error("库存不够"):203===s?(t.$Message.success(t.$t("processSucceed")),t.getOrderList(t.pageSize,t.pageNumber)):(console.error("get Order failed:"+a),console.error(r),t.$Message.error(t.$t("processFailed")))},function(e){console.log("Error in getOrderList:"+e),t.$Message.error(t.$t("processFailed"))})}else t.$Message.error(t.$t("validateFailed")),t.showOrderProcessModal=!0})},cancelProcess:function(e){this.$Message.warning(this.$t("canceled"))},handleExpressSelected:function(e){var t=this;if(this.orderModel.express=e,e&&this.orderModel.express.length>0&&this.availableExpresses.length>0){var r=this.availableExpresses.filter(function(e,r,s){return e.name===t.orderModel.express});this.selectedExpress=r[0]}},handlePaymentSelected:function(e){var t=this;if(this.orderModel.payment=e,e)if(this.orderModel.payment.length>0&&this.availablePayments.length>0){var r=this.availablePayments.filter(function(e,r,s){return e.name===t.orderModel.payment});this.selectedPayment=r[0]}else this.$Message.error("invalidPayment")}},mounted:function(){console.debug("Cart.vue mounted"),this.getOrderList(this.pageSize,this.pageNumber)},beforeCreate:function(){console.log("Cart.vue creating")}},c={render:function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"order"},[r("Row",{staticClass:"search-box"},[r("Col",{attrs:{span:"6"}},[r("Date-picker",{attrs:{type:"daterange",format:"yyyy-MM-dd",options:e.dateOptions,placement:"bottom-start",placeholder:"订单创建时间"},model:{value:e.dateRange,callback:function(t){e.dateRange=t},expression:"dateRange"}})],1),e._v(" "),r("Col",{attrs:{span:"8"}},[r("AutoComplete",{attrs:{placeholder:e.$t("localSearch"),icon:"ios-search",clearable:!0},model:{value:e.keyword,callback:function(t){e.keyword=t},expression:"keyword"}},e._l(e.aList,function(t){return r("Option",{key:t.order_no,attrs:{value:t.order_no}},[r("span",{staticClass:"name"},[e._v(e._s(t.order_no))]),e._v(" "),r("span",{staticClass:"sum_price"},[e._v(e._s(t.buyer_name))]),e._v(" "),r("span",{staticClass:"sum_price"},[e._v(e._s(e._f("currency")(t.sum_price)))])])}))],1),e._v(" "),r("Col",{attrs:{span:"3"}},[r("i-button",{attrs:{type:"primary"},on:{click:function(t){e.getOrderList(e.pageSize,e.pageNumber)}}},[e._v(e._s(e.$t("remoteSearch")))])],1),e._v(" "),r("Col",{attrs:{span:"4",push:"3"}},[r("i-button",{attrs:{type:"primary"},on:{click:function(e){}}},[e._v(e._s(e.$t("addOrder")))])],1)],1),e._v(" "),r("Table",{ref:"orderList",attrs:{stripe:"",columns:e.orderListColumns,data:e.aList}},[r("div",{staticClass:"table-header",attrs:{slot:"header"},slot:"header"},[e._v("\n      订单列表\n    ")]),e._v(" "),r("div",{staticClass:"table-footer",attrs:{slot:"footer"},slot:"footer"},[e._v("\n      共计: "),r("span",[e._v(e._s(e.total))]),e._v(" 订单，合计: "),r("span")])]),e._v(" "),r("div",{staticStyle:{margin:"10px",overflow:"hidden"}},[r("div",{staticStyle:{float:"right"}},[r("Page",{attrs:{total:e.total,current:e.pageNumber,"show-sizer":"","show-elevator":"","show-total":"","page-size":e.pageSize,"page-size-opts":[10,20,40,1e4]},on:{"on-change":e.changePage,"on-page-size-change":e.changePageSize}})],1)]),e._v(" "),r("Modal",{attrs:{title:e.$t("orderProcess")},on:{"on-ok":function(t){e.confirmProcess("processOrderForm")},"on-cancel":function(t){e.cancelProcess("orderModelForm")}},model:{value:e.showOrderProcessModal,callback:function(t){e.showOrderProcessModal=t},expression:"showOrderProcessModal"}},[r("div",{staticClass:"order-info"},[e._v("\n      "+e._s(e.$t("orderNo"))+": "),r("span",{staticClass:"order_no"},[e._v(e._s(e.orderModel.order_no))]),r("br"),e._v("\n      "+e._s(e.$t("buyer"))+": "),r("span",{staticClass:"buyer"},[e._v(e._s(e.orderModel.buyer_name))]),r("br"),e._v("\n      "+e._s(e.$t("sum_price"))+": "),r("span",{staticClass:"sum_price"},[e._v(e._s(e.orderModel.sum_price))])]),e._v(" "),r("Form",{ref:"processOrderForm",attrs:{model:e.orderModel,rules:e.ruleOrderValidate,"label-position":"left",inline:""}},[r("Form-item",{attrs:{label:e.$t("express"),prop:"express"}},[r("AutoComplete",{attrs:{placeholder:e.$t("selectExpress"),icon:"ios-search",clearable:!0},on:{"on-select":e.handleExpressSelected},model:{value:e.orderModel.express,callback:function(t){e.$set(e.orderModel,"express",t)},expression:"orderModel.express"}},e._l(e.aExpress,function(t){return r("Option",{key:t.code,attrs:{value:t.name}},[r("span",{staticClass:"product-name"},[e._v(e._s(t.name))])])})),e._v(" "),e._l(e.orderErrors.express,function(t){return r("ul",[r("li",{staticClass:"error"},[e._v(e._s(t))])])})],2),e._v(" "),r("Form-item",{attrs:{label:e.$t("expressNo"),prop:"express_no"}},[r("Input",{attrs:{type:"text"},model:{value:e.orderModel.express_no,callback:function(t){e.$set(e.orderModel,"express_no",t)},expression:"orderModel.express_no"}}),e._v(" "),e._l(e.orderErrors.express_no,function(t){return r("ul",[r("li",{staticClass:"error"},[e._v(e._s(t))])])})],2),e._v(" "),r("Form-item",{attrs:{label:e.$t("payment"),prop:"payment"}},[r("AutoComplete",{attrs:{placeholder:e.$t("selectPayment"),icon:"ios-search",clearable:!0},on:{"on-select":e.handlePaymentSelected},model:{value:e.orderModel.payment,callback:function(t){e.$set(e.orderModel,"payment",t)},expression:"orderModel.payment"}},e._l(e.aPayment,function(t){return r("Option",{key:t.code,attrs:{value:t.name}},[r("span",{staticClass:"product-name"},[e._v(e._s(t.name))])])})),e._v(" "),e._l(e.orderErrors.payment,function(t){return r("ul",[r("li",{staticClass:"error"},[e._v(e._s(t))])])})],2),e._v(" "),r("Form-item",{attrs:{label:e.$t("comment"),prop:"comment"}},[r("Input",{attrs:{type:"text"},model:{value:e.orderModel.comment,callback:function(t){e.$set(e.orderModel,"comment",t)},expression:"orderModel.comment"}}),e._v(" "),e._l(e.orderErrors.comment,function(t){return r("ul",[r("li",{staticClass:"error"},[e._v(e._s(t))])])})],2),e._v(" "),r("div",{staticStyle:{display:"none"}},[r("Input",{model:{value:e.orderModel.order_no,callback:function(t){e.$set(e.orderModel,"order_no",t)},expression:"orderModel.order_no"}}),e._v(" "),r("Input",{model:{value:e.orderModel.status,callback:function(t){e.$set(e.orderModel,"status",t)},expression:"orderModel.status"}})],1)],1)],1),e._v(" "),r("br")],1)},staticRenderFns:[]};var p=r("ngHh")(d,c,!1,function(e){r("iNln")},"data-v-488946a5",null);t.default=p.exports},iNln:function(e,t){}});
//# sourceMappingURL=15.8ca2f262c80c95559f41.js.map