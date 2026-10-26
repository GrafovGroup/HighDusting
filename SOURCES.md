# National expansion sources and editorial boundaries

## Geography

Statistics Canada, Table 98-10-0002-01: Population and dwelling counts, Canada and census subdivisions (municipalities), 2021 Census.

- Table: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810000201
- Download: https://www150.statcan.gc.ca/n1/en/tbl/csv/98100002-eng.zip
- Retrieved: September 10, 2026.
- Import: `tools/import_locations.py` reads the official CSV by DGUID level (2021A0005), retaining 5,161 subdivisions.
- Public search adds named pages where the census uses a broader or bilingual municipality label. This produces 5,163 searchable records.
- This is explicitly 2021 reference geography, not a claim that all 5,161 subdivisions are cities or that current municipal boundaries are unchanged. Smaller settlements, unorganized areas and other CSD types appear in the source. Users can submit any address even when it is absent or renamed.
- The 52 initial location pages represent a selected commercial-market rollout across all 13 provinces and territories. Fort McMurray is presented as a community within the broader Wood Buffalo area.

## Editorial content

City planning briefs are original, prospective facility-scoping guidance. They are not client case studies, promises of an office or crew in each city, or a claim that illustrated buildings exist at those locations. Each page includes a distinct facility-planning scenario, relevant services, nearby communities, local-availability qualifications and its own form. Quebec pages and the Quebec hub are French-language pages.

No unsupported local customer counts, fake completed projects, invented reviews, certifications or local-office addresses are used. Images are original AI illustrations of plausible facilities. Provenance is recorded in ASSETS.md and the image manifest. Public images use descriptive alternative text without AI or illustration labels, as requested by the owner. Images are not described as completed client projects.

## Search guidance reviewed

- Google Search Central, spam policies (doorway abuse): https://developers.google.com/search/docs/essentials/spam-policies#doorway-abuse
- Google Search Central, image best practices: https://developers.google.com/search/docs/appearance/google-images
- Google Search Central, AI features and your website: https://developers.google.com/search/docs/appearance/ai-features
- Google Search Central, canonical URLs: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls

SEO/AEO work follows the same crawlability and helpful-content foundation. Google does not require a special AI text file or special structured data for its AI search features, and eligibility does not guarantee inclusion. Service answers are original scope-planning copy based on the site's existing service boundaries. Metadata and image sitemap entries are generated from the visible final pages.

The broad reference directory links to 52 substantive location pages or a location-prefilled enquiry. It does not publish thousands of nearly identical indexable city pages or multiply every service across every municipality. Search results remain within the directory and the sitemap contains explicit authored routes only.


## Form integration

- Formspree AJAX: https://help.formspree.io/articles/building-your-form/submit-forms-with-javascript-ajax/
- Formspree uploads: https://help.formspree.io/articles/building-your-form/file-uploads/
- Formspree honeypot: https://help.formspree.io/articles/building-your-form/honeypot-spam-filtering/

The website uses the vanilla JavaScript AJAX approach with its existing form controller, direct multipart submission and English/French UI. File-upload support and storage depend on the Formspree account plan/settings. Integration tests mock responses and do not verify recipient delivery.

## Search implementation references for the post-construction expansion

Reviewed September 15, 2026:
- Google Search spam policies: https://developers.google.com/search/docs/essentials/spam-policies — retain useful city pages with distinct planning information rather than creating substantially similar service/city pages.
- Google localized-version guidance: https://developers.google.com/search/docs/specialty/international/localized-versions — reciprocal hreflang only for the two genuine English/French content pairs.

City handover text in `local_growth.py` is editorial project-planning advice based on the existing facility briefs. It does not assert local demand, branch presence, pricing or completed work. The cost guide describes scope factors; no market price statistics are claimed.
