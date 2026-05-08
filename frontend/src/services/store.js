import { reactive } from "vue";
import { api } from "./api";
import { getAuthUser, hasAuth } from "./auth";
import { courses, forums, news, notices, videos } from "./mock";

const STORAGE_KEY = "online-education-store";
const VERSION_KEY = "online-education-store-version";
const DATA_VERSION = "k12-2026-05-07-chinese-mysql-seed-v1";
const pic = "https://dummyimage.com/120x70/7373e6/ffffff&text=Img";
const image = (text, bg = "B377B3") => `https://dummyimage.com/640x360/${bg}/ffffff&text=${encodeURIComponent(text)}`;
const withTime = (date, time = "09:30:00") => `${date} ${time}`;

function seed() {
  return {
    users: [
      { id: 1, nickname: "管理员", avatar: pic, username: "admin", role: "admin", group: "管理员", email: "admin@example.com", status: "正常", create_time: "2026-05-01 08:00:00" },
      { id: 2, nickname: "林同学", avatar: pic, username: "student", role: "student", group: "学生用户", email: "student@example.com", status: "正常", create_time: "2026-05-02 09:15:30" },
      { id: 3, nickname: "陈老师", avatar: pic, username: "teacher", role: "teacher", group: "教师用户", email: "teacher@example.com", status: "正常", create_time: "2026-05-03 10:20:45" }
    ],
    courses: courses.map((x) => ({
      ...x,
      course_number: x.number,
      teacher_user: x.teacher,
      teachers_name: x.teacher,
      teaching_semester: x.semester,
      course_name: x.name,
      teaching_type: x.type,
      course_images: x.image,
      praise_len: 0,
      collect_len: 0
    })),
    orders: courses.map((x, index) => ({
      id: index + 1,
      buyer_username: index % 2 === 0 ? "student" : "林同学",
      course_number: x.number,
      teacher_user: x.teacher,
      teachers_name: x.teacher,
      teaching_semester: x.semester,
      course_name: x.name,
      teaching_type: x.type,
      buy_time: withTime(`2026-05-0${index + 1}`, `${10 + index}:20:30`),
      pay_state: index % 3 === 0 ? "待支付" : "已支付"
    })),
    videos: videos.map((x) => ({
      ...x,
      teacher_user: x.teacher,
      teachers_name: x.teacher,
      video_name: x.name,
      video_duration: x.duration,
      video_origin: x.origin,
      video_type: x.type,
      video_poster: x.poster,
      praise_len: 0,
      collect_len: 0,
      comment_len: 0
    })),
    news: news.map((x, index) => ({
      ...x,
      cover: x.image,
      cover_image: x.image,
      create_time: withTime(x.date, `${9 + index}:10:20`),
      update_time: withTime(x.date, `${10 + index}:35:45`),
      tag: "教育",
      content: "这里展示教育资讯正文内容，支持前台查看详情与发表评论。",
      praise_len: 0,
      collect_len: 0,
      comment_len: 0
    })),
    forums: forums.map((x, index) => ({
      ...x,
      cover: x.image,
      category: "交流",
      create_time: withTime(x.date, `${8 + index}:05:16`),
      update_time: withTime(x.date, `${11 + index}:26:38`),
      tag: "学习",
      istop: "否",
      praise_len: 0,
      collect_len: 0
    })),
    banners: [
      { id: 1, image: image("中小学在线学习平台"), title: "中小学在线学习平台", link: "/" },
      { id: 2, image: image("课程资料精选推荐", "993380"), title: "课程资料精选推荐", link: "/courses" }
    ],
    notices: notices.map((x, index) => ({
      ...x,
      content: x.content || "公告详情用于展示平台通知、课程安排、系统维护和服务调整等信息。",
      create_time: withTime(x.create_time, `${9 + index}:00:00`),
      update_time: withTime(x.create_time, `${12 + index}:15:30`),
      praise_len: 0
    })),
    comments: [],
    favorites: [],
    likes: [],
    purchases: []
  };
}

function load() {
  if (localStorage.getItem(VERSION_KEY) !== DATA_VERSION) {
    const data = seed();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    localStorage.setItem(VERSION_KEY, DATA_VERSION);
    return data;
  }
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY)) || seed();
    const fallback = seed();
    return {
      ...fallback,
      ...data,
      users: data.users || fallback.users,
      courses: data.courses || fallback.courses,
      orders: data.orders || fallback.orders,
      videos: data.videos || fallback.videos,
      news: data.news || fallback.news,
      forums: data.forums || fallback.forums,
      banners: data.banners || fallback.banners,
      notices: data.notices || fallback.notices,
      comments: data.comments || [],
      favorites: data.favorites || [],
      likes: data.likes || [],
      purchases: data.purchases || []
    };
  } catch {
    return seed();
  }
}

