import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import './assets/main.css'
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'; // Import styles
import { createPinia } from 'pinia'


const app = createApp(App);

app.use(router);

app.use(createPinia()) 

app.use(Toast);
app.use(ElementPlus);
app.mount("#app");
