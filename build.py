#!/usr/bin/env python3
"""
BEINTOX static site generator.

    python3 build.py

Writes every *.html page in this folder from the content + templates below.
Pure standard library: no dependencies, no build step on the host.
Edit content in the DATA section, re-run, deploy the folder as-is.
"""
from __future__ import annotations

import html
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "assets" / "img"
VERSION = "10"  # bump to bust CSS/JS caches

# =====================================================================
# DATA
# =====================================================================

CONTACT = {
    "email": "info@beintox.com",
    "phone": "+92 308 4762273",
    "tel": "+923084762273",
    "wa": "923084762273",
    "ig": "beintox",
}

NAV = [("index", "Home"), ("services", "Services"), ("portfolio", "Portfolio"), ("case-studies", "Case Studies"), ("about", "About"), ("contact", "Contact")]

SERVICES = [
    # (id, title, short, long, deliverables, case-slug or None)
    ("identity", "Brand Identity & Logo Design", "Logos, colour systems, typography and brand guidelines.",
     "A complete identity system that works everywhere your brand appears, from a social avatar to a storefront sign. Every decision is documented, so your team and suppliers apply it the same way every time.",
     ["Logo suite & variations", "Colour palette", "Typography system", "Brand guidelines book", "Mascot & illustration", "Stationery"], "khyber-sajji"),
    ("strategy", "Brand Strategy & Consulting", "Positioning, audience research and growth plans.",
     "Before design comes clarity: who you serve, what you stand for and why customers should choose you. We turn that into positioning and a message every channel can repeat.",
     ["Market & competitor review", "Audience definition", "Positioning & messaging", "Personality & tone of voice", "Growth roadmap"], "twenty-two"),
    ("packaging", "Packaging Design", "Shelf-ready packaging that sells the product.",
     "Packaging that protects, presents and sells. Designed with dielines and print production in mind, not just a render.",
     ["Structure & dielines", "Surface graphics", "Bags, boxes & wraps", "Print-ready artwork"], "shehar-e-lazzat"),
    ("registration", "Brand Registration (IPO)", "Trademark registration and legal guidance for your brand.",
     "Protect the name and mark you've invested in. We guide you through trademark search and filing, so your brand is legally yours.",
     ["Trademark availability search", "Class selection guidance", "Filing support", "Documentation & follow-up"], None),
    ("social", "Social Media Marketing", "Content planning, creatives and community growth.",
     "A consistent, recognisable feed planned month by month: campaign ideas, post design, captions and community management that keep your audience coming back.",
     ["Monthly content calendar", "Post & story design", "Captions & copywriting", "Launch & teaser campaigns", "Community management"], "khyber-sajji"),
    ("design", "Creative & Graphic Design", "Posts, campaigns, brochures and print material.",
     "Campaign visuals and print material that look like they belong to one brand: menus, brochures, billboards and everything in between.",
     ["Campaign key visuals", "Menus & brochures", "Billboards & signage", "Print production files"], "tomgai"),
    ("photo", "Photography & Videography", "Product, brand and corporate shoots.",
     "Imagery that makes the product the hero. Food, product and brand shoots planned around how the content will actually be used.",
     ["Product & food photography", "Brand lifestyle shoots", "Corporate shoots", "Retouching & grading"], "khyber-sajji"),
    ("video", "Reels & Video Editing", "Short-form videos, motion graphics and promos.",
     "Short-form video built for the feed: hooks in the first second, on-brand motion graphics and edits sized for every platform.",
     ["Reels & short-form", "Motion graphics", "Promo videos", "Editing & colour"], None),
    ("ads", "Digital Advertising", "Paid campaigns on Meta, Google and more.",
     "Paid media planned around one clear goal, whether that's footfall, orders or leads. We build the creative, set up targeting and report on what's working.",
     ["Campaign strategy", "Ad creatives", "Audience targeting", "Tracking setup", "Performance reports"], None),
    ("web", "Website Design & Development", "Modern, fast, conversion-focused websites.",
     "Websites that load fast, read clearly and turn visitors into customers, designed in your brand system and built to be easy to update.",
     ["UX & interface design", "Responsive development", "Menus & online ordering", "SEO foundations", "Launch & handover"], "khyber-sajji"),
    ("audit", "Marketing Audit", "A clear review of what's working and what isn't.",
     "An honest look at your brand, content and ads, with a prioritised list of what to fix first and what to stop doing.",
     ["Brand consistency review", "Social & ads review", "Competitor benchmark", "Prioritised action plan"], None),
]
GROUPS = [("Brand", "Foundations", ["identity", "strategy", "packaging", "registration"]),
          ("Content", "Creative & content", ["social", "design", "photo", "video"]),
          ("Growth", "Growth & digital", ["ads", "web", "audit"])]

