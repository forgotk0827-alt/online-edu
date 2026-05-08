<template>
  <ClientLayout>
    <section class="client-panel">
      <PageTitle title="课程资料" />
      <div class="toolbar">
        <el-input v-model="keyword" placeholder="课程名称搜索" clearable />
        <el-input v-model="type" placeholder="教学类型搜索" clearable />
        <button class="primary-btn">搜索</button>
        <button class="primary-btn" @click="sortByPrice">排序</button>
      </div>
      <div class="table-wrap">
        <el-table class="client-table" :data="filtered" border>
          <el-table-column prop="name" label="课程名称" min-width="220" />
          <el-table-column prop="type" label="教学类型" width="160" />
          <el-table-column prop="price" label="价格" width="120" />
          <el-table-column label="课程图片" width="180"><template #default="{ row }"><img class="thumb" :src="row.image" :alt="row.name" /></template></el-table-column>
          <el-table-column label="操作" width="150"><template #default="{ row }"><button class="primary-btn" @click="openCourse(row)">详情</button></template></el-table-column>
        </el-table>
      </div>
    </section>
    <el-dialog v-model="dialog" title="课程资料详情" width="min(860px, 94vw)">
      <h3>{{ current?.name || current?.course_name }}</h3>
      <p class="detail-text">
        当前设备：{{ deviceText }}。系统已根据设备类型选择{{ isMobile ? "移动端自适应清晰度" : "电脑端高清播放" }}方式。
      </p>
      <video class="course-player" controls :poster="current?.image || current?.course_images"></video>
      <div class="comment-list">
        <strong>互动评论</strong>
        <p v-if="comments.length === 0" class="detail-text">暂无评论</p>
        <div v-for="item in comments" :key="item.id" class="comment-item">
          <span>{{ item.nickname }}：{{ item.content }}</span>
          <small>{{ item.create_time }}</small>
        </div>
      </div>
      <el-input v-model="comment" type="textarea" :rows="4" placeholder="请输入课程评论" />
      <template #footer>
        <button class="primary-btn" @click="buyCourse">购买资料</button>
        <button class="primary-btn" @click="submitComment">发表评论</button>
      </template>
    </el-dialog>
  </ClientLayout>
</template>

<script setup>
import { computed, ref } from "vue";
import ClientLayout from "../components/ClientLayout.vue";
import PageTitle from "../components/PageTitle.vue";
import { addComment, addFavorite, addPurchase, getComments, store } from "../services/store";

const keyword = ref("");
const type = ref("");
const desc = ref(false);
const dialog = ref(false);
const current = ref(null);
const comment = ref("");
const isMobile = computed(() => window.innerWidth < 768);
const deviceText = computed(() => (isMobile.value ? "手机端" : "电脑端"));
const filtered = computed(() =>
  [...store.courses]
    .filter((item) => (!keyword.value || item.name?.includes(keyword.value) || item.course_name?.includes(keyword.value)) && (!type.value || item.type?.includes(type.value) || item.teaching_type?.includes(type.value)))
    .sort((a, b) => (desc.value ? (b.price || b.course_prices || 0) - (a.price || a.course_prices || 0) : (a.price || a.course_prices || 0) - (b.price || b.course_prices || 0)))
);
function sortByPrice() {
  desc.value = !desc.value;
}
const comments = computed(() => (current.value ? getComments("course", current.value.id) : []));
function openCourse(row) {
  current.value = row;
  dialog.value = true;
}
function submitComment() {
  if (!comment.value.trim()) return;
  addComment("course", current.value.id, comment.value.trim());
  comment.value = "";
}
function buyCourse() {
  if (!current.value) return;
  addPurchase(current.value);
  addFavorite("course", current.value.id, current.value.name || current.value.course_name);
}
</script>

<style scoped>
.detail-text {
  color: #666;
  line-height: 1.8;
}
.course-player {
  width: 100%;
  min-height: 260px;
  border-radius: 8px;
  background: #111;
}
.comment-list {
  display: grid;
  gap: 10px;
  margin: 18px 0;
}
.comment-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px;
  border-radius: 6px;
  background: #fff5f8;
}
.comment-item small {
  color: #999;
}
</style>
