<template>
  <section class="admin-panel">
    <h1 class="admin-title">轮播图管理</h1>
    <div class="admin-toolbar">
      <el-input v-model="keyword" placeholder="标题搜索" clearable />
      <button class="admin-btn" @click="page = 1">查询</button>
      <button class="admin-btn" @click="deleteSelected">删除</button>
      <button class="admin-btn" @click="openAdd">添加</button>
    </div>

    <div class="table-wrap">
      <el-table class="admin-table" :data="pagedRows" border @selection-change="selectedRows = $event">
        <el-table-column type="selection" width="52" />
        <el-table-column prop="image" label="轮播图" width="220">
          <template #default="{ row }">
            <img class="thumb banner-thumb" :src="row.image" :alt="row.title" />
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="link" label="链接" min-width="200" />
        <el-table-column prop="sort" label="排序" width="100" />
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <button class="admin-btn small" @click="showDetail(row)">详情</button>
            <button class="admin-btn small" @click="removeOne(row.id)">删除</button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-pagination
      class="pagination"
      layout="total, sizes, prev, pager, next, jumper"
      :total="filtered.length"
      v-model:current-page="page"
      v-model:page-size="pageSize"
      :page-sizes="[5, 10, 20]"
    />

    <el-dialog v-model="dialogVisible" title="添加轮播图" width="min(640px, 92vw)">
      <div class="banner-upload">
        <label class="admin-btn upload-trigger">
          选择本地图片
          <input type="file" accept="image/*" @change="handleUpload" />
        </label>
        <p class="upload-hint">图片会上传到后端本地 media 目录，保存后同步显示到前台首页。</p>
        <div v-if="form.image" class="banner-preview">
          <img :src="form.image" alt="轮播图预览" />
        </div>
      </div>

      <el-form label-width="100px">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="请输入轮播图标题" />
        </el-form-item>
        <el-form-item label="链接">
          <el-input v-model="form.link" placeholder="请输入跳转链接" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input v-model="form.sort" placeholder="数字越小越靠前" />
        </el-form-item>
      </el-form>

      <template #footer>
        <button class="admin-btn" @click="dialogVisible = false">取消</button>
        <button class="admin-btn" @click="confirmAdd">确认添加</button>
      </template>
    </el-dialog>

    <el-dialog v-model="detailVisible" title="轮播图详情" width="min(600px, 92vw)">
      <el-descriptions v-if="current" :column="1" border>
        <el-descriptions-item label="标题">{{ current.title }}</el-descriptions-item>
        <el-descriptions-item label="链接">{{ current.link }}</el-descriptions-item>
        <el-descriptions-item label="排序">{{ current.sort }}</el-descriptions-item>
        <el-descriptions-item label="图片">
          <img class="detail-banner" :src="current.image" :alt="current.title" />
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </section>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { computed, reactive, ref } from "vue";
import { api } from "../../services/api";
import { refreshBanners, removeRows, store } from "../../services/store";

const keyword = ref("");
const page = ref(1);
const pageSize = ref(10);
const selectedRows = ref([]);
const dialogVisible = ref(false);
const detailVisible = ref(false);
const current = ref(null);
const form = reactive({ image: "", title: "", link: "/", sort: 0 });

const filtered = computed(() => (store.banners || []).filter((item) => !keyword.value || item.title?.includes(keyword.value)));
const pagedRows = computed(() => filtered.value.slice((page.value - 1) * pageSize.value, page.value * pageSize.value));

function openAdd() {
  form.image = "";
  form.title = "";
  form.link = "/";
  form.sort = 0;
  dialogVisible.value = true;
}

function showDetail(row) {
  current.value = row;
  detailVisible.value = true;
}

async function deleteSelected() {
  if (!selectedRows.value.length) {
    ElMessage.warning("请先选择要删除的轮播图");
    return;
  }
  await removeRows("banners", selectedRows.value.map((item) => item.id));
  await refreshBanners();
  selectedRows.value = [];
  ElMessage.success("已删除选中轮播图");
}

async function removeOne(id) {
  await removeRows("banners", [id]);
  await refreshBanners();
  ElMessage.success("已删除轮播图");
}

async function handleUpload(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  try {
    const fd = new FormData();
    fd.append("file", file);
    const { data } = await api.post("/upload/", fd, { headers: { "Content-Type": "multipart/form-data" } });
    const path = data?.data?.path || data?.path || "";
    if (!path) throw new Error("上传成功但未返回图片地址");
    form.image = path;
    ElMessage.success("上传成功");
  } catch (error) {
    form.image = "";
    ElMessage.error(error?.response?.data?.message || error?.message || "图片上传失败，请检查后端上传接口");
  } finally {
    event.target.value = "";
  }
}

async function confirmAdd() {
  if (!form.image) {
    ElMessage.warning("请先上传轮播图图片");
    return;
  }
  if (form.image.startsWith("data:")) {
    ElMessage.error("请使用本地上传后的图片地址，不能保存 base64 预览地址");
    return;
  }
  try {
    await api.post("/admin/banners/", {
      image: form.image,
      title: form.title || "轮播图",
      link: form.link || "/",
      sort: Number(form.sort || 0)
    });
    await refreshBanners();
    dialogVisible.value = false;
    ElMessage.success("轮播图已添加，并同步到前台");
  } catch (error) {
    ElMessage.error(error?.response?.data?.message || "轮播图保存失败，请确认已登录管理员账号");
  }
}
</script>

<style scoped>
.banner-upload {
  display: grid;
  gap: 12px;
  margin-bottom: 16px;
}

.upload-trigger {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.upload-trigger input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.upload-hint {
  margin: 0;
  color: #666;
  font-size: 13px;
}

.banner-preview {
  padding: 12px;
  border: 1px solid #d4d4ff;
  border-radius: 6px;
  background: #fff;
}

.banner-preview img,
.banner-thumb,
.detail-banner {
  width: 100%;
  display: block;
  border-radius: 6px;
  object-fit: cover;
}

.banner-thumb {
  height: 84px;
}

.detail-banner {
  max-height: 240px;
}
</style>