# Case studies. Image paths are relative to assets/img.
CASES = [
    {
        "slug": "tomgai", "brief": "Create a warm, memorable identity for a new Chinese & Thai kitchen, and carry it consistently from launch billboards to takeaway bags and table service.", "services": ["identity", "design", "social", "packaging", "photo"], "name": "Tomgai Chinese", "sector": "Restaurant · Chinese & Thai", "brand": "#8f1a1e",
        "tags": ["Brand identity", "Mascot", "Social media", "Packaging", "Launch campaign"],
        "summary": "A warm, modern identity for a Chinese & Thai kitchen. A bamboo-stroke wordmark, a cheerful chef mascot and a red-and-cream system that runs from chopstick sleeves to billboards.",
        "cover": "tomgai/app-chefs", "hero": "tomgai/app-chefs", "logo": "logos/tomgai.png",
        "story": [
            "Tomgai is a fusion of warmth and tradition, inspired by the comforting essence of Asian cuisine. The name blends “Tom”, a nod to beloved soups like Tom Yum, with “Gai”, the Cantonese word for chicken: nourishment and heart in one word.",
            "Bold black typography spells the name, while a vertical red bamboo stroke replaces the “I”. It's a symbol of resilience and harmony that gives the mark its Chinese roots without leaning on cliché. The mascot is a cheerful chef holding a steaming bowl, dressed in traditional red with a branded hat.",
        ],
        "facts": [("Client", "Tomgai Chinese"), ("Sector", "Restaurant"), ("Scope", "Identity, content, packaging"), ("Deliverables", "Guidelines, mascot, 9+ applications")],
        "palette": [("#9e1c20", "#9E1C20"), ("#f9e1bb", "#F9E1BB"), ("#282725", "#282725"), ("#ffffff", "#FFFFFF")],
        "fonts": None,
        "sections": [
            ("identity", "Brand identity", "A guideline book that covers <em>every touchpoint.</em>", "Logo construction, meaning, usage rules, colour, type, pattern and character, documented so every supplier gets it right.",
             "gallery", ["bb-cover:Guidelines cover", "bb-logo-variations:Logo on colour", "bb-meaning:Name & meaning", "bb-logo-description:Logo description", "bb-logo-donts:Logo misuse", "bb-fonts:Brand fonts", "bb-palette:Colour palette", "bb-character:The Tomgai chef", "bb-pattern:Brand pattern"]),
            ("social", "Social media", "A feed that <em>tastes</em> like the menu.", "Dark, cinematic food photography with editorial type, built to stop the scroll and make the menu the hero.",
             "posts", ["post-dumplings:Chicken dumplings", "post-drink:Complimentary drink", "post-hotpot:Signature hot pot", "post-soup:19B soup", "post-legacy:The legacy of taste and love", "post-drumstick:Chicken drumstick"]),
            ("applications", "Applications", "From billboard to <em>chopstick sleeve.</em>", "The system applied across launch media, packaging, uniforms and table service.",
             "gallery", ["app-billboard-1:Launch billboard", "app-billboard-2:Launch billboard — dish", "pk-bag:Takeaway bag — “Wok your world”", "pk-chopsticks:Chopstick sleeves", "app-napkins:Napkins", "bb-business-card:Business cards", "bb-letterhead:Letterhead", "app-uniform:Chef uniform", "app-comment-card:Comment card", "app-table:Table setting", "app-hotpot:Hot pot detail", "bb-social:Teaser posts"]),
        ],
    },
    {
        "slug": "twenty-two", "brief": "Build one brand that serves two cravings, burgers and pizza, and make it instantly recognisable on every box, cup and post.", "services": ["strategy", "identity", "packaging", "social"], "name": "Twenty Two", "sector": "Fast food · Burgers & pizza", "brand": "#4b111f",
        "tags": ["Brand strategy", "Brand identity", "Guidelines", "Packaging", "Social media"],
        "summary": "Two shapes. One identity. A bold “22” monogram in orange and maroon for a burger-and-pizza brand, built into a full guideline book, a packaging range and a launch feed.",
        "cover": "twentytwo/pk-range", "hero": "twentytwo/pk-range", "logo": "logos/twentytwo.png",
        "story": [
            "Twenty Two serves two cravings under one roof. The identity turns that into a mark: two interlocking 2s, one in warm orange and one in deep maroon, standing for duality, partnership and balance.",
            "The positioning (“One craving. Two choices.”) runs through everything, from the guideline book's core values of Quality, Balance and Character to a packaging range that alternates the two colours piece by piece.",
        ],
        "facts": [("Client", "Twenty Two"), ("Sector", "Fast food"), ("Scope", "Strategy, identity, packaging, social"), ("Deliverables", "12-page guidelines, packaging range")],
        "palette": [("#4b111f", "Maroon"), ("#f0871f", "Orange"), ("#231f20", "Charcoal"), ("#f5ede4", "Warm white")],
        "fonts": ("Poppins", "Playfair Display"),
        "sections": [
            ("identity", "Brand identity", "Two shapes. One identity. <em>Endless balance.</em>", "A 12-page guideline book: story, logo system, clear space, colour, typography, backgrounds, misuse and applications.",
             "gallery", ["bb-cover:Guidelines cover", "bb-story:Our story", "bb-logo-overview:Logo overview", "bb-logo-variations:Logo variations", "bb-clear-space:Clear space & minimum size", "bb-palette:Colour palette", "bb-typography:Typography", "bb-backgrounds:Logo on backgrounds", "bb-misuse:Logo misuse", "bb-applications:Brand applications", "bb-contents:Contents", "bb-thanks:Closing page"]),
            ("packaging", "Packaging", "A range that reads as <em>one brand.</em>", "Bags, fry cartons, burger box, bucket, cups and dip lids, alternating orange and maroon so every piece is recognisable on its own.",
             "gallery2", ["pk-range:Full packaging range", "pk-delivery:Delivery bag & cooler"]),
            ("social", "Social media", "Launch content with <em>appetite.</em>", "A teaser-to-launch feed: bold serif headlines, product close-ups and the monogram as a graphic device.",
             "posts", ["post-coming:Something big is coming", "post-crunch:Crunch time", "post-pull-up:Pull up", "post-choices:One craving, two choices", "post-twice:Twice as good", "post-double:Double the flavor", "post-made-fresh:Made fresh, made right", "post-stay-cool:Stay cool", "post-double-2:Double smash burger"]),
        ],
    },
    {
        "slug": "khyber-sajji", "brief": "Introduce a traditional Khyber sajji brand to Lahore with a character people remember, and build anticipation before the doors opened.", "services": ["identity", "social", "design", "web", "photo"], "name": "Khyber Sajji", "sector": "Restaurant · Traditional sajji", "brand": "#a82c17",
        "tags": ["Brand identity", "Mascot & illustration", "Launch campaign", "Website & app", "Photography"],
        "summary": "A bold, friendly identity for Khyber-style roasted chicken: a mascot in a Peshawari cap, Urdu-first lettering and a teaser campaign that built anticipation in Lahore before the doors opened.",
        "cover": "khyber/app-storefront", "hero": "khyber/app-storefront", "logo": "logos/khyber.png",
        "story": [
            "Khyber Sajji brings the rich taste and traditional spirit of Khyber cuisine into a memorable, modern food experience. The mission is simple: flavourful, authentic roasted chicken with quality ingredients and consistent taste.",
            "The personality is bold, traditional, friendly, energetic and welcoming, so the brand got a character to match. Warm orange and deep red stand for fire, spice and appetite, and decorative display lettering is inspired by traditional South Asian signage.",
        ],
        "facts": [("Client", "Khyber Sajji"), ("Sector", "Restaurant"), ("Scope", "Identity, campaign, digital, photo"), ("Values", "Quality · Authenticity · Taste · Freshness · Hospitality")],
        "palette": [("#e8601c", "Warm orange"), ("#a82c17", "Deep red"), ("#f6b81c", "Golden yellow"), ("#6b3f22", "Dark brown"), ("#f4ead6", "Cream")],
        "fonts": ("BN Tillman", "Poppins"),
        "sections": [
            ("identity", "Brand identity", "A character people <em>remember.</em>", "Mascot, logo system, variations, colour, pattern, icon set and an illustration library for every occasion.",
             "gallery", ["bb-cover:Guidelines cover", "bb-mascot:Logo & mascot description", "bb-logo-guidelines:Logo guidelines", "bb-variations:Variations", "bb-palette:The colours", "bb-pattern:Brand pattern", "bb-icons:Brand icons & elements", "bb-illustrations:Illustrations"]),
            ("social", "Launch campaign", "“Hello Jii.” <em>Coming soon.</em>", "An Urdu-first teaser campaign for the Lahore launch: the mascot peeks through doors, curtains and newspapers until the reveal.",
             "posts", ["post-door:The door hanger", "post-curtain:Behind the curtain", "post-tension:Tension bhagao", "post-lahore:Lahore", "post-hello-jii:Hello Jii, coming soon", "post-newspaper:Something new for Lahore"]),
            ("applications", "Applications", "Storefront, fleet and <em>uniform.</em>", "The identity at full scale: signage, delivery vehicles, stationery and staff wear.",
             "gallery", ["app-storefront:Storefront", "app-van:Delivery van", "app-uniforms:Uniforms & merchandise", "app-stationery:Stationery set", "app-letterhead:Letterhead", "app-business-card:Business card"]),
            ("digital", "Website & app", "Ordering that looks like <em>the brand.</em>", "A website and mobile ordering flow designed in the brand system, from menu to checkout to order tracking.",
             "gallery", ["app-website:Website", "app-web-app:Website & app screens", "app-mobile:Mobile ordering flow"]),
            ("photo", "Photography", "Fire, smoke and <em>slow roast.</em>", "Food photography direction that shows the craft behind the dish.",
             "gallery4", ["photo-cooking:Preparation", "photo-roast:Signature sajji", "photo-grill:On the fire", "photo-chicken:Plated"]),
        ],
    },
    {
        "slug": "shehar-e-lazzat", "brief": "Give a modern bakery a premium identity rooted in tradition, one that works from the café counter to a gift box.", "services": ["identity", "packaging", "social", "design"], "name": "Shehar-e-Lazzat", "sector": "Bakery & café", "brand": "#13203a",
        "tags": ["Brand identity", "Packaging", "Stationery", "Social media"],
        "summary": "The City of Taste. A navy-and-gold identity for a modern bakery rooted in tradition: a croissant-crown logo, jar desserts, gift boxes and a feed that sells every bake.",
        "cover": "shehar/app-mockups", "hero": "shehar/app-mockups", "logo": "logos/shehar.png",
        "story": [
            "Shehar-e-Lazzat is a modern bakery inspired by tradition, created to bring people together over the simple joy of great food. The name means “the city of taste”, and the identity is built to feel like a destination.",
            "A croissant shaped like a crown sits above Urdu lettering, set in deep navy and soft gold. The personality is elegant, welcoming, authentic, timeless and refined, carried through Playfair Display headlines and clean Montserrat text.",
        ],
        "facts": [("Client", "Shehar-e-Lazzat"), ("Sector", "Bakery & café"), ("Scope", "Identity, packaging, social"), ("Values", "Quality · Authenticity · Warmth · Community")],
        "palette": [("#13203a", "Royal navy"), ("#c9a75e", "Gold"), ("#f3ead9", "Cream"), ("#8a6a4a", "Warm taupe")],
        "fonts": ("Playfair Display", "Montserrat"),
        "sections": [
            ("identity", "Brand identity", "A taste of <em>tradition.</em>", "Brand overview, logo guidelines, colour, typography, visual language, patterns and stationery.",
             "gallery", ["bb-overview:Brand overview", "bb-logo-guidelines:Logo guidelines", "bb-palette:Colour palette", "bb-typography:Typography", "bb-visual-identity:Visual identity", "bb-type-specimen:Type specimen", "app-stationery:Stationery", "app-patterns:Brand patterns", "app-marketing:Marketing material"]),
            ("packaging", "Packaging", "Gift-ready, <em>shelf-ready.</em>", "A three-jar dessert gift box, a carry box with full dieline, and a cake-slice box, all print-ready.",
             "gallery", ["pk-jar-box:Dessert jar gift box", "pk-dieline:Carry box & dieline", "pk-slice-box:Cake slice box", "app-mockups:Brand mockups"]),
            ("social", "Social media", "Every bake, <em>a moment.</em>", "Deep navy backdrops, warm light and handwritten script, a feed that feels like walking into the café.",
             "posts", ["post-golden-layers:Golden layers of happiness", "post-flavor-burst:Flavor burst", "post-cookies:Best cookies around", "post-sundae:Sundae delight", "post-croissant-box:Croissant box", "post-donuts:The most delicious donuts", "post-sweet-beginning:A sweet beginning"]),
        ],
    },
]
CASE = {c["slug"]: c for c in CASES}

