<Menu mode="horizontal" theme="primary" active-name="1" :accordion="true">
  <MenuItem name="logo">
    <div class="layout-logo">
      <Icon type="home"></Icon>主页
    </div>
  </MenuItem>
  <!-- 对已登录用户显示用户信息 -->
  <div class="account-info">
    <template v-if="user">
      <MenuItem name="userInfo">
        <Dropdown trigger="click" placement="bottom-end" style="margin-left: 20px">
          <a href="javascript:void(0)">
            {{ user.username }}
            <Avatar src="../assets/logo.png" alt="Logo"/>
            <Icon type="arrow-down-b"></Icon>
          </a>
          <DropdownMenu slot="list">
            <DropdownItem>修改密码</DropdownItem>
            <DropdownItem v-on:click="logout">退出</DropdownItem>
          </DropdownMenu>
        </Dropdown>
      </MenuItem>
      <MenuItem name="msgInfo">
        <Icon type="ios-navigate"></Icon>
        消息中心
      </MenuItem>
    </template>
    <template v-else>
      <MenuItem name="register">
        您好！
        <Icon type="person-add"></Icon>
        免费注册 
      </MenuItem>
      <MenuItem name="login">
        <Icon type="ios-play"></Icon>
        直接登录
      </MenuItem>
    </template>
  </div>
</Menu>
