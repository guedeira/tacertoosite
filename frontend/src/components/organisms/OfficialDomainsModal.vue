<script setup lang="ts">
import AppModal from "../molecules/AppModal.vue";

defineProps<{
  open: boolean;
  domains: string[];
}>();

defineEmits<{
  close: [];
}>();
</script>

<template>
  <AppModal
    :open="open"
    title="Domínios oficiais cadastrados"
    description="Esta é a lista usada na comparação para a empresa selecionada."
    @close="$emit('close')"
  >
    <div class="domain-list">
      <div v-for="domain in domains" :key="domain" class="domain-list__item">{{ domain }}</div>
    </div>
  </AppModal>
</template>

