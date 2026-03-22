// ── Config ────────────────────────────────────────────────
const API_URL = "http://127.0.0.1:8000/diagnose";

// ── Translations ──────────────────────────────────────────
const i18n = {
  en: {
    badge:            "DIAGNOSTIC SYSTEM v2.0",
    title_line1:      "What's broken?",
    title_line2:      "We'll fix it.",
    subtitle:         "Describe your device problem and get an instant analysis — possible causes and step-by-step repair instructions.",
    form_header:      "Enter Device Info",
    label_device:     "Device Type",
    select_placeholder: "Select a device…",
    dev_laptop:       "💻 Laptop",
    dev_smartphone:   "📱 Smartphone",
    dev_printer:      "🖨️ Printer",
    dev_router:       "📡 Router / WiFi",
    dev_desktop:      "🖥️ Desktop PC",
    label_problem:    "Problem Description",
    input_placeholder:"e.g. not turning on, no internet, paper jam…",
    btn_diagnose:     "Run Diagnosis",
    btn_loading:      "Analysing",
    result_header:    "Diagnosis Report",
    causes_title:     "Possible Causes",
    steps_title:      "Repair Steps",
    footer_note:      "Results are rule-based estimates. Always verify with a certified technician.",
    err_no_device:    "Please select a device type.",
    err_no_problem:   "Please describe the problem.",
    err_short:        "Problem description is too short. Add more detail.",
    err_server:       "Cannot connect to backend. Make sure the FastAPI server is running on port 8000.",
    err_generic:      "An unexpected error occurred.",
    meta_cause:       "cause found",
    meta_causes:      "causes found",
  },
  fr: {
    badge:            "SYSTÈME DE DIAGNOSTIC v2.0",
    title_line1:      "Quelque chose est cassé ?",
    title_line2:      "On va réparer ça.",
    subtitle:         "Décrivez le problème de votre appareil et obtenez une analyse instantanée — causes possibles et étapes de réparation.",
    form_header:      "Entrer les infos de l'appareil",
    label_device:     "Type d'appareil",
    select_placeholder: "Sélectionner un appareil…",
    dev_laptop:       "💻 Ordinateur portable",
    dev_smartphone:   "📱 Smartphone",
    dev_printer:      "🖨️ Imprimante",
    dev_router:       "📡 Routeur / WiFi",
    dev_desktop:      "🖥️ PC de bureau",
    label_problem:    "Description du problème",
    input_placeholder:"ex: ne s'allume pas, pas d'internet, bourrage papier…",
    btn_diagnose:     "Lancer le diagnostic",
    btn_loading:      "Analyse en cours",
    result_header:    "Rapport de diagnostic",
    causes_title:     "Causes possibles",
    steps_title:      "Étapes de réparation",
    footer_note:      "Les résultats sont des estimations. Consultez toujours un technicien certifié.",
    err_no_device:    "Veuillez sélectionner un type d'appareil.",
    err_no_problem:   "Veuillez décrire le problème.",
    err_short:        "La description est trop courte. Ajoutez plus de détails.",
    err_server:       "Impossible de se connecter au serveur. Assurez-vous que FastAPI tourne sur le port 8000.",
    err_generic:      "Une erreur inattendue s'est produite.",
    meta_cause:       "cause trouvée",
    meta_causes:      "causes trouvées",
  },
  ar: {
    badge:            "نظام التشخيص v2.0",
    title_line1:      "ما الذي تعطّل؟",
    title_line2:      "سنصلحه.",
    subtitle:         "صف مشكلة جهازك واحصل على تحليل فوري — الأسباب المحتملة وخطوات الإصلاح.",
    form_header:      "أدخل معلومات الجهاز",
    label_device:     "نوع الجهاز",
    select_placeholder: "اختر جهازاً…",
    dev_laptop:       "💻 لابتوب",
    dev_smartphone:   "📱 هاتف ذكي",
    dev_printer:      "🖨️ طابعة",
    dev_router:       "📡 راوتر / واي فاي",
    dev_desktop:      "🖥️ كمبيوتر مكتبي",
    label_problem:    "وصف المشكلة",
    input_placeholder:"مثال: لا يشتغل، لا إنترنت، ورقة عالقة…",
    btn_diagnose:     "تشغيل التشخيص",
    btn_loading:      "جارٍ التحليل",
    result_header:    "تقرير التشخيص",
    causes_title:     "الأسباب المحتملة",
    steps_title:      "خطوات الإصلاح",
    footer_note:      "النتائج تقديرية. يُرجى دائماً التحقق مع فني متخصص.",
    err_no_device:    "الرجاء اختيار نوع الجهاز.",
    err_no_problem:   "الرجاء وصف المشكلة.",
    err_short:        "الوصف قصير جداً. أضف مزيداً من التفاصيل.",
    err_server:       "لا يمكن الاتصال بالخادم. تأكد من تشغيل FastAPI على المنفذ 8000.",
    err_generic:      "حدث خطأ غير متوقع.",
    meta_cause:       "سبب محتمل",
    meta_causes:      "أسباب محتملة",
  }
};

// ── State ─────────────────────────────────────────────────
let currentLang = "en";

