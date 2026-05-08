<template>
  <main class="admin-login-page">
    <section class="admin-login-card">
      <h1>后台管理登录</h1>
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent>
        <el-form-item label="管理员账号" prop="username">
          <el-input v-model.trim="form.username" placeholder="请输入管理员账号" />
        </el-form-item>
        <el-form-item label="登录密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入登录密码" show-password />
        </el-form-item>
        <button class="admin-login-btn" type="button" @click="submit">登录</button>
      </el-form>
    </section>
  </main>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api } from "../../services/api";
import { loadDatabaseData, syncUser } from "../../services/store";

const router = useRouter();
const route = useRoute();
const formRef = ref();
const form = reactive({ username: "admin", password: "" });

const rules = {
  username: [{ required: true, message: "请输入管理员账号", trigger: "blur" }],
  password: [{ required: true, message: "请输入登录密码", trigger: "blur" }]
};

async function submit() {
  await formRef.value.validate();
  try {
    const { data } = await api.post("/auth/login/", {
      username: form.username,
      password: form.password
    });
    const user = data.data.user || {};
    if (user.role !== "admin") {
      throw new Error("当前账号不是管理员，无法进入后台");
    }
    localStorage.setItem("token", data.data.token);
    localStorage.setItem("user", JSON.stringify(user));
    syncUser(user);
    await loadDatabaseData();
    window.dispatchEvent(new Event("storage"));
    ElMessage.success("登录成功");
    router.push(route.query.redirect || "/admin/users/admin");
  } catch (error) {
    ElMessage.error(error?.response?.data?.message || error?.message || "登录失败");
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 32px 20px;
  background: linear-gradient(135deg, #f0f0ff 0%, #ffffff 56%, #e6e6ff 100%);
}

.admin-login-card {
  width: min(460px, 100%);
  padding: 34px 36px 30px;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 18px 42px rgba(90, 90, 217, 0.16);
}

.admin-login-card h1 {
  margin: 0 0 24px;
  text-align: center;
  color: #333;
  font-size: 22px;
}

:deep(.el-input__wrapper) {
  min-height: 40px;
  border-radius: 6px;
}

.admin-login-btn {
  width: 100%;
  height: 40px;
  margin-top: 8px;
  border: 0;
  border-radius: 6px;
  background: #7373e6;
  color: #fff;
  font-weight: 800;
  cursor: pointer;
}

.admin-login-btn:hover {
  background: #5a5ad9;
}
</style>
