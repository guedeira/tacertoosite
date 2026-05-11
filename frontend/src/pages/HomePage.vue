<script setup lang="ts">
import { computed, ref } from "vue";

import AppModal from "../components/molecules/AppModal.vue";
import ValidatorHero from "../components/organisms/ValidatorHero.vue";
import AppNavbar from "../components/templates/AppNavbar.vue";
import SiteFooter from "../components/templates/SiteFooter.vue";
import { scamTypes } from "../data/scams";

const selectedScamId = ref<string | null>(null);
const selectedScam = computed(() => scamTypes.find((scamType) => scamType.id === selectedScamId.value) || null);

function openScamModal(scamId: string): void {
  selectedScamId.value = scamId;
}

function closeScamModal(): void {
  selectedScamId.value = null;
}
</script>

<template>
  <main>
    <AppNavbar glossary-href="./glossario/" />
    <ValidatorHero />
    <section class="info-section" aria-label="Informações de apoio sobre links suspeitos">
      <div class="info-section__content">
        <div class="insight-grid">
          <aside class="education-panel" aria-labelledby="education-title">
            <h2 id="education-title">Sempre desconfie</h2>
            <p>
              Golpistas usam nomes conhecidos para criar urgência e fazer páginas falsas parecerem oficiais.
            </p>
            <ul class="education-panel__tips">
              <li>Desconfie de bloqueio, multa, prêmio ou taxa urgente.</li>
              <li>Confira o link antes de digitar dados.</li>
              <li>Na dúvida, abra o app ou site oficial.</li>
            </ul>
          </aside>

          <article class="insight">
            <h2>O que a ferramenta compara?</h2>
            <p>
              Ela separa o domínio principal do link e compara com os domínios oficiais da empresa escolhida.
            </p>
            <div class="domain-example" aria-label="Exemplo de comparação de domínio">
              <p><strong>Exemplo com Mercado Livre</strong></p>
              <p><span>Domínio oficial:</span> mercadolivre.com.br</p>
              <p><span>Domínio suspeito:</span> mercadolivre-ofertas.com</p>
            </div>
            <p>Como os domínios são diferentes, esse link não é o site oficial cadastrado para a empresa.</p>
          </article>

          <article class="insight">
            <h2>Quando o resultado não bater</h2>
            <p>
              Trate o link como suspeito. Não é prova de golpe, mas é um sinal para parar antes de continuar.
            </p>
            <ul class="insight-list">
              <li>Não informe senha, código, cartão ou documento.</li>
              <li>Não pague boleto, PIX ou taxa aberta pelo link.</li>
              <li>Procure a empresa por um canal oficial.</li>
            </ul>
          </article>

          <article class="insight insight--wide scam-types" aria-labelledby="scam-types-title">
            <h2 id="scam-types-title">Golpes comuns utilizando links falsos ou comprometidos</h2>
            <p>
              Muitos golpes usam o nome de uma empresa real, mas mandam você para um link falso. Conheça alguns casos em que conferir o link ajuda a evitar cilada.
            </p>
            <div class="scam-types__list">
              <button
                v-for="scamType in scamTypes.slice(0, 4)"
                :key="scamType.id"
                class="scam-type-button"
                type="button"
                @click="openScamModal(scamType.id)"
              >
                <strong>{{ scamType.name }}</strong>
                <span>{{ scamType.shortDescription }}</span>
              </button>
            </div>
            <a class="scam-types__more" href="./golpes/">Saiba mais sobre golpes comuns</a>
          </article>
        </div>
      </div>
    </section>
  </main>
  <SiteFooter />

  <AppModal
    v-if="selectedScam"
    :open="Boolean(selectedScam)"
    :title="selectedScam.name"
    :description="selectedScam.modalDescription"
    @close="closeScamModal"
  >
    <div class="scam-modal">
      <section>
        <h3>Sinais comuns</h3>
        <ul>
          <li v-for="sign in selectedScam.signs" :key="sign">{{ sign }}</li>
        </ul>
      </section>
      <section>
        <h3>O que fazer</h3>
        <p>{{ selectedScam.action }}</p>
      </section>
    </div>
  </AppModal>
</template>
