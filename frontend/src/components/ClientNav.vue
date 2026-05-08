<template>
  <header class="nav-shell">
    <div class="nav-inner container">
      <div class="left-area">
        <div class="auth-actions">
          <template v-if="isLoggedIn">
            <button class="logout-link" type="button" @click="logout">退出登录</button>
          </template>
          <template v-else>
            <router-link class="login-link" to="/login" @click="open = false">登录</router-link>
            <router-link class="register-link" to="/register" @click="open = false">注册</router-link>
          </template>
        </div>
        <router-link class="brand" to="/">在线教育平台</router-link>
      </div>
      <button class="menu-button" type="button" @click="open = !open">☰</button>
      <div :class="['nav-content', { open }]">
        <nav class="nav-menu">
          <router-link v-for="item in items" :key="item.path" :to="item.path" @click="open = false">
            <span>{{ item.label }}</span>
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { clearAuth, emitAuthChange, getAuthToken, getAuthUser } from "../services/auth";

const router = useRouter();
const open = ref(false);
const authVersion = ref(0);
const isLoggedIn = computed(() => {
  authVersion.value;
  return Boolean(getAuthToken("client"));
});
const userRole = computed(() => {
  authVersion.value;
  return getAuthUser("client")?.role || "";
});
const baseItems = [
  { path: "/", label: "首页" },
  { path: "/forum", label: "学习交流" },
  { path: "/notices", label: "网站公告" },
  { path: "/news", label: "教育资讯" },
  { path: "/courses", label: "课程资料" },
  { path: "/videos", label: "在线视频" },
  { path: "/profile", label: "个人中心" }
];
const items = computed(() => (userRole.value === "teacher" ? [...baseItems, { path: "/teacher/courses", label: "教师课程资料" }] : baseItems));

function logout() {
  clearAuth("client");
  authVersion.value += 1;
  open.value = false;
  emitAuthChange();
  router.push("/");
}

window.addEventListener("storage", () => {
  authVersion.value += 1;
});
</script>

<style scoped>
.nav-shell {
  position: fixed;
  z-index: 20;
  top: 0;
  left: 0;
  width: 100%;
  height: 72px;
  background: #d4c2e1;
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
  gap: 12px;
}

.left-area {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 0 0 auto;
}

.brand {
  padding: 10px 18px;
  border-radius: 999px;
  background: #fff;
  color: #993380;
  font-weight: 800;
}

.nav-content {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.nav-menu {
  display: flex;
  gap: 6px;
  padding: 8px;
  border-radius: 999px;
  background: #fff;
}

.nav-menu a {
  position: relative;
  padding: 10px 10px;
  border-radius: 999px;
  color: #333;
  font-size: 15px;
  white-space: nowrap;
}

.nav-menu a.router-link-active {
  color: #993380;
  font-weight: 800;
}

.nav-menu a.router-link-active::after {
  content: "♥";
  position: absolute;
  left: 50%;
  bottom: -12px;
  transform: translateX(-50%);
  color: #993380;
  font-size: 14px;
}

.auth-actions {
  display: flex;
  gap: 8px;
}

.login-link,
.register-link,
.logout-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 38px;
  padding: 0 14px;
  border-radius: 999px;
  border: 0;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
}

.login-link {
  background: #fff;
  color: #993380;
  border: 1px solid #e6d4e6;
}

.register-link,
.logout-link {
  background: #993380;
  color: #fff;
}

.menu-button {
  display: none;
  border: 0;
  background: #fff;
  color: #993380;
  font-size: 24px;
}

@media (max-width: 1120px) {
  .nav-menu a {
    padding: 10px 8px;
    font-size: 14px;
  }
}

@media (max-width: 768px) {
  .menu-button {
    display: block;
  }

  .brand {
    display: none;
  }

  .nav-content {
    position: absolute;
    top: 72px;
    right: 20px;
    display: none;
    width: min(320px, calc(100vw - 40px));
    flex-direction: column;
    align-items: stretch;
    padding: 10px;
    border-radius: 8px;
    background: #fff;
    box-shadow: 0 16px 32px rgba(153, 51, 128, 0.18);
  }

  .nav-content.open {
    display: flex;
  }

  .nav-menu {
    flex-direction: column;
    border-radius: 8px;
    padding: 0;
  }

  .nav-menu a.router-link-active::after {
    display: none;
  }
}
</style>
