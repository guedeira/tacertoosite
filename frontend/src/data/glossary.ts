export type GlossaryTerm = {
  term: string;
  meaning: string;
  practicalUse: string;
};

export const glossaryTerms: GlossaryTerm[] = [
  {
    term: "Base cadastrada",
    meaning: "Lista interna que a ferramenta usa como referência para comparar o link informado.",
    practicalUse: "Se o resultado diz que o link bateu ou não bateu, ele está comparando com essa lista de domínios oficiais cadastrados.",
  },
  {
    term: "Blacklist",
    meaning: "Lista de sites ou links já marcados por algum serviço como perigosos.",
    practicalUse: "Um link pode não estar em uma blacklist e ainda assim ser golpe. Por isso, não dependa só desse tipo de verificação.",
  },
  {
    term: "Certificado digital",
    meaning: "Recurso técnico que ajuda a proteger a conexão entre seu navegador e o site.",
    practicalUse: "O cadeado do navegador é bom sinal, mas não garante que o site é da empresa certa. Golpistas também podem ter cadeado.",
  },
  {
    term: "Caminhos ou parâmetros",
    meaning: "Partes extras de um link que aparecem depois do domínio.",
    practicalUse: "Em exemplo.com.br/promocao?cupom=10, /promocao é um caminho e ?cupom=10 é um parâmetro.",
  },
  {
    term: "DNS",
    meaning: "Sistema que ajuda a internet a encontrar o servidor correto quando você digita um endereço.",
    practicalUse: "Problemas ou truques envolvendo DNS podem levar alguém ao lugar errado. Esta ferramenta não faz esse tipo de análise técnica.",
  },
  {
    term: "Domínio",
    meaning: "Nome principal de um site, como exemplo.com.br.",
    practicalUse: "É a parte mais importante para conferir. Em exemplo.com.br/promocao, o domínio é exemplo.com.br.",
  },
  {
    term: "Domínio oficial",
    meaning: "Domínio que a empresa usa de verdade e que foi cadastrado como referência.",
    practicalUse: "Se você escolheu uma empresa e o link usa outro domínio, não digite dados nem pague antes de confirmar.",
  },
  {
    term: "Domínio principal",
    meaning: "Parte central do endereço, sem textos depois da barra e sem subpartes antes do nome principal.",
    practicalUse: "Em https://pagamento.exemplo.com.br/oferta, o domínio principal é exemplo.com.br, não pagamento.exemplo.com.br/oferta.",
  },
  {
    term: "Link",
    meaning: "Endereço que leva você para uma página, arquivo, conversa ou aplicativo.",
    practicalUse: "Links recebidos por SMS, e-mail, WhatsApp, anúncio ou rede social merecem conferência antes de qualquer ação.",
  },
  {
    term: "Malware",
    meaning: "Programa malicioso que pode roubar dados, danificar aparelho ou abrir acesso para criminosos.",
    practicalUse: "Desconfie quando um link pede para instalar aplicativo, extensão, atualização ou arquivo fora das lojas oficiais.",
  },
  {
    term: "Phishing",
    meaning: "Golpe que finge ser uma empresa ou pessoa confiável para roubar senha, código ou dados.",
    practicalUse: "Normalmente chega como alerta urgente, promoção, bloqueio, entrega pendente ou pedido de atualização cadastral.",
  },
  {
    term: "Reputação",
    meaning: "Histórico de confiança ou risco associado a um domínio, site ou endereço.",
    practicalUse: "Serviços de segurança podem usar reputação para alertar sobre sites novos, suspeitos ou já denunciados.",
  },
  {
    term: "Zero Trust",
    meaning: "Forma de pensar em que você não confia automaticamente só porque algo parece familiar.",
    practicalUse: "Antes de clicar, pagar ou informar dados, pergunte: eu confirmei isso por um canal que eu mesmo abri?",
  },
];
