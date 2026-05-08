<template>
  <ClientLayout>
    <section class="client-panel">
      <PageTitle title="教师课程资料" />
      <div class="toolbar">
        <el-input v-model="keyword" placeholder="课程名称搜索" clearable />
        <el-select v-model="type" placeholder="教学类型" clearable>
          <el-option label="小学数学" value="小学数学" />
          <el-option label="小学语文" value="小学语文" />
          <el-option label="初中英语" value="初中英语" />
          <el-option label="初中物理" value="初中物理" />
        </el-select>
        <button class="primary-btn" @click="page = 1">查询</button>
        <button class="primary-btn" @click="keyword = ''; type = ''">重置</button>
        <button class="primary-btn" @click="showAdd">添加</button>
        <button class="primary-btn" @click="deleteSelected">删除</button>
      </div>
      <div class="table-wrap">
        <el-table class="client-table" :data="paged" border @selection-change="selected = $event">
          <el-table-column type="selection" width="52" />
          <el-table-column prop="course_number" label="课程编号" width="150" />
          <el-table-column prop="teacher_user" label="教师用户" width="140" />
          <el-table-column prop="teachers_name" label="教师姓名" width="140" />
          <el-table-column prop="teaching_semester" label="授课学期" width="140" />
          <el-table-column prop="course_name" label="课程名称" min-width="200" />
          <el-table-column prop="teaching_type" label="教学类型" width="140" />
          <el-table-column label="操作" width="130">
            <template #default="{ row }"><button class="primary-btn" @click="openDetail(row)">详情</button></template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination class="pagination" layout="prev, pager, next" :total="filtered.length" :page-size="10" v-model:current-page="page" />
    </section>

    <el-dialog v-model="addVisible" title="发布课程资料" width="min(640px, 92vw)">
      <el-form label-width="110px">
        <el-form-item label="课程编号"><el-input v-model="form.course_number" /></el-form-item>
        <el-form-item label="授课学期"><el-input v-model="form.teaching_semester" /></el-form-item>
        <el-form-item label="课程名称"><el-input v-model="form.course_name" /></el-form-item>
        <el-form-item label="教学类型"><el-input v-model="form.teaching_type" /></el-form-item>
        <el-form-item label="价格"><el-input v-model="form.price" /></el-form-item>
      </el-form>
      <template #footer>
        <button class="primary-btn" @click="addVisible = false">取消</button>
        <button class="primary-btn" @click="confirmAdd">发布</button>
      </template>
    </el-dialog>

    <el-dialog v-model="detailVisible" title="课程资料详情" width="min(640px, 92vw)">
      <p>课程编号：{{ current?.course_number }}</p>
      <p>课程名称：{{ current?.course_name }}</p>
      <p>教师姓名：{{ current?.teachers_name }}</p>
      <p>教学类型：{{ current?.teaching_type }}</p>
    </el-dialog>
  </ClientLayout>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { computed, reactive, ref } from "vue";
import ClientLayout from "../components/ClientLayout.vue";
import PageTitle from "../components/PageTitle.vue";
import { addRow, currentUser, removeRows, store } from "../services/store";

const keyword = ref("");
const type = ref("");
const page = ref(1);
const selected = ref([]);
const addVisible = ref(false);
const detailVisible = ref(false);
const current = ref(null);
const form = reactive({ course_number: "", teaching_semester: "", course_name: "", teaching_type: "", price: "" });
const user = currentUser() || { username: "teacher", nickname: "教师" };

const filtered = computed(() =>
  store.courses.filter((item) => (!keyword.value || item.name?.includes(keyword.value) || item.course_name?.includes(keyword.value)) && (!type.value || item.type === type.value || item.teaching_type === type.value))
);
const paged = computed(() => filtered.value.slice((page.value - 1) * 10, page.value * 10));

function showAdd() {
  Object.assign(form, {
    course_number: `K12-${Date.now().toString().slice(-5)}`,
    teaching_semester: "2026 春季",
    course_name: "",
    teaching_type: "",
    price: ""
  });
  addVisible.value = true;
}

function confirmAdd() {
  if (!form.course_name || !form.teaching_type) {
    ElMessage.warning("请填写课程名称和教学类型");
    return;
  }
  addRow("courses", {
    course_number: form.course_number,
    number: form.course_number,
    teacher_user: user.username,
    teachers_name: user.nickname || user.username,
    teacher: user.nickname || user.username,
    teaching_semester: form.teaching_semester,
    semester: form.teaching_semester,
    course_name: form.course_name,
    name: form.course_name,
    teaching_type: form.teaching_type,
    type: form.teaching_type,
    price: Number(form.price) || 0,
    course_images: "https://dummyimage.com/640x360/B377B3/ffffff&text=Course",
    image: "https://dummyimage.com/640x360/B377B3/ffffff&text=Course"
  });
  addVisible.value = false;
  ElMessage.success("课程已发布，并同步到后台课程资料管理");
}

function deleteSelected() {
  if (!selected.value.length) {
    ElMessage.warning("请先勾选课程");
    return;
  }
  removeRows("courses", selected.value.map((item) => item.id));
  selected.value = [];
  ElMessage.success("已删除课程，并同步到后台");
}

function openDetail(row) {
  current.value = row;
  detailVisible.value = true;
}
</script>
