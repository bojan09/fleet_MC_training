# Validation
Chromium / Playwright on the current cloud machine:
- Eight module cards rendered.
- Search for reefer returned two relevant modules.
- Anatomy lesson rendered six content notes.
- Glossary rendered 51 terms; OOS search returned one.
- Five-question practice flow completed and displayed a score with explanations.
- 390px mobile viewport had no horizontal overflow.
- No JavaScript page errors observed.
- JavaScript syntax check passed.

Scope: this validates interface behavior, not mechanical accuracy, legal currency, or redistribution rights. No publication or remote push performed.

## Illustrated manual update
- Static coverage check: 18 original source-art panels, 117 note illustrations, and 51 glossary illustrations; all referenced files and manifest entries exist, and SVGs parse.
- Chromium: all 18 lessons rendered the same number of images as explanations; all lesson and glossary images loaded successfully.
- Zoom: open, 150%, fit to 100%, Escape close, and focus restoration passed.
- Component jump links scroll within the lesson while preserving its URL.
- Mobile at 390px: no horizontal overflow in the lesson or image viewer.
- Original search, lesson, glossary, and five-question practice checks still pass; no JavaScript page errors observed.
- Desktop and mobile Engine & Cooling pages visually inspected.

PDF source images remain low resolution, and their embedded labels/example values have not been independently verified. New vector graphics are simplified concept illustrations rather than service drawings.

## Full-screen and sharp-visual update
- All 18 lesson overview sheets are original SVGs; reference PNGs are retained in an expandable source-art section.
- Viewer exactly matched 1440×900 desktop and 390×844 mobile viewport dimensions.
- Fit showed the complete image with no horizontal or vertical scrolling on desktop and for all 18 mobile overview sheets.
- Zoom, reset-to-fit, previous/next keyboard navigation, Escape, and focus restoration passed.
- Browser Fullscreen API entry and exit passed in Chromium; closing the viewer passed.
- No JavaScript errors observed; local asset/manifest and SVG syntax checks passed for 213 records.
- Original 384×256 PDF artwork cannot be made genuinely sharp by enlarging it. Primary visuals now use scalable vector diagrams instead; source artwork remains unchanged.

## Static site repair
- All eight existing module assets loaded locally and under a simulated `/training/` deployment subpath.
- Application asset URLs now resolve from app.js rather than the current document route.
- Simulated missing card image displayed an explicit fallback; simulated content failure recovered through Try again.
- Previous-lesson navigation, active navigation state, and skip-to-content behavior passed.
- No horizontal overflow at viewport widths 320, 390, 768, and 1440px.
- Manrope and DM Sans loaded from local font files; their SIL OFL licenses are bundled.
- Lesson/glossary/practice and full-screen viewer regression checks passed locally.
- Netlify configuration parses and explicitly publishes the repository root; HTML, scripts, and JSON revalidate to reduce stale-content mismatches.
- Local static asset manifest validation and JavaScript syntax checks passed; no browser JavaScript errors observed.

Outstanding: requests to the live Netlify host, Wikimedia Commons API, and Wikimedia image host still receive proxy tunnel 403 denials from this task's enforced network policy. The saved draft domain additions have not become active. These local checks do not establish that the live Netlify site redeployed or that its specific image failures are resolved. High-resolution real-photo replacement is unfinished; existing PDF artwork and diagrams are not claimed as photographs. Additional GitHub-hosted photo searches did not identify a suitable set of photographs with verified reuse rights.
