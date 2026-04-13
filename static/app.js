/* ── Helpers ──────────────────────────────────────────────────────── */

const $ = (id) => document.getElementById(id);

function show(el) { el.classList.remove("hidden"); }
function hide(el) { el.classList.add("hidden"); }

function showError(el, msg) {
  el.textContent = msg;
  show(el);
}

function clearError(el) {
  el.textContent = "";
  hide(el);
}

function fmtDate(iso) {
  return new Date(iso).toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

async function apiFetch(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  // 204 has no body
  if (res.status === 204) return null;
  return { ok: res.ok, status: res.status, data: await res.json() };
}

/* ── State ────────────────────────────────────────────────────────── */

let currentCode = null; // short code currently loaded in the manage panel

/* ── Section: Shorten ─────────────────────────────────────────────── */

const formShorten   = $("form-shorten");
const inputUrl      = $("input-url");
const resultShorten = $("result-shorten");
const resultLink    = $("result-link");
const resultCode    = $("result-code");
const resultCreated = $("result-created");
const btnCopy       = $("btn-copy");
const errorShorten  = $("error-shorten");

formShorten.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearError(errorShorten);
  hide(resultShorten);

  const res = await apiFetch("/shorten", {
    method: "POST",
    body: JSON.stringify({ url: inputUrl.value.trim() }),
  });

  if (!res.ok) {
    showError(errorShorten, res.data.error ?? "Something went wrong.");
    return;
  }

  const shortUrl = `${location.origin}/${res.data.short_code}`;
  resultLink.href        = shortUrl;
  resultLink.textContent = shortUrl;
  resultCode.textContent    = res.data.short_code;
  resultCreated.textContent = fmtDate(res.data.created_at);
  show(resultShorten);
  inputUrl.value = "";
});

btnCopy.addEventListener("click", () => {
  navigator.clipboard.writeText(resultLink.href).then(() => {
    btnCopy.title = "Copied!";
    setTimeout(() => (btnCopy.title = "Copy to clipboard"), 2000);
  });
});

/* ── Section: Manage ──────────────────────────────────────────────── */

const inputCode    = $("input-code");
const btnLookup    = $("btn-lookup");
const panelRecord  = $("panel-record");
const recOriginal  = $("rec-original");
const recCode      = $("rec-code");
const recClicks    = $("rec-clicks");
const recCreated   = $("rec-created");
const errorLookup  = $("error-lookup");
const errorManage  = $("error-manage");

const btnUpdateToggle  = $("btn-update-toggle");
const updateRow        = $("update-row");
const inputNewUrl      = $("input-new-url");
const btnUpdateConfirm = $("btn-update-confirm");
const btnUpdateCancel  = $("btn-update-cancel");
const btnDelete        = $("btn-delete");
const btnStats         = $("btn-stats");

function populateRecord(data) {
  recOriginal.textContent = data.original_url;
  recCode.textContent     = data.short_code;
  recClicks.textContent   = data.clicks;
  recCreated.textContent  = fmtDate(data.created_at);
  currentCode = data.short_code;
  clearError(errorManage);
  hide(updateRow);
  show(panelRecord);
}

btnLookup.addEventListener("click", async () => {
  const code = inputCode.value.trim();
  if (!code) return;

  clearError(errorLookup);
  hide(panelRecord);

  const res = await apiFetch(`/shorten/${code}`);

  if (!res.ok) {
    showError(errorLookup, res.data.error ?? "Not found.");
    return;
  }

  populateRecord(res.data);
});

// pressing Enter in the code field triggers lookup
inputCode.addEventListener("keydown", (e) => {
  if (e.key === "Enter") btnLookup.click();
});

/* ── Update ───────────────────────────────────────────────────────── */

btnUpdateToggle.addEventListener("click", () => {
  show(updateRow);
  inputNewUrl.focus();
});

btnUpdateCancel.addEventListener("click", () => {
  hide(updateRow);
  inputNewUrl.value = "";
});

btnUpdateConfirm.addEventListener("click", async () => {
  const newUrl = inputNewUrl.value.trim();
  if (!newUrl || !currentCode) return;

  clearError(errorManage);

  const res = await apiFetch(`/shorten/${currentCode}`, {
    method: "PUT",
    body: JSON.stringify({ url: newUrl }),
  });

  if (!res.ok) {
    showError(errorManage, res.data.error ?? "Update failed.");
    return;
  }

  populateRecord(res.data);
  inputNewUrl.value = "";
});

/* ── Delete ───────────────────────────────────────────────────────── */

btnDelete.addEventListener("click", async () => {
  if (!currentCode) return;
  if (!confirm(`Delete short code "${currentCode}"? This cannot be undone.`)) return;

  clearError(errorManage);

  const res = await apiFetch(`/shorten/${currentCode}`, { method: "DELETE" });

  if (res !== null && !res.ok) {
    showError(errorManage, res.data?.error ?? "Delete failed.");
    return;
  }

  hide(panelRecord);
  inputCode.value = "";
  currentCode = null;
});

/* ── Stats modal ──────────────────────────────────────────────────── */

const modalOverlay  = $("modal-overlay");
const statsCode     = $("stats-code");
const statsOriginal = $("stats-original");
const statsClicks   = $("stats-clicks");
const statsCreated  = $("stats-created");
const btnModalClose = $("btn-modal-close");

btnStats.addEventListener("click", async () => {
  if (!currentCode) return;

  const res = await apiFetch(`/shorten/${currentCode}/stats`);

  if (!res.ok) {
    showError(errorManage, res.data.error ?? "Could not load stats.");
    return;
  }

  statsCode.textContent        = res.data.short_code;
  statsOriginal.textContent    = res.data.original_url;
  statsOriginal.href           = res.data.original_url;
  statsClicks.textContent      = res.data.clicks;
  statsCreated.textContent     = fmtDate(res.data.created_at);
  show(modalOverlay);
});

btnModalClose.addEventListener("click", () => hide(modalOverlay));
modalOverlay.addEventListener("click", (e) => {
  if (e.target === modalOverlay) hide(modalOverlay);
});
