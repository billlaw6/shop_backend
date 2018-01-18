<template>
  <i-form class="card-box" ref="formRegister" :model="formRegister" :rules="registerDataRules">
    <Form-item class="formRegister-title">
      <h3>注册</h3>
    </Form-item>

    <Form-item prop="username">
      <i-input size="large" type="text" v-model="formRegister.username" placeholder="用户名" :autofocus="true">
        <Icon type="ios-person-outline" slot="prepend"></Icon>
      </i-input>
    </Form-item>
    <Form-item prop="password">
      <i-input size="large" type="password" v-model="formRegister.password" placeholder="用户名" :autofocus="true">
        <Icon type="ios-locked-outline" slot="prepend"></Icon>
      </i-input>
    </Form-item>
  </i-form>
</template>

