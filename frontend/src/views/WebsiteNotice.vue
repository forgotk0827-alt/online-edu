<template>
  <ClientLayout>
    <section class="client-panel">
      <PageTitle title="网站公告" />
      <div class="toolbar">
        <el-input v-model="keyword" placeholder="请输入公告标题" clearable />
        <el-select v-model="category" placeholder="公告分类" clearable>
          <el-option label="课程" value="课程" />
          <el-option label="服务" value="服务" />
          <el-option label="系统" value="系统" />
        </el-select>
        <el-select v-model="sort" placeholder="排序" clearable>
          <el-option label="最新发布" value="new" />
          <el-option label="最早发布" value="old" />
        </el-select>
        <button class="primary-btn" @click="page = 1">搜索</button>
      </div>

      <div class="notice-list">
        <article v-for="item in paged" :key="item.id" class="notice-item" @click="openDetail(item)">
          <div>
            <span class="notice-tag">{{ item.category }}</span>
            <h3>{{ item.title }}</h3>
            <p>{{ item.content || "公告详情用于展示平台通知、课程安排、系统维护和服务调整等信息。" }}</p>
          </div>
          <time>{{ item.create_time }}</time>
        </article>
      </div>

      <el-empty v-if="paged.length === 0" description="暂无公告" />
      <el-pagination class="pagination" layout="prev, pager, next" :total="filtered.length" :page-size="5" v-model:current-page="page" />
    </section>

    <el-dialog v-model="dialog" title="公告详情" width="min(680px, 92vw)">
      <h3>{{ current?.title }}</h3>
      <p class="notice-detail">{{ current?.content || "这里展示网站公告详情，用户可查看平台发布的课程通知、系统维护、服务说明等内容。" }}</p>
      <template #footer>
        <button class="primary-btn" @click="dialog = false">关闭</button>
      </template>
    </el-dialog>
  </ClientLayout>
</template>

<script setup>
import { computed, ref } from "vue";
import ClientLayout from "../components/ClientLayout.vue";
import PageTitle from "../components/PageTitle.vue";
import { store } from "../services/store";

const keyword = ref("");
const category = ref("");
const sort = ref("new");
const page = ref(1);
const dialog = ref(false);
const current = ref(null);

const filtered = computed(() => {
  const rows = store.notices.filter((item) => {
    const matchKeyword = !keyword.value || item.title.includes(keyword.value);
    const matchCategory = !category.value || item.category === category.value;
    return matchKeyword && matchCategory;
  });
  return [...rows].sort((a, b) => {
    if (sort.value === "old") return String(a.create_time).localeCompare(String(b.create_time));
    return String(b.create_time).localeCompare(String(a.create_time));
  });
});

const paged = computed(() => filtered.value.slice((page.value - 1) * 5, page.value * 5));

function openDetail(item) {
  current.value = item;
  dialog.value = true;
}
</script>

<style scoped>
.notice-list {
  display: grid;
  gap: 16px;
}

.notice-item {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 16px;
  border: 1px solid #e6d4e6;
  border-radius: 8px;
  background: #fffafd;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.notice-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(153, 51, 128, 0.1);
}

.notice-tag {
  display: inline-flex;
  margin-bottom: 8px;
  padding: 4px 10px;
  border-radius: 999px;
  background: #e6d4e6;
  color: #993380;
  font-size: 13px;
  font-weight: 700;
}

.notice-item h3 {
  margin: 0 0 8px;
  font-size: 16px;
}

.notice-item p,
.notice-detail {
  margin: 0;
  color: #666;
  line-height: 1.8;
}

.notice-item time {
  flex: 0 0 auto;
  color: #b377b3;
  font-size: 14px;
}

@media (max-width: 768px) {
  .notice-item {
    flex-direction: column;
  }
}
</style>
