<script setup lang="ts">
import type { WeatherForecastResponse } from "../types";

defineProps<{
  weather: WeatherForecastResponse | null;
  loading: boolean;
  error: string;
}>();

function formatWeatherDate(dateText?: string | null, week?: string | null): string {
  const weekdayMap: Record<string, string> = {
    "1": "周一", "2": "周二", "3": "周三", "4": "周四",
    "5": "周五", "6": "周六", "7": "周日",
  };

  const weekday = week ? weekdayMap[week] || `周${week}` : "";
  const parts = dateText?.split("-") ?? [];
  const short = parts.length === 3 ? `${parts[1]}-${parts[2]}` : dateText || "待定";
  return [short, weekday].filter(Boolean).join(" ");
}
</script>

<template>
  <section class="result-card result-card--weather">
    <div class="result-card__title">天气信息</div>

    <div v-if="loading" class="weather-state">正在加载天气信息...</div>
    <div v-else-if="error" class="weather-state">{{ error }}</div>
    <div v-else-if="weather" class="weather-grid">
      <article
        v-for="day in weather.days"
        :key="`${day.date}-${day.week}`"
        class="weather-card"
      >
        <div class="weather-card__date">{{ formatWeatherDate(day.date, day.week) }}</div>
        <div class="weather-card__temp">
          {{ day.day_temp || "-" }}° / {{ day.night_temp || "-" }}°
        </div>
        <div class="weather-card__desc">白天：{{ day.day_weather || "未知" }}</div>
        <div class="weather-card__desc">夜间：{{ day.night_weather || "未知" }}</div>
      </article>
    </div>
    <div v-else class="weather-state">暂无天气信息。</div>
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

.result-card--weather {
  min-height: 330px;
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

.weather-state {
  color: #667085;
  line-height: 1.8;
}

.weather-grid {
  display: grid;
  gap: 12px;
}

.weather-card {
  padding: 14px;
  border-radius: 16px;
  background: #f8faff;
  border: 1px solid rgba(98, 116, 164, 0.08);
}

.weather-card__date {
  color: #465467;
  font-weight: 700;
}

.weather-card__temp {
  margin: 8px 0;
  color: #3b82f6;
  font-size: 24px;
  font-weight: 800;
}

.weather-card__desc {
  color: #667085;
  line-height: 1.7;
}
</style>
