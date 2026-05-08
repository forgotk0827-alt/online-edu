<template>
  <ClientLayout>
    <section class="client-panel">
      <PageTitle title="教育资讯" />
      <div class="toolbar">
        <el-input v-model="keyword" placeholder="搜索教育新闻" clearable />
        <el-select v-model="category" placeholder="分类筛选" clearable>
          <el-option label="政策" value="政策" />
          <el-option label="学校" value="学校" />
          <el-option label="科技" value="科技" />
        </el-select>
        <el-select v-model="sort" placeholder="排序" clearable>
          <el-option label="浏览量优先" value="hits" />
          <el-option label="点赞量优先" value="likes" />
        </el-select>
        <button class="primary-btn" @click="page = 1">搜索</button>
      </div>

      <CardGrid :items="paged" showActions @select="openDetail" @like="handleLike" @favorite="handleFavorite" />
      <el-pagination class="pagination" layout="prev, pager, next" :total="sorted.length" :page-size="6" v-model:current-page="page" />
    </section>

    <el-dialog v-model="dialog" title="资讯详情" width="min(720px, 92vw)">
      <h3>{{ current?.title }}</h3>
      <p class="detail-text">{{ current?.content || "这里展示教育资讯正文内容，用户可查看详情并发表评论。" }}</p>
      <div class="comment-list">
        <strong>评论区</strong>
        <p v-if="comments.length === 0" class="detail-text">暂无评论</p>
        <div v-for="item in comments" :key="item.id" class="comment-item">
          <span>{{ item.nickname }}：{{ item.content }}</span>
          <small>{{ item.create_time }}</small>
        </div>
      </div>
      <el-input v-model="comment" type="textarea" :rows="4" placeholder="请输入评论" />
      <template #footer>
        <button class="primary-btn" @click="submitComment">发表评论</button>
      </template>
    </el-dialog>
  </ClientLayout>
</template>

<script setup>
import { computed, ref } from "vue";
import CardGrid from "../components/CardGrid.vue";
import ClientLayout from "../components/ClientLayout.vue";
import PageTitle from "../components/PageTitle.vue";
import { addComment, addFavorite, addLike, currentUser, findFavorite, findLike, getComments, removeFavorite, removeLike, store } from "../services/store";

const keyword = ref("");
const category = ref("");
const sort = ref("");
const page = ref(1);
const dialog = ref(false);
const current = ref(null);
const comment = ref("");

const filtered = computed(() => store.news.filter((item) => (!keyword.value || item.title?.includes(keyword.value)) && (!category.value || item.category === category.value)));
const sorted = computed(() => [...filtered.value].sort((a, b) => (sort.value ? (b[sort.value] || 0) - (a[sort.value] || 0) : 0)));
const paged = computed(() =>
  sorted.value.slice((page.value - 1) * 6, page.value * 6).map((item) => ({
    ...item,
    liked: !!findLike("news", item.id, currentUser()?.username),
    favorited: !!findFavorite("news", item.id, currentUser()?.username)
  }))
);
const comments = computed(() => (current.value ? getComments("news", current.value.id) : []));

function openDetail(item) {
  current.value = item;
  dialog.value = true;
}

function handleLike(item) {
  const existing = findLike("news", item.id, currentUser()?.username);
  if (existing) {
    removeLike(existing.id);
    return;
  }
  addLike("news", item.id, item.title);
}

function handleFavorite(item) {
  const existing = findFavorite("news", item.id, currentUser()?.username);
  if (existing) {
    removeFavorite(existing.id);
    return;
  }
  addFavorite("news", item.id, item.title);
}

function submitComment() {
  if (!comment.value.trim() || !current.value) return;
  addComment("news", current.value.id, comment.value.trim());
  comment.value = "";
}
</script>

<style scoped>
.detail-text {
  color: #666;
  line-height: 1.8;
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
