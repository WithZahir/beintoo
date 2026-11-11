# BEINTOX website

Static site. No framework, no dependencies.

- Edit content (services, case studies, FAQ, contact details) in `build.py` → run `python3 build.py` → all `*.html` pages regenerate.
- Styles: `assets/css/style.css` (design tokens at the top). Script: `assets/js/site.js` (mobile menu, lightbox, contact form).
- Images: `assets/img/<client>/` as WebP, extracted from the 2026 portfolio PDF.
- Deploy: push this folder to Vercel (`vercel.json` enables clean URLs). `build.py` is excluded via `.vercelignore`.