export const store = reactive(load());

export function saveStore() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
}

function syncStoreFromLocalStorage() {
  const next = load();
  Object.keys(store).forEach((key) => {
    delete store[key];
  });
  Object.assign(store, next);
}

if (typeof window !== "undefined") {
  window.addEventListener("storage", (event) => {
    if (event.key === STORAGE_KEY || event.key === VERSION_KEY) {
      syncStoreFromLocalStorage();
    }
  });
}

function assignRows(type, rows) {
  store[type] = rows;
  saveStore();
}

function courseFromApi(item) {
  return {
    ...item,
    id: item.course_materials_id,
    number: item.course_number,
    name: item.course_name,
    teacher: item.teachers_name,
    type: item.teaching_type,
    price: item.course_prices,
    image: item.course_images,
    semester: item.teaching_semester
  };
}

function videoFromApi(item) {
  return {
    ...item,
    id: item.online_video_id,
    name: item.video_name,
    teacher: item.teachers_name,
    teacher_user: item.teachers_name,
    type: item.video_type,
    duration: item.video_duration,
    origin: item.video_origin,
    poster: item.video_poster,
    src: item.video_url || "",
    video_url: item.video_url || ""
  };
}

function forumFromApi(item) {
  return {
    ...item,
    id: item.forum_id,
    category: item.type,
    author: item.nickname,
    image: item.img || "https://dummyimage.com/640x360/993380/ffffff&text=%E5%AD%A6%E4%B9%A0%E4%BA%A4%E6%B5%81",
    cover: item.img || "https://dummyimage.com/640x360/993380/ffffff&text=%E5%AD%A6%E4%B9%A0%E4%BA%A4%E6%B5%81",
    date: item.create_time
  };
}

function newsFromApi(item) {
  return {
    ...item,
    id: item.news_id,
    image: item.cover_image,
    cover: item.cover_image,
    content: item.content || item.summary,
    date: item.create_time
  };
}

function userFromApi(item) {
  const groupMap = {
    admin: "管理员",
    student: "学生用户",
    teacher: "教师用户"
  };
  return {
    ...item,
    group: groupMap[item.role] || "学生用户",
    avatar: item.avatar || pic,
    create_time: item.date_joined || item.create_time || "",
    date_joined: item.date_joined || ""
  };
}

function interactionLabel(targetType) {
  return targetType === "forum" ? "学习交流" : targetType === "news" ? "教育资讯" : targetType === "course" ? "课程资料" : targetType === "video" ? "在线视频" : "内容";
}

function interactionFromApi(item) {
  return {
    id: item.id,
    targetType: item.target_type,
    targetId: item.target_id,
    targetLabel: interactionLabel(item.target_type),
    title: item.target_title || "未命名内容",
    username: currentUser()?.username || "",
    create_time: item.create_time
  };
}

function commentFromApi(item) {
  return {
    id: item.comment_id,
    targetType: item.target_type,
    targetId: item.target_id,
    targetTitle: item.target_title,
    targetLabel: interactionLabel(item.target_type),
    nickname: item.nickname,
    avatar: item.avatar,
    content: item.content,
    create_time: item.create_time
  };
}

export async function loadDatabaseData() {
  const requests = [
    api.get("/courses/", { params: { page_size: 100 } }).then(({ data }) => assignRows("courses", (data.data.items || []).map(courseFromApi))),
    api.get("/videos/", { params: { page_size: 100 } }).then(({ data }) => assignRows("videos", (data.data.items || []).map(videoFromApi))),
    api.get("/forums/", { params: { page_size: 100 } }).then(({ data }) => assignRows("forums", (data.data.items || []).map(forumFromApi))),
    api.get("/news/", { params: { page_size: 100 } }).then(({ data }) => assignRows("news", (data.data.items || []).map(newsFromApi))),
    api.get("/notices/", { params: { page_size: 100 } }).then(({ data }) => assignRows("notices", data.data.items || [])),
    api.get("/banners/").then(({ data }) => assignRows("banners", data.data.items || []))
  ];
  if (hasAuth("client")) {
    requests.push(api.get("/interactions/", { params: { kind: "like" } }).then(({ data }) => assignRows("likes", (data.data.items || []).map(interactionFromApi))));
    requests.push(api.get("/interactions/", { params: { kind: "favorite" } }).then(({ data }) => assignRows("favorites", (data.data.items || []).map(interactionFromApi))));
    requests.push(api.get("/comments/").then(({ data }) => assignRows("comments", (data.data.items || []).map(commentFromApi))));
  }
  if (hasAuth("admin")) {
    requests.push(refreshUsers());
  }
  await Promise.allSettled(requests);
}

