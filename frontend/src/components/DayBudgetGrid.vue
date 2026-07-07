<script setup lang="ts">
import { computed } from "vue";
import type { DayPlan } from "../types";

const props = defineProps<{
  days: DayPlan[];
}>();

const items = computed(() =>
  props.days.map((day) => {
    const tickets = day.spots.reduce((sum, s) => sum + (s.estimated_cost ?? 0), 0);
    const meals = day.meals.reduce((sum, m) => sum + (m.estimated_cost ?? 0), 0);
    const transport = day.transport.reduce((sum, t) => sum + (t.estimated_cost ?? 0), 0);
    const hotel = day.hotel?.estimated_cost ?? 0;
    const total = tickets + meals + transport + hotel;

    return {
      key: day.day_index,
      title: `第${day.day_index}天`,
      subtitle: day.theme || "未命名主题",
      tickets, meals, transport, hotel, total,
    };
  })
);
</script>

<template>
  <section class="result-card result-card--full">
    <div class="result-card__title">按天花费</div>
    <div class="day-budget-grid">
      <article
        v-for="item in items"
        :key="item.key"
        class="day-budget-card"
      >
        <div class="day-budget-card__header">
          <span>{{ item.title }}</span>
          <span>{{ item.subtitle }}</span>
        </div>
        <div class="day-budget-card__body">
          <div class="day-budget-row">
            <span>门票</span>
            <strong>¥{{ item.tickets.toFixed(0) }}</strong>
          </div>
          <div class="day-budget-row">
            <span>餐饮</span>
            <strong>¥{{ item.meals.toFixed(0) }}</strong>
          </div>
          <div class="day-budget-row">
            <span>交通</span>
            <strong>¥{{ item.transport.toFixed(0) }}</strong>
          </div>
          <div class="day-budget-row">
            <span>住宿</span>
            <strong>¥{{ item.hotel.toFixed(0) }}</strong>
          </div>
          <div class="day-budget-row day-budget-row--total">
            <span>当日合计</span>
            <strong>¥{{ item.total.toFixed(0) }}</strong>
          </div>
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

.day-budget-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}

.day-budget-card {
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(98, 116, 164, 0.08);
  background: #fbfcff;
}

.day-budget-card__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  background: rgba(109, 130, 222, 0.08);
  color: #465467;
  font-weight: 700;
}

.day-budget-card__body {
  display: grid;
  gap: 10px;
  padding: 16px;
}

.day-budget-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: #475467;
}

.day-budget-row--total {
  padding-top: 10px;
  border-top: 1px solid rgba(98, 116, 164, 0.08);
  color: #2f4fa5;
}
</style>
