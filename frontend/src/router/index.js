import { createRouter, createWebHashHistory } from "vue-router";

import AdminLayout from "../views/admin/AdminLayout.vue";
import AdminChart from "../views/admin/AdminChart.vue";
import AdminLogin from "../views/admin/AdminLogin.vue";
import BannerPage from "../views/admin/BannerPage.vue";
import AdminTablePage from "../views/admin/AdminTablePage.vue";
import CourseMaterials from "../views/CourseMaterials.vue";
import EducationNews from "../views/EducationNews.vue";
import Forum from "../views/Forum.vue";
import ForumPublish from "../views/ForumPublish.vue";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import OnlineVideo from "../views/OnlineVideo.vue";
import PersonalCenter from "../views/PersonalCenter.vue";
import Register from "../views/Register.vue";
import TeacherCourses from "../views/TeacherCourses.vue";
import WebsiteNotice from "../views/WebsiteNotice.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/forum", component: Forum },
  { path: "/forum/publish", component: ForumPublish },
  { path: "/notices", component: WebsiteNotice },
  { path: "/news", component: EducationNews },
  { path: "/courses", component: CourseMaterials },
  { path: "/videos", component: OnlineVideo },
  { path: "/profile", component: PersonalCenter },
  { path: "/teacher/courses", component: TeacherCourses },
  { path: "/admin/login", component: AdminLogin },
  {
    path: "/admin",
    component: AdminLayout,
    meta: { requiresAdmin: true },
    children: [
      { path: "", redirect: "/admin/users/admin" },
      { path: "users", redirect: "/admin/users/admin" },
      { path: "users/admin", component: AdminTablePage, props: { type: "users", userRole: "admin" } },
      { path: "users/student", component: AdminTablePage, props: { type: "users", userRole: "student" } },
      { path: "users/teacher", component: AdminTablePage, props: { type: "users", userRole: "teacher" } },
      { path: "courses", component: AdminTablePage, props: { type: "courses" } },
      { path: "orders", component: AdminTablePage, props: { type: "orders" } },
      { path: "videos", component: AdminTablePage, props: { type: "videos" } },
      { path: "news", component: AdminTablePage, props: { type: "news" } },
      { path: "forums", component: AdminTablePage, props: { type: "forums" } },
      { path: "banners", component: BannerPage },
      { path: "notices", component: AdminTablePage, props: { type: "notices" } },
      { path: "statistics", component: AdminChart }
    ]
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

router.beforeEach((to) => {
  if (!to.matched.some((record) => record.meta.requiresAdmin)) {
    return true;
  }
  try {
    const user = JSON.parse(localStorage.getItem("user") || "null");
    const token = localStorage.getItem("token");
    if (token && user?.role === "admin") {
      return true;
    }
  } catch {
    // Fall through to login.
  }
  return { path: "/admin/login", query: { redirect: to.fullPath } };
});

export default router;
