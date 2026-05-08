const image = (text, bg = "B377B3") => `https://dummyimage.com/640x360/${bg}/ffffff&text=${encodeURIComponent(text)}`;

export const forums = [
  { id: 1, date: "2026-05-01", title: "六年级数学应用题解题方法交流", author: "林同学", likes: 28, hits: 230, image: image("小学数学") },
  { id: 2, date: "2026-05-02", title: "初一英语单词记忆打卡小组", author: "刘老师", likes: 39, hits: 318, image: image("初中英语", "993380") },
  { id: 3, date: "2026-05-03", title: "小学语文阅读理解答题技巧", author: "王同学", likes: 16, hits: 121, image: image("阅读理解") },
  { id: 4, date: "2026-05-04", title: "初二物理浮力实验现象讨论", author: "赵同学", likes: 45, hits: 410, image: image("初中物理", "993380") },
  { id: 5, date: "2026-05-05", title: "中考数学压轴题资料整理", author: "孙老师", likes: 52, hits: 488, image: image("中考数学") },
  { id: 6, date: "2026-05-06", title: "课后作业提交与错题本使用反馈", author: "何同学", likes: 18, hits: 167, image: image("课后作业", "993380") }
];

export const news = [
  { id: 1, date: "2026-04-28", title: "义务教育阶段数字课堂建设持续推进", category: "政策", likes: 12, hits: 302, image: image("教育新闻") },
  { id: 2, date: "2026-04-30", title: "多地中小学开展课后服务质量提升行动", category: "校园", likes: 22, hits: 420, image: image("校园动态", "993380") },
  { id: 3, date: "2026-05-01", title: "小学科学实验课程资源包上线", category: "小学", likes: 9, hits: 156, image: image("科学实验") },
  { id: 4, date: "2026-05-03", title: "初中教师信息化教学能力培训启动", category: "教师", likes: 31, hits: 377, image: image("教师培训", "993380") },
  { id: 5, date: "2026-05-04", title: "AI 学习助手进入中小学个性化辅导场景", category: "科技", likes: 44, hits: 520, image: image("AI学习助手") },
  { id: 6, date: "2026-05-05", title: "学生居家自主学习平台使用指南发布", category: "学习", likes: 18, hits: 268, image: image("学习指南", "993380") }
];

export const courses = [
  { id: 1, number: "K12-MATH-001", teacher: "陈老师", semester: "2026 春季", name: "六年级数学应用题专项", type: "小学数学", price: 29.9, image: image("小学数学") },
  { id: 2, number: "K12-CHN-002", teacher: "王老师", semester: "2026 春季", name: "小学语文阅读理解提升", type: "小学语文", price: 19.9, image: image("小学语文", "993380") },
  { id: 3, number: "K12-ENG-003", teacher: "刘老师", semester: "2026 春季", name: "初一英语词汇与语法精讲", type: "初中英语", price: 24.9, image: image("初中英语") },
  { id: 4, number: "K12-PHY-004", teacher: "赵老师", semester: "2026 秋季", name: "初二物理力学基础", type: "初中物理", price: 34.9, image: image("初中物理", "993380") },
  { id: 5, number: "K12-CHE-005", teacher: "孙老师", semester: "2026 秋季", name: "初三化学基础知识梳理", type: "初中化学", price: 39.9, image: image("初中化学") },
  { id: 6, number: "K12-HIS-006", teacher: "周老师", semester: "2026 春季", name: "中考历史专题复习", type: "初中历史", price: 30, image: image("初中历史", "993380") }
];

export const videos = [
  { id: 1, teacher: "陈老师", name: "小升初数学错题讲解", duration: "18:20", origin: "本校录制", type: "小学数学", poster: image("数学视频") },
  { id: 2, teacher: "王老师", name: "记叙文阅读答题步骤", duration: "20:10", origin: "平台课程", type: "小学语文", poster: image("语文阅读", "993380") },
  { id: 3, teacher: "刘老师", name: "初一英语自然拼读复习", duration: "22:10", origin: "平台课程", type: "初中英语", poster: image("英语视频") },
  { id: 4, teacher: "赵老师", name: "初二物理力与运动", duration: "25:45", origin: "平台课程", type: "初中物理", poster: image("物理视频", "993380") }
];

export const notices = [
  { id: 1, title: "小学数学思维训练课程资料更新通知", category: "课程", create_time: "2026-05-01 09:00:00" },
  { id: 2, title: "期中复习专题直播安排公告", category: "教学", create_time: "2026-05-02 10:30:00" },
  { id: 3, title: "家长端学习报告查看功能维护通知", category: "系统", create_time: "2026-05-03 18:00:00" },
  { id: 4, title: "在线学习交流文明公约", category: "交流", create_time: "2026-05-04 14:20:00" }
];
