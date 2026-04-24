const API_BASE_URL = "http://localhost:8000";
const GITHUB_NEW_ISSUE_URL = "https://github.com/SEU_USUARIO/SEU_REPOSITORIO/issues/new";

const form = document.querySelector("#validation-form");
const brandSelect = document.querySelector("#brand-select");
const domainInput = document.querySelector("#domain-input");
const resultBox = document.querySelector("#result");
const openRequestModalButton = document.querySelector("#open-request-modal");
const closeRequestModalButton = document.querySelector("#close-request-modal");
const requestModal = document.querySelector("#request-modal");
const requestForm = document.querySelector("#request-form");
const requestBrandName = document.querySelector("#request-brand-name");
const requestDomain = document.querySelector("#request-domain");
const requestSource = document.querySelector("#request-source");
const requestResultBox = document.querySelector("#request-result");
const officialDomainsModal = document.querySelector("#official-domains-modal");
const closeOfficialDomainsModalButton = document.querySelector("#close-official-domains-modal");
const officialDomainsList = document.querySelector("#official-domains-list");

let currentOfficialDomains = [];

async function loadBrands() {
  try {
    const response = await fetch(`${API_BASE_URL}/brands`);
    if (!response.ok) {
      throw new Error("Não foi possível carregar as marcas.");
    }

    const brands = await response.json();
    renderBrandOptions(brands);
  } catch (error) {
    renderError("Não foi possível carregar a lista de marcas.");
  }
}

function renderBrandOptions(brands) {
  brandSelect.innerHTML = '<option value="">Selecione uma marca</option>';

  brands.forEach((brand) => {
    const option = document.createElement("option");
    option.value = brand.id;
    option.textContent = brand.name;
    brandSelect.appendChild(option);
  });
}

