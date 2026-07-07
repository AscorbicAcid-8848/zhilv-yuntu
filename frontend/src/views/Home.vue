<script setup lang="ts">
import axios from "axios";
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { message } from "ant-design-vue";

import { generateTrip } from "../services/api";
import { setItinerary } from "../stores/itinerary";
import type { Itinerary, TripRequestPayload } from "../types";

const router = useRouter();

const preferenceOptions = ["自然风景", "拍照", "美食", "古镇", "休闲"];
const dietaryOptions = ["少辣", "不吃香菜", "不吃葱"];

const quickDestinations = [
  { label: "大理", icon: "🏔️" },
  { label: "成都", icon: "🐼" },
  { label: "杭州", icon: "🌊" },
  { label: "西安", icon: "🏯" },
  { label: "厦门", icon: "🌴" },
  { label: "青岛", icon: "🍺" },
];

function quickFill(dest: string) {
  formState.destination = dest;
}

function formatDate(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

const today = new Date();
const todayPlus2 = new Date(today);
todayPlus2.setDate(todayPlus2.getDate() + 2);

const formDefaults = {
  destination: "",
  startDate: formatDate(today),
  endDate: formatDate(todayPlus2),
  travelers: 2,
  budget: 3200,
  hotelLevel: "舒适型",
  pace: "轻松",
  preferences: [] as string[],
  dietaryPreferences: [] as string[],
  notes: "",
};

const formState = reactive({ ...formDefaults });

const isSubmitting = ref(false);

const dayCount = computed(() => {
  const start = new Date(formState.startDate);
  const end = new Date(formState.endDate);
  const diff = end.getTime() - start.getTime();
  return Number.isNaN(diff) ? 0 : Math.max(Math.floor(diff / 86400000) + 1, 0);
});

function resetForm() {
  Object.assign(formState, { ...formDefaults });
}

async function handleSubmit() {
  if (!formState.destination.trim()) {
    message.warning("请输入目的地城市。");
    return;
  }

  const payload: TripRequestPayload = {
    destination: formState.destination,
    start_date: formState.startDate,
    end_date: formState.endDate,
    travelers: formState.travelers,
    budget: formState.budget,
    preferences: formState.preferences,
    pace: formState.pace,
    dietary_preferences: formState.dietaryPreferences,
    hotel_level: formState.hotelLevel,
    special_notes: formState.notes,
  };

  isSubmitting.value = true;
  try {
    const itinerary = await generateTrip(payload);
    setItinerary(itinerary);
    message.success("行程生成成功！");
    router.push({ name: "result" });
  } catch (error) {
    console.error(error);
    if (axios.isAxiosError(error)) {
      if (error.code === "ECONNABORTED") {
        message.error("行程生成超时，模型返回较慢，请稍后再试。");
      } else if (error.response) {
        message.error(`行程生成失败：后端返回 ${error.response.status}。`);
      } else {
        message.error("行程生成失败，请检查前端到后端的连接。");
      }
    } else {
      message.error("行程生成失败，请检查后端地址或服务状态。");
    }
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <section class="home-page">
    <div class="planner-card">
      <div class="section-title">
        <span>目的地与日期</span>
      </div>

      <a-row :gutter="[16, 16]">
        <a-col :xs="24" :md="8">
          <label class="field-label">目的地城市</label>
          <a-input v-model:value="formState.destination" placeholder="请输入目的地" />
          <div class="quick-dest-row">
            <button
              v-for="d in quickDestinations"
              :key="d.label"
              :class="['quick-dest-btn', { 'quick-dest-btn--active': formState.destination === d.label }]"
              type="button"
              @click="quickFill(d.label)"
            >
              {{ d.icon }} {{ d.label }}
            </button>
          </div>
        </a-col>
        <a-col :xs="24" :md="5">
          <label class="field-label">开始日期</label>
          <a-input v-model:value="formState.startDate" />
        </a-col>
        <a-col :xs="24" :md="5">
          <label class="field-label">结束日期</label>
          <a-input v-model:value="formState.endDate" />
        </a-col>
        <a-col :xs="12" :md="3">
          <label class="field-label">人数</label>
          <a-input-number v-model:value="formState.travelers" :min="1" style="width: 100%" />
        </a-col>
        <a-col :xs="12" :md="3">
          <label class="field-label">旅行天数</label>
          <div class="pill-box">{{ dayCount }} 天</div>
        </a-col>
      </a-row>
    </div>

    <div class="planner-card">
      <div class="section-title">偏好设置</div>

      <a-row :gutter="[16, 16]">
        <a-col :xs="24" :md="8">
          <label class="field-label">节奏偏好</label>
          <a-select
            v-model:value="formState.pace"
            :options="[
              { label: '轻松', value: '轻松' },
              { label: '适中', value: '适中' },
              { label: '紧凑', value: '紧凑' }
            ]"
          />
        </a-col>
        <a-col :xs="24" :md="8">
          <label class="field-label">住宿偏好</label>
          <a-select
            v-model:value="formState.hotelLevel"
            :options="[
              { label: '舒适型', value: '舒适型' },
              { label: '高档型', value: '高档型' },
              { label: '经济型', value: '经济型' }
            ]"
          />
        </a-col>
        <a-col :xs="24" :md="8">
          <label class="field-label">预算</label>
          <a-input-number v-model:value="formState.budget" :min="0" style="width: 100%" />
        </a-col>
      </a-row>

      <div class="checkbox-area">
        <label class="field-label">旅行偏好</label>
        <a-checkbox-group v-model:value="formState.preferences" :options="preferenceOptions" />
      </div>

      <div class="checkbox-area">
        <label class="field-label">饮食偏好</label>
        <a-checkbox-group v-model:value="formState.dietaryPreferences" :options="dietaryOptions" />
      </div>
    </div>

    <div class="planner-card">
      <div class="section-title">额外要求</div>
      <a-textarea
        v-model:value="formState.notes"
        :rows="4"
        placeholder="输入想要保留的偏好、节奏和备注"
      />
    </div>

    <div class="submit-panel">
      <button
        class="submit-panel__button"
        :disabled="isSubmitting"
        @click="handleSubmit"
      >
        {{ isSubmitting ? "正在生成中..." : "开始规划" }}
      </button>
      <div class="submit-panel__status">
        当前已接上 /trip/generate 接口
      </div>
    </div>
  </section>
</template>

<style scoped>
.home-page {
  display: grid;
  gap: 18px;
}

.planner-card {
  padding: 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 22px 55px rgba(98, 116, 164, 0.12);
  backdrop-filter: blur(14px);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(106, 116, 215, 0.18);
  color: #394867;
  font-size: 16px;
  font-weight: 700;
}

.field-label {
  display: block;
  margin-bottom: 8px;
  color: #667085;
  font-size: 13px;
  font-weight: 600;
}

.quick-dest-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}

