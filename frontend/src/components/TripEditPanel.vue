<script setup lang="ts">
import { ref } from "vue";
import type { Itinerary } from "../types";

const props = defineProps<{
  itinerary: Itinerary;
  editing: boolean;
}>();

const emit = defineEmits<{
  edit: [scope: string, instruction: string];
}>();

const editScope = ref(`day_${props.itinerary.days[0]?.day_index ?? 1}`);
const editInstruction = ref("这一天节奏更轻松一点，减少固定安排。");
</script>

<template>
  <section class="result-card result-card--full">
    <div class="result-card__title">智能调整行程</div>
    <div class="edit-panel">
      <div class="edit-panel__controls">
        <label class="edit-field">
          <span>调整范围</span>
          <select v-model="editScope">
            <option
              v-for="day in itinerary.days"
              :key="day.day_index"
              :value="`day_${day.day_index}`"
            >
              第{{ day.day_index }}天 · {{ day.theme || "未命名主题" }}
            </option>
          </select>
        </label>
        <button
          class="edit-submit-button"
          :disabled="editing"
          @click="emit('edit', editScope, editInstruction)"
        >
          {{ editing ? "调整中..." : "智能调整" }}
        </button>
      </div>
      <textarea
        v-model="editInstruction"
        class="edit-textarea"
        rows="3"
        placeholder="例如：第二天轻松一点，不要安排太满；第三天想换成适合看日落的地点。"
      ></textarea>
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

.edit-panel {
  display: grid;
  gap: 14px;
}

.edit-panel__controls {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 150px;
  gap: 12px;
  align-items: end;
}

.edit-field {
  display: grid;
  gap: 8px;
  color: #465467;
  font-weight: 700;
}

.edit-field select,
.edit-textarea {
  width: 100%;
  border: 1px solid rgba(98, 116, 164, 0.18);
  border-radius: 14px;
  background: #fbfcff;
  color: #334155;
  font: inherit;
  outline: none;
}

.edit-field select {
  min-height: 44px;
  padding: 0 14px;
}

.edit-textarea {
  resize: vertical;
  min-height: 92px;
  padding: 12px 14px;
  line-height: 1.7;
}

.edit-field select:focus,
.edit-textarea:focus {
  border-color: rgba(109, 130, 222, 0.65);
  box-shadow: 0 0 0 3px rgba(109, 130, 222, 0.12);
}

.edit-submit-button {
  min-height: 44px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #7386e0 0%, #8f71d8 100%);
  color: #ffffff;
  font-weight: 800;
  cursor: pointer;
}

.edit-submit-button:disabled {
  opacity: 0.7;
  cursor: wait;
}

@media (max-width: 960px) {
  .edit-panel__controls {
    grid-template-columns: 1fr;
  }
}
</style>
