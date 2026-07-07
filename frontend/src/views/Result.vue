<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { message } from "ant-design-vue";

import AmapTripMap from "../components/AmapTripMap.vue";
import BudgetBreakdown from "../components/BudgetBreakdown.vue";
import DailyPlan from "../components/DailyPlan.vue";
import DayBudgetGrid from "../components/DayBudgetGrid.vue";
import PointGallery from "../components/PointGallery.vue";
import ResultOverview from "../components/ResultOverview.vue";
import TripEditPanel from "../components/TripEditPanel.vue";
import WeatherPanel from "../components/WeatherPanel.vue";
import {
  editTrip,
  fetchWeatherForecast,
  getMarkdownExportUrl,
  getPdfExportUrl,
  saveTrip,
} from "../services/api";
import { currentItinerary, setItinerary } from "../stores/itinerary";
import type { Itinerary, WeatherForecastResponse } from "../types";
import type { TripMapPoint } from "../types/map";

const router = useRouter();

// -- side effects --------------------------------------------------------
const saving = ref(false);
const exportingPdf = ref(false);
const exportingMarkdown = ref(false);
const editing = ref(false);

// -- weather -------------------------------------------------------------
const weatherLoading = ref(false);
const weatherError = ref("");
const weather = ref<WeatherForecastResponse | null>(null);

const weatherText = computed(() => {
  if (!weather.value) return "";
  return weather.value.days
    .map((d) => `${d.day_weather || ""}${d.night_weather || ""}`)
    .join(" ");
});

const hasRainyWeather = computed(() => {
  const rainKeywords = ["雨", "阵雨", "雷阵雨", "小雨", "中雨", "大雨"];
  return rainKeywords.some((kw) => weatherText.value.includes(kw));
});

const displayTips = computed(() => {
  if (!currentItinerary.value) return [];

  const technicalKeywords = ["LLM", "RAG", "LangChain", "Chroma", "演示", "测试", "规则", "模型", "源码"];
  const sunnyKeywords = ["防晒", "太阳", "日照", "晒"];

  const tips = currentItinerary.value.tips
    .map((t) => t.trim())
    .filter(Boolean)
    .filter((t) => !technicalKeywords.some((kw) => t.includes(kw)));

  const filtered = hasRainyWeather.value
    ? tips.filter((t) => !sunnyKeywords.some((kw) => t.includes(kw)))
    : tips;

  if (hasRainyWeather.value) {
    filtered.push("天气可能有雨，建议随身带伞或轻便雨衣。");
    filtered.push("阴雨天路面湿滑，洱海边和古镇石板路建议穿防滑鞋。");
  }

  const unique = Array.from(new Set(filtered));
  if (unique.length) return unique;

  return [
    `建议根据${currentItinerary.value.destination}当天实时天气准备雨具或薄外套。`,
    "古镇、生态廊道和石板路更适合慢慢走，鞋子尽量选择舒适防滑的款式。",
  ];
});

function buildVisibleItinerary(): Itinerary | null {
  if (!currentItinerary.value) return null;
  return { ...currentItinerary.value, tips: displayTips.value };
}

const sidebarNav = [
  { label: "行程概览", icon: "📋", target: "section-overview" },
  { label: "预算明细", icon: "💰", target: "section-budget" },
  { label: "景点地图", icon: "🗺️", target: "section-map" },
  { label: "天气信息", icon: "🌤️", target: "section-weather" },
  { label: "智能调整", icon: "✨", target: "section-edit" },
  { label: "按天花费", icon: "📊", target: "section-day-budget" },
  { label: "点位明细", icon: "📍", target: "section-points" },
  { label: "每日行程", icon: "📅", target: "section-days" },
];

function scrollToSection(id: string) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
}
const mapPoints = computed<TripMapPoint[]>(() => {
  if (!currentItinerary.value) return [];

  return currentItinerary.value.days.flatMap((day) =>
    day.spots.map((spot) => ({
      key: `${day.day_index}-${spot.name}`,
      dayIndex: day.day_index,
      date: day.date || "待定",
      theme: day.theme || "未命名主题",
      name: spot.name,
      address: spot.address || spot.location || "待补充",
      latitude: spot.latitude,
      longitude: spot.longitude,
      poiId: spot.poi_id,
      imageUrl: spot.image_url,
      description: spot.description || "暂无说明",
    }))
  );
});

// -- actions -------------------------------------------------------------
async function loadWeather() {
  if (!currentItinerary.value?.destination) { weather.value = null; return; }
  weatherLoading.value = true;
  weatherError.value = "";
  try {
    weather.value = await fetchWeatherForecast(currentItinerary.value.destination);
  } catch {
    weather.value = null;
    weatherError.value = "天气信息加载失败。";
  } finally {
    weatherLoading.value = false;
  }
}

watch(() => currentItinerary.value?.destination, () => { void loadWeather(); }, { immediate: true });

async function handleSave() {
  const it = buildVisibleItinerary();
  if (!it) return;
  saving.value = true;
  try {
    await saveTrip(it);
    message.success("行程已保存，可以去历史列表查看。");
  } catch {
    message.error("保存行程失败。");
  } finally {
    saving.value = false;
  }
}

async function handleEdit(scope: string, instruction: string) {
  if (!currentItinerary.value) return;
  editing.value = true;
  try {
    const updated = await editTrip({
      trip_id: currentItinerary.value.trip_id,
      current_itinerary: currentItinerary.value,
      user_instruction: instruction,
      edit_scope: scope,
      preserve_constraints: ["保留预算结构", "保留目的地和旅行日期"],
    });
    setItinerary(updated);
    message.success("行程已智能调整。");
  } catch {
    message.error("智能调整失败，请稍后再试。");
  } finally {
    editing.value = false;
  }
}