export async function refreshUsers() {
  try {
    const { data } = await api.get("/admin/users/", { params: { page_size: 100 } });
    assignRows("users", (data.data.items || []).map(userFromApi));
  } catch {
    return store.users;
  }
  return store.users;
}

export async function refreshBanners() {
  try {
    const { data } = await api.get("/banners/");
    assignRows("banners", data.data.items || []);
  } catch {
    return store.banners;
  }
  return store.banners;
}

export function addRow(type, row) {
  const rows = store[type];
  const localRow = { id: Date.now(), ...row };
  rows.unshift(localRow);
  saveStore();
  return persistAdd(type, localRow);
}

export function removeRows(type, ids) {
  store[type] = store[type].filter((row) => !ids.includes(row.id));
  saveStore();
  return persistRemove(type, ids);
}

export function updateRow(type, row) {
  const rows = store[type];
  const index = rows.findIndex((item) => item.id === row.id);
  if (index >= 0) rows[index] = { ...rows[index], ...row };
  saveStore();
  return persistUpdate(type, row);
}

function persistAdd(type, row) {
  const map = {
    courses: () =>
      api.post("/courses/", {
        course_number: row.course_number || row.number || `K12-${Date.now()}`,
        teachers_name: row.teachers_name || row.teacher || "",
        teaching_semester: row.teaching_semester || row.semester || "",
        course_name: row.course_name || row.name || "",
        teaching_type: row.teaching_type || row.type || "",
        course_prices: Number(row.course_prices || row.price || 0),
        course_images: row.course_images || row.image || "",
        course_introduction: row.course_introduction || ""
      }),
    videos: () =>
      api.post("/videos/", {
        teachers_name: row.teachers_name || row.teacher || "",
        video_name: row.video_name || row.name || "",
        video_duration: row.video_duration || row.duration || "",
        video_origin: row.video_origin || row.origin || "",
        video_type: row.video_type || row.type || "",
        video_content: row.video_content || "",
        video_poster: row.video_poster || row.poster || "",
        video_url: row.video_url || row.src || ""
      }),
    forums: () =>
      api.post("/forums/", {
        title: row.title || "",
        description: row.description || "",
        tag: row.tag || "",
        type: row.type || row.category || "",
        img: row.img || row.image || row.cover || ""
      }),
    news: () =>
      api.post("/news/", {
        title: row.title || "",
        category: row.category || "",
        tag: row.tag || "",
        cover_image: row.cover_image || row.cover || row.image || "",
        summary: row.summary || "",
        content: row.content || row.summary || "",
        author: row.author || ""
      }),
    banners: () => api.post("/admin/banners/", { title: row.title || "轮播图", image: row.image || "", link: row.link || "", sort: Number(row.sort || 0) })
    ,
    notices: () =>
      api.post("/notices/", {
        title: row.title || "",
        category: row.category || "",
        content: row.content || "",
        publish_state: row.publish_state || "已发布"
      }).then(({ data }) => {
        Object.assign(row, data.data || {});
        saveStore();
        return data.data;
      })
  };
  map[type]?.().catch(() => {});
}

function persistRemove(type, ids) {
  const map = {
    banners: () => api.delete("/admin/banners/", { data: { ids } }),
    courses: () => Promise.all(ids.map((id) => api.delete(`/courses/${id}/`))),
    videos: () => Promise.all(ids.map((id) => api.delete(`/videos/${id}/`))),
    forums: () => Promise.all(ids.map((id) => api.delete(`/forums/${id}/`))),
    news: () => Promise.all(ids.map((id) => api.delete(`/news/${id}/`))),
    notices: () => Promise.all(ids.map((id) => api.delete(`/notices/${id}/`)))
  };
  map[type]?.().catch(() => {});
}

