import { ref } from "vue";
import type { Itinerary } from "../types";

export const currentItinerary = ref<Itinerary | null>(null);

export function setItinerary(itinerary: Itinerary) {
  currentItinerary.value = itinerary;
}

export function clearItinerary() {
  currentItinerary.value = null;
}
