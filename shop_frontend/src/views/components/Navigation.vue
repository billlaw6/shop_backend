<template>
  <Row type="flex">
    <div class="layout-header">
      <i-button>
        <Icon type="navicon"></Icon>
      </i-button>
      <div class="user-info">
        <Dropdown placement="bottom-end">
          <span class="head-img">
            <img src="" alt="用户名">
          </span>
          <Dropdown-menu>
            <Dropdown-item>修改密码</Dropdown-item>
            <Dropdown-item>退出登录</Dropdown-item>
          </Dropdown-menu>
        </Dropdown>
      </div>
    </div>
  </Row>
</template>

<script>
</script>

<style lang="stylus" scoped>
  @import '../styles/vars'
  .user-info
    display: inline-block
    float: right
</style>