FAQ = [
    ("How long does a brand identity project take?", "Most identity projects take 3–6 weeks, depending on scope and how quickly feedback comes back. You'll get a timeline with clear milestones before any work starts."),
    ("Do you work with new and small businesses?", "Yes. Several of the brands in our portfolio were built from scratch before opening, including their name story, identity, packaging and launch campaign."),
    ("Can I hire you for a single service?", "Yes. Every service is available on its own: a logo, a packaging range, a month of social content or a website. Combine them when it makes sense."),
    ("What do I receive at the end of an identity project?", "Final logo files in every format you need, a brand guidelines document, colour and typography specifications, and the applications agreed in scope, such as stationery, packaging or signage."),
    ("Can you help register our trademark?", "Yes. Our Brand Registration (IPO) service covers availability search, class guidance and filing support so your name and mark are protected."),
    ("How do we get started?", "Send us a short brief through the contact form or WhatsApp. We'll ask a few questions, then come back with a scoped proposal. Proposals are free."),
]

# Instagram profiles shown on the Portfolio page. Profile numbers are taken from the
# client's 2026 portfolio deck; update them here when they change.
IG = {
    "tomgai": {
        "handle": "tomgaichinese", "name": "TOMGAI Chinese", "category": "Chinese restaurant",
        "bio": ["Authentic Thai & Chinese flavors.", "From our kitchen to your cravings. 🍜"], "link": "tomgai.com",
        "posts": "158", "followers": "14.2K", "following": "182",
        "highlights": [("tomgai/post-hotpot", "Menu"), ("tomgai/app-billboard-1", "Launch"), ("tomgai/pk-bag", "Takeaway"), ("tomgai/bb-character", "Chef"), ("tomgai/app-chefs", "Kitchen")],
        "grid": ["post-drumstick:Chicken drumstick", "post-legacy:The legacy of taste and love", "post-soup:19B soup",
                 "post-hotpot:Signature hot pot", "post-drink:Complimentary drink", "post-dumplings:Chicken dumplings",
                 "app-billboard-1:Now open — launch", "pk-bag:Wok your world — takeaway", "app-chefs:The Tomgai kitchen"],
    },
    "twenty-two": {
        "handle": "twentytwo.official", "name": "Twenty Two", "category": "Restaurant",
        "bio": ["Twice the taste in one bite.", "Burgers · Pizza · Fries"], "link": "twentytwo.official",
        "posts": "124", "followers": "12.4K", "following": "153",
        "highlights": [("twentytwo/post-double", "Burgers"), ("twentytwo/post-pull-up", "Pizza"), ("twentytwo/post-crunch", "Sides"), ("twentytwo/pk-delivery", "Delivery"), ("twentytwo/post-coming", "Launch")],
        "grid": ["post-made-fresh:Made fresh, made right", "post-double:Double the flavor", "post-stay-cool:Stay cool",
                 "post-crunch:Crunch time", "post-pull-up:Pull up", "post-choices:One craving, two choices",
                 "post-twice:Twice as good", "post-double-2:Double smash burger", "post-coming:Something big is coming"],
    },
    "khyber-sajji": {
        "handle": "khyber.sajji", "name": "خیبر سجی · Khyber Sajji", "category": "Restaurant",
        "bio": ["Khyber Sajji serves taste from Khyber.", "Lahore 🔥"], "link": "khybersajji.official",
        "posts": "124", "followers": "12.4K", "following": "153",
        "highlights": [("khyber/post-hello-jii", "Coming soon"), ("khyber/photo-roast", "Sajji"), ("khyber/app-storefront", "Store"), ("khyber/app-van", "Delivery"), ("khyber/bb-mascot", "Mascot")],
        "grid": ["post-newspaper:Lahore, something new is coming", "post-door:The door hanger", "post-curtain:Behind the curtain",
                 "post-lahore:Lahore", "post-tension:Tension bhagao", "post-hello-jii:Hello Jii, coming soon",
                 "photo-roast:Signature sajji", "app-storefront:The storefront", "photo-grill:On the fire"],
    },
    "shehar-e-lazzat": {
        "handle": "shehar_e_lazzat", "name": "Shehar_e_Lazzat | Bakery & Cafe", "category": "Bakery",
        "bio": ["The ultimate baking experience 🥐✨", "The City of Taste"], "link": "Order now",
        "posts": "263", "followers": "1.7K", "following": "219",
        "highlights": [("shehar/post-golden-layers", "Café"), ("shehar/post-sundae", "Desserts"), ("shehar/post-cookies", "Cookies"), ("shehar/pk-jar-box", "Gifting"), ("shehar/app-mockups", "Brand")],
        "grid": ["post-golden-layers:Golden layers of happiness", "post-flavor-burst:Flavor burst", "post-cookies:Best cookies around",
                 "post-sundae:Sundae delight", "post-croissant-box:Croissant box", "post-donuts:The most delicious donuts",
                 "post-sweet-beginning:A sweet beginning", "pk-jar-box:Dessert jar gift box", "pk-slice-box:Cake slice box"],
    },
}

# Image shown beside each service on the Services page: one image, or three posts as a strip.
SVC_IMG = {
    "identity": "khyber/bb-cover",
    "strategy": "twentytwo/bb-story",
    "packaging": "shehar/pk-jar-box",
    "registration": "tomgai/bb-logo-variations",
    "social": "khyber/post-curtain",
    "design": "tomgai/app-billboard-1",
    "photo": "khyber/photo-roast",
    "video": "tomgai/app-hotpot",
    "ads": "twentytwo/post-double",
    "web": "khyber/app-website",
    "audit": "twentytwo/bb-contents",
}

STEPS = [("Discover", "We study your business, audience and competitors to find what makes you worth choosing."),
         ("Define", "Positioning, personality and message: the strategy every design decision answers to."),
         ("Design", "Identity, content and campaigns crafted with one look, one voice and one feeling."),
         ("Grow", "We launch, measure and refine, turning attention into lasting customer relationships.")]

WHY = [("One team, every discipline", "Strategy, identity, content, ads and web under one roof, so your brand speaks with one voice everywhere."),
       ("Strategy before pixels", "We define who you're for and why you win before we design anything. Every visual answers to that."),
       ("Systems, not one-offs", "Each identity ships with guidelines, so the brand stays consistent long after launch."),
       ("Bilingual creative", "Urdu and English campaigns written and designed for how your customers actually talk."),
       ("Production-ready", "Dielines, print files, signage and uniforms. We design for the real world, not just the screen."),
       ("Clear process", "Defined scope, milestones and one point of contact. You always know what's next.")]

PLANS = [("Project", "Single project", "One defined deliverable with a fixed scope and timeline.", ["Logo or identity refresh", "Packaging range", "Website", "Campaign creatives"], False),
         ("For new brands", "Brand launch", "Everything a new business needs to open strong, from name story to first posts.", ["Strategy & positioning", "Full identity + guidelines", "Packaging & stationery", "Launch campaign & social setup"], True),
         ("Ongoing", "Monthly retainer", "A dedicated team running your content and ads month after month.", ["Monthly content calendar", "Post, story & reel design", "Paid ads management", "Monthly performance report"], False)]

# Team (from the client's previous website). photo=None renders initials until a real photo is supplied.
FOUNDER = ("Ali Imtiaz", "CEO & Founder", "team/ali", "Leading BEINTOX with a vision to redefine branding and marketing standards.")
TEAM = [("Arslan Khizar", "Lead Designer", "team/arslan"),
        ("Farhan Ali", "Graphic Designer, Branding", "team/farhan"),
        ("Fahad", "Videographer", "team/fahad"),
        ("Memona Muneer", "Full Stack Web Developer", None)]

# =====================================================================
# HELPERS
# =====================================================================

E = html.escape