function persistUpdate(type, row) {
  if (type === "courses" && row.course_materials_id) {
    api.patch(`/courses/${row.course_materials_id}/`, row).catch(() => {});
  } else if (type === "videos" && row.online_video_id) {
    api.patch(`/videos/${row.online_video_id}/`, row).catch(() => {});
  } else if (type === "forums" && row.forum_id) {
    api.patch(`/forums/${row.forum_id}/`, row).catch(() => {});
  } else if (type === "news" && row.news_id) {
    api.patch(`/news/${row.news_id}/`, row).catch(() => {});
  } else if (type === "notices" && row.id) {
    api.patch(`/notices/${row.id}/`, row).catch(() => {});
  }
}

export function syncUser(user) {
  const role = user.role || "student";
  const groupMap = {
    admin: "管理员",
    student: "学生用户",
    teacher: "教师用户"
  };
  const row = {
    id: user.id || Date.now(),
    username: user.username,
    nickname: user.nickname || user.username,
    email: user.email || "",
    role,
    group: groupMap[role] || "学生用户",
    avatar: user.avatar || pic,
    status: user.status || "正常",
    create_time: user.create_time || new Date().toLocaleString("zh-CN", { hour12: false }).replace(/\//g, "-")
  };
  const index = store.users.findIndex((item) => item.username === row.username || item.id === row.id);
  if (index >= 0) {
    store.users[index] = { ...store.users[index], ...row };
  } else {
    store.users.unshift(row);
  }
  saveStore();
}

export function currentUser() {
  return getAuthUser("client");
}

export function addComment(targetType, targetId, content) {
  const user = currentUser() || { username: "游客", nickname: "游客" };
  const target = findTarget(targetType, targetId);
  store.comments.unshift({
    id: Date.now(),
    targetType,
    targetId,
    targetTitle: target.title,
    targetLabel: target.label,
    content,
    username: user.username,
    nickname: user.nickname || user.username,
    create_time: new Date().toLocaleString("zh-CN", { hour12: false }).replace(/\//g, "-")
  });
  saveStore();
  api.post("/comments/", {
    target_type: targetType,
    target_id: targetId,
    target_title: target.title,
    content
  }).catch(() => {});
}

export function getComments(targetType, targetId) {
  if (!Array.isArray(store.comments)) {
    store.comments = [];
    saveStore();
  }
  return store.comments.filter((item) => item.targetType === targetType && String(item.targetId) === String(targetId));
}

function findTarget(targetType, targetId) {
  const id = String(targetId);
  const maps = {
    course: store.courses,
    video: store.videos,
    forum: store.forums,
    news: store.news,
    notice: store.notices
  };
  const target = (maps[targetType] || []).find((item) => String(item.id) === id || String(item.course_materials_id) === id || String(item.online_video_id) === id || String(item.news_id) === id || String(item.forum_id) === id);
  const labelMap = {
    course: "课程资料",
    video: "在线视频",
    forum: "学习交流",
    news: "教育资讯",
    notice: "网站公告"
  };
  return {
    title: target?.title || target?.name || target?.course_name || target?.video_name || target?.course_name || target?.title || "未命名内容",
    label: labelMap[targetType] || targetType
  };
}

export function removeComment(id) {
  if (!Array.isArray(store.comments)) store.comments = [];
  store.comments = store.comments.filter((item) => item.id !== id);
  saveStore();
  api.delete("/comments/", { data: { id } }).catch(() => {});
}

export function addFavorite(targetType, targetId, title) {
  if (!Array.isArray(store.favorites)) store.favorites = [];
  const user = currentUser() || { username: "游客", nickname: "游客" };
  if (store.favorites.some((item) => item.targetType === targetType && String(item.targetId) === String(targetId) && item.username === user.username)) return;
  const target = getTargetStoreItem(targetType, targetId);
  if (target) {
    target.collect_len = Number(target.collect_len || 0) + 1;
  }
  store.favorites.unshift({
    id: Date.now(),
    targetType,
    targetId,
    targetLabel: targetType === "forum" ? "学习交流" : targetType === "news" ? "教育资讯" : targetType === "course" ? "课程资料" : targetType === "video" ? "在线视频" : "内容",
    title,
    username: user.username,
    create_time: new Date().toLocaleString("zh-CN", { hour12: false }).replace(/\//g, "-")
  });
  saveStore();
  api.post("/interactions/?kind=favorite", { target_type: targetType, target_id: targetId }).catch(() => {});
}

export function getFavoriteCount(targetType, targetId) {
  const target = getTargetStoreItem(targetType, targetId);
  if (target && target.collect_len !== undefined) return Number(target.collect_len || 0);
  return store.favorites.filter((item) => item.targetType === targetType && String(item.targetId) === String(targetId)).length;
}

export function addLike(targetType, targetId, title) {
  if (!Array.isArray(store.likes)) store.likes = [];
  const user = currentUser() || { username: "游客", nickname: "游客" };
  if (store.likes.some((item) => item.targetType === targetType && String(item.targetId) === String(targetId) && item.username === user.username)) return;
  const target = getTargetStoreItem(targetType, targetId);
  if (target) {
    target.praise_len = Number(target.praise_len || 0) + 1;
  }
  store.likes.unshift({
    id: Date.now(),
    targetType,
    targetId,
    targetLabel: targetType === "forum" ? "学习交流" : targetType === "news" ? "教育资讯" : targetType === "course" ? "课程资料" : targetType === "video" ? "在线视频" : "内容",
    title,
    username: user.username,
    create_time: new Date().toLocaleString("zh-CN", { hour12: false }).replace(/\//g, "-")
  });
  saveStore();
  api.post("/interactions/?kind=like", { target_type: targetType, target_id: targetId }).catch(() => {});
}

export function removeLike(id) {
  if (!Array.isArray(store.likes)) store.likes = [];
  const target = store.likes.find((item) => item.id === id);
  if (target) {
    const content = getTargetStoreItem(target.targetType, target.targetId);
    if (content && content.praise_len !== undefined) {
      content.praise_len = Math.max(0, Number(content.praise_len || 0) - 1);
    }
    api.delete("/interactions/?kind=like", { data: { target_type: target.targetType, target_id: target.targetId } }).catch(() => {});
  }
  store.likes = store.likes.filter((item) => item.id !== id);
  saveStore();
}

export function getLikeCount(targetType, targetId) {
  const target = getTargetStoreItem(targetType, targetId);
  if (target && target.praise_len !== undefined) return Number(target.praise_len || 0);
  return store.likes.filter((item) => item.targetType === targetType && String(item.targetId) === String(targetId)).length;
}

export function removeFavorite(id) {
  if (!Array.isArray(store.favorites)) store.favorites = [];
  const target = store.favorites.find((item) => item.id === id);
  if (target) {
    const content = getTargetStoreItem(target.targetType, target.targetId);
    if (content && content.collect_len !== undefined) {
      content.collect_len = Math.max(0, Number(content.collect_len || 0) - 1);
    }
    api.delete("/interactions/?kind=favorite", { data: { target_type: target.targetType, target_id: target.targetId } }).catch(() => {});
  }
  store.favorites = store.favorites.filter((item) => item.id !== id);
  saveStore();
}

export function findLike(targetType, targetId, username = currentUser()?.username) {
  return store.likes.find(
    (item) => item.targetType === targetType && String(item.targetId) === String(targetId) && (!username || item.username === username)
  );
}

export function findFavorite(targetType, targetId, username = currentUser()?.username) {
  return store.favorites.find(
    (item) => item.targetType === targetType && String(item.targetId) === String(targetId) && (!username || item.username === username)
  );
}

export function addPurchase(course) {
  if (!Array.isArray(store.purchases)) store.purchases = [];
  if (!Array.isArray(store.orders)) store.orders = [];
  const title = course.name || course.course_name;
  const now = new Date().toLocaleString("zh-CN", { hour12: false }).replace(/\//g, "-");
  const id = Date.now();
  store.purchases.unshift({
    id,
    title,
    targetId: course.id,
    create_time: now
  });
  store.orders.unshift({
    id,
    buyer_username: currentUser()?.username || currentUser()?.nickname || "student",
    course_number: course.number || course.course_number,
    teacher_user: course.teacher || course.teacher_user,
    teachers_name: course.teachers_name || course.teacher,
    teaching_semester: course.semester || course.teaching_semester,
    course_name: title,
    teaching_type: course.type || course.teaching_type,
    buy_time: now,
    pay_state: "已支付"
  });
  saveStore();
  const courseId = course.course_materials_id || course.id;
  if (courseId) api.post(`/courses/${courseId}/buy/`).catch(() => {});
}

function getTargetStoreItem(targetType, targetId) {
  const id = String(targetId);
  const map = {
    course: store.courses,
    video: store.videos,
    forum: store.forums,
    news: store.news,
    notice: store.notices
  };
  return (map[targetType] || []).find(
    (item) =>
      String(item.id) === id ||
      String(item.course_materials_id) === id ||
      String(item.online_video_id) === id ||
      String(item.news_id) === id ||
      String(item.forum_id) === id
  );
}
