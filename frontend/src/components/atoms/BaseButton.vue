<script setup lang="ts">
import type { Component } from "vue";

defineProps<{
  variant?: "primary" | "secondary" | "ghost" | "danger";
  type?: "button" | "submit";
  disabled?: boolean;
  icon?: Component;
}>();
</script>

<template>
  <button
    class="base-button"
    :class="`base-button--${variant || 'primary'}`"
    :type="type || 'button'"
    :disabled="disabled"
  >
    <component :is="icon" v-if="icon" class="base-button__icon" aria-hidden="true" />
    <span><slot /></span>
  </button>
</template>

