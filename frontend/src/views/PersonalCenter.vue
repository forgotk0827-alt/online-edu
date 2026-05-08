<template>
  <ClientLayout>
    <section class="client-panel">
      <div class="profile-tabs">
        <button v-for="item in tabs" :key="item" :class="{ active: active === item }" @click="active = item">{{ item }}</button>
      </div>
      <PageTitle title="欢迎来到个人中心" />
      <div class="profile-box">
        <template v-if="active === '个人首页'">
          <p>用户名：{{ user?.username || '未登录用户' }}</p>
          <p>身份：{{ roleText }}</p>
        </template>
        <template v-else-if="active === '购买资料'">
          <div v-for="item in purchases" :key="item.id" class="profile-item">{{ item.title }} <small>{{ item.create_time }}</small></div>
          <p v-if="purchases.length === 0">暂无购买资料</p>
        </template>
        <template v-else-if="active === '收藏'">
          <div v-for="item in favorites" :key="item.id" class="profile-item">
            <span>{{ item.targetLabel || '内容' }} - {{ item.title }}</span> <button @click="removeFavorite(item.id)">删除</button>
          </div>
          <p v-if="favorites.length === 0">暂无收藏内容</p>
        </template>
        <template v-else-if="active === '点赞'">
          <div v-for="item in likes" :key="item.id" class="profile-item">
            <span>{{ item.targetLabel || '内容' }} - {{ item.title }}</span> <button @click="removeLike(item.id)">删除</button>
          </div>
          <p v-if="likes.length === 0">暂无点赞内容</p>
        </template>
        <template v-else-if="active === '评论管理'">
          <div v-for="item in comments" :key="item.id" class="profile-item">
            <span>{{ item.targetLabel || '内容' }} - {{ item.targetTitle || item.targetId }}：{{ item.content }}</span> <button @click="removeComment(item.id)">删除</button>
          </div>
          <p v-if="comments.length === 0">暂无评论内容</p>
        </template>
        <template v-else-if="active === '教师课程资料'">
          <router-link class="primary-btn teacher-link" to="/teacher/courses">进入教师课程资料管理</router-link>
        </template>
        <template v-else>
          <p>当前栏目：{{ active }}</p>
          <p>可查看和管理与该栏目相关的学习记录。</p>
        </template>
      </div>
    </section>
  </ClientLayout>
</template>

<script setup>
import { computed, ref } from "vue";
import ClientLayout from "../components/ClientLayout.vue";
import PageTitle from "../components/PageTitle.vue";
import { currentUser, removeComment, removeFavorite, removeLike, store } from "../services/store";

const user = currentUser();
const roleTextMap = { student: "学生", teacher: "教师", admin: "管理员" };
const roleText = computed(() => roleTextMap[user?.role] || "未登录");
const purchases = computed(() => (Array.isArray(store.purchases) ? store.purchases : []));
const favorites = computed(() => (Array.isArray(store.favorites) ? store.favorites : []));
const likes = computed(() => (Array.isArray(store.likes) ? store.likes : []));
const comments = computed(() => (Array.isArray(store.comments) ? store.comments : []));
const baseTabs = ["个人首页", "课程资料", "购买资料", "在线视频", "学习交流", "收藏", "点赞", "评论管理"];
const tabs = user?.role === "teacher" ? [...baseTabs, "教师课程资料"] : baseTabs;
const active = ref(tabs[0]);
</script>

<style scoped>
.profile-tabs {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.profile-tabs button {
  flex: 0 0 auto;
  height: 40px;
  padding: 0 18px;
  border: 0;
  border-radius: 6px;
  background: #d4c2e1;
  color: #333;
  font-weight: 700;
}

.profile-tabs .active {
  background: #993380;
  color: #fff;
}

.profile-box {
  text-align: center;
  color: #666;
}

.profile-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  max-width: 760px;
  margin: 10px auto;
  padding: 12px;
  border-radius: 6px;
  background: #fff5f8;
}

.profile-item button {
  border: 0;
  border-radius: 6px;
  padding: 6px 12px;
  background: #993380;
  color: #fff;
}

.teacher-link {
  display: inline-flex;
  align-items: center;
  margin-top: 10px;
}
</style>