def img_size(path: Path) -> tuple[int, int]:
    """Read pixel dimensions of a WebP/PNG without third-party libraries."""
    b = path.read_bytes()[:40]
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", b[16:24])
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        kind = b[12:16]
        if kind == b"VP8X":
            return (int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1)
        if kind == b"VP8 ":
            w, h = struct.unpack("<HH", b[26:30])
            return (w & 0x3FFF, h & 0x3FFF)
        if kind == b"VP8L":
            v = int.from_bytes(b[21:25], "little")
            return ((v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1)
    raise ValueError(f"Unsupported image: {path}")


def src(rel: str) -> str:
    return rel if "." in rel.rsplit("/", 1)[-1] else rel + ".webp"


def img(rel: str, alt: str, eager: bool = False, cls: str = "") -> str:
    path = src(rel)
    w, h = img_size(IMG / path)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="assets/img/{path}" alt="{E(alt)}" width="{w}" height="{h}" {load} decoding="async"{c}>'


def href(page: str) -> str:
    return f"{page}.html"


ICON = {
    "arrow": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "check": '<svg viewBox="0 0 18 18" fill="none" aria-hidden="true"><circle cx="9" cy="9" r="8.25" stroke="currentColor" stroke-opacity=".35"/><path d="M5.5 9.2l2.2 2.2 4.8-4.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "menu": '<svg viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M2 5h14M2 9h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    "close": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    "prev": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "next": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "mail": '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="2.5" y="4.5" width="15" height="11" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M3 5.5l7 5 7-5" stroke="currentColor" stroke-width="1.5"/></svg>',
    "phone": '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M5 2.8h2.6l1.3 3.4-1.7 1.1a9.5 9.5 0 0 0 5.5 5.5l1.1-1.7 3.4 1.3V15a2.2 2.2 0 0 1-2.2 2.2A13.2 13.2 0 0 1 2.8 5 2.2 2.2 0 0 1 5 2.8Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>',
    "ig": '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="2.75" y="2.75" width="14.5" height="14.5" rx="4" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="10" r="3.4" stroke="currentColor" stroke-width="1.5"/><circle cx="14.4" cy="5.6" r=".9" fill="currentColor"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.2-.2-.5-.3Z"/></svg>',
}
ARROW = ICON["arrow"]

# BEINTOX wordmark — letter paths traced from the brand PDF; X redrawn as vector with the brand gold.
LOGO_PATHS = (
    "M87.84 76.57C86.23 76.99 84.54 77.25 82.88 77.25C64.01 77.3 45.14 77.29 26.27 77.29C25.73 77.29 25.19 77.18 24.34 77.08L24.34 59.9C25.91 59.9 27.26 59.9 28.61 59.9C46.09 59.89 63.56 59.86 81.04 59.9C83.25 59.91 85.51 60.15 87.67 60.62C91.83 61.54 93.62 64.47 93.72 68.55C93.83 72.71 91.94 75.52 87.84 76.57M107.12 50.43C106.96 50.33 106.96 49.96 106.84 49.58C107.18 49.25 107.56 48.86 107.96 48.5C123.17 35.01 119.78 12.41 100.94 4.82C95.02 2.43 88.18 1.47 81.74 1.38C55.86 1.01 29.97 1.23 4.08 1.24C2.85 1.24 1.62 1.37 .23 1.44L.23 22.39C1.58 22.46 2.54 22.56 3.51 22.56C27.99 22.52 52.48 22.45 76.97 22.46C80.16 22.46 83.41 22.63 86.55 23.2C90.55 23.93 92.46 26.76 92.4 30.75C92.35 34.71 90.44 37.44 86.4 38.18C84.09 38.6 81.69 38.79 79.33 38.8C54.57 38.86 29.8 38.86 5.03 38.88C3.41 38.88 1.78 38.88 .08 38.88L.08 100.76C1.53 100.85 2.76 100.98 3.98 100.98C30.98 100.99 57.99 101.01 84.99 100.93C88.47 100.92 92.02 100.7 95.41 100C107.05 97.61 115.95 91.79 118.73 79.43C121.47 67.22 117.75 57.4 107.12 50.43Z"
    "M785.91 64.32C783.36 71.67 778.25 76.97 770.45 77.26C754.13 77.86 737.76 77.87 721.44 77.33C713.34 77.05 707.86 71.85 705.28 64.1C702.41 55.48 702.44 46.72 705.09 38.12C707.83 29.22 714.92 24.19 725.14 23.76C731.99 23.47 738.85 23.71 745.71 23.71C752.56 23.7 759.43 23.45 766.27 23.76C777.64 24.28 784.7 30.45 786.98 41.57C788.55 49.22 788.49 56.86 785.91 64.32M812.63 48.09C811.81 21.2 797.61 4.33 771.46 1.73C754.31 .03 736.8 .61 719.54 1.65C705.45 2.51 693.58 9.06 685.86 21.59C678.95 32.8 677.73 45.21 678.72 57.94C680.58 81.75 694.94 97.44 718.55 100.47C727.34 101.6 736.4 100.65 745.34 100.65C745.34 100.75 745.34 100.84 745.34 100.94C753.58 100.94 761.86 101.41 770.07 100.85C791.03 99.41 806.2 87.07 810.75 67.59C812.23 61.28 812.83 54.58 812.63 48.09Z"
    "M481.19 66.45C479.88 65.39 479.11 64.84 478.42 64.21C456.71 44.25 435.01 24.27 413.27 4.34C411.96 3.15 410.39 1.48 408.88 1.42C401.81 1.11 394.72 1.28 387.48 1.28L387.48 100.68L410.51 100.68L410.51 30.58C412.94 32.85 414.64 34.43 416.32 36.03C438.05 56.79 459.77 77.56 481.52 98.3C482.6 99.33 483.93 100.77 485.19 100.82C491.54 101.08 497.91 100.94 504.27 100.94L504.27 1.59L481.19 1.59Z"
    "M542.62 23.15H585.75V100.81H609.78V22.93H652.61V1.53H542.62Z"
    "M159.89 77.56h110.59v23.06H159.89zM160.07 1.44h110.62v21.39H160.07zM314.61 1.47h23.1v99.22h-23.1zM160.05 38.44h93.35v21.6H160.05z"
)
X_PATHS = ("M835.75 99.75H868.25L965.75 1.5H935.75Z", "M838.25 1.5H872L899.5 29.25L880.75 46.5Z", "M905 71.5L923.25 54.25L967 99.75H933.25Z")


def logo(light: bool = False, sub: bool = True) -> str:
    xs = "".join(f'<path d="{d}" fill="url(#bxg)"/>' for d in X_PATHS)
    s = '<small>MARKETING SOLUTIONS</small>' if sub else ""
    return (f'<span class="logo{" logo--light" if light else ""}"><svg viewBox="0 0 968 102" role="img" aria-label="BEINTOX">'
            f'<path d="{LOGO_PATHS}" fill="currentColor"/>{xs}</svg>{s}</span>')


GRAD_DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
             '<linearGradient id="bxg" x1="830" y1="100" x2="968" y2="0" gradientUnits="userSpaceOnUse">'
             '<stop offset="0" stop-color="#8a5a22"/><stop offset=".35" stop-color="#d9a838"/>'
             '<stop offset=".55" stop-color="#f7ec8f"/><stop offset="1" stop-color="#c99a3c"/></linearGradient></defs></svg>')


def checks(items) -> str:
    return '<ul class="checks">' + "".join(f"<li>{ICON['check']}<span>{E(i)}</span></li>" for i in items) + "</ul>"


def head_block(eyebrow: str, title: str, lead: str = "", aside: str = "", h: str = "h2") -> str:
    tag = "h1" if h == "h1" else "h2"
    right = f'<p class="lead">{lead}</p>' if lead else ""
    return (f'<div class="head"><div><span class="eyebrow">{eyebrow}</span><{tag} class="{h}">{title}</{tag}></div>'
            f'<div class="head__aside">{right}{aside}</div></div>')


def cta_band(title="Ready to make your brand <em>unforgettable?</em>",
             lead="Tell us where your brand is today and where you want it to go. We'll reply with a scoped proposal.") -> str:
    return f'''<section class="sec"><div class="wrap"><div class="cta">
  <div><h2 class="h2">{title}</h2><p class="lead">{lead}</p></div>
  <div class="btns"><a class="btn btn--gold" href="contact.html">Request a proposal {ARROW}</a>
  <a class="btn btn--ghost" href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener">WhatsApp us</a></div>
</div></div></section>'''


def svc_by_id(i: str):
    return next(s for s in SERVICES if s[0] == i)


def svc_num(i: str) -> str:
    return f"{[s[0] for s in SERVICES].index(i) + 1:02d}"


# =====================================================================
# LAYOUT
# =====================================================================

def layout(page: str, title: str, desc: str, body: str, schema: dict | None = None) -> str:
    cur = ' aria-current="page"'
    links = "".join(
        f'<li><a href="{href(k)}"{cur if k == page or (page.startswith("case:") and k == "case-studies") else ""}>{l}</a></li>'
        for k, l in NAV)
    base = '<base href="/">\n' if page == "404" else ""
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    case_links = "".join(f'<li><a href="case-study-{c["slug"]}.html">{E(c["name"])}</a></li>' for c in CASES)
    svc_links = "".join(f'<li><a href="services.html#{s[0]}">{E(s[1].split(" &")[0].replace(" (IPO)", ""))}</a></li>' for s in SERVICES[:6])
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
{base}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#0e0d0c">
<meta property="og:type" content="website">
<meta property="og:site_name" content="BEINTOX Marketing Solutions">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@1&family=Montserrat:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/css/style.css?v={VERSION}">
{ld}
</head>
<body>
{GRAD_DEFS}
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <span class="topbar__note">Brand &amp; marketing studio: strategy, branding, design, marketing.</span>
  <ul>
    <li><a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></li>
    <li><a href="tel:{CONTACT["tel"]}">{CONTACT["phone"]}</a></li>
    <li><a href="https://instagram.com/{CONTACT["ig"]}" target="_blank" rel="noopener">Instagram</a></li>
  </ul>
