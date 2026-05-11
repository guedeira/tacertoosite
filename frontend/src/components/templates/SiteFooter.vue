<script setup lang="ts">
import { ArrowUp } from "lucide-vue-next";
import { onBeforeUnmount, onMounted, ref } from "vue";

const SCROLL_TOP_VISIBILITY_OFFSET = 520;

const props = withDefaults(
  defineProps<{
    termsHref?: string;
  }>(),
  {
    termsHref: "./politicas/termos-de-uso.html",
  },
);

const showBackToTop = ref(false);

function updateBackToTopVisibility(): void {
  showBackToTop.value = window.scrollY > SCROLL_TOP_VISIBILITY_OFFSET;
}

function scrollToTop(): void {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

onMounted(() => {
  updateBackToTopVisibility();
  window.addEventListener("scroll", updateBackToTopVisibility, { passive: true });
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", updateBackToTopVisibility);
});
</script>

<template>
  <footer class="site-footer">
    <a :href="props.termsHref">Termos de uso</a>
    <span class="site-footer__made-by">Feito com 🖤 pelo Guedeira</span>
    <button
      class="back-to-top"
      :class="{ 'back-to-top--visible': showBackToTop }"
      type="button"
      aria-label="Voltar ao topo"
      @click="scrollToTop"
    >
      <ArrowUp aria-hidden="true" />
    </button>
  </footer>
</template>
