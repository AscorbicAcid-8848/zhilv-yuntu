<script setup lang="ts">
import type { Itinerary } from "../types";

defineProps<{
  itinerary: Itinerary;
  displayTips: string[];
}>();
</script>

<template>
  <section class="result-card">
    <div class="result-card__title">{{ itinerary.destination }}旅行计划</div>
    <div class="info-row"><strong>行程 ID：</strong>{{ itinerary.trip_id }}</div>
    <div class="info-row">
      <strong>日期：</strong>
      {{ itinerary.days[0]?.date || "待定" }} 至
      {{ itinerary.days[itinerary.days.length - 1]?.date || "待定" }}
    </div>
    <div class="info-row"><strong>地点：</strong>{{ itinerary.destination }}</div>
    <div class="info-row summary-text">{{ itinerary.summary }}</div>
    <div v-if="displayTips.length" class="overview-tips">
      <div class="overview-tips__title">旅行提示</div>
      <ul>
        <li v-for="tip in displayTips" :key="tip">{{ tip }}</li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
.result-card {
  padding: 18px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 22px 55px rgba(98, 116, 164, 0.12);
  backdrop-filter: blur(14px);
}

.result-card__title {
  margin-bottom: 14px;
  padding: 12px 14px;
  border-radius: 14px;
  background: linear-gradient(135deg, #6d82de 0%, #8a67cf 100%);
  color: #ffffff;
  font-size: 15px;
  font-weight: 700;
}

.info-row {
  margin-bottom: 10px;
  color: #475467;
  line-height: 1.7;
}

.summary-text {
  margin-top: 14px;
}

.overview-tips {
  margin-top: 18px;
  padding: 14px 16px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(109, 130, 222, 0.08), rgba(138, 103, 207, 0.08));
  border: 1px solid rgba(98, 116, 164, 0.08);
}

.overview-tips__title {
  margin-bottom: 8px;
  color: #465467;
  font-weight: 800;
}

.overview-tips ul {
  display: grid;
  gap: 8px;
  margin: 0;
  padding-left: 18px;
  color: #5d6675;
  line-height: 1.7;
}
</style>
