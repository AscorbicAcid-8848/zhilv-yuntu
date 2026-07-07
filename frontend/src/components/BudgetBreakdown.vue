<script setup lang="ts">
import { computed } from "vue";
import type { BudgetBreakdown } from "../types";

const props = defineProps<{
  estimatedBudget: number;
  budgetBreakdown: BudgetBreakdown;
}>();

const items = computed(() => [
  { label: "景点门票", value: `¥${props.budgetBreakdown.tickets.toFixed(0)}` },
  { label: "酒店住宿", value: `¥${props.budgetBreakdown.hotel.toFixed(0)}` },
  { label: "餐饮费用", value: `¥${props.budgetBreakdown.meals.toFixed(0)}` },
  { label: "交通费用", value: `¥${props.budgetBreakdown.transport.toFixed(0)}` },
]);
</script>

<template>
  <section class="result-card">
    <div class="result-card__title">预算明细</div>
    <div class="budget-grid">
      <div v-for="item in items" :key="item.label" class="budget-box">
        <div class="budget-box__label">{{ item.label }}</div>
        <div class="budget-box__value">{{ item.value }}</div>
      </div>
    </div>
    <div class="budget-total">
      <span>预估总费用</span>
      <strong>¥{{ estimatedBudget.toFixed(0) }}</strong>
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

.budget-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.budget-box {
  padding: 16px;
  border-radius: 16px;
  background: #f8faff;
  border: 1px solid rgba(98, 116, 164, 0.08);
}

.budget-box__label {
  color: #667085;
  font-size: 13px;
}

.budget-box__value {
  margin-top: 10px;
  color: #3b82f6;
  font-size: 22px;
  font-weight: 700;
}

.budget-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 14px;
  padding: 16px 18px;
  border-radius: 18px;
  background: linear-gradient(135deg, #7386e0 0%, #8f71d8 100%);
  color: #ffffff;
}

.budget-total strong {
  font-size: 28px;
}
</style>