.quick-dest-btn {
  border: 1px solid rgba(109, 130, 222, 0.22);
  border-radius: 999px;
  padding: 5px 14px;
  background: rgba(255, 255, 255, 0.7);
  color: #475467;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.quick-dest-btn:hover {
  background: rgba(109, 130, 222, 0.1);
  border-color: rgba(109, 130, 222, 0.45);
}

.quick-dest-btn--active {
  background: linear-gradient(135deg, #7386e0 0%, #8f71d8 100%);
  color: #ffffff;
  border-color: transparent;
}

.pill-box {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 32px;
  border-radius: 12px;
  background: linear-gradient(135deg, #7386e0 0%, #8f71d8 100%);
  color: #ffffff;
  font-weight: 700;
}

.checkbox-area {
  margin-top: 18px;
}

.submit-panel {
  padding: 12px 8px 0;
  text-align: center;
}

.submit-panel__button {
  min-width: 220px;
  border: none;
  border-radius: 999px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #7d8ff0 0%, #a57fd8 100%);
  color: #ffffff;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 18px 35px rgba(120, 129, 225, 0.25);
}

.submit-panel__button:disabled {
  opacity: 0.7;
  cursor: wait;
}

.submit-panel__status {
  margin-top: 12px;
  color: #6b7280;
  font-size: 13px;
}
</style>
