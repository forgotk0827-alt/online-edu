<template>
  <aside class="admin-sidebar">
    <h2 class="admin-logo">后台管理</h2>
    <div class="admin-user">
      <span>{{ user?.nickname || user?.username || "管理员" }}</span>
      <button type="button" @click="logout">退出登录</button>
    </div>
    <el-menu router :default-active="$route.path" background-color="#7373E6" text-color="#fff" active-text-color="#fff">
      <el-menu-item index="/admin/users/admin"><span class="label">后台首页</span></el-menu-item>
      <el-sub-menu index="/admin/users">
        <template #title><span class="label">系统用户</span></template>
        <el-menu-item index="/admin/users/admin"><span class="label">管理员</span></el-menu-item>
        <el-menu-item index="/admin/users/student"><span class="label">学生用户</span></el-menu-item>
        <el-menu-item index="/admin/users/teacher"><span class="label">教师用户</span></el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/admin/statistics"><span class="label">购买统计</span></el-menu-item>
      <el-menu-item index="/admin/courses"><span class="label">课程资料管理</span></el-menu-item>
      <el-menu-item index="/admin/orders"><span class="label">购买资料列表</span></el-menu-item>
      <el-menu-item index="/admin/videos"><span class="label">在线视频管理</span></el-menu-item>
      <el-menu-item index="/admin/news"><span class="label">教育资讯管理</span></el-menu-item>
      <el-menu-item index="/admin/forums"><span class="label">学习交流管理</span></el-menu-item>
      <el-menu-item index="/admin/banners"><span class="label">轮播图管理</span></el-menu-item>
      <el-menu-item index="/admin/notices"><span class="label">网站公告管理</span></el-menu-item>
    </el-menu>
  </aside>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
let user = null;

try {
  user = JSON.parse(localStorage.getItem("user") || "null");
} catch {
  user = null;
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.dispatchEvent(new Event("storage"));
  router.push("/admin/login");
}
</script>

<style scoped>
.admin-user {
  display: grid;
  gap: 8px;
  padding: 0 14px 14px;
  color: #fff;
  font-size: 13px;
}

.admin-user button {
  height: 30px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.14);
  color: #fff;
  cursor: pointer;
}
</style>
