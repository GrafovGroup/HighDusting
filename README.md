# HighDusting.ca

Image-rich B2B website based on the previous “High Dusting Business Plan” conversation. Includes 100 indexable pages: 52 cities, 13 province/territory hubs, 20 services, six industries, directories, homepage and privacy notices, plus two cost guides and a French post-construction service page. Also includes a custom 404 and a single-step quote form.

## Run

Requires Python 3.10 or newer; no pip packages or frontend build dependencies.

```sh
python3 build.py
python3 server.py --port 4321
```

Open http://127.0.0.1:4321. On this Mac, the bundled Python executable is `/Users/grafov/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` (the system `python3` command is not a working Python 3 runtime).

`build.py` and `expansion.py` are the content/template sources. `service_answers.py` contains service-specific buyer questions; `seo.py` derives structured data and the image sitemap from the final pages. Run `python3 build.py` after editing these sources. `styles.css` and `app.js` are served directly.

## Quote handling

All 98 quote forms submit directly to `https://formspree.io/f/mqpkndrp` using vanilla JavaScript AJAX. The endpoint is declared in the base form’s `action`; `formspree.js` sends multipart `FormData` with `Accept: application/json`. The single-step controller in `app.js` handles validation, state, localized messages and duplicate-submit prevention. No additional form library or SMTP credentials are needed.

The form asks for name, email, city/province and a short message, with optional phone. Photos/videos are emailed separately to info@highdusting.ca. It retains the contact-consent checkbox. Detailed facility questions are handled during follow-up. The payload includes those details, selected city/service, submission page, originating page and language. File inputs are deliberately absent: a live test returned HTTP 400, File Uploads Not Permitted. Do not restore uploads until the provider account supports them and a live upload succeeds. Recipient delivery, domain restrictions, spam protection and account quotas are managed in the Formspree dashboard. Provider-side validations should match the required fields; browser validation alone is not an abuse boundary.

The forms keep their field values on failure and display success only after Formspree accepts the request. No local database reference number is shown. A hidden `_gotcha` honeypot supports Formspree spam filtering. With JavaScript disabled, the same single-step form remains usable and the browser posts to Formspree directly; browser-native Formspree responses control that fallback journey.

OpenAI Sites is the selected host and GoDaddy manages the domain. The public website now needs only static hosting; it does not depend on `/api/quotes`, SQLite, an upload server or SMTP. Domain connection and publishing are separate from this local integration change. Package only public pages, assets, `styles.css`, `formspree.js`, `app.js`, favicon, robots and sitemap. Do not publish the entire project root or the private `.data/` directory.

`server.py`, `notifications.py` and `manage_quotes.py` remain legacy local tools so existing saved records are preserved. New website submissions go to Formspree and are not written to the local SQLite database or notification outbox.

## Validation

```sh
python3 -m unittest test_content test_seo test_growth
node --test test_formspree.cjs
python3 test_server.py
```

Generated-page checks verify every quote endpoint, multipart attributes, script order, local links, metadata and images. The JavaScript transport tests use mocked responses for success, attachments, field errors, rate limits and network failures; they do not send enquiries or verify inbox delivery. The Python server tests exercise the retained local backend with temporary isolated data and verify public file serving. Live English homepage and French service submissions were accepted on October 25, 2026. A city-form attachment failed; see FORM_VERIFICATION.md for findings and the fix.

## Images

The initial four images and 88 expansion images were generated with the built-in image generation tool and converted to WebP for web delivery. They are illustrative service/facility scenes, not claimed client projects. See `ASSETS.md` for filenames and generation prompts. No invented testimonials, customer logos, certifications or completion statistics are included.

## National expansion (September 2026)

The extended build adds 52 city pages, 13 province/territory hubs, 16 service pages, six industry pages, a searchable nationwide directory and French Quebec enquiries. `expansion.py` extends the original templates; `data/cities.json` owns the city planning briefs and `data/municipalities.json` stores the imported Statistics Canada reference geography. See `SOURCES.md` for scope and dataset limitations.

