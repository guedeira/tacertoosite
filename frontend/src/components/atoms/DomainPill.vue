<script setup lang="ts">
defineProps<{
  domain: string;
}>();
</script>

<template>
  <span class="domain-pill">{{ domain }}</span>
</template>