// ── DOM refs ──────────────────────────────────────────────
const deviceSelect  = document.getElementById("device");
const problemInput  = document.getElementById("problem");
const diagnoseBtn   = document.getElementById("diagnoseBtn");
const errorMsg      = document.getElementById("errorMsg");
const resultSection = document.getElementById("resultSection");
const causesList    = document.getElementById("causesList");
const stepsList     = document.getElementById("stepsList");
const resultMeta    = document.getElementById("resultMeta");

// ── Language switcher ─────────────────────────────────────
function setLang(lang) {
  currentLang = lang;

  // Update active button
  document.querySelectorAll(".lang-btn").forEach(btn => {
    btn.classList.toggle("active", btn.textContent.trim().toLowerCase() === lang ||
      (lang === "ar" && btn.textContent.trim() === "ع"));
  });

  // Apply Arabic font class
  document.body.classList.remove("lang-en", "lang-fr", "lang-ar");
  document.body.classList.add("lang-" + lang);

  const t = i18n[lang];

  // Update all data-i18n elements
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (t[key] !== undefined) {
      // Handle elements with child <span data-i18n>
      if (el.children.length === 0) {
        el.textContent = t[key];
      } else {
        // Replace only direct text node (for hero title with inner span)
        for (const node of el.childNodes) {
          if (node.nodeType === Node.TEXT_NODE) {
            node.textContent = t[key];
            break;
          }
        }
      }
    }
  });

  // Update placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (t[key]) el.placeholder = t[key];
  });

  // Update select options
  const opts = {
    dev_laptop:     "💻 " + (lang === "ar" ? "لابتوب" : lang === "fr" ? "Ordinateur portable" : "Laptop"),
    dev_smartphone: "📱 " + (lang === "ar" ? "هاتف ذكي" : "Smartphone"),
    dev_printer:    "🖨️ " + (lang === "ar" ? "طابعة" : lang === "fr" ? "Imprimante" : "Printer"),
    dev_router:     "📡 " + (lang === "ar" ? "راوتر / واي فاي" : lang === "fr" ? "Routeur / WiFi" : "Router / WiFi"),
    dev_desktop:    "🖥️ " + (lang === "ar" ? "كمبيوتر مكتبي" : lang === "fr" ? "PC de bureau" : "Desktop PC"),
  };

  document.querySelectorAll("option[data-i18n]").forEach(opt => {
    const key = opt.getAttribute("data-i18n");
    if (opts[key]) opt.textContent = opts[key];
    if (key === "select_placeholder") opt.textContent = t["select_placeholder"];
  });

  // Update page title
  const titles = { en: "Smart Repair", fr: "Smart Repair", ar: "الإصلاح الذكي" };
  document.title = titles[lang];
}

// ── Allow Enter key to submit ──────────────────────────────
problemInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") runDiagnosis();
});

// ── Main function ─────────────────────────────────────────
async function runDiagnosis() {
  const device  = deviceSelect.value.trim();
  const problem = problemInput.value.trim();
  const t = i18n[currentLang];

  clearError();

  if (!device) {
    showError(t.err_no_device);
    deviceSelect.focus();
    return;
  }
  if (!problem) {
    showError(t.err_no_problem);
    problemInput.focus();
    return;
  }
  if (problem.length < 3) {
    showError(t.err_short);
    problemInput.focus();
    return;
  }

  setLoading(true);
  hideResults();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ device, problem }),
    });

    if (!response.ok) throw new Error(`Server error: ${response.status}`);

    const data = await response.json();
    renderResults(data);

  } catch (err) {
    if (err.message.includes("fetch") || err.message.includes("Failed")) {
      showError(t.err_server);
    } else {
      showError(err.message || t.err_generic);
    }
  } finally {
    setLoading(false);
  }
}

// ── Render results ────────────────────────────────────────
function renderResults(data) {
  const t = i18n[currentLang];
  const deviceLabel = data.device.charAt(0).toUpperCase() + data.device.slice(1);
  const causeWord = data.causes.length === 1 ? t.meta_cause : t.meta_causes;
  resultMeta.textContent = `${deviceLabel} · ${data.causes.length} ${causeWord}`;

  causesList.innerHTML = "";
  data.causes.forEach(cause => {
    const li = document.createElement("li");
    li.textContent = cause;
    causesList.appendChild(li);
  });

  stepsList.innerHTML = "";
  data.steps.forEach(step => {
    const li = document.createElement("li");
    li.textContent = step;
    stepsList.appendChild(li);
  });

  resultSection.classList.add("visible");
  resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

// ── Helpers ───────────────────────────────────────────────
function setLoading(on) {
  const t = i18n[currentLang];
  if (on) {
    diagnoseBtn.classList.add("loading");
    diagnoseBtn.querySelector(".btn-text").textContent = t.btn_loading;
    diagnoseBtn.querySelector(".btn-icon").textContent = "";
  } else {
    diagnoseBtn.classList.remove("loading");
    diagnoseBtn.querySelector(".btn-text").textContent = t.btn_diagnose;
    diagnoseBtn.querySelector(".btn-icon").textContent = "→";
  }
}

function showError(msg) {
  errorMsg.textContent = "⚠ " + msg;
  errorMsg.classList.add("visible");
}

function clearError() {
  errorMsg.textContent = "";
  errorMsg.classList.remove("visible");
}

function hideResults() {
  resultSection.classList.remove("visible");
}

// ── Init ──────────────────────────────────────────────────
setLang("en");