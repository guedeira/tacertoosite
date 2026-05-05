<script setup lang="ts">
import { AlertCircle, CheckCircle2, Info, LoaderCircle } from "lucide-vue-next";
import { computed } from "vue";

const props = defineProps<{
  tone?: "info" | "success" | "warning" | "error";
  message: string;
  busy?: boolean;
}>();

const icon = computed(() => {
  if (props.busy) {
    return LoaderCircle;
  }

  return {
    info: Info,
    success: CheckCircle2,
    warning: AlertCircle,
    error: AlertCircle,
  }[props.tone || "info"];
});
</script>

<template>
  <div class="status-message" :class="`status-message--${tone || 'info'}`" role="status" aria-live="polite">
    <component :is="icon" class="status-message__icon" :class="{ 'status-message__icon--spin': busy }" aria-hidden="true" />
    <span>{{ message }}</span>
  </div>
</template>

