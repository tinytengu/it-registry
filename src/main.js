import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'


import App from './App.vue'
import Home from './components/Home.vue'
import List from './components/List.vue'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import "./style.css"

const routes = [
    {
        path: "/",
        component: Home,
    },
    {
        path: "/list",
        component: List
    }

]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

const app = createApp(App);
app.use(router)
app.mount('#app')
