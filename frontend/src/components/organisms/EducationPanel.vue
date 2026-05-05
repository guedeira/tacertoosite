<script setup lang="ts">
import { Eye, ShieldAlert, Sparkles } from "lucide-vue-next";
</script>

<template>
  <aside class="education-panel" aria-labelledby="education-title">
    <div class="education-panel__header">
      <ShieldAlert aria-hidden="true" />
      <div>
        <h2 id="education-title">Compare antes de clicar</h2>
        <p>Golpes costumam usar links parecidos com os de empresas reais para criar pressa e confiança.</p>
      </div>
    </div>

    <div class="education-panel__block">
      <Sparkles aria-hidden="true" />
      <div>
        <h3>Como usar</h3>
        <ol>
          <li>Escolha a empresa que o link diz representar.</li>
          <li>Cole o link recebido por mensagem, e-mail ou rede social.</li>
          <li>Confira se o domínio comparado bate com o cadastro oficial.</li>
        </ol>
      </div>
    </div>

    <div class="education-panel__block">
      <Eye aria-hidden="true" />
      <div>
        <h3>O que observar</h3>
        <p>Urgência, prêmios, ameaça de bloqueio, cobrança inesperada ou pedido de senha são sinais para ir com calma.</p>
      </div>
    </div>
  </aside>
</template>

