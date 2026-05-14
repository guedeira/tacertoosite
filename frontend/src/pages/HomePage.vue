<script setup lang="ts">
import ValidatorHero from "../components/organisms/ValidatorHero.vue";
import AppNavbar from "../components/templates/AppNavbar.vue";
import SiteFooter from "../components/templates/SiteFooter.vue";
</script>

<template>
  <main>
    <AppNavbar glossary-href="./glossario/" active-page="home" />
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

        </div>
      </div>
    </section>
  </main>
  <SiteFooter />
</template>
