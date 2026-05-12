<script setup lang="ts">
import AppNavbar from "../components/templates/AppNavbar.vue";
import SiteFooter from "../components/templates/SiteFooter.vue";
import { scamTypes } from "../data/scams";

const groupedScams = scamTypes.reduce<Record<string, typeof scamTypes>>((groups, scamType) => {
  groups[scamType.category] = [...(groups[scamType.category] || []), scamType];
  return groups;
}, {});

function getGroupId(category: string): string {
  return `scam-group-${category.toLowerCase().replace(/\s+/g, "-")}`;
}
</script>

<template>
  <AppNavbar
    home-href="../index.html"
    glossary-href="../glossario/"
    guide-href="./"
    active-page="guide"
  />
  <main class="scams-page-shell">
    <section class="scams-page" aria-labelledby="scams-page-title">
      <header class="scams-page__header">
        <p class="hero__eyebrow">Guia simples de atenção</p>
        <h1 id="scams-page-title">Golpes comuns utilizando links falsos ou comprometidos</h1>
        <p>
          Golpes digitais normalmente exploram pressa, distração e confiança. Use esta página para reconhecer sinais antes de informar dados,
          enviar dinheiro, instalar aplicativos ou entrar em uma conta.
        </p>
      </header>

      <section class="scams-page__quick-check" aria-labelledby="quick-check-title">
        <h2 id="quick-check-title">Antes de clicar em qualquer link</h2>
        <ul>
          <li>Veja se o link combina com o site oficial.</li>
          <li>Desconfie de urgência, ameaça, prêmio fácil ou desconto grande demais.</li>
          <li>Não informe senha, código, cartão ou documento em páginas abertas por links recebidos.</li>
          <li>Quando houver dúvida, feche o link e entre pelo aplicativo ou site oficial.</li>
        </ul>
        <div class="zero-trust-note">
          <h3>Uma forma simples de pensar: Zero Trust (Confiança Zero)</h3>
          <p>
            Zero Trust significa não confiar automaticamente em algo só porque ele parece familiar ou verídico. Antes de agir, confirme.
          </p>
          <ul>
            <li><strong>Verifique sempre:</strong> confira link, contexto e canal oficial.</li>
            <li><strong>Use o mínimo necessário:</strong> não entregue senha, código ou documento sem necessidade clara.</li>
            <li><strong>Assuma risco:</strong> trate mensagens urgentes como suspeitas até confirmar por outro caminho.</li>
          </ul>
        </div>
      </section>

      <div class="scams-page__groups">
        <section v-for="(items, category) in groupedScams" :key="category" class="scam-group" :aria-labelledby="getGroupId(category)">
          <h2 :id="getGroupId(category)">{{ category }}</h2>
          <div class="scam-guide-grid">
            <article v-for="scamType in items" :key="scamType.id" class="scam-guide-card">
              <h3>{{ scamType.name }}</h3>
              <p>{{ scamType.modalDescription }}</p>
              <h4>Sinais de alerta</h4>
              <ul>
                <li v-for="sign in scamType.signs" :key="sign">{{ sign }}</li>
              </ul>
              <h4>Dica importante</h4>
              <p class="scam-guide-card__action">{{ scamType.action }}</p>
            </article>
          </div>
        </section>
      </div>

      <section class="scams-page__final-message" aria-labelledby="scams-final-title">
        <h2 id="scams-final-title">Lembre-se</h2>
        <p>
          O objetivo desta ferramenta é ajudar você a identificar links suspeitos conferindo se o domínio do link bate com a lista oficial da empresa.
        </p>
        <p>
          Verificar o link antes de clicar já reduz bastante o risco de cair em fraudes comuns na internet.
        </p>
        <p>
          Se você ainda estiver em dúvida, procure ajuda especializada ou fale com o suporte oficial da empresa antes de interagir com o site.
        </p>
      </section>
    </section>
  </main>
  <SiteFooter terms-href="../politicas/termos-de-uso.html" privacy-href="../politicas/politica-de-privacidade.html" />
</template>
