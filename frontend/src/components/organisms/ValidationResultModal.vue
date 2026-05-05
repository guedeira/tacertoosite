<script setup lang="ts">
import { AlertTriangle, CheckCircle2 } from "lucide-vue-next";
import { computed } from "vue";

import type { ValidationResult } from "../../types/api";
import AppModal from "../molecules/AppModal.vue";
import ValidationResultCard from "../molecules/ValidationResultCard.vue";

const props = defineProps<{
  open: boolean;
  result: ValidationResult | null;
}>();

defineEmits<{
  close: [];
}>();

const modalTitle = computed(() =>
  props.result?.is_match ? "Resultado da comparação" : "Atenção antes de continuar",
);

const modalDescription = computed(() =>
  props.result?.is_match
    ? "O domínio informado bate com o cadastro oficial para a empresa escolhida."
    : "O domínio informado não bate com o cadastro oficial para a empresa escolhida.",
);
</script>

<template>
  <AppModal
    class="result-modal"
    :open="open"
    :title="modalTitle"
    :description="modalDescription"
    @close="$emit('close')"
  >
    <div v-if="result" class="result-modal__body">
      <ValidationResultCard :result="result" show-all-domains />

      <section class="next-steps" aria-labelledby="next-steps-title">
        <div class="next-steps__header">
          <component :is="result.is_match ? CheckCircle2 : AlertTriangle" aria-hidden="true" />
          <h3 id="next-steps-title">{{ result.is_match ? "Próximos cuidados" : "O que fazer agora" }}</h3>
        </div>

        <ul v-if="result.is_match">
          <li>Confira se a página realmente pertence à empresa antes de informar dados sensíveis.</li>
          <li>Evite seguir links recebidos com urgência, prêmio, ameaça ou cobrança inesperada.</li>
          <li>Quando houver dúvida, acesse a empresa digitando o endereço oficial no navegador.</li>
        </ul>

        <ul v-else>
          <li>Não informe senha, código, cartão, documento ou dados bancários nesse link.</li>
          <li>Procure a empresa por um canal oficial que você já conheça.</li>
          <li>Se o domínio oficial estiver incompleto na base, peça a inclusão para revisão.</li>
        </ul>
      </section>
    </div>
  </AppModal>
</template>
