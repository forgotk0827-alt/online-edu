import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import { createApp } from "vue";

import App from "./App.vue";
import router from "./router";
import { loadDatabaseData } from "./services/store";
import "./styles.css";

async function bootstrap() {
  await loadDatabaseData();
  createApp(App).use(router).use(ElementPlus).mount("#app");
}

bootstrap();
