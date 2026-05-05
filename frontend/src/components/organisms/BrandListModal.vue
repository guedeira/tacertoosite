<script setup lang="ts">
import type { Brand } from "../../types/api";
import AppModal from "../molecules/AppModal.vue";

defineProps<{
  open: boolean;
  brands: Brand[];
}>();

const emit = defineEmits<{
  close: [];
  select: [brand: Brand];
}>();
</script>

<template>
  <AppModal
    :open="open"
    title="Empresas disponíveis"
    description="Escolha uma das empresas que já estão cadastradas para comparação."
    @close="$emit('close')"
  >
    <div class="brand-list">
      <p v-if="brands.length === 0" class="muted-text">Lista indisponível no momento.</p>
      <button
        v-for="brand in [...brands].sort((first, second) => first.name.localeCompare(second.name, 'pt-BR'))"
        :key="brand.id"
        class="brand-list__item"
        type="button"
        @click="emit('select', brand)"
      >
        {{ brand.name }}
      </button>
    </div>
  </AppModal>
</template>

