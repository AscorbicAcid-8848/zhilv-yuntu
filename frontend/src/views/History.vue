<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { message } from "ant-design-vue";

import { deleteTrip, getTripDetail, listTrips } from "../services/api";
import { setItinerary } from "../stores/itinerary";
import type { TripSummaryItem } from "../types";

const router = useRouter();

const loading = ref(false);
const allItems = ref<TripSummaryItem[]>([]);
const deletingTripId = ref("");

const page = ref(1);
const pageSize = 6;

const totalPages = computed(() => Math.max(1, Math.ceil(allItems.value.length / pageSize)));

const items = computed(() => {
  const start = (page.value - 1) * pageSize;
  return allItems.value.slice(start, start + pageSize);
});

function goPage(p: number) {
  if (p >= 1 && p <= totalPages.value) page.value = p;
}

async function loadTrips() {
  loading.value = true;
  try {
    const response = await listTrips();
    allItems.value = response.items;
    page.value = 1;
  } catch {
    message.error("历史列表加载失败。");
  } finally {
    loading.value = false;
  }
}

async function openTrip(tripId: string) {
  try {
    const response = await getTripDetail(tripId);
    setItinerary(response.itinerary);
    message.success("已加载已保存行程。");
    router.push({ name: "result" });
  } catch {
    message.error("读取行程详情失败。");
  }
}

async function removeTrip(tripId: string) {
  if (!window.confirm("确定要删除这条已保存行程吗？删除后无法恢复。")) return;

  deletingTripId.value = tripId;
  try {
    await deleteTrip(tripId);
    allItems.value = allItems.value.filter((item) => item.trip_id !== tripId);
    if (items.value.length === 0 && page.value > 1) page.value--;
    message.success("行程已删除。");
  } catch {
    message.error("删除行程失败。");
  } finally {
    deletingTripId.value = "";
  }
}

onMounted(() => { void loadTrips(); });
</script>

<template>
  <section class="history-page">
    <div class="history-header">
      <div>
        <h2>历史行程</h2>
        <p>
          共 {{ allItems.length }} 条记录
          <template v-if="totalPages > 1">，第 {{ page }} / {{ totalPages }} 页</template>
        </p>
      </div>
      <button class="refresh-button" :disabled="loading" @click="loadTrips">
        {{ loading ? "加载中..." : "刷新列表" }}
      </button>
    </div>

    <!-- Skeleton loading -->
    <div v-if="loading" class="history-grid">
      <article v-for="n in 3" :key="'skel-' + n" class="history-card history-card--skeleton">
        <div class="skel-block skel-block--title"></div>
        <div class="skel-block skel-block--id"></div>
        <div class="skel-block skel-block--text"></div>
        <div class="skel-block skel-block--text skel-block--short"></div>
        <div class="skel-block skel-block--actions"></div>
      </article>
    </div>

    <!-- Empty -->
    <div v-else-if="allItems.length === 0" class="empty-state-card">
      <div class="empty-icon">📋</div>
      <h3>还没有已保存的行程</h3>
      <p>生成行程后在结果页点击「保存行程」即可出现在这里。</p>
      <button class="go-btn" @click="router.push({ name: 'home' })">去规划行程</button>
    </div>

    <!-- Data -->
    <template v-else>
      <div class="history-grid">
        <article
          v-for="item in items"
          :key="item.trip_id"
          class="history-card"
        >
          <div class="history-card__destination">{{ item.destination }}</div>
          <div class="history-card__trip-id">{{ item.trip_id }}</div>
          <p class="history-card__summary">{{ item.summary }}</p>
          <div class="history-card__time">
            更新时间：{{ item.updated_at || "未记录" }}
          </div>
          <div class="history-card__actions">
            <button class="history-card__button" @click="openTrip(item.trip_id)">查看详情</button>
            <button
              class="history-card__button history-card__button--danger"
              :disabled="deletingTripId === item.trip_id"
              @click="removeTrip(item.trip_id)"
            >
              {{ deletingTripId === item.trip_id ? "删除中..." : "删除" }}
            </button>
          </div>
        </article>
      </div>

      <!-- Pagination -->
      <nav v-if="totalPages > 1" class="pagination">
        <button class="page-btn" :disabled="page === 1" @click="goPage(1)">首页</button>
        <button class="page-btn" :disabled="page === 1" @click="goPage(page - 1)">上一页</button>
        <template v-for="p in totalPages" :key="p">
          <button
            v-if="p === 1 || p === totalPages || (p >= page - 1 && p <= page + 1)"
            :class="['page-btn', { 'page-btn--active': p === page }]"
            @click="goPage(p)"
          >
            {{ p }}
          </button>
          <span v-else-if="p === page - 2 || p === page + 2" class="page-ellipsis">...</span>
        </template>
        <button class="page-btn" :disabled="page === totalPages" @click="goPage(page + 1)">下一页</button>
        <button class="page-btn" :disabled="page === totalPages" @click="goPage(totalPages)">末页</button>
      </nav>
    </template>
  </section>