</div></div>
<header class="nav"><div class="wrap">
  <a href="index.html" aria-label="BEINTOX home">{logo()}</a>
  <ul class="nav__links" id="nav-links">{links}</ul>
  <a class="btn btn--dark btn--s nav__cta" href="contact.html">Request a proposal {ARROW}</a>
  <button class="nav__toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav-links">{ICON["menu"]}</button>
</div></header>
<main id="main">
{body}
</main>
<footer class="footer"><div class="wrap">
  <div class="footer__grid">
    <div class="footer__brand">{logo(light=True)}<p>Strategy, branding, design and marketing under one roof. We build brands made to last.</p></div>
    <div><h4>Services</h4><ul>{svc_links}<li><a href="services.html">All services</a></li></ul></div>
    <div><h4>Case studies</h4><ul>{case_links}<li><a href="case-studies.html">All case studies</a></li></ul></div>
    <div><h4>Contact</h4><ul>
      <li><a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a></li>
      <li><a href="tel:{CONTACT["tel"]}">{CONTACT["phone"]}</a></li>
      <li><a href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener">WhatsApp</a></li>
      <li><a href="https://instagram.com/{CONTACT["ig"]}" target="_blank" rel="noopener">@{CONTACT["ig"]}</a></li>
    </ul></div>
  </div>
  <div class="footer__bar"><span>© <span data-year>2026</span> BEINTOX Marketing Solutions</span><span>Being memorable is what makes brands grow.</span></div>
</div></footer>
<a class="wa" href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{ICON["wa"]}</a>
<dialog class="lb" id="lb" aria-label="Image viewer"><img alt=""><div class="lb__bar"><span></span>
  <button type="button" data-prev aria-label="Previous">{ICON["prev"]}</button><button type="button" data-next aria-label="Next">{ICON["next"]}</button><button type="button" data-close aria-label="Close">{ICON["close"]}</button></div></dialog>
<script src="assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
'''


# =====================================================================
# COMPONENTS
# =====================================================================

def case_card(c: dict, eager=False) -> str:
    tags = "".join(f'<span class="tag">{E(t)}</span>' for t in c["tags"][:4])
    return f'''<a class="case" href="case-study-{c["slug"]}.html">
  <div class="case__img">{img(c["cover"], f'{c["name"]} brand work by BEINTOX', eager)}</div>
  <div class="case__body"><h3 class="h3">{E(c["name"])}</h3><span class="case__sector">{E(c["sector"])}</span>
  <p>{E(c["summary"])}</p><div class="tags">{tags}</div></div></a>'''


def svc_card(sid: str, num: bool = True) -> str:
    s = svc_by_id(sid)
    n = f'<span class="card__n">{svc_num(s[0])}</span>' if num else ""
    return f'''<a class="card svc-card" href="services.html#{s[0]}">{n}
  <h3 class="h3">{E(s[1])}</h3><p>{E(s[2])}</p><span class="card__go">Learn more {ARROW}</span></a>'''


def post_grid(items, folder, cls="posts", link_case=None, group=True) -> str:
    out = []
    for it in items:
        key, cap = it.split(":", 1)
        rel = f"{folder}/{key}"
        if link_case:
            out.append(f'<a class="post" href="case-study-{link_case}.html" title="{E(cap)}">{img(rel, cap)}</a>')
        else:
            out.append(f'<a class="post" href="assets/img/{src(rel)}" data-lb="{E(cap)}">{img(rel, cap)}</a>')
    g = " data-lb-group" if group and not link_case else ""
    return f'<div class="{cls}"{g}>' + "".join(out) + "</div>"


def gallery(items, folder, cls="gallery") -> str:
    out = []
    for it in items:
        key, cap = it.split(":", 1)
        rel = f"{folder}/{key}"
        out.append(f'<figure class="shot"><a href="assets/img/{src(rel)}" data-lb="{E(cap)}">{img(rel, cap)}</a><figcaption>{E(cap)}</figcaption></figure>')
    return f'<div class="{cls}" data-lb-group>' + "".join(out) + "</div>"


# =====================================================================
# PAGES
# =====================================================================

def steps_html() -> str:
    return '<div class="steps">' + "".join(
        f'<div class="step"><span class="step__n">{i + 1}</span><h3 class="h3">{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(STEPS)) + "</div>"


def why_html() -> str:
    return '<div class="values values--6">' + "".join(
        f'<div><span class="card__n">{i + 1:02d}</span><h3 class="h3">{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(WHY)) + "</div>"


def plans_html() -> str:
    return '<div class="grid g3">' + "".join(
        f'''<div class="card plan{" plan--featured" if f else ""}"><span class="plan__k">{k}</span><h3 class="h3" style="font-size:21px">{t}</h3><p>{d}</p>{checks(items)}
        <a class="btn {"btn--dark" if f else "btn--line"} btn--s" href="contact.html">Discuss this {ARROW}</a></div>'''
        for k, t, d, items, f in PLANS) + "</div>"


def faq_html() -> str:
    return '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ) + "</div>"


def logo_marquee() -> str:
    one = "".join(f'<a href="portfolio.html#{c["slug"]}" aria-label="{E(c["name"])}">{img(c["logo"], c["name"] + " logo", eager=True)}</a>' for c in CASES)
    half = one * 2
    dup = half.replace("<a ", '<a tabindex="-1" aria-hidden="true" ')
    return f'''<section class="clients" aria-label="Clients"><div class="wrap">
  <span class="clients__label">Brands we've built</span>
  <div class="marquee"><div class="marquee__track">{half}{dup}</div></div>
</div></section>'''


# Hero creative wall: three columns scrolling in alternating directions. Mixed portrait posts and landscape mockups.
WALL = [
    ["tomgai/post-drumstick", "twentytwo/pk-range", "shehar/post-golden-layers", "khyber/post-door", "tomgai/app-billboard-1", "twentytwo/post-crunch"],
    ["twentytwo/post-pull-up", "khyber/app-storefront", "shehar/post-sundae", "tomgai/post-dumplings", "shehar/app-mockups", "khyber/post-hello-jii"],
    ["khyber/post-tension", "shehar/post-cookies", "tomgai/app-chefs", "twentytwo/post-double", "khyber/photo-roast", "shehar/post-donuts", "tomgai/post-legacy"],
]
WALL_BRAND = {"tomgai": ("tomgai", "Tomgai"), "twentytwo": ("twenty-two", "Twenty Two"), "khyber": ("khyber-sajji", "Khyber Sajji"), "shehar": ("shehar-e-lazzat", "Shehar-e-Lazzat")}


def creative_wall() -> str:
    cols = []
    for ci, col in enumerate(WALL):
        def tile(rel: str, first: bool, hidden: bool) -> str:
            slug, name = WALL_BRAND[rel.split("/")[0]]
            attrs = ' tabindex="-1" aria-hidden="true"' if hidden else ""
            return f'<a class="wall__item" href="portfolio.html#{slug}"{attrs}>{img(rel, f"{name} creative by BEINTOX", eager=first)}<span>{name}</span></a>'
        a = "".join(tile(r, i < 3, False) for i, r in enumerate(col))
        b = "".join(tile(r, False, True) for r in col)
        cols.append(f'<div class="wall__col{" wall__col--down" if ci == 1 else ""}" style="--dur:{[64, 76, 58][ci]}s"><div class="wall__track">{a}{b}</div></div>')
    return f'<div class="hero__wall" aria-label="Creatives designed by BEINTOX">{"".join(cols)}</div>'


def page_home() -> str:
    mosaic_html = creative_wall()
    featured = ["identity", "social", "packaging", "ads", "web", "photo", "strategy"]
    schema = {
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": "BEINTOX Marketing Solutions",
        "description": "Brand strategy, identity, design and marketing studio.", "email": CONTACT["email"], "telephone": CONTACT["tel"],
        "address": {"@type": "PostalAddress", "addressCountry": "PK"}, "sameAs": [f"https://instagram.com/{CONTACT['ig']}"],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}} for s in SERVICES],
    }
    body = f'''
<section class="hero"><div class="wrap">
  <div>
    <span class="eyebrow"><b>BEINTOX</b> Marketing Solutions</span>
    <h1 class="h1">Your brand story <em>starts here.</em></h1>
    <p class="lead">Strategy, branding, design and marketing under one roof, for businesses that want to be noticed, trusted and chosen.</p>
    <div class="btns"><a class="btn btn--gold" href="contact.html">Request a proposal {ARROW}</a><a class="btn btn--ghost" href="portfolio.html">View portfolio</a></div>
    <dl class="hero__facts"><div><dt>11</dt><dd>Services, one team</dd></div><div><dt>4</dt><dd>Complete brand systems</dd></div><div><dt>3–6 wk</dt><dd>Typical identity project</dd></div></dl>
  </div>
  {mosaic_html}
</div></section>

