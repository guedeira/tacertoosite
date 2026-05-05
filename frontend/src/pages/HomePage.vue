<script setup lang="ts">
import EducationPanel from "../components/organisms/EducationPanel.vue";
import ValidatorHero from "../components/organisms/ValidatorHero.vue";
import SiteFooter from "../components/templates/SiteFooter.vue";
</script>

<template>
  <main>
    <ValidatorHero />
    <section class="info-section" aria-labelledby="details-title">
      <div class="info-section__content">
        <EducationPanel />

        <div class="insight-grid">
          <article class="insight">
            <h2 id="details-title">O que a ferramenta compara?</h2>
            <p>
              Ela separa o domínio principal do link informado e compara com os domínios oficiais cadastrados para a empresa escolhida.
            </p>
            <p class="example-text">Ex.: em https://www.gov.br/servicos, o domínio comparado é gov.br.</p>
          </article>

          <article class="insight">
            <h2>Quando o resultado não bater</h2>
            <p>
              Pare antes de clicar, pagar ou informar dados. Confira o endereço por outro canal oficial da empresa ou instituição.
            </p>
          </article>

          <article class="insight insight--wide">
            <h2>Limite importante</h2>
            <p>
              Um endereço bater com o cadastro não garante que toda página é segura. A comparação é uma etapa de apoio para reduzir erro e pressa.
            </p>
          </article>
        </div>
      </div>
    </section>
  </main>
  <SiteFooter />
</template>

