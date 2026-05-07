<script setup lang="ts">
import { computed, nextTick, ref, watch } from "vue";

import type { Company } from "../../types/api";
import { filterCompanies, normalizeText } from "../../utils/text";

const props = defineProps<{
  companies: Company[];
  modelValue: string;
  selectedCompanyId: string;
  disabled?: boolean;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
  "update:selectedCompanyId": [value: string];
  requestCompany: [];
  openCompanies: [];
}>();

const isOpen = ref(false);
const isSelectingOption = ref(false);

const matches = computed(() => filterCompanies(props.companies, props.modelValue));
const hasTerm = computed(() => props.modelValue.trim().length > 0);
const notFound = computed(() => hasTerm.value && matches.value.length === 0);
const exactMatch = computed(() =>
  props.companies.find((company) => normalizeText(company.name) === normalizeText(props.modelValue)),
);

watch(
  () => props.modelValue,
  () => {
    emit("update:selectedCompanyId", exactMatch.value?.id || "");

    if (isSelectingOption.value || exactMatch.value) {
      isOpen.value = false;
      return;
    }

    isOpen.value = hasTerm.value && matches.value.length > 0;
  },
);

function selectCompany(company: Company): void {
  isSelectingOption.value = true;
  emit("update:modelValue", company.name);
  emit("update:selectedCompanyId", company.id);
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
  <div class="company-autocomplete" @focusout="closeWhenFocusLeaves">
    <label class="field__label" for="company-search">Empresa</label>
    <input
      id="company-search"
      class="field__control"
      :value="modelValue"
      placeholder="Digite o nome da empresa"
      autocomplete="off"
      required
      :disabled="disabled"
      aria-describedby="company-search-hint"
      aria-controls="company-options"
      :aria-expanded="isOpen"
      role="combobox"
      @focus="isOpen = !exactMatch && matches.length > 0"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    >

    <div v-if="isOpen" id="company-options" class="company-autocomplete__options" role="listbox">
      <button
        v-for="company in matches"
        :key="company.id"
        type="button"
        role="option"
        class="company-autocomplete__option"
        @mousedown.prevent
        @click="selectCompany(company)"
      >
        {{ company.name }}
      </button>
    </div>

    <p id="company-search-hint" class="field__hint">
      Comece a digitar e selecione uma empresa da lista.
      <button class="inline-link" type="button" @click="$emit('openCompanies')">Ver empresas disponíveis</button>.
    </p>
    <p v-if="notFound" class="field__hint field__hint--alert">
      Não encontrou a empresa?
      <button class="inline-link" type="button" @click="$emit('requestCompany')">Peça a inclusão</button>.
    </p>
  </div>
</template>