{logo_marquee()}

<section class="sec"><div class="wrap">
  {head_block("<b>01</b> What we do", "Eleven services. <em>One clear voice.</em>", "Strategy, creativity and marketing under one roof, so your brand looks, sounds and feels the same everywhere.")}
  <div class="grid g4">{"".join(svc_card(s, num=False) for s in featured)}
    <a class="card card--dark svc-card" href="services.html"><div><span class="card__n">+4 more</span><h3 class="h3">Registration, design, video &amp; audits.</h3></div><span class="card__go">All services {ARROW}</span></a>
  </div>
</div></section>

<section class="sec sec--white bt"><div class="wrap">
  {head_block("<b>02</b> Portfolio", "Brands we've <em>built.</em>", "Complete brand systems, from the logo to the packaging, the storefront and the feed.", f'<div class="btns" style="gap:20px"><a class="link" href="case-studies.html">Read the case studies {ARROW}</a><a class="link" href="portfolio.html">Open the portfolio {ARROW}</a></div>')}
  <div class="grid g2">{"".join(case_card(c) for c in CASES)}</div>
</div></section>

{cta_band()}
'''
    return layout("index", "BEINTOX: Branding & Digital Marketing Agency | Strategy, Identity, Social Media",
                  "BEINTOX is a brand and marketing studio offering brand strategy, identity design, packaging, social media, advertising and websites, all under one roof.",
                  body, schema)


def svc_tile(sid: str) -> str:
    s = svc_by_id(sid)
    m = SVC_IMG.get(sid)
    m = m[0] if isinstance(m, list) else m
    see = ""
    if s[5]:
        c = CASE[s[5]]
        see = f'<a class="svc3__see" href="case-study-{c["slug"]}.html">See it in {E(c["name"])} {ARROW}</a>'
    items = "".join(f"<li>{E(d)}</li>" for d in s[4])
    return f'''<article class="svc3" id="{s[0]}">
  <div class="svc3__img">{img(m, f"{s[1]}: example from our work")}</div>
  <div class="svc3__body">
    <span class="card__n">{svc_num(s[0])}</span>
    <h3 class="h3">{E(s[1])}</h3>
    <p>{E(s[3])}</p>
    <ul class="svc3__list">{items}</ul>
    {see}
  </div>
</article>'''


def page_services() -> str:
    tiles = "".join(svc_tile(x[0]) for x in SERVICES)
    cta = f'''<a class="svc3 svc3--cta" href="contact.html"><div class="svc3__body"><span class="card__n">Not sure where to start?</span>
  <h3 class="h3">Tell us your goal. We'll recommend the smallest set of services that gets you there.</h3>
  <span class="svc3__see">Request a proposal {ARROW}</span></div></a>'''
    body = f'''
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Services</span></nav>
  <h1 class="h1">Strategy, creativity and marketing <em>under one roof.</em></h1>
  <p class="lead">Eleven services. Hire one, or let us run the whole brand.</p>
</div></section>
<section class="sec"><div class="wrap"><div class="svc-grid">{tiles}{cta}</div></div></section>
<section class="sec sec--white bt" id="process"><div class="wrap">
  {head_block("<b>Process</b>", "From idea to <em>identity.</em>", "A clear four-step process, so you always know what's happening, what's next and why.")}
  {steps_html()}
</div></section>
<section class="sec" id="engagement"><div class="wrap">
  {head_block("<b>Engagement</b>", "Pay per project, or <em>retain the team.</em>", "Start with what you need now. Every engagement begins with a scoped proposal: no surprises, no lock-in.")}
  {plans_html()}
</div></section>
<section class="sec sec--white bt" id="faq"><div class="wrap">
  <div class="split" style="align-items:start">
    <div><span class="eyebrow"><b>FAQ</b></span><h2 class="h2 mt-s">Asked <em>often.</em></h2><p class="lead mt-s">Something else on your mind? Message us on WhatsApp and we'll answer directly.</p>
    <div class="btns mt-m"><a class="btn btn--line" href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener">Ask on WhatsApp</a></div></div>
    {faq_html()}
  </div>
</div></section>
{cta_band("Not sure which service you need?", "Start with a marketing audit or a short call. We'll recommend the smallest set of services that gets you the result.")}
'''
    return layout("services", "Services: Branding, Social Media, Advertising, Packaging & Web | BEINTOX",
                  "Brand identity, strategy, packaging, trademark registration, social media, creative design, photography, video, advertising, websites and marketing audits.", body)


VERIFIED = '<svg class="ig__tick" viewBox="0 0 40 40" aria-label="Verified"><path fill="#0095f6" d="M19.998 3.094 14.638 0l-2.972 5.15H5.432v6.354L0 14.64 3.094 20 0 25.359l5.432 3.137v5.905h5.975L14.638 40l5.36-3.094L25.358 40l3.232-5.6h6.162v-6.01L40 25.359 36.905 20 40 14.641l-5.248-3.03v-6.46h-6.419L25.358 0l-5.36 3.094Zm7.415 11.225 2.254 2.287-11.43 11.5-6.835-6.93 2.244-2.258 4.587 4.581 9.18-9.18Z"/></svg>'
IG_GRID = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="1" stroke="currentColor" stroke-width="1.8"/><path d="M9 3v18M15 3v18M3 9h18M3 15h18" stroke="currentColor" stroke-width="1.8"/></svg>'
IG_REEL = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4" stroke="currentColor" stroke-width="1.8"/><path d="M3 8h18M8 3l3 5M14 3l3 5M10 12v5l4.5-2.5z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>'
IG_TAG = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="1.8"/><path d="M6.5 19c1-2.5 3-3.6 5.5-3.6s4.5 1.1 5.5 3.6" stroke="currentColor" stroke-width="1.8"/></svg>'


def ig_profile(c: dict) -> str:
    g = IG[c["slug"]]
    folder = c["cover"].split("/")[0]
    hl = "".join(f'<li><span class="ig__hl">{img(p, l)}</span><small>{E(l)}</small></li>' for p, l in g["highlights"])
    tiles = []
    for it in g["grid"]:
        key, cap = it.split(":", 1)
        rel = f"{folder}/{key}"
        tiles.append(f'<a class="ig__tile" href="assets/img/{src(rel)}" data-lb="{E(cap)}">{img(rel, cap)}<span>{E(cap)}</span></a>')
    return f'''<div class="ig" aria-label="{E(c["name"])} Instagram feed designed by BEINTOX">
  <div class="ig__bar"><b>{E(g["handle"])}</b>{VERIFIED}<span class="ig__dots" aria-hidden="true">•••</span></div>
  <div class="ig__head">
    <div class="ig__avatar">{img(c["logo"], c["name"] + " profile picture")}</div>
    <ul class="ig__stats"><li><b>{g["posts"]}</b><span>posts</span></li><li><b>{g["followers"]}</b><span>followers</span></li><li><b>{g["following"]}</b><span>following</span></li></ul>
  </div>
  <div class="ig__bio"><b>{E(g["name"])}</b><span class="ig__cat">{E(g["category"])}</span>{"".join(f"<span>{E(l)}</span>" for l in g["bio"])}<span class="ig__link">{E(g["link"])}</span></div>
  <div class="ig__btns"><span class="ig__btn ig__btn--blue">Follow</span><span class="ig__btn">Message</span><span class="ig__btn">Contact</span></div>
  <ul class="ig__hls">{hl}</ul>
  <div class="ig__tabs"><span class="is-on">{IG_GRID}</span><span>{IG_REEL}</span><span>{IG_TAG}</span></div>
  <div class="ig__grid" data-lb-group>{"".join(tiles)}</div>
</div>'''


def case_counts(c: dict) -> dict:
    n = {"identity": 0, "posts": 0, "applications": 0}
    for sid, _l, _t, _d, kind, items in c["sections"]:
        if kind == "posts":
            n["posts"] += len(items)
        elif sid == "identity":
            n["identity"] += len(items)
        else:
            n["applications"] += len(items)
    return n


def page_portfolio() -> str:
    blocks = []
    for i, c in enumerate(CASES):
        n = case_counts(c)
        sw = "".join(f'<i title="{E(nm)}" style="background:{h}"></i>' for h, nm in c["palette"])
        svc_links = "".join(f'<a class="tag" href="services.html#{sid}">{E(svc_by_id(sid)[1].split(" &")[0].replace(" (IPO)", ""))}</a>' for sid in c["services"])
        fonts = f'{c["fonts"][0]} / {c["fonts"][1]}' if c["fonts"] else "Custom wordmark"
        g = IG[c["slug"]]
        blocks.append(f'''<section class="pf{" bt" if i else ""}" id="{c["slug"]}">
  <div class="pf__info">
    <span class="eyebrow"><b>{i + 1:02d}</b> {E(c["sector"])}</span>
    <h2 class="h2 mt-s"><a href="case-study-{c["slug"]}.html">{E(c["name"])}</a></h2>
    <p class="lead mt-s">{E(c["summary"])}</p>
    <dl class="spec mt-m">
      <div><dt>Instagram</dt><dd>@{E(g["handle"])} · {g["followers"]} followers</dd></div>
      <div><dt>Brand book</dt><dd>{n["identity"]} pages shown</dd></div>
      <div><dt>Social creatives</dt><dd>{n["posts"]} designed posts</dd></div>
      <div><dt>Applications</dt><dd>{n["applications"]} touchpoints</dd></div>
      <div><dt>Typography</dt><dd>{E(fonts)}</dd></div>
      <div><dt>Palette</dt><dd><span class="spec__sw">{sw}</span></dd></div>
    </dl>
    <span class="eyebrow" style="display:block;margin:22px 0 10px">Services delivered</span>
    <div class="tags" style="margin:0">{svc_links}</div>
    <div class="btns mt-m"><a class="btn btn--gold" href="case-study-{c["slug"]}.html">Read the case study {ARROW}</a><a class="btn btn--line" href="case-studies.html">All case studies</a></div>
  </div>
  {ig_profile(c)}
