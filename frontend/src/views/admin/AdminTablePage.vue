<template>
  <section class="admin-panel">
    <h1 class="admin-title">{{ pageTitle }}</h1>
    <div class="admin-toolbar">
      <el-input v-for="input in config.inputs" :key="input.key" v-model="filters[input.key]" :placeholder="input.label" clearable />
      <el-select v-if="config.select" v-model="filters.select" :placeholder="config.select" clearable>
        <el-option label="全部" value="" />
        <el-option v-for="option in selectOptions" :key="option" :label="option" :value="option" />
      </el-select>
      <el-date-picker v-if="config.date" v-model="filters.date" type="daterange" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" />
      <button class="admin-btn" @click="handleSearch">查询</button>
      <button class="admin-btn" @click="deleteSelected">删除</button>
      <button v-if="config.add" class="admin-btn" @click="showAdd">添加</button>
    </div>
    <div class="table-wrap">
      <el-table class="admin-table" :data="pagedRows" border @selection-change="selectedRows = $event">
        <el-table-column type="selection" width="52" />
        <el-table-column v-for="col in config.columns" :key="col.prop" :prop="col.prop" :label="col.label" :min-width="col.width || 130">
          <template v-if="col.image" #default="{ row }"><img class="thumb" :src="row[col.prop]" :alt="col.label" /></template>
        </el-table-column>
        <el-table-column label="操作" width="190">
          <template #default="{ row }">
            <button class="admin-btn small" @click="showDetail(row)">详情</button>
            <button v-if="config.comment" class="admin-btn small" @click="showComments(row)">查看评论</button>
            <button v-if="config.audit" class="admin-btn small" @click="showAudit(row)">审核</button>
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
      :page-sizes="[5, 10, 20, 50]"
    />

    <el-dialog v-model="detailVisible" :title="`${pageTitle}详情`" width="min(680px, 92vw)">
      <el-descriptions v-if="currentRow" :column="2" border>
        <el-descriptions-item v-for="col in detailFields" :key="col.prop" :label="col.label">
          <img v-if="col.image" class="thumb" :src="currentRow[col.prop]" :alt="col.label" />
          <span v-else>{{ currentRow[col.prop] || "-" }}</span>
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow.buy_time" label="购买时间">{{ currentRow.buy_time }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRow.pay_state" label="支付状态">{{ currentRow.pay_state }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <el-dialog v-model="auditVisible" title="订单审核" width="min(520px, 92vw)">
      <el-form v-if="currentRow" label-width="90px">
        <el-form-item label="课程名称">{{ currentRow.course_name }}</el-form-item>
        <el-form-item label="支付状态">
          <el-select v-model="auditForm.pay_state" placeholder="请选择支付状态">
            <el-option label="已支付" value="已支付" />
            <el-option label="待支付" value="待支付" />
            <el-option label="已取消" value="已取消" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <button class="admin-btn" @click="auditVisible = false">取消</button>
        <button class="admin-btn" @click="confirmAudit">确认订单</button>
      </template>
    </el-dialog>

    <el-dialog v-model="addVisible" :title="`添加${pageTitle}`" width="min(640px, 92vw)">
      <div v-if="props.type === 'videos'" class="video-upload-box">
        <label class="admin-btn video-upload-trigger">
          选择本地视频
          <input type="file" accept="video/*" :disabled="uploadingVideo" @change="handleVideoUpload" />
        </label>
        <p class="video-upload-hint">{{ addForm.video_url ? `已上传：${addForm.video_url}` : "支持 mp4、webm、ogg、mov、m4v，保存后前台在线视频列表可播放。" }}</p>
      </div>
      <el-form label-width="110px">
        <el-form-item v-for="field in formFields" :key="field.prop" :label="field.label">
          <el-input v-model="addForm[field.prop]" :placeholder="`请输入${field.label}`" />
        </el-form-item>
      </el-form>
      <template #footer>
        <button class="admin-btn" @click="addVisible = false">取消</button>
        <button class="admin-btn" @click="confirmAdd">确认添加</button>
      </template>
    </el-dialog>

    <el-dialog v-model="commentVisible" title="评论列表" width="min(640px, 92vw)">
      <el-table :data="comments" border>
        <el-table-column prop="nickname" label="用户" width="140" />
        <el-table-column prop="content" label="评论内容" />
        <el-table-column prop="create_time" label="评论时间" width="180" />
      </el-table>
    </el-dialog>
  </section>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { computed, onMounted, reactive, ref, watch } from "vue";
import { api } from "../../services/api";
import { addRow, getComments, loadDatabaseData, refreshUsers, removeRows, saveStore, store, updateRow } from "../../services/store";

const props = defineProps({
  type: { type: String, required: true },
  userRole: { type: String, default: "" }
});
const now = () => new Date().toLocaleString("zh-CN", { hour12: false }).replace(/\//g, "-");

const configs = {
  users: {
    title: "系统用户",
    inputs: [{ key: "keyword", label: "昵称搜索" }],
    add: true,
    columns: [
      { prop: "nickname", label: "昵称" },
      { prop: "avatar", label: "头像", image: true },
      { prop: "username", label: "用户名" },
      { prop: "group", label: "用户组" },
      { prop: "email", label: "邮箱" },
      { prop: "status", label: "状态" },
      { prop: "create_time", label: "创建时间" }
    ]
  },
  courses: {
    title: "课程资料管理",
    inputs: [{ key: "keyword", label: "课程名称搜索" }],
    select: "教学类型",
    columns: [
      { prop: "course_number", label: "课程编号" },
      { prop: "teacher_user", label: "教师用户" },
      { prop: "teachers_name", label: "教师姓名" },
      { prop: "teaching_semester", label: "授课学期" },
      { prop: "course_name", label: "课程名称" },
      { prop: "teaching_type", label: "教学类型" }
    ]
  },
  orders: {
    title: "购买资料列表",
    inputs: [{ key: "keyword", label: "课程名称搜索" }],
    date: true,
    select: "支付状态",
    selectOptions: ["已支付", "待支付", "已取消"],
    audit: true,
    columns: [
      { prop: "buyer_username", label: "购买用户" },
      { prop: "course_number", label: "课程编号" },
      { prop: "teacher_user", label: "教师用户" },
      { prop: "teachers_name", label: "教师姓名" },
      { prop: "teaching_semester", label: "授课学期" },
      { prop: "course_name", label: "课程名称" },
      { prop: "teaching_type", label: "教学类型" }
    ]
  },
  videos: {
    title: "在线视频管理",
    inputs: [{ key: "keyword", label: "视频名称搜索" }, { key: "type", label: "视频类型搜索" }],
    add: true,
    comment: true,
    columns: [
      { prop: "teacher_user", label: "教师用户" },
      { prop: "teachers_name", label: "教师姓名" },
      { prop: "video_name", label: "视频名称" },
      { prop: "video_duration", label: "视频时长" },
      { prop: "video_origin", label: "视频产地" },
      { prop: "video_type", label: "视频类型" }
    ]
  },
  news: {
    title: "教育资讯管理",
    inputs: [{ key: "keyword", label: "标题搜索" }, { key: "tag", label: "标签搜索" }],
    select: "分类筛选",
    add: true,
    comment: true,
    columns: [
      { prop: "title", label: "标题", width: 180 },
      { prop: "cover", label: "封面图", image: true },
      { prop: "category", label: "文章分类" },
      { prop: "tag", label: "标签" },
      { prop: "create_time", label: "创建时间" },
      { prop: "update_time", label: "更新时间" }
    ]
  },
  forums: {
    title: "学习交流管理",
    inputs: [{ key: "keyword", label: "标题搜索" }],
    select: "分类筛选",
    add: true,
    comment: true,
    columns: [
      { prop: "title", label: "标题", width: 180 },
      { prop: "cover", label: "封面图", image: true },
      { prop: "category", label: "分类" },
      { prop: "tag", label: "标签" },
      { prop: "istop", label: "置顶状态" },
      { prop: "create_time", label: "创建时间" },
      { prop: "update_time", label: "更新时间" }
    ]
  },
  banners: {
    title: "轮播图管理",
    inputs: [{ key: "keyword", label: "标题搜索" }],
    add: true,
    columns: [
      { prop: "image", label: "轮播图", image: true },
      { prop: "title", label: "标题" },
      { prop: "link", label: "链接" }
    ]
  },
  notices: {
    title: "网站公告管理",
    inputs: [{ key: "keyword", label: "标题搜索" }],
    select: "分类筛选",
    add: true,
    columns: [
      { prop: "title", label: "标题" },
      { prop: "category", label: "分类" },
      { prop: "create_time", label: "创建时间" },
      { prop: "update_time", label: "更新时间" }
    ]
  }
};

const config = computed(() => configs[props.type]);
const filters = reactive({});
const page = ref(1);
const pageSize = ref(10);
const selectedRows = ref([]);
const detailVisible = ref(false);
const auditVisible = ref(false);
const addVisible = ref(false);
const commentVisible = ref(false);
const currentRow = ref(null);
const auditForm = reactive({ pay_state: "" });
const addForm = reactive({});
const comments = ref([]);
const uploadingVideo = ref(false);
const userTitleMap = {
  admin: "管理员",
  student: "学生用户",
  teacher: "教师用户"
};
const pageTitle = computed(() => (props.type === "users" && props.userRole ? userTitleMap[props.userRole] : config.value.title));
const selectOptions = computed(() => config.value.selectOptions || ["已发布", "待审核"]);
const formFields = computed(() => {
  if (props.type === "videos") {
    return [
      { prop: "teachers_name", label: "教师姓名" },
      { prop: "video_name", label: "视频名称" },
      { prop: "video_duration", label: "视频时长" },
      { prop: "video_origin", label: "视频产地" },
      { prop: "video_type", label: "视频类型" },
      { prop: "video_content", label: "视频简介" },
      { prop: "video_poster", label: "视频海报" }
    ];
  }
  if (props.type === "notices") {
    return [
      { prop: "title", label: "公告标题" },
      { prop: "category", label: "公告分类" },
      { prop: "content", label: "公告内容" }
    ];
  }
  return config.value.columns.filter((column) => !column.image && !["create_time", "update_time"].includes(column.prop)).slice(0, 8);
});
const detailFields = computed(() => {
  if (props.type === "videos") {
    return [...config.value.columns, { prop: "video_content", label: "视频简介" }, { prop: "video_url", label: "视频地址" }];
  }
  if (props.type === "notices") {
    return [...config.value.columns, { prop: "content", label: "公告内容" }, { prop: "publish_state", label: "发布状态" }];
  }
  return config.value.columns;
});
const filtered = computed(() => {
  let rows = store[props.type] || [];
  if (props.type === "users" && props.userRole) {
    rows = rows.filter((row) => row.role === props.userRole);
  }
  const keyword = filters.keyword || "";
  return rows.filter((row) => {
    const matchKeyword = !keyword || JSON.stringify(row).includes(keyword);
    const matchSelect = !filters.select || row.pay_state === filters.select || row.category === filters.select || row.teaching_type === filters.select;
    const matchDate = !filters.date || !row.buy_time || (new Date(row.buy_time) >= filters.date[0] && new Date(row.buy_time) <= filters.date[1]);
    return matchKeyword && matchSelect && matchDate;
  });
});

const pagedRows = computed(() => filtered.value.slice((page.value - 1) * pageSize.value, page.value * pageSize.value));

watch([filtered, pageSize], () => {
  if ((page.value - 1) * pageSize.value >= filtered.value.length) {
    page.value = 1;
  }
});

async function handleSearch() {
  page.value = 1;
  if (props.type === "users") {
    await refreshUsers();
  }
}

function deleteSelected() {
  if (!selectedRows.value.length) {
    ElMessage.warning("请先勾选要删除的记录");
    return;
  }
  removeRows(props.type, selectedRows.value.map((row) => row.id));
  selectedRows.value = [];
  ElMessage.success("已删除选中记录");
}

function showDetail(row) {
  currentRow.value = row;
  detailVisible.value = true;
}

function showAudit(row) {
  currentRow.value = row;
  auditForm.pay_state = row.pay_state;
  auditVisible.value = true;
}

function confirmAudit() {
  if (currentRow.value) {
    currentRow.value.pay_state = auditForm.pay_state;
    updateRow(props.type, currentRow.value);
  }
  auditVisible.value = false;
  ElMessage.success("订单状态已更新");
}

function showAdd() {
  Object.keys(addForm).forEach((key) => delete addForm[key]);
  formFields.value.forEach((field) => {
    addForm[field.prop] = "";
  });
  if (props.type === "videos") {
    addForm.video_url = "";
    addForm.video_origin = "本地上传";
    addForm.video_duration = "本地视频";
  }
  addVisible.value = true;
}

async function handleVideoUpload(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  if (!file.type.startsWith("video/")) {
    ElMessage.warning("请选择视频文件");
    event.target.value = "";
    return;
  }
  uploadingVideo.value = true;
  try {
    const fd = new FormData();
    fd.append("file", file);
    const { data } = await api.post("/upload/", fd, { headers: { "Content-Type": "multipart/form-data" } });
    const path = data?.data?.path || "";
    if (!path) throw new Error("上传成功但后端未返回视频地址");
    const filename = file.name.replace(/\.[^.]+$/, "");
    addForm.video_url = path;
    addForm.video_name = addForm.video_name || filename;
    addForm.video_type = addForm.video_type || file.type || "视频";
    addForm.video_origin = addForm.video_origin || "本地上传";
    addForm.video_duration = addForm.video_duration || "本地视频";
    addForm.video_poster = addForm.video_poster || "https://dummyimage.com/640x360/993380/ffffff&text=Video";
    ElMessage.success("视频上传成功");
  } catch (error) {
    addForm.video_url = "";
    ElMessage.error(error?.response?.data?.message || error?.message || "视频上传失败，请确认后端服务正常并已登录管理员账号");
  } finally {
    uploadingVideo.value = false;
    event.target.value = "";
  }
}

async function confirmAdd() {
  const row = { ...addForm };
  if (props.type === "videos") {
    if (!row.video_url) {
      ElMessage.warning("请先选择并上传本地视频");
      return;
    }
    if (!row.video_name) {
      ElMessage.warning("请输入视频名称");
      return;
    }
    try {
      await api.post("/videos/", {
        teachers_name: row.teachers_name || "管理员",
        video_name: row.video_name,
        video_duration: row.video_duration || "本地视频",
        video_origin: row.video_origin || "本地上传",
        video_type: row.video_type || "视频",
        video_content: row.video_content || "",
        video_poster: row.video_poster || "https://dummyimage.com/640x360/993380/ffffff&text=Video",
        video_url: row.video_url
      });
      await loadDatabaseData();
      addVisible.value = false;
      ElMessage.success("视频已添加，并同步到前台");
    } catch (error) {
      ElMessage.error(error?.response?.data?.message || "视频保存失败，请确认已登录管理员账号");
    }
    return;
  }
  if (props.type === "users") {
    row.role = props.userRole || "student";
    row.group = userTitleMap[row.role] || row.group || "学生用户";
    row.status = row.status || "正常";
    row.create_time = now();
  }
  if (props.type === "news" || props.type === "forums" || props.type === "notices") {
    row.create_time = now();
    row.update_time = now();
  }
  if (props.type === "orders") {
    row.pay_state = row.pay_state || "待支付";
    row.buy_time = row.buy_time || now();
    row.buyer_username = row.buyer_username || "student";
  }
  if (props.type === "courses") {
    row.name = row.course_name;
    row.type = row.teaching_type;
    row.teacher = row.teachers_name || row.teacher_user;
    row.number = row.course_number;
    row.semester = row.teaching_semester;
    row.image = row.course_images || "https://dummyimage.com/640x360/B377B3/ffffff&text=Course";
  }
  if (props.type === "videos") {
    row.name = row.video_name;
    row.type = row.video_type;
    row.teacher = row.teachers_name || row.teacher_user;
    row.duration = row.video_duration;
    row.origin = row.video_origin;
    row.poster = row.video_poster || "https://dummyimage.com/640x360/993380/ffffff&text=Video";
  }
  if (props.type === "news") {
    row.image = row.cover || row.cover_image || "https://dummyimage.com/640x360/B377B3/ffffff&text=News";
    row.cover = row.image;
    row.cover_image = row.image;
    row.date = row.create_time;
    row.likes = 0;
    row.hits = 0;
  }
  if (props.type === "forums") {
    row.image = row.cover || "https://dummyimage.com/640x360/993380/ffffff&text=Forum";
    row.date = row.create_time;
    row.author = row.nickname || "管理员";
    row.likes = 0;
    row.hits = 0;
  }
  await addRow(props.type, row);
  addVisible.value = false;
  ElMessage.success("添加成功，客户端数据已同步");
}

function showComments(row) {
  const targetMap = { news: "news", forums: "forum", videos: "video", courses: "course" };
  const targetType = targetMap[props.type] || props.type;
  comments.value = getComments(targetType, row.id);
  commentVisible.value = true;
}

watch(
  () => store,
  () => saveStore(),
  { deep: true }
);

onMounted(() => {
  if (props.type === "users") {
    refreshUsers();
  }
});
</script>

<style scoped>
.small {
  height: 30px;
  padding: 0 10px;
  margin-right: 6px;
}

.video-upload-box {
  display: grid;
  gap: 10px;
  margin-bottom: 16px;
}

.video-upload-trigger {
  position: relative;
  width: fit-content;
}

.video-upload-trigger input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.video-upload-hint {
  margin: 0;
  color: #666;
  font-size: 13px;
  line-height: 1.6;
  word-break: break-all;
}
</style>
