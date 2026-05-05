<script setup lang="ts">
import { AlertTriangle, CheckCircle2 } from "lucide-vue-next";
import { computed } from "vue";

import type { ValidationResult } from "../../types/api";
import BaseButton from "../atoms/BaseButton.vue";
import DomainPill from "../atoms/DomainPill.vue";

const props = defineProps<{
  result: ValidationResult;
  showAllDomains?: boolean;
}>();

defineEmits<{
  showDomains: [];
}>();

const visibleDomains = computed(() =>
  props.showAllDomains ? props.result.official_domains : props.result.official_domains.slice(0, 4),
);
const title = computed(() =>
  props.result.is_match
    ? "O link bate com o endereço oficial cadastrado."
    : "Atenção: o link não bate com o cadastro oficial.",
);
</script>

<template>
  <section class="result-card" :class="{ 'result-card--match': result.is_match }" role="status" aria-live="polite">
    <component :is="result.is_match ? CheckCircle2 : AlertTriangle" class="result-card__icon" aria-hidden="true" />
    <div class="result-card__content">
      <strong>{{ title }}</strong>
      <p>{{ result.message }}</p>
      <small v-if="result.submitted_domain">Domínio comparado: {{ result.submitted_domain }}</small>

      <div v-if="!result.is_match && result.official_domains.length" class="result-card__domains">
        <span>{{ result.official_domains.length === 1 ? "Endereço oficial cadastrado:" : "Endereços oficiais cadastrados:" }}</span>
        <div class="result-card__pills">
          <DomainPill v-for="domain in visibleDomains" :key="domain" :domain="domain" />
          <BaseButton
            v-if="!showAllDomains && result.official_domains.length > visibleDomains.length"
            variant="ghost"
            @click="$emit('showDomains')"
          >
            Ver todos
          </BaseButton>
        </div>
      </div>
    </div>
  </section>
</template>
