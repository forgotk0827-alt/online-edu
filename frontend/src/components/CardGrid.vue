<template>
  <div class="card-grid">
    <article v-for="item in items" :key="item.id" class="paper-card" @click="$emit('select', item)">
      <img :src="item.image || item.cover_image" :alt="item.title" />
      <div class="card-date">{{ item.date || item.create_time }}</div>
      <div class="wave"></div>
      <h3 class="card-title">{{ item.title }}</h3>
      <div class="card-meta">
        <span>{{ item.author || item.category || "平台" }}</span>
        <span>♥ {{ item.praise_len || 0 }} ｜ 👁 {{ item.hits || 0 }}</span>
      </div>
      <div v-if="showActions" class="card-actions" @click.stop>
        <button class="ghost-btn like" @click="$emit('like', item)">{{ item.liked ? "取消点赞" : "点赞" }} {{ item.praise_len || 0 }}</button>
        <button class="ghost-btn collect" @click="$emit('favorite', item)">{{ item.favorited ? "取消收藏" : "收藏" }} {{ item.collect_len || 0 }}</button>
      </div>
    </article>
  </div>
</template>

<script setup>
defineProps({
  items: { type: Array, default: () => [] },
  showActions: { type: Boolean, default: false }
});

defineEmits(["select", "like", "favorite"]);
</script>

<style scoped>
.card-actions {
  display: flex;
  gap: 10px;
  margin-top: 12px;
}

.ghost-btn {
  flex: 1;
  height: 34px;
  border: 1px solid #e6d4e6;
  border-radius: 6px;
  background: #fff;
  color: #993380;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.ghost-btn:hover {
  background: #fff5f8;
}
</style>
