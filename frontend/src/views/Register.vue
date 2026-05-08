<template>
  <main class="register-page">
    <section class="register-card">
      <h1>Register</h1>
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent>
        <el-form-item label="账号" prop="username">
          <el-input v-model.trim="form.username" placeholder="请输入 4-16 位账号" />
        </el-form-item>
        <el-form-item label="设置密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入 6-20 位密码" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm">
          <el-input v-model="form.confirm" type="password" placeholder="请再次输入密码" show-password />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model.trim="form.nickname" placeholder="2个字符到12个字符" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model.trim="form.email" placeholder="例: example@123.com" />
        </el-form-item>
        <button class="register-submit" type="button" @click="submit">注册</button>
        <router-link class="login-link" to="/login">已有账号？去登录</router-link>
      </el-form>
    </section>
  </main>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { api } from "../services/api";
import { syncUser } from "../services/store";

const router = useRouter();
const formRef = ref();
const form = reactive({ username: "", password: "", confirm: "", nickname: "", email: "" });
const rules = {
  username: [
    { required: true, message: "账号不能为空", trigger: "blur" },
    { min: 4, max: 16, message: "账号长度为 4-16 位", trigger: "blur" }
  ],
  password: [
    { required: true, message: "密码不能为空", trigger: "blur" },
    { min: 6, max: 20, message: "密码长度为 6-20 位", trigger: "blur" }
  ],
  confirm: [
    { required: true, message: "请再次输入密码", trigger: "blur" },
    { validator: (_, value, callback) => (value === form.password ? callback() : callback(new Error("两次密码不一致"))), trigger: "blur" }
  ],
  nickname: [
    { required: true, message: "昵称不能为空", trigger: "blur" },
    { min: 2, max: 12, message: "昵称长度为 2-12 个字符", trigger: "blur" }
  ],
  email: [
    { required: true, message: "邮箱不能为空", trigger: "blur" },
    { type: "email", message: "邮箱格式不正确", trigger: "blur" }
  ]
};

async function submit() {
  await formRef.value.validate();
  try {
    const { data } = await api.post("/auth/register/", form);
    if (data.code && data.code !== 200) throw new Error(data.message);
    syncUser({
      id: data.data?.id,
      username: form.username,
      nickname: form.nickname,
      email: form.email,
      role: data.data?.role || "student",
      status: "正常"
    });
    ElMessage.success("注册成功，请登录");
    router.push("/login");
  } catch (error) {
    ElMessage.error(error.response?.data?.message || error.message || "注册失败");
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 40px 20px;
  background: #fff;
}

.register-card {
  width: min(800px, 100%);
}

h1 {
  margin: 0 0 32px;
  text-align: center;
  color: #566079;
  font-family: Inter, "PingFang SC", "Microsoft YaHei", sans-serif;
  font-size: 32px;
  letter-spacing: 4px;
}

:deep(.el-form-item) {
  margin-bottom: 22px;
}

:deep(.el-form-item__label) {
  width: 100%;
  justify-content: center;
  margin-bottom: 12px;
  color: #333;
  font-size: 14px;
}

:deep(.el-input__wrapper) {
  min-height: 56px;
  border-radius: 8px;
  background: #f0f0f0;
  box-shadow: none;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-input__wrapper:has(input:not(:placeholder-shown))) {
  background: #e6f0ff;
}

.register-submit {
  width: 100%;
  height: 48px;
  border: 0;
  border-radius: 6px;
  background: #993380;
  color: #fff;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
}

.register-submit:hover {
  background: #7f2468;
}

.login-link {
  display: block;
  margin-top: 16px;
  text-align: center;
  color: #993380;
  font-weight: 800;
}
</style>
