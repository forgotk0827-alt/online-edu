<template>
  <ClientLayout>
    <section class="client-panel">
      <PageTitle title="学习交流" />
      <div class="toolbar">
        <el-select v-model="type" placeholder="分类筛选" clearable>
          <el-option label="学习经验" value="学习" />
          <el-option label="课程讨论" value="课程" />
        </el-select>
        <el-input v-model="keyword" placeholder="请输入帖子关键词" clearable />
        <button class="primary-btn" @click="page = 1">搜索</button>
        <router-link class="primary-btn link-btn" to="/forum/publish">发布</router-link>
      </div>

      <CardGrid :items="paged" showActions @select="openDetail" @like="handleLike" @favorite="handleFavorite" />
      <el-pagination class="pagination" layout="prev, pager, next" :total="filtered.length" :page-size="6" v-model:current-page="page" />
    </section>

    <el-dialog v-model="dialog" title="学习交流详情" width="min(760px, 92vw)">
      <h3>{{ current?.title }}</h3>
      <p class="detail-text">{{ current?.description || "这里展示学习交流的主要内容，用户可以查看详情并发表评论。" }}</p>
      <div class="comment-list">
        <strong>评论区</strong>
        <p v-if="comments.length === 0" class="empty-text">暂无评论</p>
        <div v-for="item in comments" :key="item.id" class="comment-item">
          <span>{{ item.nickname }}：{{ item.content }}</span>
          <small>{{ item.create_time }}</small>
        </div>
      </div>
      <el-input v-model="comment" type="textarea" :rows="4" placeholder="请输入评论内容" />
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
const type = ref("");
const page = ref(1);
const dialog = ref(false);
const current = ref(null);
const comment = ref("");

const filtered = computed(() =>
  store.forums.filter(
    (item) =>
      (!keyword.value || item.title?.includes(keyword.value)) &&
      (!type.value || item.category?.includes(type.value) || item.type?.includes(type.value) || item.title?.includes(type.value))
  )
);
const paged = computed(() =>
  filtered.value.slice((page.value - 1) * 6, page.value * 6).map((item) => ({
    ...item,
    liked: !!findLike("forum", item.id, currentUser()?.username),
    favorited: !!findFavorite("forum", item.id, currentUser()?.username)
  }))
);
const comments = computed(() => (current.value ? getComments("forum", current.value.id) : []));

function openDetail(item) {
  current.value = item;
  dialog.value = true;
}

function handleLike(item) {
  const existing = findLike("forum", item.id, currentUser()?.username);
  if (existing) {
    removeLike(existing.id);
    return;
  }
  addLike("forum", item.id, item.title);
}

function handleFavorite(item) {
  const existing = findFavorite("forum", item.id, currentUser()?.username);
  if (existing) {
    removeFavorite(existing.id);
    return;
  }
  addFavorite("forum", item.id, item.title);
}

function submitComment() {
  if (!comment.value.trim() || !current.value) return;
  addComment("forum", current.value.id, comment.value.trim());
  comment.value = "";
}
</script>

<style scoped>
.link-btn {
  display: inline-flex;
  align-items: center;
}

.detail-text,
.empty-text {
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
  color: #333;
}

.comment-item small {
  color: #999;
}
</style>