</section>''')
    filt = "".join(f'<li><a href="#{c["slug"]}">{img(c["logo"], "", eager=True)}<span>{E(c["name"])}</span></a></li>' for c in CASES)
    body = f'''
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Portfolio</span></nav>
  <h1 class="h1">Brands we've <em>built.</em></h1>
  <p class="lead">Four complete brand systems: identity, guidelines, packaging, launch campaigns and the Instagram feeds we design and run.</p>
</div></section>
<nav class="subnav subnav--brands" aria-label="Brands"><div class="wrap"><ul>{filt}</ul></div></nav>
<section class="sec" style="padding-top:40px"><div class="wrap">
  {"".join(blocks)}
</div></section>
{cta_band("Your brand could be <em>next.</em>")}
'''
    return layout("portfolio", "Portfolio: Brand Identity, Packaging & Instagram Work | BEINTOX",
                  "Portfolio: Tomgai Chinese, Twenty Two, Khyber Sajji and Shehar-e-Lazzat. Brand identities, guidelines, packaging, launch campaigns and Instagram feeds.", body)


def page_case_studies() -> str:
    rows = []
    for i, c in enumerate(CASES):
        n = case_counts(c)
        delivered = "".join(f"<li>{ICON['check']}<span>{E(svc_by_id(sid)[1])}</span></li>" for sid in c["services"])
        rows.append(f'''<a class="cs" href="case-study-{c["slug"]}.html" style="--brand:{c["brand"]}">
  <div class="cs__img">{img(c["cover"], f'{c["name"]} case study', eager=i == 0)}<span class="cs__logo">{img(c["logo"], c["name"] + " logo")}</span></div>
  <div class="cs__body">
    <div class="cs__top"><span class="eyebrow"><b>Case {i + 1:02d}</b> {E(c["sector"])}</span></div>
    <h2 class="h2">{E(c["name"])}</h2>
    <div class="cs__brief"><span class="eyebrow">The brief</span><p>{E(c["brief"])}</p></div>
    <div class="cs__cols">
      <div><span class="eyebrow">What we delivered</span><ul class="checks">{delivered}</ul></div>
      <dl class="cs__nums">
        <div><dt>{n["identity"]}</dt><dd>Brand book pages</dd></div>
        <div><dt>{n["posts"]}</dt><dd>Social creatives</dd></div>
        <div><dt>{n["applications"]}</dt><dd>Applications</dd></div>
      </dl>
    </div>
    <span class="btn btn--gold cs__btn">Read the case study {ARROW}</span>
  </div>
</a>''')
    body = f'''
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Case studies</span></nav>
  <h1 class="h1">How we built <em>each brand.</em></h1>
  <p class="lead">The brief, the idea and everything we delivered: identity, guidelines, packaging, campaigns and content. Pick a project to read the full story.</p>
</div></section>
<section class="sec"><div class="wrap"><div class="cs-list">{"".join(rows)}</div></div></section>
{cta_band("Want a case study <em>like these?</em>")}
'''
    return layout("case-studies", "Case Studies: Branding & Marketing Projects | BEINTOX",
                  "Case studies from BEINTOX: the brief, the idea and the full deliverables for Tomgai Chinese, Twenty Two, Khyber Sajji and Shehar-e-Lazzat.", body)


def page_case(c: dict) -> str:
    folder = c["cover"].split("/")[0]
    facts = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in c["facts"])
    sub = "".join(f'<li><a href="#{s[0]}">{s[1]}</a></li>' for s in c["sections"])
    tags = "".join(f'<span class="tag">{E(t)}</span>' for t in c["tags"])
    sw = "".join(f'<div class="swatch"><i style="background:{h}"></i>{E(n)}</div>' for h, n in c["palette"])
    fonts = ""
    if c["fonts"]:
        fonts = f'<div class="mt-m"><span class="eyebrow">Typography</span><p class="mt-s small"><b>{c["fonts"][0]}</b> primary · <b>{c["fonts"][1]}</b> secondary</p></div>'
    secs = []
    for i, (sid, label, title, lead, kind, items) in enumerate(c["sections"]):
        if kind == "posts":
            media = post_grid(items, folder, "posts posts--3" if len(items) in (6, 9) else "posts posts--4" if len(items) in (4, 8) else "posts")
        elif kind == "gallery2":
            media = gallery(items, folder, "gallery gallery--2")
        elif kind == "gallery4":
            media = gallery(items, folder, "gallery gallery--4")
        else:
            media = gallery(items, folder)
        bg = " sec--white bt" if i % 2 == 0 else ""
        secs.append(f'''<section class="sec{bg}" id="{sid}"><div class="wrap">
  {head_block(f"<b>{i + 2:02d}</b> {label}", title, lead)}
  {media}
</div></section>''')
    idx = CASES.index(c)
    nxt = CASES[(idx + 1) % len(CASES)]
    overview_media = f'<div class="ig-wrap">{ig_profile(c)}</div>'
    body = f'''
<section class="chero" style="--brand:{c["brand"]}"><div class="wrap">
  <div class="chero__copy">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><a href="case-studies.html">Case studies</a><span>/</span><span>{E(c["name"])}</span></nav>
    <h1 class="h1">{E(c["name"])}</h1>
    <p class="lead">{E(c["summary"])}</p>
    <div class="tags" style="margin-top:18px">{tags}</div>
  </div>
  <div class="chero__img">{img(c["hero"], c["name"] + " brand applications", eager=True)}</div>
</div></section>
<div class="sec--white" style="border-bottom:1px solid var(--line)"><div class="wrap"><dl class="facts" style="border:0">{facts}</dl></div></div>
<nav class="subnav" aria-label="Case study sections"><div class="wrap"><ul><li><a href="#overview">Overview</a></li>{sub}</ul></div></nav>

<section class="sec" id="overview"><div class="wrap">
  <div class="split">
    <div><span class="eyebrow"><b>01</b> Overview</span><h2 class="h2 mt-s">The <em>idea.</em></h2>
      <div class="prose mt-m">{"".join(f"<p>{E(p)}</p>" for p in c["story"])}</div>
      <div class="mt-l"><span class="eyebrow">Colour</span><div class="palette">{sw}</div></div>{fonts}
    </div>
    {overview_media}
  </div>
</div></section>
{"".join(secs)}
<section class="sec--white bt"><div class="wrap next">
  <a class="link" href="case-studies.html">All case studies</a><span class="eyebrow">Next case study</span>
  <a class="h2" href="case-study-{nxt["slug"]}.html">{E(nxt["name"])} {ARROW}</a>
</div></section>
{cta_band()}
'''
    return layout(f"case:{c['slug']}", f"{c['name']}: {c['sector'].split(' · ')[0]} Branding Case Study | BEINTOX",
                  f"{c['name']} case study by BEINTOX: {', '.join(c['tags']).lower()}. {c['summary']}", body)


def team_html() -> str:
    n, role, photo, bio = FOUNDER
    members = []
    for name, r, ph in TEAM:
        face = img(ph, f"{name}, {r} at BEINTOX") if ph else f'<span class="member__ini" aria-hidden="true">{"".join(w[0] for w in name.split()[:2])}</span>'
        members.append(f'<li class="member"><div class="member__ph">{face}</div><b>{E(name)}</b><span>{E(r)}</span></li>')
    return f'''<div class="founder">
  <div class="founder__ph">{img(photo, f"{n}, {role} of BEINTOX")}</div>
  <div class="founder__txt"><span class="eyebrow"><b>Leadership</b></span>
    <blockquote class="h2 mt-s">“{E(bio)}”</blockquote>
    <p class="founder__name"><b>{E(n)}</b><span>{E(role)}</span></p>
  </div>
