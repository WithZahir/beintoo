/* BEINTOX — site runtime. Progressive enhancement only; every page works without JS. */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* Mobile nav */
  const nav = $(".nav"), toggle = $(".nav__toggle");
  if (nav && toggle) {
    const set = (open) => { nav.classList.toggle("is-open", open); toggle.setAttribute("aria-expanded", String(open)); };
    toggle.addEventListener("click", () => set(!nav.classList.contains("is-open")));
    addEventListener("keydown", (e) => e.key === "Escape" && set(false));
    $$(".nav__links a").forEach((a) => a.addEventListener("click", () => set(false)));
  }

  /* Lightbox: any [data-lb] link inside a [data-lb-group] container */
  const lb = $("#lb");
  if (lb && typeof lb.showModal === "function") {
    const img = $("img", lb), cap = $("span", lb);
    let list = [], i = 0;
    const show = (n) => {
      i = (n + list.length) % list.length;
      const a = list[i], thumb = $("img", a);
      img.src = a.href; img.alt = thumb ? thumb.alt : "";
      cap.textContent = `${a.dataset.lb || img.alt}  ·  ${i + 1} / ${list.length}`;
    };
    document.addEventListener("click", (e) => {
      const a = e.target.closest("a[data-lb]");
      if (!a || e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      list = $$("a[data-lb]", a.closest("[data-lb-group]") || document);
      show(list.indexOf(a)); lb.showModal();
    });
    $("[data-prev]", lb).addEventListener("click", () => show(i - 1));
    $("[data-next]", lb).addEventListener("click", () => show(i + 1));
    $("[data-close]", lb).addEventListener("click", () => lb.close());
    lb.addEventListener("click", (e) => e.target === lb && lb.close());
    lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") show(i - 1); if (e.key === "ArrowRight") show(i + 1); });
    lb.addEventListener("close", () => img.removeAttribute("src"));
  }

  /* Contact form → WhatsApp or email with the brief pre-filled (no backend required) */
  const form = $("#brief");
  if (form) {
    const compose = () => {
      const d = new FormData(form);
      const services = d.getAll("services").join(", ") || "Not sure yet";
      return [
        `Hi BEINTOX, I'd like to discuss a project.`, ``,
        `Name: ${d.get("name")}`,
        `Business: ${d.get("business") || "-"}`,
        `Contact: ${d.get("contact")}`,
        `Interested in: ${services}`,
        `Timeline: ${d.get("timeline")}`, ``,
        `${d.get("message") || ""}`,
      ].join("\n").trim();
    };
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const via = e.submitter && e.submitter.value === "email" ? "email" : "whatsapp";
      const text = compose();
      const url = via === "email"
        ? `mailto:${form.dataset.email}?subject=${encodeURIComponent("Project enquiry — " + (new FormData(form).get("business") || new FormData(form).get("name")))}&body=${encodeURIComponent(text)}`
        : `https://wa.me/${form.dataset.wa}?text=${encodeURIComponent(text)}`;
      if (via === "email") location.href = url; else window.open(url, "_blank", "noopener");
    });
  }

  const y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
