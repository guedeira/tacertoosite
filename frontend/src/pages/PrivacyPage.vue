<script setup lang="ts">
import AppNavbar from "../components/templates/AppNavbar.vue";
import SiteFooter from "../components/templates/SiteFooter.vue";
</script>

<template>
  <AppNavbar
    home-href="../index.html"
    glossary-href="../glossario/"
    guide-href="../golpes/"
  />
  <main class="policy-shell">
    <article class="policy-page" aria-labelledby="policy-title">
      <h1 id="policy-title">Política de privacidade</h1>
      <p class="policy-updated">Última atualização: 11 de maio de 2026</p>

      <section>
        <h2>1. Objetivo desta política</h2>
        <p>
          Esta política explica quais informações são coletadas pelo <strong>Tá certo o site?</strong>, por que elas são coletadas e como são usadas.
        </p>
        <p>
          A aplicação é pública, gratuita e não exige cadastro, login ou identificação da pessoa que usa a ferramenta.
        </p>
      </section>

      <section>
        <h2>2. Informações coletadas</h2>
        <p>Quando uma pessoa usa a ferramenta para conferir um link, podemos registrar informações técnicas sobre essa consulta:</p>
        <ul>
          <li>empresa selecionada;</li>
          <li>domínio extraído do link informado no campo de consulta;</li>
          <li>endereço informado quando não for possível extrair um domínio válido;</li>
          <li>resultado da comparação, como correspondência, divergência ou link inválido;</li>
          <li>data e horário da consulta;</li>
          <li>rota acessada, método da requisição, código de resposta e tempo de resposta;</li>
          <li>endereço IP;</li>
          <li>identificação técnica do navegador ou dispositivo, quando enviada pelo navegador.</li>
        </ul>
      </section>

      <section>
        <h2>3. Finalidade da coleta</h2>
        <p>
          As informações são coletadas apenas para fins de análise, melhoria e segurança da aplicação.
        </p>
        <p>
          Esses registros ajudam a entender como agentes de ameaça criam campanhas, quais empresas são mais usadas em tentativas de fraude, quais padrões aparecem nos links enviados e quais domínios suspeitos precisam de atenção.
        </p>
        <p>
          Também usamos esses dados para corrigir erros, acompanhar estabilidade, melhorar a experiência e identificar uso abusivo da infraestrutura.
        </p>
      </section>

      <section>
        <h2>4. O que não coletamos</h2>
        <ul>
          <li>não exigimos nome, e-mail, telefone, documento, senha ou cadastro;</li>
          <li>não coletamos dados bancários;</li>
          <li>não pedimos credenciais de acesso;</li>
          <li>não usamos os registros para vender perfis, anúncios ou listas de usuários.</li>
        </ul>
      </section>

      <section>
        <h2>5. Atenção ao link informado</h2>
        <p>
          O domínio extraído do link colado na ferramenta é registrado para permitir análise de campanhas e padrões de fraude. Quando não for possível extrair um domínio válido, o endereço informado também pode ser registrado para entendermos o erro ou padrão suspeito.
        </p>
        <p>
          Evite colar links que contenham dados pessoais, tokens, códigos de acesso, senhas ou informações sensíveis.
        </p>
      </section>

      <section>
        <h2>6. Compartilhamento</h2>
        <p>
          Os registros podem ser analisados internamente para operação, pesquisa, melhoria e segurança do projeto.
        </p>
        <p>
          Podemos divulgar aprendizados agregados, exemplos técnicos ou indicadores de ameaça sem a intenção de identificar pessoas usuárias da ferramenta.
        </p>
      </section>

      <section>
        <h2>7. Retenção</h2>
        <p>
          Os registros técnicos são mantidos por período limitado. A configuração atual remove automaticamente logs antigos após 30 dias, podendo ser ajustada conforme necessidade operacional e segurança da aplicação.
        </p>
      </section>

      <section>
        <h2>8. Segurança</h2>
        <p>
          Adotamos medidas técnicas razoáveis para restringir o acesso aos registros e reduzir exposição indevida. Ainda assim, nenhum sistema conectado à internet é completamente livre de riscos.
        </p>
      </section>

      <section>
        <h2>9. Alterações nesta política</h2>
        <p>
          Esta política pode ser atualizada a qualquer momento. A versão vigente será aquela publicada nesta página.
        </p>
      </section>
    </article>
  </main>
  <SiteFooter terms-href="./termos-de-uso.html" privacy-href="./politica-de-privacidade.html" />
</template>
