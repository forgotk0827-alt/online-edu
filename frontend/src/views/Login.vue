<template>
  <main class="login-page">
    <section class="login-card">
      <h1>Login</h1>
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent>
        <el-form-item label="用户名" prop="username" required>
          <el-input v-model.trim="form.username" placeholder="请输入用户名" />
          <p v-if="form.username" class="valid-text">校验通过</p>
        </el-form-item>

        <el-form-item label="密码" prop="password" required>
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
          <p v-if="form.password" class="valid-text">校验通过</p>
        </el-form-item>

        <el-form-item label="验证" prop="captcha" required>
          <div class="captcha-row">
            <el-input v-model.trim="form.captcha" placeholder="不区分大小写" />
            <button class="captcha-image" type="button" @click="refreshCaptcha" :title="'点击刷新验证码'">
              <img :src="captchaImage" alt="验证码" />
            </button>
          </div>
          <p v-if="captchaPassed" class="valid-text">校验通过</p>
        </el-form-item>

        <button class="login-submit" type="button" @click="submit">登录</button>
        <div class="secondary-actions">
          <button class="secondary-btn" type="button">找回密码</button>
          <router-link class="secondary-btn" to="/register">创建一个账户吧！</router-link>
        </div>
      </el-form>
    </section>
  </main>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { emitAuthChange, setAuth } from "../services/auth";
import { api } from "../services/api";
import { loadDatabaseData, syncUser } from "../services/store";

const router = useRouter();
const formRef = ref();
const form = reactive({ username: "", password: "", captcha: "" });
const captchaCode = ref("");
const captchaImage = ref("");
const captchaPassed = computed(() => form.captcha && form.captcha.toLowerCase() === captchaCode.value.toLowerCase());

const rules = {
  username: [
    { required: true, message: "用户名不能为空", trigger: "blur" },
    { pattern: /^[A-Za-z0-9_]{3,20}$/, message: "用户名需为 3-20 位字母、数字或下划线", trigger: "blur" }
  ],
  password: [
    { required: true, message: "密码不能为空", trigger: "blur" },
    { min: 6, max: 20, message: "密码长度为 6-20 位", trigger: "blur" }
  ],
  captcha: [
    { required: true, message: "验证码不能为空", trigger: "blur" },
    {
      validator: (_, value, callback) => {
        if (String(value).toLowerCase() === captchaCode.value.toLowerCase()) callback();
        else callback(new Error("验证码不正确"));
      },
      trigger: "blur"
    }
  ]
};

function makeCode() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  return Array.from({ length: 4 }, () => chars[Math.floor(Math.random() * chars.length)]).join("");
}

function refreshCaptcha() {
  captchaCode.value = makeCode();
  const text = captchaCode.value;
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="110" height="48" viewBox="0 0 110 48">
      <rect width="110" height="48" rx="6" fill="#ffffff"/>
      <path d="M8 33 C24 4, 45 50, 66 15 S93 42, 105 10" fill="none" stroke="#B377B3" stroke-width="2"/>
      <path d="M5 13 L104 36" stroke="#E6D4E6" stroke-width="1.5"/>
      <text x="15" y="32" font-size="22" font-family="Inter, Microsoft YaHei, sans-serif" font-weight="800" fill="#993380" transform="rotate(-8 55 24)">${text}</text>
    </svg>`;
  captchaImage.value = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
}

async function submit() {
  await formRef.value.validate();
  try {
    const { data } = await api.post("/auth/login/", {
      username: form.username,
      password: form.password
    });
    if (data.code && data.code !== 200) throw new Error(data.message);
    setAuth("client", data.data.token, data.data.user || {});
    if (data.data.user?.username) {
      syncUser(data.data.user);
    }
    loadDatabaseData();
    emitAuthChange();
    ElMessage.success("登录成功");
    router.push("/");
  } catch (error) {
    refreshCaptcha();
    ElMessage.error(error.response?.data?.message || error.message || "登录失败");
  }
}

onMounted(refreshCaptcha);
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 36px 20px;
  background: linear-gradient(135deg, #fff5f8 0%, #ffffff 52%, #f6e7f2 100%);
}

.login-card {
  width: min(600px, 100%);
  padding: 34px 40px 28px;
  border-radius: 4px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(153, 51, 128, 0.14);
}

h1 {
  margin: 0 0 28px;
  text-align: center;
  color: #566079;
  font-family: Inter, "PingFang SC", "Microsoft YaHei", sans-serif;
  font-size: 28px;
  letter-spacing: 4px;
}

:deep(.el-form-item) {
  margin-bottom: 18px;
}

:deep(.el-form-item__label) {
  width: 100%;
  justify-content: center;
  color: #333;
  font-size: 14px;
}

:deep(.el-form-item.is-required .el-form-item__label::before) {
  color: #ff4d4f;
}

:deep(.el-input__wrapper) {
  min-height: 48px;
  border-radius: 6px;
  background: #f0f0f0;
  box-shadow: none;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-input__wrapper:has(input:not(:placeholder-shown))) {
  background: #e6f0ff;
}

.valid-text {
  width: 100%;
  margin: 6px 0 0;
  color: #20a162;
  font-size: 12px;
  line-height: 1;
}

.captcha-row {
  display: grid;
  grid-template-columns: 1fr 110px;
  gap: 12px;
  width: 100%;
}

.captcha-image {
  height: 48px;
  padding: 0;
  border: 1px solid #e6d4e6;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  overflow: hidden;
}

.captcha-image img {
  width: 100%;
  height: 100%;
  display: block;
}

.login-submit,
.secondary-btn {
  height: 44px;
  border: 0;
  border-radius: 4px;
  background: #993380;
  color: #fff;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
}

.login-submit {
  width: 100%;
  margin-top: 4px;
}

.login-submit:hover,
.secondary-btn:hover {
  background: #7f2468;
}

.secondary-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-top: 12px;
}

.secondary-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 520px) {
  .login-card {
    padding: 28px 20px 24px;
  }

  .captcha-row,
  .secondary-actions {
    grid-template-columns: 1fr;
  }
}
</style>
