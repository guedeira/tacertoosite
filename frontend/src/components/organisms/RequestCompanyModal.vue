<script setup lang="ts">
import { computed, ref } from "vue";

import BaseButton from "../atoms/BaseButton.vue";
import BaseField from "../atoms/BaseField.vue";
import StatusMessage from "../atoms/StatusMessage.vue";
import AppModal from "../molecules/AppModal.vue";

const GITHUB_NEW_ISSUE_URL = "https://github.com/guedeira/tacertoosite/issues/new";

const props = defineProps<{
  open: boolean;
  suggestedName?: string;
}>();

defineEmits<{
  close: [];
}>();

const brandName = ref("");
const domain = ref("");
const source = ref("");
const description = ref("");
const message = ref("");
const messageTone = ref<"success" | "error">("success");

const descriptionCount = computed(() => description.value.length);

function submitRequest(): void {
  const normalizedBrandName = brandName.value.trim() || props.suggestedName?.trim() || "";
  const normalizedDomain = domain.value.trim().toLowerCase();

  if (!normalizedBrandName || !normalizedDomain) {
    showMessage("Preencha o nome da empresa e o domínio oficial.", "error");
    return;
  }

  if (description.value.length > 500) {
    showMessage("A descrição deve ter no máximo 500 caracteres.", "error");
    return;
  }

  const title = `Incluir domínio oficial: ${normalizedBrandName}`;
  const body = [
    "## Pedido de inclusão de empresa",
    "",
    `Empresa: ${normalizedBrandName}`,
    `Domínio oficial sugerido: ${normalizedDomain}`,
    `Fonte para conferência: ${source.value.trim() || "Não informada"}`,
    `Descrição: ${description.value.trim() || "Não informada"}`,
    "",
    "## Critérios",
    "",
    "- [ ] O domínio foi conferido em uma fonte oficial.",
    "- [ ] A empresa ainda não existe no cadastro.",
    "- [ ] A alteração mantém o cadastro simples e auditável.",
  ].join("\n");

  const issueUrl = `${GITHUB_NEW_ISSUE_URL}?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`;
  window.open(issueUrl, "_blank", "noopener,noreferrer");
  showMessage("O pedido foi aberto no GitHub para revisão.", "success");
  brandName.value = "";
  domain.value = "";
  source.value = "";
  description.value = "";
}

function showMessage(value: string, tone: "success" | "error"): void {
  message.value = value;
  messageTone.value = tone;
}
</script>

<template>
  <AppModal
    :open="open"
    title="Pedir inclusão de empresa"
    description="Envie uma sugestão para revisão manual antes de entrar na lista."
    @close="$emit('close')"
  >
    <form class="request-form" @submit.prevent="submitRequest">
      <BaseField
        id="request-brand-name"
        v-model="brandName"
        label="Nome da empresa"
        placeholder="Ex.: Empresa XPTO"
        autocomplete="organization"
        required
      />
      <BaseField
        id="request-domain"
        v-model="domain"
        label="Domínio oficial"
        placeholder="Ex.: empresaxpto.com.br"
        required
      />
      <BaseField
        id="request-source"
        v-model="source"
        label="Fonte para conferência"
        type="url"
        placeholder="Ex.: https://www.empresaxpto.com.br/sobre"
        hint="Use um site oficial, perfil verificado, documento público ou outra fonte confiável."
      />

      <div class="field">
        <label class="field__label" for="request-description">Descrição da solicitação</label>
        <textarea
          id="request-description"
          v-model="description"
          class="field__control field__control--textarea"
          maxlength="500"
          rows="4"
          placeholder="Opcional: conte por que essa empresa deveria entrar na lista."
        />
        <p class="field__hint">Opcional, até 500 caracteres. {{ descriptionCount }}/500</p>
      </div>

      <BaseButton type="submit" variant="secondary">Enviar pedido</BaseButton>
      <StatusMessage v-if="message" :tone="messageTone" :message="message" />
    </form>
  </AppModal>
</template>

