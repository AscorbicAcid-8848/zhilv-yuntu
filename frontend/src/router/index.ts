import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../views/Home.vue";
import Result from "../views/Result.vue";
import History from "../views/History.vue";

const routes = [
  { path: "/", name: "home", component: Home },
  { path: "/result", name: "result", component: Result },
  { path: "/history", name: "history", component: History },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
