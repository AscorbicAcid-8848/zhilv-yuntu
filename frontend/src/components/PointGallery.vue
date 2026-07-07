<script setup lang="ts">
import type { TripMapPoint } from "../types/map";

defineProps<{
  points: TripMapPoint[];
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
    <div class="result-card__title">地图点位明细</div>
    <div class="point-grid">
      <article v-for="point in points" :key="point.key" class="point-card">
        <div class="point-card__header">
          <span>第{{ point.dayIndex }}天 · {{ point.name }}</span>
          <span>{{ formatShortDate(point.date) }}</span>
        </div>
        <div class="point-card__body">
          <div
            v-if="point.imageUrl"
            class="point-card__image"
            :style="{ backgroundImage: `url(${point.imageUrl})` }"
          ></div>
          <div v-else class="point-card__image point-card__image--empty">暂无景点图片</div>
          <div class="point-card__line">
            <strong>主题：</strong><span>{{ point.theme }}</span>
          </div>
          <div class="point-card__line">
            <strong>地址：</strong><span>{{ point.address }}</span>
          </div>
          <div class="point-card__desc">{{ point.description }}</div>
        </div>
      </article>
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

.point-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px;
}

.point-card {
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(98, 116, 164, 0.08);
  background: #fbfcff;
}

.point-card__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  background: rgba(109, 130, 222, 0.08);
  color: #465467;
  font-weight: 700;
}

.point-card__body {
  display: grid;
  gap: 10px;
  padding: 16px;
}

.point-card__image {
  min-height: 150px;
  border-radius: 14px;
  background-position: center;
  background-size: cover;
  background-color: #eef3ff;
}

.point-card__image--empty {
  display: grid;
  place-items: center;
  color: #7b8494;
  font-weight: 700;
  background:
    linear-gradient(135deg, rgba(129, 179, 255, 0.18), rgba(137, 108, 230, 0.15)),
    #f7f9ff;
}

.point-card__line {
  color: #475467;
  line-height: 1.7;
}

.point-card__desc {
  padding-top: 10px;
  border-top: 1px solid rgba(98, 116, 164, 0.08);
  color: #667085;
  line-height: 1.7;
}
</style>