</div>
<ul class="team">{"".join(members)}</ul>'''


def page_about() -> str:
    body = f'''
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>About</span></nav>
  <h1 class="h1">Beyond ordinary. <em>Built to be noticed.</em></h1>
  <p class="lead">BEINTOX is a brand and marketing studio. We combine smart strategy, bold design and performance-driven marketing, so your audience stops, connects and chooses you.</p>
</div></section>

<section class="sec sec--white"><div class="wrap">
  <div class="split">
    <div>
      <span class="eyebrow"><b>01</b> The BEINTOX philosophy</span>
      <h2 class="h2 mt-s">A brand isn't made by a logo or a post. It's made by a <em>clear idea.</em></h2>
      <div class="prose mt-m">
        <p>A brand is a clear idea, a consistent look and a message people can trust. Being online isn't enough anymore: brands need to be seen, understood and remembered.</p>
        <p>That's why we bring strategy, creativity and marketing together under one roof, so your brand speaks with one clear voice everywhere. Everything we create has one job: to make your audience stop, connect and choose you.</p>
      </div>
    </div>
    <div class="split__media" style="aspect-ratio:4/3">{img("brand/chess-hand", "A hand moving a gold king on a chessboard", eager=True)}</div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  {head_block("<b>02</b> What we believe", "Be seen. Be understood. <em>Be remembered.</em>")}
  <div class="values">
    <div><span class="card__n">01</span><h3 class="h3">Be seen</h3><p>Visibility is earned with design that stops the scroll and media placed where your customers already are.</p></div>
    <div><span class="card__n">02</span><h3 class="h3">Be understood</h3><p>A clear position and a simple message, so people know in seconds what you offer and why it matters.</p></div>
    <div><span class="card__n">03</span><h3 class="h3">Be remembered</h3><p>Consistency builds memory. One look, one voice, repeated everywhere until your brand is the one they choose.</p></div>
  </div>
</div></section>

<section class="sec sec--white bt"><div class="wrap">
  <div class="split">
    <div class="split__media" style="aspect-ratio:16/10">{img("shehar/app-mockups", "Shehar-e-Lazzat brand mockups")}</div>
    <div>
      <span class="eyebrow"><b>03</b> What we're building</span>
      <h2 class="h2 mt-s">From “just another name” to a brand with <em>real presence.</em></h2>
      <div class="prose mt-m"><p>We help businesses turn ideas into identities, and identities into lasting customer relationships. We don't create content just for today. We build brands made to last.</p></div>
      {checks(["Strategy, design and marketing in one team", "Complete brand systems with guidelines", "Bilingual Urdu & English creative", "Production-ready files for print, packaging and signage"])}
      <div class="btns mt-m"><a class="btn btn--dark" href="portfolio.html">See the work {ARROW}</a><a class="btn btn--line" href="services.html">Our services</a></div>
    </div>
  </div>
</div></section>

<section class="sec" id="team"><div class="wrap">
  {head_block("<b>04</b> The team", "The people behind <em>the work.</em>", "Strategy, design, video and development: one close team, under one roof.")}
  {team_html()}
</div></section>

<section class="sec sec--white bt"><div class="wrap">
  {head_block("<b>05</b> Why BEINTOX", "Being memorable is what <em>makes brands grow.</em>", "Every day your customers see hundreds of brands, and most are forgotten in seconds. We shape how yours looks, sounds and feels, so people notice you, trust you and come back.")}
  {why_html()}
</div></section>

<section class="sec"><div class="wrap">
  {head_block("<b>06</b> How we work", "One team, one process, <em>no handoffs.</em>")}
  <div class="steps">
    <div class="step"><span class="step__n">1</span><h3 class="h3">Discover</h3><p>Business, audience and competitor research to find what makes you worth choosing.</p></div>
    <div class="step"><span class="step__n">2</span><h3 class="h3">Define</h3><p>Positioning, personality and messaging: the brief every design decision answers to.</p></div>
    <div class="step"><span class="step__n">3</span><h3 class="h3">Design</h3><p>Identity, guidelines, packaging and content built as one connected system.</p></div>
    <div class="step"><span class="step__n">4</span><h3 class="h3">Grow</h3><p>Launch, measure and refine across social, ads and web.</p></div>
  </div>
</div></section>
{cta_band()}
'''
    return layout("about", "About BEINTOX: Brand & Marketing Studio",
                  "BEINTOX combines smart strategy, bold design and performance-driven marketing to build brands that are seen, understood and remembered.", body)


def page_contact() -> str:
    chips = "".join(f'<label><input type="checkbox" name="services" value="{E(s[1])}"><span>{E(s[1].split(" &")[0].replace(" (IPO)", ""))}</span></label>' for s in SERVICES)
    body = f'''
<section class="phero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Contact</span></nav>
  <h1 class="h1">Let's build something <em>worth remembering.</em></h1>
  <p class="lead">Tell us about your business and what you need. We'll reply with questions and a scoped proposal. Proposals are free.</p>
</div></section>
<section class="sec"><div class="wrap contact">
  <form class="card form" id="brief" data-wa="{CONTACT["wa"]}" data-email="{CONTACT["email"]}" style="padding:28px">
    <div class="field"><label for="f-name">Your name *</label><input id="f-name" name="name" required autocomplete="name"></div>
    <div class="field"><label for="f-biz">Business / brand</label><input id="f-biz" name="business" autocomplete="organization"></div>
    <div class="field field--full"><label for="f-contact">Phone or email *</label><input id="f-contact" name="contact" required autocomplete="email"></div>
    <div class="field field--full"><span style="font-size:13px;font-weight:600">What do you need?</span><div class="chips">{chips}</div></div>
    <div class="field field--full"><label for="f-time">Timeline</label><select id="f-time" name="timeline"><option>As soon as possible</option><option>Within 1 month</option><option>1–3 months</option><option>Just exploring</option></select></div>
    <div class="field field--full"><label for="f-msg">About the project</label><textarea id="f-msg" name="message" placeholder="Where is your brand today, and where do you want it to go?"></textarea></div>
    <div class="form__foot">
      <button class="btn btn--gold" type="submit" value="whatsapp">Send via WhatsApp {ARROW}</button>
      <button class="btn btn--line" type="submit" value="email">Send via email</button>
      <span class="form__note">Opens WhatsApp or your email app with your brief filled in.</span>
    </div>
  </form>
  <aside>
    <span class="eyebrow">Direct</span>
    <div class="clist mt-s">
      <a href="https://wa.me/{CONTACT["wa"]}" target="_blank" rel="noopener"><i>{ICON["wa"]}</i><span><small>WhatsApp, fastest reply</small><b>{CONTACT["phone"]}</b></span></a>
      <a href="tel:{CONTACT["tel"]}"><i>{ICON["phone"]}</i><span><small>Call</small><b>{CONTACT["phone"]}</b></span></a>
      <a href="mailto:{CONTACT["email"]}"><i>{ICON["mail"]}</i><span><small>Email</small><b>{CONTACT["email"]}</b></span></a>
      <a href="https://instagram.com/{CONTACT["ig"]}" target="_blank" rel="noopener"><i>{ICON["ig"]}</i><span><small>Instagram</small><b>@{CONTACT["ig"]}</b></span></a>
    </div>
    <div class="card mt-m"><span class="eyebrow">What happens next</span>
      <ol class="checks">{"".join(f"<li>{ICON['check']}<span>{t}</span></li>" for t in ["We read your brief and reply with a few questions.", "A short call to understand goals, audience and budget.", "You receive a scoped proposal with timeline and cost.", "Kick-off, and discovery begins."])}</ol>
    </div>
  </aside>
</div></section>
'''
    return layout("contact", "Contact BEINTOX: Request a Proposal",
                  f"Request a proposal from BEINTOX. WhatsApp or call {CONTACT['phone']}, email {CONTACT['email']}.", body)


def page_404() -> str:
    body = f'''<section class="sec err"><div class="wrap"><span class="eyebrow">404</span><h1 class="h1 mt-s">This page <em>doesn't exist.</em></h1>
<p class="lead mt-s" style="margin-inline:auto">The link may be old or mistyped.</p><div class="btns mt-m" style="justify-content:center"><a class="btn btn--dark" href="index.html">Back to home</a><a class="btn btn--line" href="portfolio.html">See our work</a></div></div></section>'''
    return layout("404", "Page not found | BEINTOX", "Page not found.", body)


# =====================================================================
# BUILD
# =====================================================================

def main() -> None:
    pages = {"index": page_home(), "services": page_services(), "portfolio": page_portfolio(), "case-studies": page_case_studies(),
             "about": page_about(), "contact": page_contact(), "404": page_404()}
    for c in CASES:
        pages[f"case-study-{c['slug']}"] = page_case(c)
    for name, out in pages.items():
        (ROOT / f"{name}.html").write_text(out, encoding="utf-8")
    print(f"Built {len(pages)} pages: {', '.join(sorted(pages))}")


if __name__ == "__main__":
    main()
