<script setup lang="ts">
defineProps<{
  id: string;
  label: string;
  hint?: string;
  modelValue: string;
  placeholder?: string;
  type?: string;
  required?: boolean;
  disabled?: boolean;
  autocomplete?: string;
}>();

defineEmits<{
  "update:modelValue": [value: string];
}>();
</script>

<template>
  <div class="field">
    <label class="field__label" :for="id">{{ label }}</label>
    <input
      :id="id"
      class="field__control"
      :type="type || 'text'"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :autocomplete="autocomplete || 'off'"
      :aria-describedby="hint ? `${id}-hint` : undefined"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    >
    <p v-if="hint" :id="`${id}-hint`" class="field__hint">{{ hint }}</p>
  </div>
</template>

