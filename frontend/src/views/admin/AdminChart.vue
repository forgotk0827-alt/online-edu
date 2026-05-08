<template>
  <section class="admin-panel">
    <h1 class="admin-title">购买资料统计</h1>
    <div ref="chartRef" class="chart"></div>
    <div class="chart-actions">
      <button class="admin-btn" @click="download">下载图表</button>
    </div>
  </section>
</template>

<script setup>
import * as echarts from "echarts";
import { onMounted, ref } from "vue";

const chartRef = ref();
let chart;

onMounted(() => {
  chart = echarts.init(chartRef.value);
  chart.setOption({
    color: ["#7373E6", "#5A5AD9", "#9B9BFF"],
    tooltip: { trigger: "axis" },
    legend: { data: ["Python 程序设计", "大学英语精讲", "高等数学"] },
    grid: { left: 40, right: 20, bottom: 40, top: 60 },
    xAxis: { type: "category", data: ["1月", "2月", "3月", "4月", "5月", "6月"] },
    yAxis: { type: "value" },
    series: [
      { name: "Python 程序设计", type: "line", smooth: true, data: [12, 18, 30, 25, 42, 56] },
      { name: "大学英语精讲", type: "line", smooth: true, data: [8, 15, 18, 28, 33, 40] },
      { name: "高等数学", type: "line", smooth: true, data: [6, 10, 16, 22, 31, 38] }
    ]
  });
  window.addEventListener("resize", () => chart.resize());
});

function download() {
  const link = document.createElement("a");
  link.download = "购买资料统计.png";
  link.href = chart.getDataURL({ pixelRatio: 2, backgroundColor: "#fff" });
  link.click();
}
</script>

<style scoped>
.chart {
  width: 100%;
  height: 430px;
}

.chart-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
