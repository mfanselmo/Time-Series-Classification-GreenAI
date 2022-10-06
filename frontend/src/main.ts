import { createApp } from 'vue'
import './tailwind.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router/auto'
import { VueQueryPlugin } from "vue-query";
import { createHead } from '@vueuse/head'
import { createPinia } from "pinia";


const app = createApp(App)
const head = createHead()

const router = createRouter({
  history: createWebHistory(),
})



app.use(router)
app.use(head)
app.use(VueQueryPlugin)
app.use(createPinia())
app.mount(document.body)
