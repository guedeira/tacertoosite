const API_BASE_URL = "https://tacertoosite.onrender.com";
const GITHUB_NEW_ISSUE_URL = "https://github.com/guedeira/tacertoosite/issues/new";

const form = document.querySelector("#validation-form");
const brandSearch = document.querySelector("#brand-search");
const brandIdInput = document.querySelector("#brand-id");
const brandSuggestions = document.querySelector("#brand-suggestions");
const brandNotFound = document.querySelector("#brand-not-found");
const domainInput = document.querySelector("#domain-input");
const resultBox = document.querySelector("#result");
const serviceStatus = document.querySelector("#service-status");
const openRequestModalButton = document.querySelector("#open-request-modal");
const closeRequestModalButton = document.querySelector("#close-request-modal");
const requestModal = document.querySelector("#request-modal");
const requestForm = document.querySelector("#request-form");
const requestBrandName = document.querySelector("#request-brand-name");
const requestDomain = document.querySelector("#request-domain");
const requestSource = document.querySelector("#request-source");
const requestDescription = document.querySelector("#request-description");
const requestResultBox = document.querySelector("#request-result");
const officialDomainsModal = document.querySelector("#official-domains-modal");
const closeOfficialDomainsModalButton = document.querySelector("#close-official-domains-modal");
const officialDomainsList = document.querySelector("#official-domains-list");
const openRequestModalInlineButton = document.querySelector("#open-request-modal-inline");

let brands = [];
let currentOfficialDomains = [];

async function initializeApp() {
  setFormAvailability(false);
  showServiceStatus("Inicializando os serviços. Isso pode levar alguns segundos na primeira visita.");

  const isBackendReady = await waitForBackend();
  if (!isBackendReady) {
    showServiceStatus("Não foi possível conectar ao serviço agora. Aguarde um pouco e tente recarregar a página.", "error");
    setBrands([]);
    return;
  }

  hideServiceStatus();
  await loadBrands();
  setFormAvailability(true);
}

async function waitForBackend() {
  const maxAttempts = 8;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      const response = await fetchWithTimeout(`${API_BASE_URL}/health`, 8000);
      if (response.ok) {
        return true;
      }
    } catch (error) {
      showServiceStatus(`Inicializando os serviços. Tentativa ${attempt} de ${maxAttempts}...`);
    }

    await wait(2500);
  }

  return false;
}

async function fetchWithTimeout(url, timeoutInMs, options = {}) {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutInMs);

  try {
    return await fetch(url, {
      ...options,
      signal: controller.signal,
    });
  } finally {
    window.clearTimeout(timeoutId);
  }
}

function wait(milliseconds) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, milliseconds);
  });
}

async function loadBrands() {
  try {
    const response = await fetch(`${API_BASE_URL}/brands`);
    if (!response.ok) {
      throw new Error("Não foi possível carregar as marcas.");
    }

    const loadedBrands = await response.json();
    setBrands(loadedBrands);
  } catch (error) {
    renderError("Não foi possível carregar a lista de marcas.");
  }
}

function setBrands(loadedBrands) {
  brands = loadedBrands;
  brandSearch.placeholder = brands.length === 0
    ? "Marcas indisponíveis no momento"
    : "Digite o nome da marca";
}

function showServiceStatus(message, type = "info") {
  serviceStatus.className = `service-status ${type}`;
  serviceStatus.hidden = false;
  serviceStatus.textContent = message;
}

function hideServiceStatus() {
  serviceStatus.hidden = true;
  serviceStatus.textContent = "";
}

function setFormAvailability(isAvailable) {
  brandSearch.disabled = !isAvailable;
  domainInput.disabled = !isAvailable;
  form.querySelector("button").disabled = !isAvailable;
}

function handleBrandSearchInput() {
  brandIdInput.value = "";
  const term = brandSearch.value.trim();

  if (!term) {
    hideBrandSuggestions();
    brandNotFound.hidden = true;
    return;
  }

  const matchedBrands = findMatchingBrands(term);
  const exactMatch = brands.find((brand) => normalizeText(brand.name) === normalizeText(term));
  if (exactMatch) {
    brandIdInput.value = exactMatch.id;
  }

  renderBrandSuggestions(matchedBrands);
  brandNotFound.hidden = matchedBrands.length > 0;
}

function findMatchingBrands(term) {
  const normalizedTerm = normalizeText(term);

  return brands
    .filter((brand) => normalizeText(brand.name).includes(normalizedTerm))
    .slice(0, 6);
}

function renderBrandSuggestions(matchedBrands) {
  if (matchedBrands.length === 0) {
    hideBrandSuggestions();
    return;
  }

  brandSuggestions.innerHTML = matchedBrands
    .map((brand) => `
      <button class="brand-suggestion" type="button" data-brand-id="${escapeHtml(brand.id)}">
        ${escapeHtml(brand.name)}
      </button>
    `)
    .join("");
  brandSuggestions.hidden = false;
}

function hideBrandSuggestions() {
  brandSuggestions.hidden = true;
  brandSuggestions.innerHTML = "";
}

function handleBrandSuggestionClick(event) {
  const button = event.target.closest(".brand-suggestion");
  if (!button) {
    return;
  }

  const selectedBrand = brands.find((brand) => brand.id === button.dataset.brandId);
  if (!selectedBrand) {
    return;
  }

  brandSearch.value = selectedBrand.name;
  brandIdInput.value = selectedBrand.id;
  brandNotFound.hidden = true;
  hideBrandSuggestions();
}

function handleDocumentClick(event) {
  if (!event.target.closest(".brand-search")) {
    hideBrandSuggestions();
  }
}

function normalizeText(value) {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

async function validateDomain(event) {
  event.preventDefault();
  clearResult();

  const payload = {
    brand_id: brandIdInput.value,
    input: domainInput.value,
  };

  if (!payload.brand_id) {
    renderError("Selecione uma marca da lista.");
    return;
  }

  if (!payload.input.trim()) {
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
  if (brandSearch.value.trim()) {
    requestBrandName.value = brandSearch.value.trim();
  }

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
  const description = requestDescription.value.trim();

  if (!brandName || !domain) {
    renderRequestMessage("Preencha o nome da empresa e o domínio oficial.", "error");
    return;
  }

  if (description.length > 500) {
    renderRequestMessage("A descrição deve ter no máximo 500 caracteres.", "error");
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
    `Descrição: ${description || "Não informada"}`,
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
brandSearch.addEventListener("input", handleBrandSearchInput);
brandSuggestions.addEventListener("click", handleBrandSuggestionClick);
document.addEventListener("click", handleDocumentClick);
openRequestModalButton.addEventListener("click", openRequestModal);
openRequestModalInlineButton.addEventListener("click", openRequestModal);
closeRequestModalButton.addEventListener("click", closeRequestModal);
requestModal.addEventListener("click", closeRequestModalOnBackdrop);
requestForm.addEventListener("submit", requestBrandAddition);
closeOfficialDomainsModalButton.addEventListener("click", closeOfficialDomainsModal);
officialDomainsModal.addEventListener("click", closeOfficialDomainsModalOnBackdrop);
initializeApp();
