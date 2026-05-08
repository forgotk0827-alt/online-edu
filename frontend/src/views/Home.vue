<template>
  <ClientLayout>
    <section class="hero">
      <el-carousel class="hero-carousel" height="380px" indicator-position="outside" :interval="4500">
        <el-carousel-item v-for="banner in bannerSlides" :key="banner.id">
          <div class="banner-slide" :style="{ backgroundImage: `url(${banner.image})` }">
            <div class="banner-mask"></div>
            <div class="blackboard">
              <p>Online Education</p>
              <h1>{{ banner.title }}</h1>
              <span>{{ banner.subtitle }}</span>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </section>

    <section class="client-panel">
      <PageTitle title="推荐课程" />
      <div class="course-mini">
        <article v-for="course in courses" :key="course.id">
          <img :src="course.image" :alt="course.name" />
          <strong>{{ course.name }}</strong>
          <span>{{ course.type }} ｜ ￥{{ course.price }}</span>
        </article>
      </div>
    </section>
  </ClientLayout>
</template>

<script setup>
import { computed, onMounted } from "vue";
import ClientLayout from "../components/ClientLayout.vue";
import PageTitle from "../components/PageTitle.vue";
import { refreshBanners, store } from "../services/store";

const defaultSlides = [
  { title: "让学习保持在线", subtitle: "课程、视频、资料与交流一站完成", image: "https://dummyimage.com/1200x380/23372f/ffffff&text=Online+Education" },
  { title: "发现适合你的课程", subtitle: "基于学习行为的个性化推荐", image: "https://dummyimage.com/1200x380/993380/ffffff&text=Course+Recommendation" },
  { title: "师生共享知识", subtitle: "教师上传资源，学生沉淀学习", image: "https://dummyimage.com/1200x380/B377B3/ffffff&text=Teacher+%26+Student" }
];

const bannerSlides = computed(() => {
  const source = Array.isArray(store.banners) && store.banners.length ? store.banners : defaultSlides;
  return source.map((item, index) => ({
    id: item.id || index + 1,
    image: item.image || defaultSlides[index % defaultSlides.length].image,
    title: item.title || defaultSlides[index % defaultSlides.length].title,
    subtitle: item.subtitle || defaultSlides[index % defaultSlides.length].subtitle
  }));
});

const courses = store.courses;

onMounted(() => {
  refreshBanners();
});
</script>

<style scoped>
.hero {
  margin: 30px 0;
}

.hero-carousel {
  border-radius: 8px;
  overflow: hidden;
}

.banner-slide {
  position: relative;
  height: 380px;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.banner-mask {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(35, 55, 47, 0.72), rgba(35, 55, 47, 0.28));
}

.blackboard {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  align-content: center;
  gap: 18px;
  padding: 36px;
  color: #fff;
  text-align: center;
  z-index: 1;
}

.blackboard h1 {
  margin: 0;
  font-size: 40px;
}

.blackboard p,
.blackboard span {
  margin: 0;
  color: #f5d7ee;
}

.course-mini {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.course-mini article {
  padding: 16px;
  border: 1px solid #e6d4e6;
  border-radius: 8px;
  background: #fff;
}

.course-mini img {
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  border-radius: 6px;
}

.course-mini strong,
.course-mini span {
  display: block;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .course-mini {
    grid-template-columns: 1fr;
  }

  .blackboard h1 {
    font-size: 30px;
  }
}
</style>
