<template>
  <ClientLayout>
    <section class="client-panel publish-panel">
      <PageTitle title="发布学习交流" />
      <el-form label-position="top">
        <el-form-item label="标题"><el-input v-model="form.title" placeholder="请输入交流标题" /></el-form-item>
        <el-form-item label="分类"><el-input v-model="form.category" placeholder="如：学习经验、课程讨论" /></el-form-item>
        <el-form-item label="标签"><el-input v-model="form.tag" placeholder="如：数学、英语、错题本" /></el-form-item>
        <el-form-item label="主要内容"><el-input v-model="form.description" type="textarea" :rows="6" placeholder="请输入主要内容" /></el-form-item>
        <button class="primary-btn" type="button" @click="publish">发布</button>
      </el-form>
    </section>
  </ClientLayout>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { reactive } from "vue";
import { useRouter } from "vue-router";
import ClientLayout from "../components/ClientLayout.vue";
import PageTitle from "../components/PageTitle.vue";
import { addRow, currentUser } from "../services/store";

const router = useRouter();
const form = reactive({ title: "", category: "", tag: "", description: "" });

function publish() {
  if (!form.title || !form.description) {
    ElMessage.warning("请填写标题和主要内容");
    return;
  }
  const user = currentUser() || { nickname: "游客", username: "guest" };
  addRow("forums", {
    title: form.title,
    category: form.category || "学习交流",
    tag: form.tag,
    description: form.description,
    author: user.nickname || user.username,
    nickname: user.nickname || user.username,
    image: "https://dummyimage.com/640x360/993380/ffffff&text=Forum",
    cover: "https://dummyimage.com/640x360/993380/ffffff&text=Forum",
    date: new Date().toISOString().slice(0, 10),
    create_time: new Date().toLocaleString("zh-CN", { hour12: false }).replace(/\//g, "-"),
    update_time: new Date().toLocaleString("zh-CN", { hour12: false }).replace(/\//g, "-"),
    likes: 0,
    hits: 0,
    istop: "否"
  });
  ElMessage.success("发布成功");
  router.push("/forum");
}
</script>

<style scoped>
.publish-panel {
  max-width: 860px;
  margin-left: auto;
  margin-right: auto;
}
</style>
