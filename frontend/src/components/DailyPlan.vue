<script setup lang="ts">
import type { DayPlan } from "../types";

defineProps<{
  days: DayPlan[];
}>();

function formatShortDate(dateText?: string | null): string {
  if (!dateText) return "待定";
  const parts = dateText.split("-");
  if (parts.length !== 3) return dateText;
  return `${parts[1]}-${parts[2]}`;
}
</script>

<template>
  <section class="result-card result-card--full">
    <div class="result-card__title">每日行程</div>
    <div class="day-list">
      <details
        v-for="day in days"
        :key="day.day_index"
        class="day-card"
        :open="day.day_index === 1"
      >
        <summary class="day-card__header">
          <span>第{{ day.day_index }}天 · {{ day.theme || "未命名主题" }}</span>
          <span class="day-card__meta">{{ formatShortDate(day.date) }}</span>
        </summary>

        <div class="day-card__body">
          <div class="day-card__section">
            <strong>主要景点：</strong>
            <span>{{ day.spots[0]?.name || "未安排" }}</span>
          </div>
          <div class="day-card__section">
            <strong>景点地址：</strong>
            <span>{{ day.spots[0]?.address || day.spots[0]?.location || "待补充" }}</span>
          </div>
          <div class="day-card__section">
            <strong>餐饮建议：</strong>
            <span>{{ day.meals[0]?.name || "未安排" }}</span>
          </div>
          <div class="day-card__section">
            <strong>住宿安排：</strong>
            <span>{{ day.hotel?.name || "未安排" }}</span>
          </div>
          <div class="day-card__section">
            <strong>交通信息：</strong>
            <span>
              {{
                day.transport[0]?.distance_km != null
                  ? `${day.transport[0].distance_km.toFixed(2)} km / ${day.transport[0].estimated_minutes ?? 0} 分钟`
                  : day.transport[0]?.duration || "待补充"
              }}
            </span>
          </div>
          <div class="day-card__section">
            <strong>备注：</strong>
            <span>{{ day.notes[day.notes.length - 1] || "无" }}</span>
          </div>
        </div>
      </details>
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

.result-card--full {
  grid-column: 1 / -1;
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

.day-list {
  display: grid;
  gap: 12px;
}

.day-card {
  border-radius: 18px;
  border: 1px solid rgba(98, 116, 164, 0.08);
  background: #fbfcff;
  overflow: hidden;
}

.day-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: rgba(109, 130, 222, 0.08);
  color: #465467;
  font-weight: 700;
  cursor: pointer;
  list-style: none;
}

.day-card__header::-webkit-details-marker {
  display: none;
}

.day-card__header::after {
  content: "展开";
  flex: 0 0 auto;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(109, 130, 222, 0.12);
  color: #5b5bd6;
  font-size: 12px;
}

.day-card[open] .day-card__header::after {
  content: "收起";
}

.day-card__meta {
  margin-left: auto;
  color: #667085;
  font-size: 13px;
}

.day-card__body {
  display: grid;
  gap: 10px;
  padding: 16px;
}

.day-card__section {
  color: #475467;
  line-height: 1.7;
}
</style>