</template>

<style scoped>
.history-page {
  display: grid;
  gap: 18px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 16px;
  padding: 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 22px 55px rgba(98, 116, 164, 0.12);
}

.history-header h2 { margin: 0 0 8px; font-size: 28px; color: #31456a; }
.history-header p { margin: 0; color: #667085; }

.refresh-button,
.history-card__button,
.go-btn {
  border: none;
  border-radius: 14px;
  padding: 12px 22px;
  background: linear-gradient(135deg, #7386e0 0%, #8f71d8 100%);
  color: #ffffff;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
}

.refresh-button:hover,
.history-card__button:hover,
.go-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(109, 130, 222, 0.3);
}

.refresh-button:disabled,
.history-card__button:disabled {
  opacity: 0.65;
  cursor: wait;
  transform: none;
}

/* -- empty -- */
.empty-state-card {
  padding: 56px 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 22px 55px rgba(98, 116, 164, 0.12);
  text-align: center;
}

.empty-icon { font-size: 48px; margin-bottom: 16px; }

.empty-state-card h3 { margin: 0 0 10px; color: #31456a; }

.empty-state-card p { margin: 0 0 22px; color: #667085; line-height: 1.7; }

.go-btn { padding: 12px 28px; }

/* -- skeleton -- */
.history-card--skeleton { pointer-events: none; }

.skel-block {
  border-radius: 10px;
  background: linear-gradient(90deg, #eef2ff 25%, #e0e4f8 50%, #eef2ff 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

.skel-block--title { height: 32px; width: 55%; }
.skel-block--id { height: 18px; width: 80%; }
.skel-block--text { height: 16px; width: 100%; margin-top: 4px; }
.skel-block--short { width: 65%; }
.skel-block--actions { height: 44px; width: 100%; margin-top: 6px; }

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* -- grid & cards -- */
.history-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
}

.history-card {
  display: grid;
  gap: 12px;
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 22px 55px rgba(98, 116, 164, 0.12);
  transition: transform 0.2s, box-shadow 0.2s;
}

.history-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 26px 60px rgba(98, 116, 164, 0.18);
}

.history-card__destination {
  font-size: 28px;
  font-weight: 800;
  color: #42558d;
}

.history-card__trip-id {
  color: #8a94a6;
  font-size: 13px;
  word-break: break-all;
}

.history-card__summary {
  margin: 0;
  color: #475467;
  line-height: 1.7;
}

.history-card__time { color: #667085; font-size: 13px; }

.history-card__actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.history-card__button--danger {
  background: rgba(239, 68, 68, 0.12);
  color: #c2410c;
}

/* -- pagination -- */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  padding: 20px 0;
}

.page-btn {
  min-width: 40px;
  height: 40px;
  border: 1px solid rgba(109, 130, 222, 0.18);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.85);
  color: #475467;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.page-btn:hover:not(:disabled):not(.page-btn--active) {
  background: rgba(109, 130, 222, 0.08);
  border-color: rgba(109, 130, 222, 0.35);
}

.page-btn--active {
  background: linear-gradient(135deg, #7386e0 0%, #8f71d8 100%);
  color: #ffffff;
  border-color: transparent;
}

.page-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.page-ellipsis {
  width: 40px;
  text-align: center;
  color: #9ca3af;
  font-weight: 700;
}

@media (max-width: 640px) {
  .pagination { flex-wrap: wrap; }
}
</style>
