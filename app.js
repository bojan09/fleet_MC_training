"use strict";
let content;
let category = "All";
let query = "";
let questionIndex = 0;
let score = 0;
const $ = (s) => document.querySelector(s);
const APP_BASE = new URL(".", document.currentScript.src);
const assetURL = (path) => new URL(path, APP_BASE).href;
function setNavigationState(id) {
  document.querySelectorAll("header nav a").forEach((a) => {
    const target = a.hash.slice(1);
    const active =
      target === id || (target === "modules" && /^(module|lesson)-/.test(id));
    if (active) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
}
function enhanceImages(container = document) {
  container.querySelectorAll("img").forEach((img) => {
    if (img.id === "viewer-image" || img.dataset.checked) return;
    img.dataset.checked = "true";
    img.decoding = "async";
    const failed = () => {
      img.hidden = true;
      const visual = img.closest(".visual-open");
      if (visual) {
        visual.disabled = true;
        visual.classList.add("image-unavailable");
      }
      const frame = img.parentElement;
      if (!frame.querySelector(".image-error")) {
        const label = document.createElement("span");
        label.className = "image-error";
        label.textContent = "Image unavailable";
        frame.append(label);
      }
    };
    img.addEventListener("error", failed);
    if (img.complete && !img.naturalWidth && img.getAttribute("src")) failed();
  });
}

const escapeHTML = (s) =>
  String(s).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const questions = [
  {
    q: "A driver reports a repeated low-air warning. What is the first priority?",
    a: [
      "Confirm a safe stop and exact location, then coordinate qualified brake service.",
      "Ask the driver to continue to the nearest delivery.",
      "Clear the warning and wait for it to return.",
    ],
    correct: 0,
    why: "A low-air warning needs urgent attention. Do not authorize continued driving. Safety and location come before vendor coordination.",
    lesson: "lesson-18",
  },
  {
    q: "What do PM A, B, and C mean?",
    a: [
      "Universal DOT inspection levels.",
      "Fleet-defined preventive maintenance service tiers.",
      "Three standardized engine fault codes.",
    ],
    correct: 1,
    why: "PM tiers are company-defined. Use the applicable fleet and OEM schedules rather than assuming a universal interval.",
    lesson: "lesson-16",
  },
  {
    q: "A reefer is above the requested temperature. What information should you capture?",
    a: [
      "Only the requested setpoint.",
      "Only the trailer number.",
      "Setpoint, actual temperatures, alarms, model, cargo risk, and location.",
    ],
    correct: 2,
    why: "Setpoint and actual temperature are different. Record both, escalate cargo risk, and coordinate an appropriate reefer specialist.",
    lesson: "lesson-10",
  },
  {
    q: "Where is the fifth wheel located?",
    a: [
      "On the tractor; it couples with the trailer kingpin.",
      "Inside the trailer refrigeration unit.",
      "On the trailer rear axle.",
    ],
    correct: 0,
    why: "The fifth wheel is the tractor coupling plate. The kingpin belongs to the trailer. Qualified personnel verify engagement.",
    lesson: "lesson-9",
  },
  {
    q: "What does a diagnostic trouble code prove by itself?",
    a: [
      "Exactly which part must be replaced.",
      "That the vehicle is always safe to drive.",
      "It identifies a reported fault condition, but is not a standalone diagnosis.",
    ],
    correct: 2,
    why: "Document the exact code, vehicle, symptoms, and warnings. Qualified technicians interpret codes using appropriate OEM information.",
    lesson: "lesson-13",
  },
];
function cards() {
  const grid = $("#module-grid");
  const matches = content.modules.filter(
    (m) =>
      (category === "All" || m.category === category) &&
      `${m.title} ${m.description} ${m.lessons.map((i) => content.lessons[i].notes.join(" ")).join(" ")}`
        .toLowerCase()
        .includes(query),
  );
  grid.innerHTML = matches
    .map(
      (m) =>
        `<a class="module-card" href="#${m.id}"><div class="card-image"><img src="${assetURL(m.image)}" alt="${escapeHTML(m.title)} illustration from the supplied manual" loading="lazy" width="384" height="256"><span class="card-number">${m.id.split("-")[1].padStart(2, "0")}</span><span class="illustration-tag">MANUAL ILLUSTRATION</span></div><div class="card-body"><div class="card-category">${m.category} & ${m.category === "Equipment" ? "systems" : "coordination"}</div><h3>${m.title}</h3><p>${m.description}</p><div class="card-meta"><span>▤ &nbsp; ${m.lessons.length} lessons &nbsp; · &nbsp; ${m.lessons.length * 4} min read</span><span>→</span></div></div></a>`,
    )
    .join("");
  $("#empty").hidden = !!matches.length;
  $("#module-count").textContent =
    `${matches.length} module${matches.length === 1 ? "" : "s"}`;
  enhanceImages(grid);
}
function source(page) {
  return `<aside class="source-note">Source: user-supplied <strong>Fleet MC Training</strong> PDF${page ? `, page ${page}` : ""}. Educational material; not an OEM procedure or inspection certification. Confirm vehicle-specific instructions and current rules. <a href="#sources">Source notes →</a></aside>`;
}
function lessonLink(l, n) {
  return `<a class="lesson-link" href="#${l.id}"><img class="lesson-thumb" src="${assetURL(l.overviewImage)}" alt="" loading="lazy"><span class="eyebrow">${String(n + 1).padStart(2, "0")}</span><div><b>${escapeHTML(l.title)}</b><small>${escapeHTML(l.subtitle)}</small></div><span>→</span></a>`;
}
function visualButton(image, alt, className = "") {
  return `<button type="button" class="visual-open ${className}" data-visual="${escapeHTML(assetURL(image))}" data-alt="${escapeHTML(alt)}" aria-label="Open full-screen image: ${escapeHTML(alt)}"><img src="${escapeHTML(assetURL(image))}" alt="${escapeHTML(alt)}" loading="lazy"><span class="zoom-cue" aria-hidden="true">⤢ &nbsp; Enlarge</span></button>`;
}
function lessonVisuals(lesson) {
  return `<section class="lesson-visual-overview" aria-label="Illustrated lesson overview"><div class="visual-guide"><div class="eyebrow">LOOK · IDENTIFY · UNDERSTAND</div><h2>A visual guide to ${escapeHTML(lesson.title.toLowerCase())}</h2><p>Select the illustrated overview or any individual diagram to open the full-screen viewer.</p></div><figure class="pdf-figure overview-figure">${visualButton(lesson.overviewImage, lesson.overviewAlt, "overview-art")}<figcaption>Illustrated overview · Simplified concepts, not a mechanical service drawing.</figcaption></figure><div class="visual-jump-links">${lesson.visualNotes.map((n, i) => `<a href="#visual-note-${i + 1}" data-note-jump="visual-note-${i + 1}"><span>${String(i + 1).padStart(2, "0")}</span>${escapeHTML(n.title)}</a>`).join("")}</div><details class="original-artwork"><summary>View the original PDF artwork (low-resolution source)</summary><figure class="pdf-figure">${visualButton(lesson.referenceImage, lesson.referenceAlt, "source-art")}<figcaption>Original artwork · PDF page ${lesson.page}. The supplied image is only 384 × 256 pixels. Its embedded labels and example values are unverified.</figcaption></figure></details></section>`;
}
function visualNotes(lesson) {
  return `<div class="notes illustrated-notes">${lesson.visualNotes.map((n, i) => `<article class="note illustrated-note" id="visual-note-${i + 1}"><div class="note-heading"><span>${String(i + 1).padStart(2, "0")}</span><h3>${escapeHTML(n.title)}</h3></div>${visualButton(n.image, n.alt)}<p>${escapeHTML(n.text)}</p></article>`).join("")}</div>`;
}
let previousVisualFocus;
function setupVisualViewer() {
  const dialog = document.createElement("dialog");
  dialog.id = "visual-viewer";
  dialog.className = "visual-viewer";
  dialog.setAttribute("aria-labelledby", "visual-title");
  dialog.innerHTML = `<div class="viewer-bar"><div><span class="eyebrow">VISUAL REFERENCE</span><h2 id="visual-title">Image</h2></div><button type="button" class="viewer-close" aria-label="Close enlarged image">Close ×</button></div><div class="viewer-controls"><button type="button" data-previous aria-label="Previous image">←</button><span id="visual-position"></span><button type="button" data-next aria-label="Next image">→</button><span class="control-divider"></span><button type="button" data-zoom="out" aria-label="Zoom out">−</button><output id="zoom-level" aria-live="polite">100%</output><button type="button" data-zoom="in" aria-label="Zoom in">+</button><button type="button" data-zoom="reset">Fit image</button><button type="button" data-fullscreen>Enter fullscreen</button><span class="viewer-help">Arrow keys to browse · Escape to close</span></div><div class="viewer-scroll"><img id="viewer-image" alt=""></div>`;
  document.body.append(dialog);
  let zoom = 1,
    items = [],
    index = 0;
  const viewport = dialog.querySelector(".viewer-scroll");
  const img = $("#viewer-image");
  const viewerStatus = document.createElement("p");
  viewerStatus.className = "viewer-status";
  viewerStatus.setAttribute("role", "status");
  viewerStatus.hidden = true;
  viewport.append(viewerStatus);
  img.addEventListener("error", () => {
    viewerStatus.textContent =
      "This image could not load. Close the viewer and try again.";
    viewerStatus.hidden = false;
    img.hidden = true;
  });
  function resize() {
    if (!dialog.open || !img.naturalWidth) return;
    const availableWidth = Math.max(1, viewport.clientWidth - 24),
      availableHeight = Math.max(1, viewport.clientHeight - 24);
    const scale = Math.min(
      availableWidth / img.naturalWidth,
      availableHeight / img.naturalHeight,
    );
    img.style.width = `${Math.floor(img.naturalWidth * scale * zoom)}px`;
    img.style.height = `${Math.floor(img.naturalHeight * scale * zoom)}px`;
    $("#zoom-level").textContent = `${Math.round(zoom * 100)}%`;
    dialog.querySelector('[data-zoom="out"]').disabled = zoom <= 1;
    dialog.querySelector('[data-zoom="in"]').disabled = zoom >= 4;
  }
  function show(position) {
    index = position;
    zoom = 1;
    const b = items[index];
    img.hidden = false;
    viewerStatus.hidden = true;
    img.removeAttribute("src");
    img.src = b.dataset.visual;
    img.alt = b.dataset.alt;
    $("#visual-title").textContent = b.dataset.alt.split(":")[0];
    $("#visual-position").textContent = `${index + 1} / ${items.length}`;
    dialog.querySelector("[data-previous]").disabled = index === 0;
    dialog.querySelector("[data-next]").disabled = index === items.length - 1;
    img.onload = () => {
      resize();
      viewport.scrollTo(0, 0);
    };
    if (img.complete) resize();
  }
  function close() {
    if (document.fullscreenElement === document.documentElement)
      document.exitFullscreen().catch(() => {});
    dialog.close();
  }
  dialog.querySelector(".viewer-close").onclick = close;
  dialog.querySelector("[data-previous]").onclick = () => {
    if (index > 0) show(index - 1);
  };
  dialog.querySelector("[data-next]").onclick = () => {
    if (index < items.length - 1) show(index + 1);
  };
  dialog.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight" && index < items.length - 1) {
      e.preventDefault();
      show(index + 1);
    }
    if (e.key === "ArrowLeft" && index > 0) {
      e.preventDefault();
      show(index - 1);
    }
  });
  dialog.addEventListener("close", () => {
    document.body.classList.remove("viewer-open");
    if (previousVisualFocus?.isConnected)
      previousVisualFocus.focus({ preventScroll: true });
    img.removeAttribute("src");
  });
  dialog.querySelectorAll("[data-zoom]").forEach(
    (b) =>
      (b.onclick = () => {
        zoom =
          b.dataset.zoom === "reset"
            ? 1
            : Math.max(
                1,
                Math.min(4, zoom + (b.dataset.zoom === "in" ? 0.5 : -0.5)),
              );
        resize();
        if (zoom === 1) viewport.scrollTo(0, 0);
      }),
  );
  const fullscreen = dialog.querySelector("[data-fullscreen]");
  fullscreen.hidden = !document.documentElement.requestFullscreen;
  fullscreen.onclick = async () => {
    try {
      if (document.fullscreenElement === document.documentElement)
        await document.exitFullscreen();
      else await document.documentElement.requestFullscreen();
    } catch {
      fullscreen.textContent = "Screen-sized view active";
    }
  };
  document.addEventListener("fullscreenchange", () => {
    fullscreen.textContent =
      document.fullscreenElement === document.documentElement
        ? "Exit fullscreen"
        : "Enter fullscreen";
    requestAnimationFrame(resize);
  });
  new ResizeObserver(() => {
    if (dialog.open) resize();
  }).observe(viewport);
  document.addEventListener("click", (e) => {
    const jump = e.target.closest("[data-note-jump]");
    if (jump) {
      e.preventDefault();
      const target = document.getElementById(jump.dataset.noteJump);
      target?.scrollIntoView({
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "instant"
          : "smooth",
        block: "start",
      });
      if (target) {
        target.tabIndex = -1;
        target.focus({ preventScroll: true });
      }
      return;
    }
    const b = e.target.closest("[data-visual]");
    if (!b || b.disabled) return;
    previousVisualFocus = b;
    items = [...b.closest("main").querySelectorAll("[data-visual]")].filter(
      (x) => x.getClientRects().length > 0 && !x.closest("details:not([open])"),
    );
    index = items.indexOf(b);
    dialog.showModal();
    document.body.classList.add("viewer-open");
    show(index);
  });
  window.addEventListener("hashchange", () => {
    if (dialog.open) close();
  });
}
function route() {
  const id = location.hash.slice(1) || "home";
  if (id === "main") {
    history.replaceState(null, "", "#home");
    $("#home").hidden = false;
    $("#reader").hidden = true;
    $("#main").focus();
    return;
  }
  setNavigationState(id);
  const reader = $("#reader");
  const home = $("#home");
  if (id === "home" || id === "modules") {
    home.hidden = false;
    reader.hidden = true;
    document.title = "Fleet MC Training — Know the truck. Own the process.";
    if (id === "modules")
      requestAnimationFrame(() => $("#modules").scrollIntoView());
    else window.scrollTo(0, 0);
    return;
  }
  let html = "";
  const module = content.modules.find((x) => x.id === id);
  const lesson = content.lessons.find((x) => x.id === id);
  if (module) {
    html = `<a class="back" href="#modules">← All learning modules</a><div class="eyebrow" style="margin-top:35px">MODULE ${module.id.split("-")[1].padStart(2, "0")} · ${module.category.toUpperCase()}</div><h1>${module.title}</h1><p class="intro">${module.description}</p><p>${module.lessons.length} lessons · Approximately ${module.lessons.length * 4} minutes · Read in any order</p><div class="lesson-list">${module.lessons.map((i, n) => lessonLink(content.lessons[i], n)).join("")}</div>${source()}`;
  } else if (lesson) {
    const m = content.modules.find((m) =>
      m.lessons.some((i) => content.lessons[i].id === lesson.id),
    );
    const pos = m.lessons.findIndex((i) => content.lessons[i].id === id);
    const next = m.lessons[pos + 1];
    const previous = m.lessons[pos - 1];
    html = `<a class="back" href="#${m.id}">← ${m.title}</a><div class="eyebrow" style="margin-top:35px">LESSON ${pos + 1} OF ${m.lessons.length} · ${m.title.toUpperCase()}</div><h1>${lesson.title}</h1><p class="intro">${escapeHTML(lesson.subtitle)}</p>${lessonVisuals(lesson)}<h2 class="visual-section-title">Explore each part & concept</h2>${visualNotes(lesson)}${source(lesson.page)}<div class="reader-bottom">${previous !== undefined ? `<a class="button previous-lesson" href="#${content.lessons[previous].id}">← Previous lesson</a>` : ""}<a class="button primary" href="#quiz">Check your understanding →</a><a class="button" href="#${next !== undefined ? content.lessons[next].id : m.id}">${next !== undefined ? "Next lesson" : "Back to module"} →</a></div>`;
  } else if (id === "glossary") {
    html = `<a class="back" href="#home">← Back to the manual</a><h1>The trucking glossary.</h1><p class="intro">51 essential terms. Plain English. A shared language for better coordination.</p><label class="search glossary-search"><span>⌕</span><input type="search" id="glossary-search" placeholder="Search a term or definition…" aria-label="Search glossary"></label><p id="gloss-count" aria-live="polite"></p><dl class="glossary-grid" id="glossary-grid"></dl>${source("20–22")}`;
  } else if (id === "quiz") {
    questionIndex = 0;
    score = 0;
    html = `<a class="back" href="#home">← Back to the manual</a><h1>Make the right next call.</h1><p class="intro">Five quick scenarios to put your knowledge to work. This is learning practice; answers and results are never saved.</p><div id="quiz-content"></div>`;
  } else if (id === "sources") {
    html = `<a class="back" href="#home">← Back to the manual</a><h1>A field guide for learning.</h1><p class="intro">Built for the people who keep equipment, drivers, and operations connected.</p><h2>What’s in the manual</h2><p>Eight modules, 18 lessons, and 51 glossary terms adapted from the user-supplied 23-page Fleet_MC_Training.pdf. Reading times are estimates. Content focuses on recognition, communication, documentation, and escalation.</p><h2>Source review & imagery</h2><p>The supplied PDF’s text was reviewed in full. Its embedded images are illustrative and may contain inaccurate labels. Each lesson includes the original PDF artwork and individual original vector concept illustrations. These explain relationships and coordinator workflows; they are not mechanical service drawings. The original PDF images are low resolution and are presented unchanged with source captions. Reuse rights outside this project have not been independently confirmed. The two other PDFs named in the Markdown briefs were not supplied.</p><h2>Reference starting points</h2><p>These official resources are provided for further checking; this site does not claim that its content was independently validated against current rules.</p><div class="lesson-list"><a class="lesson-link" href="https://www.fmcsa.dot.gov/" target="_blank" rel="noopener noreferrer">FMCSA — Motor carrier safety →</a><a class="lesson-link" href="https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-396" target="_blank" rel="noopener noreferrer">49 CFR Part 396 — Inspection, repair, and maintenance →</a><a class="lesson-link" href="https://www.cvsa.org/" target="_blank" rel="noopener noreferrer">CVSA — Commercial vehicle inspection resources →</a></div><h2>Your privacy</h2><p>No accounts, databases, cookies, analytics, or local storage. Search and practice state exist only while the page is open. Fonts and images are served from this site; the interface does not require third-party font services.</p>${source()}`;
  } else {
    html =
      '<h1>Topic not found.</h1><p>The link may have changed.</p><a class="button primary" href="#modules">Browse the manual →</a>';
  }
  home.hidden = true;
  reader.hidden = false;
  reader.innerHTML = html;
  document.title = `${module?.title || lesson?.title || { glossary: "Glossary", quiz: "Practice", sources: "About & sources" }[id] || "Topic not found"} — Fleet MC Training`;
  window.scrollTo(0, 0);
  reader.focus({ preventScroll: true });
  enhanceImages(reader);
  if (id === "glossary") {
    renderGlossary("");
    $("#glossary-search").addEventListener("input", (e) =>
      renderGlossary(e.target.value),
    );
  }
  if (id === "quiz") renderQuestion();
}
function renderGlossary(q) {
  const list = content.glossary.filter((x) =>
    `${x.term} ${x.definition}`.toLowerCase().includes(q.toLowerCase()),
  );
  $("#gloss-count").textContent = `${list.length} terms`;
  $("#glossary-grid").innerHTML = list.length
    ? list
        .map(
          (x) =>
            `<div class="glossary-term"><dt>${escapeHTML(x.term)}</dt><dd>${visualButton(x.image, x.alt)}<p>${escapeHTML(x.definition)}</p></dd></div>`,
        )
        .join("")
    : "<p>No matching terms. Try another keyword.</p>";
}
function renderQuestion() {
  const panel = $("#quiz-content");
  if (questionIndex >= questions.length) {
    panel.innerHTML = `<div class="quiz-panel"><div class="eyebrow">PRACTICE COMPLETE</div><h2>${score} of ${questions.length} correct</h2><p>Every clear report starts with observation, documentation, and appropriate escalation. Revisit the modules whenever you need a refresher.</p><button class="button primary" id="restart">Practice again ↻</button> <a class="button" href="#modules">Explore the modules →</a></div>`;
    $("#restart").onclick = () => {
      score = 0;
      questionIndex = 0;
      renderQuestion();
    };
    return;
  }
  const q = questions[questionIndex];
  panel.innerHTML = `<div class="quiz-panel"><div class="eyebrow">QUESTION ${questionIndex + 1} / ${questions.length}</div><h2>${q.q}</h2><div class="quiz-visual">${visualButton(content.lessons.find((l) => l.id === q.lesson).visualNotes[0].image, content.lessons.find((l) => l.id === q.lesson).visualNotes[0].alt)}</div><div class="answers">${q.a.map((a, i) => `<button class="answer" data-answer="${i}">${a}</button>`).join("")}</div><div class="feedback" aria-live="polite"></div></div>`;
  panel.querySelectorAll("[data-answer]").forEach(
    (b) =>
      (b.onclick = () => {
        const selected = Number(b.dataset.answer);
        if (selected === q.correct) score++;
        panel.querySelectorAll("[data-answer]").forEach((x) => {
          x.disabled = true;
          if (Number(x.dataset.answer) === q.correct)
            x.classList.add("correct");
        });
        if (selected !== q.correct) b.classList.add("incorrect");
        $(".feedback").innerHTML =
          `<strong>${selected === q.correct ? "That’s right." : "A useful learning moment."}</strong><p>${q.why}</p><a class="text-link" href="#${q.lesson}">Review the lesson →</a><p><button class="button primary" id="next-question">${questionIndex === questions.length - 1 ? "See results" : "Next question"} →</button></p>`;
        $("#next-question").onclick = () => {
          questionIndex++;
          renderQuestion();
        };
      }),
  );
}
async function loadManual() {
  try {
    const response = await fetch(assetURL("data/content.json?v=4"), {
      cache: "no-cache",
    });
    if (!response.ok) throw new Error("Content unavailable");
    content = await response.json();
    cards();
    route();
    $("#loading-state").hidden = true;
  } catch (error) {
    $("#loading-state").hidden = false;
    $("#loading-state").innerHTML =
      '<h2>The manual could not load</h2><p>Check your connection and try again.</p><button class="button primary" id="retry-content">Try again</button>';
    $("#retry-content").onclick = loadManual;
  }
}
setupVisualViewer();
document.querySelector(".skip").addEventListener("click", (e) => {
  e.preventDefault();
  const target = $("#reader").hidden ? $("#main") : $("#reader");
  target.focus({ preventScroll: true });
  target.scrollIntoView({ behavior: "instant" });
});
window.addEventListener("hashchange", () => {
  if (content) route();
});
$("#module-search").addEventListener("input", (e) => {
  query = e.target.value.trim().toLowerCase();
  if (content) cards();
});
document.querySelectorAll("[data-filter]").forEach(
  (b) =>
    (b.onclick = () => {
      category = b.dataset.filter;
      document.querySelectorAll("[data-filter]").forEach((x) => {
        x.classList.toggle("active", x === b);
        x.setAttribute("aria-pressed", String(x === b));
      });
      if (content) cards();
    }),
);
document.addEventListener("keydown", (e) => {
  if (
    e.key === "/" &&
    !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) &&
    !document.querySelector("dialog[open]")
  ) {
    e.preventDefault();
    if ($("#home").hidden) location.hash = "modules";
    requestAnimationFrame(() => {
      $("#module-search").focus();
      $("#modules").scrollIntoView();
    });
  }
});
enhanceImages();
loadManual();
