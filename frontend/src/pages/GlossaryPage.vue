<script setup lang="ts">
import { glossaryTerms } from "../data/glossary";
import AppNavbar from "../components/templates/AppNavbar.vue";
import SiteFooter from "../components/templates/SiteFooter.vue";
</script>

<template>
  <AppNavbar
    home-href="../index.html"
    glossary-href="./"
    guide-href="../golpes/"
    active-page="glossary"
  />
  <main class="glossary-shell">
    <section class="glossary-page" aria-labelledby="glossary-title">
      <header class="glossary-page__header">
        <p class="hero__eyebrow">Glossário</p>
        <h1 id="glossary-title">Palavras técnicas em linguagem simples</h1>
        <p>
          Termos que aparecem na ferramenta, nos alertas e nos cuidados contra golpes digitais.
        </p>
      </header>

      <div class="glossary-table" role="table" aria-label="Glossário de termos técnicos">
        <div class="glossary-table__head" role="row">
          <span role="columnheader">Termo</span>
          <span role="columnheader">Em palavras simples</span>
          <span role="columnheader">Na prática</span>
        </div>

        <article v-for="item in glossaryTerms" :key="item.term" class="glossary-row" role="row">
          <h2 role="cell">{{ item.term }}</h2>
          <p role="cell">{{ item.meaning }}</p>
          <p role="cell">{{ item.practicalUse }}</p>
        </article>
      </div>
    </section>
  </main>
  <SiteFooter terms-href="../politicas/termos-de-uso.html" privacy-href="../politicas/politica-de-privacidade.html" />
</template>