All city, service, industry and province hero images have distinct files. Supporting galleries may intentionally reuse the relevant service photograph. The complete prompt/provenance manifest is in `data/image-manifest.json`. These are illustrative AI facility scenes, not actual local jobs or city photography.

The form continues to submit `selected_city`, `selected_service`, `source_page` and `originating_page`. These fields now travel to Formspree with the enquiry. Previous SQLite records and private attachments remain untouched. The optional SMTP configuration in `.env.example` applies only to the legacy local backend and is not needed for Sites/Formspree hosting.

## Search and answer-engine implementation

The build emits unique titles and descriptions, canonical URLs, matching Open Graph URLs/locales, large-image preview permission, and linked Organization, WebSite and WebPage graphs on all 100 indexable pages. Collection pages and visible breadcrumbs describe the directory hierarchy. The 20 service pages and 52 city pages have Service entities; city areas describe the location being scoped, not branch offices. French pages use `fr-CA`. No translation alternate links are invented for pages without equivalent translations.

All 20 services include visible answers about their specific scope, cost factors and quote preparation. These are normal HTML and remain readable without JavaScript. Structured data describes the visible content; no special AI-only schema, fake reviews, prices or credentials are added. `sitemap.xml` includes only authored canonical pages and their actual displayed images. The 404 has `noindex` and no homepage canonical.

Run `python3 -m unittest test_content test_seo test_growth` after rebuilding. This checks all generated routes/assets, distinct required images, unique metadata, linked graph references, visible breadcrumb agreement, language consistency, service answers and image sitemap coverage. These are local content checks; they do not establish live indexing, ranking or rich-result eligibility.

After production deployment, verify the actual domain in Google Search Console and Bing Webmaster Tools, submit the sitemap, inspect representative English/French/service/city URLs, and measure enquiries against search performance. Add real project photos, permissioned case studies and substantiated business credentials as they become available. Expansion to further cities should add useful local information, not just substituted place names.

Public-image copy preference: use descriptive alternative text without AI-generation or illustration labels in visible content, image attributes or social metadata. Keep generation provenance in the project documentation. Do not describe images as completed client projects without supporting evidence.

## Publish staging

After generating the pages, run `python3 tools/prepare_publish.py` to stage the public files in `dist/`. The Sites hosting manifest uses that directory. Staging copies only sitemap pages, the 404, referenced public assets, the directory data and shared browser files; private quote records and source files are excluded. Use the Sites hosting workflow to save and deploy the matching source revision.

## Post-construction service and city planning

The site includes `/services/post-construction-high-dusting/` and `/guides/high-dusting-cost/`, with complete French counterparts at `/fr/services/depoussierage-apres-construction/` and `/fr/guides/prix-depoussierage-hauteur/`. The matching translations have reciprocal language links and hreflang metadata. The cost guides explain quote factors and scope comparisons without unverified price ranges.

`local_growth.py` owns the new service, guide copy and 52 distinct city handover scenarios. The scenarios are planning examples, not claims about local offices, completed projects or guaranteed availability. All existing city pages link to the relevant service and cost guide with city and source context carried into the single-step enquiry form. City titles/descriptions include the city and province. No duplicate service-by-city route grid is generated.

The 100 indexable pages include 73 Service entities (52 cities, 20 English services and one French service) and two cost-guide Article entities. Tests cover the new routes, city-link context, translation reciprocity and schema types. Browser checks cover English and French service, guide and city pages at phone and desktop widths.

## Focused overhead services

`niche_services.py` owns acoustic baffle/ceiling cloud dusting, warehouse rack-top cleaning and gymnasium overhead cleaning. Each service has its own photo, planning details, scope boundaries, buyer questions and quote context. Relevant city and industry pages link to these scopes; French city enquiries use localized labels and preserve the selected service. New service navigation uses text cards so each new photo is displayed only on its own page.

Acoustic material boundaries were checked against Armstrong commercial ceiling maintenance guidance: https://www.armstrongceilings.com/commercial/en/technical-downloads/ceiling-maintenance.html. No acoustic performance restoration, rack certification or sports-equipment servicing is claimed.