async function openExport(format: "pdf" | "markdown") {
  const it = buildVisibleItinerary();
  if (!it) return;

  const exporting = format === "pdf" ? exportingPdf : exportingMarkdown;
  exporting.value = true;
  const w = window.open("about:blank", "_blank");
  try {
    await saveTrip(it);
    const url = format === "pdf" ? getPdfExportUrl(it.trip_id) : getMarkdownExportUrl(it.trip_id);
    if (w) w.location.href = url;
    else window.location.href = url;
  } catch {
    w?.close();
    message.error(`导出 ${format.toUpperCase()} 前同步当前行程失败。`);
  } finally {
    exporting.value = false;
  }
}
</script>

<template>
  <section v-if="currentItinerary" class="result-page">
    <aside class="sidebar-card">
      <div class="sidebar-card__title">行程导航</div>
      <ul class="sidebar-list">
        <li
          v-for="item in sidebarNav"
          :key="item.target"
          class="sidebar-list__item"
          @click="scrollToSection(item.target)"
        >
          <span class="sidebar-list__icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </li>
      </ul>

      <div class="sidebar-actions">
        <button class="back-button" @click="router.push({ name: 'home' })">返回规划页</button>
        <button class="save-button" :disabled="saving" @click="handleSave">
          {{ saving ? "保存中..." : "保存行程" }}
        </button>
        <button class="history-button" @click="router.push({ name: 'history' })">历史列表</button>
        <button class="export-button" :disabled="exportingPdf" @click="openExport('pdf')">
          {{ exportingPdf ? "准备 PDF..." : "导出 PDF" }}
        </button>
        <button
          class="export-button export-button--light"
          :disabled="exportingMarkdown"
          @click="openExport('markdown')"
        >
          {{ exportingMarkdown ? "准备中..." : "导出 Markdown" }}
        </button>
      </div>
    </aside>

    <div class="result-grid">
      <div id="section-overview">
        <ResultOverview :itinerary="currentItinerary" :display-tips="displayTips" />
      </div>
      <div id="section-budget">
        <BudgetBreakdown
          :estimated-budget="currentItinerary.estimated_budget"
          :budget-breakdown="currentItinerary.budget_breakdown"
        />
      </div>

      <section id="section-map" class="result-card result-card--map">
        <div class="result-card__title">景点地图</div>
        <AmapTripMap :points="mapPoints" />
      </section>

      <div id="section-weather">
        <WeatherPanel :weather="weather" :loading="weatherLoading" :error="weatherError" />
      </div>

      <div id="section-edit">
        <TripEditPanel
          :itinerary="currentItinerary"
          :editing="editing"
          @edit="handleEdit"
        />
      </div>

      <div id="section-day-budget">
        <DayBudgetGrid :days="currentItinerary.days" />
      </div>
      <div id="section-points">
        <PointGallery :points="mapPoints" />
      </div>
      <div id="section-days">
        <DailyPlan :days="currentItinerary.days" />
      </div>
    </div>
  </section>

  <section v-else class="empty-state">
    <div class="empty-state__card">
      <h2>还没有生成结果</h2>
      <p>先回到规划页生成一条 itinerary，结果页就会开始展示真实数据。</p>
      <button class="back-button" @click="router.push({ name: 'home' })">返回规划页</button>
    </div>
  </section>
</template>

<style scoped>
.result-page {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 22px;
}

.sidebar-card,
.result-card,
.empty-state__card {
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 22px 55px rgba(98, 116, 164, 0.12);
  backdrop-filter: blur(14px);
}

.sidebar-card {
  align-self: start;
  padding: 18px;
}

.sidebar-card__title,
.result-card__title {
  margin-bottom: 14px;
  padding: 12px 14px;
  border-radius: 14px;
  background: linear-gradient(135deg, #6d82de 0%, #8a67cf 100%);
  color: #ffffff;
  font-size: 15px;
  font-weight: 700;
}

.sidebar-list {
  display: grid;
  gap: 6px;
  padding: 0;
  margin: 0 0 18px;
  list-style: none;
  color: #475467;
  font-size: 14px;
}

.sidebar-list__item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.15s;
}

.sidebar-list__item:hover {
  background: rgba(109, 130, 222, 0.08);
  color: #5f60c8;
}

.sidebar-list__icon {
  font-size: 16px;
  width: 24px;
  text-align: center;
}

.sidebar-actions {
  display: grid;
  gap: 10px;
}

.back-button,
.save-button,
.history-button,
.export-button {
  width: 100%;
  border: none;
  border-radius: 14px;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.back-button {
  background: rgba(109, 130, 222, 0.12);
  color: #5d66c3;
}

.save-button {
  background: linear-gradient(135deg, #7386e0 0%, #8f71d8 100%);
  color: #ffffff;
}

.save-button:disabled,
.export-button:disabled {
  opacity: 0.7;
  cursor: wait;
}

.history-button {
  background: rgba(79, 70, 229, 0.1);
  color: #5b5bd6;
}

.export-button {
  background: rgba(59, 130, 246, 0.12);
  color: #3568d4;
}

.export-button--light {
  background: rgba(16, 185, 129, 0.12);
  color: #0f8c63;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.result-card {
  padding: 18px;
}

.result-card--map {
  min-height: 330px;
}

.empty-state {
  display: grid;
  place-items: center;
  min-height: 360px;
}

.empty-state__card {
  max-width: 560px;
  padding: 36px;
  text-align: center;
}

.empty-state__card h2 { margin: 0 0 12px; }

.empty-state__card p {
  margin: 0 0 18px;
  color: #667085;
  line-height: 1.7;
}

@media (max-width: 960px) {
  .result-page { grid-template-columns: 1fr; }
  .result-grid { grid-template-columns: 1fr; }
}
</style>
