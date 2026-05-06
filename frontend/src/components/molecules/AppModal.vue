<script setup lang="ts">
import { X } from "lucide-vue-next";
import { nextTick, ref, watch } from "vue";

import BaseButton from "../atoms/BaseButton.vue";

const props = defineProps<{
  open: boolean;
  title: string;
  description?: string;
}>();

const emit = defineEmits<{
  close: [];
}>();

const dialog = ref<HTMLDialogElement | null>(null);

watch(
  () => props.open,
  async (isOpen) => {
    await nextTick();

    if (!dialog.value) {
      return;
    }

    if (isOpen && !dialog.value.open) {
      dialog.value.showModal();
    }

    if (!isOpen && dialog.value.open) {
      dialog.value.close();
    }
  },
  { immediate: true },
);

function handleBackdropClick(event: MouseEvent): void {
  if (!dialog.value || event.target !== dialog.value) {
    return;
  }

  const rect = dialog.value.getBoundingClientRect();
  const clickedOutsideDialog =
    event.clientX < rect.left ||
    event.clientX > rect.right ||
    event.clientY < rect.top ||
    event.clientY > rect.bottom;

  if (clickedOutsideDialog) {
    emit("close");
  }
}
</script>

<template>
  <dialog ref="dialog" class="modal" @click="handleBackdropClick" @cancel.prevent @close="emit('close')">
    <div class="modal__header">
      <div>
        <h2>{{ title }}</h2>
        <p v-if="description">{{ description }}</p>
      </div>
      <BaseButton class="modal__close" variant="ghost" :icon="X" aria-label="Fechar" @click="emit('close')" />
    </div>
    <slot />
  </dialog>
</template>
