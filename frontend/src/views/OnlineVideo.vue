<template>
  <ClientLayout>
    <section class="client-panel">
      <PageTitle title="在线视频" />
      <div class="toolbar">
        <el-input v-model="keyword" placeholder="视频名称搜索" clearable />
        <el-input v-model="type" placeholder="视频类型搜索" clearable />
        <button class="primary-btn" @click="page = 1">搜索</button>
        <button class="primary-btn" @click="desc = !desc">排序</button>
        <label class="upload-btn">
          上传模拟视频
          <input type="file" accept="video/*" @change="handleUpload" />
        </label>
      </div>

      <div class="upload-tip">
        可选择本地 mp4、webm、ogg 等浏览器支持的视频文件，系统会模拟添加到在线视频列表并直接播放。
      </div>

      <div class="table-wrap">
        <el-table class="client-table" :data="paged" border>
          <el-table-column prop="name" label="视频名称" min-width="220" />
          <el-table-column prop="type" label="视频类型" width="160" />
          <el-table-column prop="duration" label="视频时长" width="140" />
          <el-table-column label="视频海报" width="180">
            <template #default="{ row }">
              <img class="thumb" :src="row.poster" :alt="row.name" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="170">
            <template #default="{ row }">
              <button class="primary-btn" @click="playVideo(row)">播放</button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <el-pagination class="pagination" layout="prev, pager, next" :total="filtered.length" :page-size="5" v-model:current-page="page" />
    </section>

    <el-dialog v-model="dialog" :title="current?.name || '视频播放'" width="min(860px, 94vw)" @closed="stopVideo">
      <video v-if="current?.src" ref="videoRef" class="player" :src="current.src" controls autoplay />
      <div v-else class="mock-player">
        <img :src="current?.poster" :alt="current?.name" />
        <p>这是模拟视频数据，可上传本地视频进行真实播放测试。</p>
      </div>
      <div class="comment-list">
        <strong>评论区</strong>
        <p v-if="comments.length === 0" class="empty-text">暂无评论</p>
        <div v-for="item in comments" :key="item.id" class="comment-item">
          <span>{{ item.nickname }}：{{ item.content }}</span>
          <small>{{ item.create_time }}</small>
        </div>
      </div>
      <el-input v-model="comment" type="textarea" :rows="4" placeholder="请输入视频评论" />
      <template #footer><button class="primary-btn" @click="submitComment">发表评论</button></template>
    </el-dialog>
  </ClientLayout>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from "vue";
import ClientLayout from "../components/ClientLayout.vue";
import PageTitle from "../components/PageTitle.vue";
import { addComment, addRow, getComments, store } from "../services/store";

const keyword = ref("");
const type = ref("");
const desc = ref(false);
const page = ref(1);
const dialog = ref(false);
const current = ref(null);
const videoRef = ref();
const comment = ref("");
const uploadedUrls = [];

const poster = "https://dummyimage.com/640x360/993380/ffffff&text=Uploaded+Video";
const videoRows = computed(() => [
  ...store.videos.map((item) => ({
    ...item,
    name: item.name || item.video_name,
    type: item.type || item.video_type,
    duration: item.duration || item.video_duration,
    poster: item.poster || item.video_poster,
    src: item.src || item.video_url || ""
  }))
]);

const filtered = computed(() =>
  [...videoRows.value]
    .filter((item) => (!keyword.value || item.name.includes(keyword.value)) && (!type.value || item.type.includes(type.value)))
    .sort((a, b) => (desc.value ? b.id - a.id : a.id - b.id))
);

const paged = computed(() => filtered.value.slice((page.value - 1) * 5, page.value * 5));
const comments = computed(() => (current.value ? getComments("video", current.value.id) : []));

function handleUpload(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  const src = URL.createObjectURL(file);
  uploadedUrls.push(src);
  const row = {
    id: Date.now(),
    teacher: "本地测试",
    teacher_user: "本地测试",
    teachers_name: "本地测试",
    name: file.name.replace(/\.[^.]+$/, ""),
    video_name: file.name.replace(/\.[^.]+$/, ""),
    duration: "本地视频",
    video_duration: "本地视频",
    origin: "模拟上传",
    video_origin: "模拟上传",
    type: file.type || "video",
    video_type: file.type || "video",
    poster,
    video_poster: poster,
    video_url: src,
    src
  };
  addRow("videos", row);
  page.value = 1;
  event.target.value = "";
}

function playVideo(row) {
  current.value = row;
  dialog.value = true;
}

function stopVideo() {
  if (videoRef.value) {
    videoRef.value.pause();
    videoRef.value.currentTime = 0;
  }
}
function submitComment() {
  if (!comment.value.trim() || !current.value) return;
  addComment("video", current.value.id, comment.value.trim());
  comment.value = "";
}

onBeforeUnmount(() => {
  uploadedUrls.forEach((url) => URL.revokeObjectURL(url));
});
</script>

<style scoped>
.upload-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 10px 20px;
  border-radius: 6px;
  background: #993380;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.upload-btn:hover {
  background: #7f2468;
}

.upload-btn input {
  display: none;
}

.upload-tip {
  margin: -10px 0 18px;
  color: #666;
  font-size: 14px;
}

.player {
  width: 100%;
  max-height: 68vh;
  display: block;
  border-radius: 8px;
  background: #111;
}

.mock-player {
  display: grid;
  gap: 16px;
  place-items: center;
  padding: 20px;
  color: #666;
  text-align: center;
}

.mock-player img {
  width: min(640px, 100%);
  border-radius: 8px;
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

.comment-item small,
.empty-text {
  color: #999;
}
</style>
