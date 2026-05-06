<script setup lang="ts">
import { ArrowRight, Building2, ClipboardCheck, Link2, SearchCheck } from "lucide-vue-next";
import { onMounted, ref } from "vue";

import { checkHealth, getBrands, validateDomain } from "../../services/api";
import type { Brand, ValidationResult } from "../../types/api";
import AppLogo from "../atoms/AppLogo.vue";
import BaseButton from "../atoms/BaseButton.vue";
import BaseField from "../atoms/BaseField.vue";
import StatusMessage from "../atoms/StatusMessage.vue";
import BrandAutocomplete from "../molecules/BrandAutocomplete.vue";
import BrandListModal from "./BrandListModal.vue";
import RequestCompanyModal from "./RequestCompanyModal.vue";
import ValidationResultModal from "./ValidationResultModal.vue";

const brands = ref<Brand[]>([]);
const brandSearch = ref("");
const selectedBrandId = ref("");
const domainInput = ref("");
const result = ref<ValidationResult | null>(null);
const statusMessage = ref("Conectando com o servidor. Isso pode levar alguns segundos na primeira visita.");
const statusTone = ref<"info" | "error">("info");
const isBackendReady = ref(false);
const isLoading = ref(false);
const isBrandsModalOpen = ref(false);
const isRequestModalOpen = ref(false);
const isResultModalOpen = ref(false);

onMounted(() => {
  void initialize();
});

async function initialize(): Promise<void> {
  isBackendReady.value = false;
  statusMessage.value = "Conectando com o servidor. Isso pode levar alguns segundos na primeira visita.";
  statusTone.value = "info";

  const backendReady = await waitForBackend();

  if (!backendReady) {
    statusTone.value = "error";
    statusMessage.value = "Não conseguimos conectar agora. Aguarde um pouco e recarregue a página.";
    return;
  }

  try {
    brands.value = await getBrands();
    isBackendReady.value = true;
    statusMessage.value = "";
  } catch {
    statusTone.value = "error";
    statusMessage.value = "Não conseguimos carregar a lista de empresas.";
  }
}

async function waitForBackend(): Promise<boolean> {
  for (let attemptsLeft = 8; attemptsLeft > 0; attemptsLeft -= 1) {
    const isReady = await checkHealth();

    if (isReady) {
      return true;
    }

    await new Promise((resolve) => window.setTimeout(resolve, 2500));
  }

  return false;
}

async function submitValidation(): Promise<void> {
  result.value = null;

  if (!selectedBrandId.value) {
    statusTone.value = "error";
    statusMessage.value = "Selecione uma empresa da lista.";
    return;
  }

  if (!domainInput.value.trim()) {
    statusTone.value = "error";
    statusMessage.value = "Digite um link ou endereço válido.";
    return;
  }

  isLoading.value = true;
  statusMessage.value = "";

  try {
    result.value = await validateDomain({
      brand_id: selectedBrandId.value,
      input: domainInput.value,
    });
    isResultModalOpen.value = true;
  } catch {
    statusTone.value = "error";
    statusMessage.value = "Não conseguimos comparar agora. Tente de novo em instantes.";
  } finally {
    isLoading.value = false;
  }
}

function selectBrand(brand: Brand): void {
  brandSearch.value = brand.name;
  selectedBrandId.value = brand.id;
  isBrandsModalOpen.value = false;
}
</script>

<template>
  <section class="hero" aria-labelledby="page-title">
    <div class="hero__context">
      <AppLogo />
      <p class="hero__eyebrow">Uma pausa rápida antes do clique</p>
      <h1 id="page-title">Confira se o link combina com o site oficial.</h1>
      <p class="hero__intro">
        Escolha a empresa, cole o endereço recebido e veja se o domínio principal bate com a base cadastrada.
        É uma forma simples de perceber links suspeitos antes de informar dados, senhas ou fazer pagamentos.
      </p>
      <div class="hero__facts" aria-label="Resumo da ferramenta">
        <span><Building2 aria-hidden="true" /> Empresas cadastradas</span>
        <span><SearchCheck aria-hidden="true" /> Domínios validados</span>
      </div>
      <div class="hero__future-tools" aria-label="Ferramentas futuras">
        <h2>Outras ferramentas estão a caminho</h2>
        <div class="hero__future-actions">
          <button type="button" aria-disabled="true" aria-label="Checklist antigolpe em desenvolvimento">
            <ClipboardCheck aria-hidden="true" />
            Checklist antigolpe
            <span role="tooltip">Em desenvolvimento</span>
          </button>
          <button type="button" aria-disabled="true" aria-label="Resolvedor de short links em desenvolvimento">
            <Link2 aria-hidden="true" />
            Resolver short link
            <span role="tooltip">Em desenvolvimento</span>
          </button>
        </div>
      </div>
    </div>

    <div class="hero__tool">
      <div class="tool-card">
        <div class="tool-card__header">
          <h2>Conferir um link</h2>
          <p>Cole o endereço completo, inclusive quando ele vier cheio de números, caminhos ou parâmetros.</p>
        </div>

        <StatusMessage v-if="statusMessage" :tone="statusTone" :message="statusMessage" :busy="statusTone === 'info' && !isBackendReady" />

        <form class="validator-form" @submit.prevent="submitValidation">
          <BrandAutocomplete
            v-model="brandSearch"
            v-model:selected-brand-id="selectedBrandId"
            :brands="brands"
            :disabled="!isBackendReady"
            @request-brand="isRequestModalOpen = true"
            @open-brands="isBrandsModalOpen = true"
          />

          <BaseField
            id="domain-input"
            v-model="domainInput"
            label="Link recebido"
            placeholder="Ex.: https://exemplo.com.br/promocao"
            required
            :disabled="!isBackendReady"
          />

          <BaseButton type="submit" :disabled="!isBackendReady || isLoading" :icon="ArrowRight">
            {{ isLoading ? "Comparando..." : "Comparar" }}
          </BaseButton>
        </form>

        <BaseButton variant="ghost" @click="isRequestModalOpen = true">Pedir inclusão de empresa</BaseButton>
      </div>
    </div>
  </section>

  <BrandListModal
    :open="isBrandsModalOpen"
    :brands="brands"
    @close="isBrandsModalOpen = false"
    @select="selectBrand"
  />
  <ValidationResultModal
    :open="isResultModalOpen"
    :result="result"
    @close="isResultModalOpen = false"
  />
  <RequestCompanyModal
    :open="isRequestModalOpen"
    :suggested-name="brandSearch"
    @close="isRequestModalOpen = false"
  />
</template>
