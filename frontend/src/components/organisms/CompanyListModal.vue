<script setup lang="ts">
import type { Company } from "../../types/api";
import AppModal from "../molecules/AppModal.vue";

defineProps<{
  open: boolean;
  companies: Company[];
}>();

const emit = defineEmits<{
  close: [];
  select: [company: Company];
}>();
</script>

<template>
  <AppModal
    :open="open"
    title="Empresas disponíveis"
    description="Escolha uma das empresas que já estão cadastradas para comparação."
    @close="$emit('close')"
  >
    <div class="company-list">
      <p v-if="companies.length === 0" class="muted-text">Lista indisponível no momento.</p>
      <button
        v-for="company in [...companies].sort((first, second) => first.name.localeCompare(second.name, 'pt-BR'))"
        :key="company.id"
        class="company-list__item"
        type="button"
        @click="emit('select', company)"
      >
        {{ company.name }}
      </button>
    </div>
  </AppModal>
</template>
