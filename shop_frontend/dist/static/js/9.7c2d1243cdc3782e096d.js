webpackJsonp([9],{"099G":function(e,r,t){"use strict";Object.defineProperty(r,"__esModule",{value:!0});var s=t("J7R3"),o=t("AHIA"),a={components:{TimerBtn:s.a,Captcha:o.a},data:function(){return{orderFormDataRules:{cell_phone:[{required:!0,message:"请填写正确的手机号",trigger:"blur"}],captcha:[{required:!0,message:"请证明您不是机器人",trigger:"blur"},{type:"string",min:4,message:"验证码长度不小于4位",trigger:"blur"}],address:[{required:!0,message:"请输入邮寄地址",trigger:"blur"}],verify_code:[{required:!0,message:"请输入手机收到的验证码",trigger:"blur"}]},orderForm:{cell_phone:"",captcha:"",verify_code:"",address:""}}},methods:{submitOrder:function(){console.log("submitOrder")}}},l={render:function(){var e=this,r=e.$createElement,t=e._self._c||r;return t("div",{staticClass:"products"},[e._m(0),e._v(" "),t("div",{staticClass:"order"},[t("Form",{ref:"orderForm",attrs:{model:e.orderForm,rules:e.orderFormDataRules}},[t("FormItem",{attrs:{prop:"cell_phone"}},[t("Input",{attrs:{size:"large",type:"text",placeholder:"注册使用的手机号",autofocus:!0},model:{value:e.orderForm.cell_phone,callback:function(r){e.$set(e.orderForm,"cell_phone",r)},expression:"orderForm.cell_phone"}},[t("span",{attrs:{slot:"prepend"},slot:"prepend"},[e._v("0086")])])],1),e._v(" "),t("captcha",{attrs:{height:40}}),e._v(" "),t("FormItem",{attrs:{prop:"verify_code"}},[t("Row",[t("Col",{attrs:{span:"10"}},[t("Input",{attrs:{size:"large",type:"text",placeholder:"请输入短信验证码"},model:{value:e.orderForm.verify_code,callback:function(r){e.$set(e.orderForm,"verify_code",r)},expression:"orderForm.verify_code"}})],1),e._v(" "),t("Col",{attrs:{span:"14"}},[t("timer-btn",{attrs:{second:6}})],1)],1)],1),e._v(" "),t("FormItem",[t("Row",[t("Col",{attrs:{span:"8"}},[t("Button",{attrs:{type:"primary"},on:{click:e.submitOrder}},[e._v("下单")])],1)],1)],1)],1)],1),e._v(" "),t("div",{staticClass:"sale-record"}),e._v(" "),t("div",{staticClass:"comments"})])},staticRenderFns:[function(){var e=this.$createElement,r=this._self._c||e;return r("div",{staticClass:"product"},[r("div",{staticClass:"picture"},[r("img",{attrs:{src:"",alt:"1"}}),this._v(" "),r("img",{attrs:{src:"",alt:"2"}}),this._v(" "),r("img",{attrs:{src:"",alt:"3"}})]),this._v(" "),r("div",{staticClass:"description"},[r("div")])])}]},i=t("X4nt")(a,l,!1,null,null,null);r.default=i.exports}});
//# sourceMappingURL=9.7c2d1243cdc3782e096d.js.map