async function validateDomain(event) {
  event.preventDefault();
  clearResult();

  const payload = {
    brand_id: brandSelect.value,
    input: domainInput.value,
  };

  if (!payload.brand_id || !payload.input.trim()) {
    renderError("Digite um endereço válido.");
    return;
  }

  setLoading(true);

  try {
    const response = await fetch(`${API_BASE_URL}/validate-domain`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();
    renderValidationResult(result);
  } catch (error) {
    renderError("Não foi possível verificar o endereço agora.");
  } finally {
    setLoading(false);
  }
}

function renderValidationResult(result) {
  const statusText = result.is_match
    ? "Esse endereço corresponde ao domínio oficial cadastrado."
    : "Atenção: esse endereço não corresponde ao domínio oficial cadastrado.";
  const officialDomains = Array.isArray(result.official_domains) ? result.official_domains : [];
  const officialDomainsHtml = result.is_match ? "" : renderOfficialDomainsPreview(officialDomains);

  currentOfficialDomains = officialDomains;

  resultBox.className = `result ${result.is_match ? "match" : "no-match"}`;
  resultBox.hidden = false;
  resultBox.innerHTML = `
    <strong>${statusText}</strong>
    <span>${escapeHtml(result.message)}</span>
    ${officialDomainsHtml}
    ${result.submitted_domain ? `<small>Domínio verificado: ${escapeHtml(result.submitted_domain)}</small>` : ""}
  `;
}

function renderOfficialDomainsPreview(officialDomains) {
  if (officialDomains.length === 0) {
    return "";
  }

  const visibleDomains = officialDomains.slice(0, 4);
  const label = officialDomains.length === 1
    ? "Domínio oficial cadastrado:"
    : "Domínios oficiais cadastrados:";
  const domainsHtml = visibleDomains
    .map((domain) => `<strong class="domain-pill">${escapeHtml(domain)}</strong>`)
    .join("");
  const buttonHtml = officialDomains.length > 4
    ? '<button id="open-official-domains-modal" class="inline-button" type="button">Ver mais</button>'
    : "";

  return `
    <div class="official-domains-preview">
      <span>${label}</span>
      <div class="domain-pills">${domainsHtml}${buttonHtml}</div>
    </div>
  `;
}

function renderError(message) {
  resultBox.className = "result error";
  resultBox.hidden = false;
  resultBox.innerHTML = `<strong>${message}</strong>`;
}

function clearResult() {
  resultBox.hidden = true;
  resultBox.textContent = "";
}

function setLoading(isLoading) {
  const button = form.querySelector("button");
  button.disabled = isLoading;
  button.textContent = isLoading ? "Comparando..." : "Comparar";
}

function openRequestModal() {
  requestModal.showModal();
  requestBrandName.focus();
}

function closeRequestModal() {
  requestModal.close();
  requestResultBox.hidden = true;
  requestResultBox.textContent = "";
  openRequestModalButton.focus();
}

function closeRequestModalOnBackdrop(event) {
  if (clickedOutsideModal(event, requestModal)) {
    closeRequestModal();
  }
}

function openOfficialDomainsModal() {
  officialDomainsList.innerHTML = currentOfficialDomains
    .map((domain) => `<div>${escapeHtml(domain)}</div>`)
    .join("");
  officialDomainsModal.showModal();
  closeOfficialDomainsModalButton.focus();
}

function closeOfficialDomainsModal() {
  officialDomainsModal.close();
}

function closeOfficialDomainsModalOnBackdrop(event) {
  if (clickedOutsideModal(event, officialDomainsModal)) {
    closeOfficialDomainsModal();
  }
}

function handleResultClick(event) {
  if (event.target.id === "open-official-domains-modal") {
    openOfficialDomainsModal();
  }
}

function clickedOutsideModal(event, modal) {
  const modalBounds = modal.getBoundingClientRect();

  return (
    event.clientX < modalBounds.left ||
    event.clientX > modalBounds.right ||
    event.clientY < modalBounds.top ||
    event.clientY > modalBounds.bottom
  );
}

function requestBrandAddition(event) {
  event.preventDefault();

  const brandName = requestBrandName.value.trim();
  const domain = requestDomain.value.trim().toLowerCase();
  const source = requestSource.value.trim();

  if (!brandName || !domain) {
    renderRequestMessage("Preencha o nome da empresa e o domínio oficial.", "error");
    return;
  }

  if (GITHUB_NEW_ISSUE_URL.includes("SEU_USUARIO")) {
    renderRequestMessage("Configure a URL do repositório no arquivo app.js antes de enviar solicitações.", "error");
    return;
  }

  const title = `Adicionar domínio oficial: ${brandName}`;
  const body = [
    "## Solicitação de nova empresa",
    "",
    `Empresa: ${brandName}`,
    `Domínio oficial sugerido: ${domain}`,
    `Fonte para conferência: ${source || "Não informada"}`,
    "",
    "## Critérios",
    "",
    "- [ ] O domínio foi conferido em uma fonte oficial.",
    "- [ ] A empresa ainda não existe no cadastro.",
    "- [ ] A alteração mantém o cadastro simples e auditável.",
  ].join("\n");

  const issueUrl = `${GITHUB_NEW_ISSUE_URL}?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`;
  window.open(issueUrl, "_blank", "noopener,noreferrer");

  renderRequestMessage("A solicitação foi aberta no GitHub para revisão.", "match");
  requestForm.reset();
}

function renderRequestMessage(message, type) {
  requestResultBox.className = `result ${type}`;
  requestResultBox.hidden = false;
  requestResultBox.innerHTML = `<strong>${message}</strong>`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

form.addEventListener("submit", validateDomain);
resultBox.addEventListener("click", handleResultClick);
openRequestModalButton.addEventListener("click", openRequestModal);
closeRequestModalButton.addEventListener("click", closeRequestModal);
requestModal.addEventListener("click", closeRequestModalOnBackdrop);
requestForm.addEventListener("submit", requestBrandAddition);
closeOfficialDomainsModalButton.addEventListener("click", closeOfficialDomainsModal);
officialDomainsModal.addEventListener("click", closeOfficialDomainsModalOnBackdrop);
loadBrands();
