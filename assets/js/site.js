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

  /* Reveal cards once as they scroll in, and count numbers up from 0 */
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const reveals = $$(".rv"), counters = $$("[data-count]");
  const count = (el) => {
    const end = +el.dataset.count, t0 = performance.now(), dur = 1800;
    const tick = (now) => {
      const p = Math.min((now - t0) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 4)));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if (still || !("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("in"));
  } else {
    counters.forEach((el) => (el.textContent = "0"));
    const io = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      if (e.target.matches("[data-count]")) count(e.target); else e.target.classList.add("in");
    }), { threshold: 0.2 });
    reveals.forEach((el) => io.observe(el));
    counters.forEach((el) => io.observe(el));
  }

  /* 3D tilt + moving light on [data-tilt] (founder portrait) */
  if (!still && matchMedia("(hover: hover)").matches) {
    $$("[data-tilt]").forEach((el) => {
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        el.classList.add("is-tilting");
        el.style.setProperty("--ry", `${(x - 0.5) * 12}deg`);
        el.style.setProperty("--rx", `${(0.5 - y) * 12}deg`);
        el.style.setProperty("--mx", `${x * 100}%`);
        el.style.setProperty("--my", `${y * 100}%`);
      });
      el.addEventListener("pointerleave", () => {
        el.classList.remove("is-tilting");
        el.style.setProperty("--rx", "0deg"); el.style.setProperty("--ry", "0deg");
      });
    });
  }

  const y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
