<script setup lang="ts">
import { computed, ref } from "vue";

const props = defineProps<{
  id: string;
  label: string;
  hint?: string;
  modelValue: string;
  placeholder?: string;
  type?: string;
  required?: boolean;
  disabled?: boolean;
  autocomplete?: string;
  maxlength?: number;
  showRequiredMarker?: boolean;
  validateRequiredOnBlur?: boolean;
}>();

defineEmits<{
  "update:modelValue": [value: string];
}>();

const wasBlurred = ref(false);
const requiredErrorId = computed(() => `${props.id}-required-error`);
const hintId = computed(() => `${props.id}-hint`);
const showRequiredError = computed(
  () => Boolean(props.validateRequiredOnBlur && props.required && wasBlurred.value && !props.modelValue.trim()),
);
const describedBy = computed(() => {
  if (showRequiredError.value) {
    return requiredErrorId.value;
  }

  return props.hint ? hintId.value : undefined;
});
</script>

<template>
  <div class="field">
    <label class="field__label" :for="id">
      {{ label }}
      <span v-if="required && showRequiredMarker" class="field__required" aria-hidden="true">*</span>
    </label>
    <input
      :id="id"
      class="field__control"
      :type="type || 'text'"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :autocomplete="autocomplete || 'off'"
      :maxlength="maxlength"
      :aria-invalid="showRequiredError"
      :aria-describedby="describedBy"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      @blur="wasBlurred = true"
    >
    <p v-if="showRequiredError" :id="requiredErrorId" class="field__error">Campo obrigatório.</p>
    <p v-else-if="hint" :id="hintId" class="field__hint">{{ hint }}</p>
  </div>
</template>
