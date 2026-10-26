# Form verification — October 25, 2026

## Finding and fix

The live English homepage and French service form accepted synthetic text-only enquiries. A live Toronto city enquiry with a 0.3 MB WebP failed. A direct multipart diagnostic returned HTTP 400 with `File Uploads Not Permitted` from the existing Formspree endpoint.

Removed unsupported file inputs from the shared template and all 98 generated quote forms. English and French forms now invite customers to email photos/videos separately to info@highdusting.ca, including their name and city. Successful submission also provides the photo email link. Failed submissions preserve typed information and offer an email fallback. Optional IntersectionObserver support no longer blocks initialization on older browsers.

## Verification

- 98 quote forms checked for the correct Formspree action, POST method, script order, absence of file inputs and photo email link.
- 17 Python content, SEO and growth tests passed.
- Four mocked transport tests passed, covering success, provider field errors, HTTP failures, invalid JSON and network errors. Multipart attachment transport remains covered for a future provider upgrade; uploads are disabled in the UI today.
- Live text-only tests: English homepage and French post-construction service accepted by Formspree.
- Inbox receipt is not independently verified; owner confirms info@highdusting.ca receives mail.

## Operations

Hosting remains OpenAI Sites. GitHub contains the complete source, images, build scripts and tests; pushing to GitHub alone does not deploy to Sites. No Formspree credentials or private enquiry records are required in this repository. Provider recipient, quotas and spam rules remain managed in Formspree.

Re-enable web uploads only after enabling support in Formspree and validating an end-to-end upload. Do not simply restore the input: it would block customers again.
