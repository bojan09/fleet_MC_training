# Fleet MC Training
A static learning manual built with HTML, CSS, and vanilla JavaScript. No build tools, database, authentication, analytics, cookies, or browser storage.

## Run
From this directory: `python3 -m http.server 8000`. Open the server in a browser. JSON content requires HTTP rather than opening index.html directly. Deploy the directory to any static host; all internal paths are relative.

## Contents
Eight modules, 18 lessons from the supplied PDF, 51 glossary definitions, module keyword search and category filters, five practice questions with explanations, and hash-based direct links with browser history. Practice answers only live in memory. Responsive layout, keyboard focus, and reduced-motion support.

## Sources and scope
See docs/source-map.md and assets/manifest.json. Both supplied Markdown briefs were read as reference material. The user's requested name and no-storage requirement override their conflicting branding and persistence suggestions. The 33-gallery encyclopedia is a potential expansion, not represented as completed in this manual. Two other PDFs mentioned by the briefs were not supplied. Text is educational and not independently validated current legal/OEM guidance. Every lesson opens with a sharp SVG illustrated overview. The full-screen viewer fits both width and height, with zoom, previous/next navigation, and optional browser fullscreen. Low-resolution PDF images are preserved in a separate expandable source reference. Every lesson has its original uncropped PDF illustration and each of the 117 explanation cards has an original vector concept diagram. The 51 glossary terms and practice scenarios also include illustrations. Images support an accessible dialog with zoom, fit, Escape, and focus restoration. Original SVGs are regenerated with `python3 scripts/build-visuals.py`; no image service is required. PDF artwork remains unchanged; rights for independent redistribution and embedded technical labels remain unverified.

Fonts are bundled locally under their SIL Open Font License, with system fallbacks. Netlify publishes the repository root using netlify.toml; there is no build command. No JavaScript dependency or external image request is needed.


## Current photo limitation
The original PDF contains only 384×256 raster illustrations. Those are not high-resolution photographs. The requested replacement with real truck/component photos is still unfinished because Wikimedia Commons and the live Netlify URL are denied by the execution environment’s current network policy. Existing SVGs remain conceptual illustrations; no photo replacement is claimed. The photo-source and live-site domains are saved in the environment configuration draft but are not yet active.
