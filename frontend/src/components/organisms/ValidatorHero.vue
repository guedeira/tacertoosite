<script setup lang="ts">
import { ArrowRight } from "lucide-vue-next";
import { onMounted, ref } from "vue";

import { checkHealth, getCompanies, validateDomain } from "../../services/api";
import type { Company, ValidationResult } from "../../types/api";
import { SUBMITTED_LINK_MAX_LENGTH, submittedLinkSchema } from "../../utils/linkValidation";
import BaseButton from "../atoms/BaseButton.vue";
import BaseField from "../atoms/BaseField.vue";
import StatusMessage from "../atoms/StatusMessage.vue";
import CompanyAutocomplete from "../molecules/CompanyAutocomplete.vue";
import CompanyListModal from "./CompanyListModal.vue";
import ValidationResultModal from "./ValidationResultModal.vue";

const REQUEST_COMPANY_FORM_URL = "https://forms.gle/k7DeUUrqarm95VQX7";

const companies = ref<Company[]>([]);
const companySearch = ref("");
const selectedCompanyId = ref("");
const domainInput = ref("");
const result = ref<ValidationResult | null>(null);
const statusMessage = ref("Conectando com o servidor. Isso pode levar alguns segundos na primeira visita.");
const statusTone = ref<"info" | "error">("info");
const isBackendReady = ref(false);
const isLoading = ref(false);
const isCompaniesModalOpen = ref(false);
const isResultModalOpen = ref(false);

onMounted(() => {
  void initialize();
});

async function initialize(): Promise<void> {
  isBackendReady.value = false;
  statusMessage.value = "Conectando com o servidor. Isso pode levar alguns segundos na primeira visita.";
  statusTone.value = "info";

  if (await loadCompanies()) {
    return;
  }

  const backendReady = await waitForBackend();
  if (!backendReady) {
    statusTone.value = "error";
    statusMessage.value = "Não conseguimos conectar agora. Aguarde um pouco e recarregue a página.";
    return;
  }

  if (!(await loadCompanies())) {
    statusTone.value = "error";
    statusMessage.value = "Não conseguimos carregar a lista de empresas.";
  }
}

async function loadCompanies(): Promise<boolean> {
  try {
    companies.value = await getCompanies();
    isBackendReady.value = true;
    statusMessage.value = "";
    return true;
  } catch {
    return false;
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

  if (!selectedCompanyId.value) {
    statusTone.value = "error";
    statusMessage.value = "Selecione uma empresa da lista.";
    return;
  }

  const parsedDomainInput = submittedLinkSchema.safeParse(domainInput.value);

  if (!parsedDomainInput.success) {
    statusTone.value = "error";
    statusMessage.value = parsedDomainInput.error.issues[0]?.message || "Digite um link válido.";
    return;
  }

  isLoading.value = true;
  statusMessage.value = "";

  try {
    result.value = await validateDomain({
      company_id: selectedCompanyId.value,
      input: parsedDomainInput.data,
    });
    isResultModalOpen.value = true;
  } catch {
    statusTone.value = "error";
    statusMessage.value = "Não conseguimos comparar agora. Tente de novo em instantes.";
  } finally {
    isLoading.value = false;
  }
}

function selectCompany(company: Company): void {
  companySearch.value = company.name;
  selectedCompanyId.value = company.id;
  isCompaniesModalOpen.value = false;
}

function openRequestCompanyForm(): void {
  window.open(REQUEST_COMPANY_FORM_URL, "_blank", "noopener,noreferrer");
}
</script>

<template>
  <section id="comparar-site" class="hero" aria-labelledby="page-title">
    <div class="hero__context">
      <p class="hero__eyebrow">Nem tudo é o que parece</p>
      <h1 id="page-title">O site parece verdadeiro, o link talvez não seja.</h1>
      <p class="hero__intro">
        Cole o link recebido e compare o domínio dele com os domínios oficiais da empresa.
        Uma forma simples de identificar páginas falsas antes de informar dados, senhas ou realizar pagamentos.
        Evite golpes, fique tranquilo 😎
      </p>
      <section class="hero-metrics" aria-labelledby="hero-metrics-title" aria-disabled="true">
        <div class="hero-metrics__header">
          <div>
            <p>Resumo da semana</p>
            <small>Atualizado diariamente</small>
          </div>
          <span>Em implementação</span>
        </div>
        <h2 id="hero-metrics-title">Visão geral das verificações realizadas</h2>
        <p class="hero-metrics__copy">
          Acompanhe o volume de verificações realizadas, correspondências com a lista oficial e empresas analisadas.
        </p>
        <dl class="hero-metrics__grid">
          <div>
            <dt>Verificações</dt>
            <dd>--</dd>
          </div>
          <div>
            <dt>Válidos</dt>
            <dd>--</dd>
          </div>
          <div>
            <dt>Inválidos</dt>
            <dd>--</dd>
          </div>
          <div>
            <dt>Checklists</dt>
            <dd>--</dd>
          </div>
        </dl>
      </section>
    </div>

    <div class="hero__tool">
      <div class="tool-card">
        <div class="tool-card__header">
          <h2>Conferir um link</h2>
          <p>Informe o endereço que você quer conferir, a comparação considera o domínio principal.</p>
        </div>

        <StatusMessage v-if="statusMessage" :tone="statusTone" :message="statusMessage" :busy="statusTone === 'info' && !isBackendReady" />

        <form class="validator-form" @submit.prevent="submitValidation">
          <CompanyAutocomplete
            v-model="companySearch"
            v-model:selected-company-id="selectedCompanyId"
            :companies="companies"
            :disabled="!isBackendReady"
            @request-company="openRequestCompanyForm"
            @open-companies="isCompaniesModalOpen = true"
          />

          <BaseField
            id="domain-input"
            v-model="domainInput"
            label="Link recebido"
            placeholder="Ex.: https://exemplo.com.br/promocao"
            required
            :maxlength="SUBMITTED_LINK_MAX_LENGTH"
            :disabled="!isBackendReady"
          />

          <BaseButton type="submit" :disabled="!isBackendReady || isLoading" :icon="ArrowRight">
            {{ isLoading ? "Conferindo..." : "Conferir link" }}
          </BaseButton>
        </form>

        <BaseButton variant="ghost" @click="openRequestCompanyForm">Pedir inclusão de empresa</BaseButton>
      </div>
    </div>
  </section>

  <CompanyListModal
    :open="isCompaniesModalOpen"
    :companies="companies"
    @close="isCompaniesModalOpen = false"
    @select="selectCompany"
  />
  <ValidationResultModal
    :open="isResultModalOpen"
    :result="result"
    @close="isResultModalOpen = false"
  />
</template>
