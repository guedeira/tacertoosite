<script setup lang="ts">
import { computed, nextTick, ref, watch } from "vue";

import type { Brand } from "../../types/api";
import { filterBrands, normalizeText } from "../../utils/text";

const props = defineProps<{
  brands: Brand[];
  modelValue: string;
  selectedBrandId: string;
  disabled?: boolean;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
  "update:selectedBrandId": [value: string];
  requestBrand: [];
  openBrands: [];
}>();

const isOpen = ref(false);
const isSelectingOption = ref(false);

const matches = computed(() => filterBrands(props.brands, props.modelValue));
const hasTerm = computed(() => props.modelValue.trim().length > 0);
const notFound = computed(() => hasTerm.value && matches.value.length === 0);
const exactMatch = computed(() =>
  props.brands.find((brand) => normalizeText(brand.name) === normalizeText(props.modelValue)),
);

watch(
  () => props.modelValue,
  () => {
    emit("update:selectedBrandId", exactMatch.value?.id || "");

    if (isSelectingOption.value || exactMatch.value) {
      isOpen.value = false;
      return;
    }

    isOpen.value = hasTerm.value && matches.value.length > 0;
  },
);

function selectBrand(brand: Brand): void {
  isSelectingOption.value = true;
  emit("update:modelValue", brand.name);
  emit("update:selectedBrandId", brand.id);
  isOpen.value = false;

  void nextTick(() => {
    isOpen.value = false;
    isSelectingOption.value = false;
  });
}

function closeWhenFocusLeaves(event: FocusEvent): void {
  const nextFocusedElement = event.relatedTarget;

  if (!(nextFocusedElement instanceof Node) || !event.currentTarget) {
    isOpen.value = false;
    return;
  }

  if (!(event.currentTarget as HTMLElement).contains(nextFocusedElement)) {
    isOpen.value = false;
  }
}
</script>

<template>
  <div class="brand-autocomplete" @focusout="closeWhenFocusLeaves">
    <label class="field__label" for="brand-search">Empresa</label>
    <input
      id="brand-search"
      class="field__control"
      :value="modelValue"
      placeholder="Digite o nome da empresa"
      autocomplete="off"
      required
      :disabled="disabled"
      aria-describedby="brand-search-hint"
      aria-controls="brand-options"
      :aria-expanded="isOpen"
      role="combobox"
      @focus="isOpen = !exactMatch && matches.length > 0"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    >

    <div v-if="isOpen" id="brand-options" class="brand-autocomplete__options" role="listbox">
      <button
        v-for="brand in matches"
        :key="brand.id"
        type="button"
        role="option"
        class="brand-autocomplete__option"
        @mousedown.prevent
        @click="selectBrand(brand)"
      >
        {{ brand.name }}
      </button>
    </div>

    <p id="brand-search-hint" class="field__hint">
      Comece a digitar e selecione uma empresa da lista.
      <button class="inline-link" type="button" @click="$emit('openBrands')">Ver empresas disponíveis</button>.
    </p>
    <p v-if="notFound" class="field__hint field__hint--alert">
      Não encontrou a empresa?
      <button class="inline-link" type="button" @click="$emit('requestBrand')">Peça a inclusão</button>.
    </p>
  </div>
</template>
