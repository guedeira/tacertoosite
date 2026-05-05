<script setup lang="ts">
import { SearchCheck } from "lucide-vue-next";

defineProps<{
  href?: string;
  label?: string;
}>();
</script>

<template>
  <a class="brand-mark" :href="href || './index.html'" :aria-label="label || 'Página inicial'">
    <SearchCheck aria-hidden="true" />
    <span>Tá certo o site?</span>
  </a>
</template>
