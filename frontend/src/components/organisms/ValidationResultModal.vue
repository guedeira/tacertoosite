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
  props.result?.is_match ? "Domínio reconhecido" : "Domínio desconhecido",
);

const modalDescription = computed(() =>
  props.result?.is_match
    ? "O endereço principal do link aparece na lista oficial cadastrada para esta empresa."
    : "O endereço principal do link não aparece entre os domínios oficiais cadastrados para esta empresa.",
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
          <h3 id="next-steps-title">{{ result.is_match ? "Cuidado nunca é demais" : "Ações recomendadas" }}</h3>
        </div>

        <ul v-if="result.is_match">
          <li>Este resultado confirma o domínio principal, mas não garante que a página, oferta ou mensagem seja verdadeira.</li>
          <li>Antes de informar senha, código, cartão ou documento, confira se você esperava esse contato e se a ação faz sentido.</li>
          <li>Se o link veio com urgência, cobrança, prêmio ou ameaça, abra o app ou digite o site oficial no navegador em vez de continuar pelo link recebido.</li>
          <li>Na dúvida, entre em contato com o suporte oficial da empresa por um canal verificado: aplicativo, site digitado manualmente, telefone do cartão/boleto ou perfil verificado.</li>
        </ul>

        <ul v-else>
          <li>Não preencha login, código de confirmação, cartão, documento, PIX ou qualquer dado sensível nesse endereço.</li>
          <li>Se você já enviou informações, troque senhas, bloqueie cartões ou pagamentos suspeitos e avise o suporte oficial sobre o link recebido.</li>
          <li>Entre em contato com o suporte oficial da empresa por um canal verificado: aplicativo, site digitado manualmente, telefone do cartão/boleto ou perfil verificado.</li>
          <li>Se você sabe que esse domínio também é oficial, ajude a deixar a internet mais segura pedindo a inclusão com uma fonte confiável para revisão.</li>
        </ul>
      </section>
    </div>
  </AppModal>
</template>
