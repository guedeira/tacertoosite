<script setup lang="ts">
import { BookOpen, ClipboardCheck, House, ShieldCheck } from "lucide-vue-next";

import AppLogo from "../atoms/AppLogo.vue";

const props = withDefaults(
  defineProps<{
    homeHref?: string;
    checklistHref?: string;
    glossaryHref?: string;
    guideHref?: string;
    activePage?: "home" | "checklist" | "glossary" | "guide" | "terms" | "none";
  }>(),
  {
    homeHref: "./index.html",
    guideHref: "./golpes/",
    activePage: "none",
  },
);
</script>

<template>
  <nav class="tools-menu" aria-label="Navegação principal">
    <div class="tools-menu__inner">
      <div class="tools-menu__brand">
        <AppLogo :href="props.homeHref" />
      </div>

      <div class="tools-menu__actions">
        <a
          class="tools-menu__nav-link"
          :class="{ 'tools-menu__nav-link--active': props.activePage === 'home' }"
          :href="props.homeHref"
          :aria-current="props.activePage === 'home' ? 'page' : undefined"
        >
          <House aria-hidden="true" />
          <span>Início</span>
        </a>

        <a
          v-if="props.glossaryHref"
          class="tools-menu__nav-link"
          :class="{ 'tools-menu__nav-link--active': props.activePage === 'glossary' }"
          :href="props.glossaryHref"
          :aria-current="props.activePage === 'glossary' ? 'page' : undefined"
        >
          <BookOpen aria-hidden="true" />
          <span>Glossário</span>
        </a>

        <button v-else class="tools-menu__nav-link" type="button" disabled>
          <BookOpen aria-hidden="true" />
          <span>Glossário</span>
        </button>

        <a
          v-if="props.checklistHref"
          class="tools-menu__nav-link"
          :class="{ 'tools-menu__nav-link--active': props.activePage === 'checklist' }"
          :href="props.checklistHref"
          :aria-current="props.activePage === 'checklist' ? 'page' : undefined"
        >
          <ClipboardCheck aria-hidden="true" />
          <span>Checklist Antigolpes</span>
        </a>

        <button v-else class="tools-menu__nav-link" type="button" disabled>
          <ClipboardCheck aria-hidden="true" />
          <span>Checklist Antigolpes</span>
        </button>

        <a
          class="tools-menu__nav-link"
          :class="{ 'tools-menu__nav-link--active': props.activePage === 'guide' }"
          :href="props.guideHref"
          :aria-current="props.activePage === 'guide' ? 'page' : undefined"
        >
          <ShieldCheck aria-hidden="true" />
          <span>Guia Antigolpes</span>
        </a>
      </div>
    </div>
  </nav>
</template>
