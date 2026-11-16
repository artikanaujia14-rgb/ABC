# HOVEN AI Image Auditor — Google AI Studio Build Mode Prompt

Copy the full prompt below into **Google AI Studio → Build**. Build a full-stack web application, not a static mockup or offline HTML demo.

---

## BUILD PROMPT (paste everything in this section)

Build a complete, polished, responsive, full-stack web application named **HOVEN AI Image Auditor** for an Indian ecommerce brand selling bathroom fittings and home-improvement products on Amazon India and Flipkart.

### Non-negotiable architecture

1. Use Google AI Studio Build Mode's full-stack web runtime: React frontend and Node.js server/backend.
2. Use Google's official `@google/genai` SDK for all AI calls. **Do not use OpenAI, OpenAI SDKs, or any other AI provider.**
3. Use the AI Studio-managed Gemini API secret available to the server as `process.env.GEMINI_API_KEY`. AI Studio Build should configure this secret automatically. Do not ask the user to create, paste, or expose an API key manually. Never put secrets in browser code, local storage, source maps, logs, or API responses.
4. All image analysis and chat must run online through server-side Gemini requests. The browser may do image preview and basic file metadata only. It must never mark an image passed/approved using offline heuristics. If Gemini is unavailable, show a clear error and say **Not analysed**; never produce a pass result.
5. Do not create a fake UI with hardcoded sample scores. Dashboard metrics must be calculated from real completed analyses; otherwise show an em dash / empty state.
6. Use a currently available Gemini vision-capable model via a single server-side model configuration constant. If a model name is unavailable, show a clear server configuration error and use a model confirmed available in AI Studio rather than silently switching to another provider.

### Product purpose and user flow

The user uploads a complete product listing image set. Immediately after upload, Gemini must inspect the actual images and automatically identify what each image represents, report problems, recommend improvements, and allow the user to ask questions in a live chat about the uploaded images and audit.

Create this workflow:

1. Select marketplace: **Amazon India**, **Flipkart**, or **Both**.
2. Enter optional product details: product name, SKU, HOVEN brand, category, variant/colour, material, dimensions, verified product facts, package contents, and any test certificates or technical evidence.
3. Upload up to 12 listing images in one batch.
4. Optionally upload up to 8 original/raw product reference photos. These are the ground-truth visual reference for comparison and must not be counted as gallery images.
5. Send the images to Gemini from the server. Show a progress state: uploading → classifying → auditing → report ready.
6. Classify every listing image automatically, assign a confidence score, and recommend the gallery order separately for Amazon and Flipkart. Do not assume upload order equals gallery order.
7. Show image-by-image findings, set-level findings, missing image types, policy source citations, and seller confirmations needed.
8. Enable an interactive Hindi/Hinglish/English AI chat grounded in the current audit, uploaded images, original reference photos, product details, and the policy sources. The user should be able to ask follow-up questions without re-uploading.
9. Allow the user to correct an image's detected type, change gallery sequence with drag-and-drop, mark findings as resolved, and re-run an audit.
10. Export reports as PDF and CSV (and optionally JSON). Include the marketplace, product/SKU, image filename, detected role, recommended sequence, issues, evidence, correction advice, policy source URL, and verification date.

### Automatic image-type classification

For each uploaded listing image, classify it into exactly one primary role, plus optional secondary tags:

- `MAIN_PRODUCT_CANDIDATE` — isolated product presentation that could be considered for the main image.
- `LIFESTYLE` — product installed, shown in a real environment, or in use.
- `FEATURE_INFOGRAPHIC` — benefits, features, callouts, icons, diagrams or promotional text.
- `DIMENSIONS` — measurements, dimensions, technical size diagram.
- `INSTALLATION` — installation steps, connection guidance or how-to.
- `CLOSE_UP_DETAIL` — finish, material appearance, joints, threads, handle or other product detail.
- `PACKAGE_CONTENTS` — items/accessories shown as included in the package.
- `BRAND_TRUST` — brand, warranty, support, quality or trust messaging.
- `COMPARISON` — comparison against alternatives or variants.
- `OTHER` — anything else or uncertain.

Return `role_confidence` from 0 to 1 and a brief visible-evidence explanation. If uncertain, classify as `OTHER` or lower confidence; do not invent an image role. Make the classification editable by the user.

### Gallery sequence recommendations

- Recommend image order independently for Amazon India and Flipkart.
- The first slot must be the best **main-image candidate** only if it appears to meet that marketplace's verified main-image rules. Otherwise show **No suitable main-image candidate detected** and explain why.
- Recommend the remaining image sequence based on clarity, customer decision needs, product category, and marketplace-specific published requirements.
- Clearly distinguish “recommended order” from mandatory marketplace rules. Do not state that a particular gallery order is required unless a current official source says so.
- Keep all uploaded image IDs and filenames mapped accurately. Include each listing image exactly once in each proposed sequence.

### Audit dimensions

Gemini must inspect each image individually and compare the set as a whole:

1. Product accuracy: visible shape, silhouette, colour, finish, handle, joints, threads, outlets, connectors, visible components, and apparent quantity.
2. Reference comparison: compare listing images against original product reference photos. Flag possible changes/additions/omissions. State exactly what visual area differs. This is visual comparison only, not a physical product inspection.
3. Image quality: resolution, visible blur, compression artifacts, lighting, shadows, contrast, colour cast, glare/reflections, and readability.
4. Composition: cropping, complete product visibility, alignment, framing, clutter, empty space, scale in frame, and mobile readability.
5. Background and props: background suitability, distractions, unrelated props, accessories that may imply inclusion, and visual realism.
6. Text and graphics: spelling, grammar, text density, text size, contrast, icon clarity, overlapping/cut-off content, and unsupported claims.
7. Brand consistency: HOVEN logo/brand name where appropriate, wrong third-party brand marks, consistent typography, colours, icon style, and premium visual system.
8. Technical information: dimensions, connection/fitment details, material, package contents, installation details. Missing or inconsistent information must be flagged; never infer exact technical specs from pixels.
9. Trust/claims: warranty, rust resistance, corrosion resistance, leak-proof, durability, pressure, material, compatibility and performance claims. Mark as **seller evidence required** unless supporting product documentation/test results are supplied.
10. Gallery completeness: missing key image types and duplicate/repetitive images.

### Product truth and safety rules

- Never alter the product's actual design, shape, proportions, colour, finish, components, threads, joints, handle, outlets, dimensions, or included accessories in any suggested edit.
- Never tell an image generator/designer to invent or add a feature not present in the reference product.
- Separate `OBSERVED`, `POSSIBLE_DIFFERENCE`, `SELLER_CONFIRMATION_REQUIRED`, and `SUGGESTION` in the UI/report.
- An image cannot prove PTMT/brass/PVC/ABS composition, exact thread size, pressure rating, leak-proof performance, corrosion resistance, durability, warranty, or package contents. Those require seller-provided specifications, tests, certificates, or packaging evidence.
- Do not treat the presence of water, hose, or a usage scene as proof of technical performance or compatibility.
- Never mark a product accurate simply because it looks plausible.

### Marketplace policy and current-source research

The app is an advisory image auditor, **not an Amazon/Flipkart approval system**.

- Do not claim access to private ranking algorithms, internal search ranking weights, AutoQC internals, seller account moderation, or private marketplace systems.
- Do not promise listing approval, ranking, impressions, sales, conversion, or suppression avoidance.
- Audit only against published, current, country- and category-relevant rules and transparent creative best practices.
- Keep Amazon India and Flipkart rules separate.
- For policy research, use Gemini's Google Search grounding where supported by the selected model/SDK. Search for official sources first: Amazon India Seller Central (`sellercentral.amazon.in`) and Flipkart Seller Hub (`seller.flipkart.com`). Use official engineering/blog sources only as supporting context, not as a substitute for current Seller Hub rules.
- Store policy rule metadata: marketplace, country, product category, rule text, source title, source URL, source type (official / supporting), date checked, applicability, and confidence/verification level.
- Show source citations/links beside every policy-related warning. Show “last checked” date.
- If a Seller Central/Seller Hub page is login-gated, inaccessible, ambiguous, outdated, or category-specific and cannot be confirmed, label the rule **VERIFY IN SELLER HUB / SELLER CENTRAL**. Do not invent dimensions, file limits, image-count requirements, or text-overlay rules.
- Use the bundled `reference/policy_sources_2026-11-14.json` only as a starting snapshot. Re-check official sources before treating it as current. Do not silently convert the snapshot into universal policy.
- Distinguish `FAIL` (confirmed rule violated), `VERIFY` (policy not currently confirmable), and `PASS` (specific published requirement checked and no violation detected). A policy `PASS` is not official platform approval.
- Provide a “Refresh policy sources” action that runs grounded searches, stores citations and checked date, and requires human confirmation before changing the policy rule library. If Google Search grounding is not available in the selected model/runtime, explain that refresh cannot run rather than pretending it did.

### Example policy starting point

The supplied policy snapshot dated 2026-11-14 records these Amazon India public-rule notes: main image pure white RGB 255,255,255; entire product visible; product approximately 85% of image area; one unit and only included accessories; no added text/seller logo/watermark/border/graphics on the main image; images accurately represent the product; longest side 500–10,000 px; 1,000+ px supports/recommended for zoom; JPEG/TIFF/PNG/non-animated GIF; RGB preferred; category requirements may apply. Treat every item as subject to current Seller Central re-verification and category applicability.

For Flipkart the supplied snapshot says the official Seller Hub image guidelines may require login and exact current category rules must be verified there. An older public Flipkart engineering example mentions centered/clear images and at least 70% product coverage in that example only. Do not apply 70% as a universal current rule. Mark unverifiable specifics as `VERIFY_IN_SELLER_HUB`.

### Status and scoring design — avoid false approvals

Use these audit statuses only:
- `HIGH_RISK` — a clearly visible serious issue or confirmed rule violation.
- `NEEDS_REVIEW` — uncertainty, missing evidence, or an issue requiring correction/confirmation.
- `LIKELY_OK` — no issue detected within the checks actually performed; **not platform approval**.

Never use the words “Approved”, “Marketplace approved”, “Guaranteed compliant”, or a green “Ready to list” badge. A green visual-quality indicator may be used only for image-quality checks and must not imply policy approval.

If using numeric scores, separate:
- `visual_quality_score` (0–100, based on observable image quality/composition/readability),
- `policy_risk` (LOW / MEDIUM / HIGH / VERIFY),
- `product_accuracy` (MATCH / POSSIBLE_DIFFERENCE / INSUFFICIENT_REFERENCE / SELLER_CONFIRMATION_REQUIRED).

Do not merge these into a single “compliance score” that hides uncertainty. Explain how each score was calculated. Use “Not analysed” when the AI call fails.

### Structured Gemini audit response

Use Gemini structured JSON output/schema where available. Validate the response server-side before rendering. At minimum return:

- `overall_status`, `overall_summary`, `policy_last_checked`, `important_caveats`
- `images`: each uploaded image exactly once with `image_id`, `filename`, `role`, `role_confidence`, `secondary_tags`, `recommended_position_amazon`, `recommended_position_flipkart`, `visual_quality_score`, `policy_risk`, `product_accuracy`, `observations`, `issues`, `improvement_suggestions`, `seller_confirmation_needed`, and `source_citations`
- `gallery_order_amazon` and `gallery_order_flipkart`
- `missing_image_types`
- `reference_comparison` entries for listing/reference image pairs with specific visual evidence
- `marketplace_summary` with separate Amazon and Flipkart status, checked rules, failures, verifies, and citations

Each issue must include: severity, title, evidence, why_it_matters, exact_fix, affected_marketplaces, and whether the fix is a confirmed requirement or a recommendation.

### AI chat assistant

Add a persistent chat panel titled **Ask HOVEN AI** next to/below the audit results. It must:
- Answer naturally in Hindi, Hinglish, or English based on the user's language.
- Know the current audit, image IDs/filenames, detected roles, exact issue list, gallery orders, product facts, reference photos, and the policy-source notes.
- Support follow-ups such as: “Image 2 mein kya problem hai?”, “Isko first image rakh sakte hain?”, “Designer ko exact correction message likh do”, “Amazon aur Flipkart mein kya difference hai?”, “Kaunsi image missing hai?”, “Product original se compare karo”.
- Cite policy URLs when making policy claims and explain uncertainty.
- Ask for missing seller facts only when needed. Never hallucinate missing product specifications.
- Preserve context while the audit session is active. Add clear “new chat / clear audit” controls.

### Dashboard and UX

Create a premium professional dashboard inspired by a modern SaaS audit console. Use HOVEN's premium identity: navy blue, white, cool grey, restrained chrome/silver accent, clear typography, clean icons, generous spacing.

Navigation:
- Dashboard
- New Image Audit
- Audit History
- Product Library
- Marketplace Rules
- Reports
- Settings

Dashboard cards must show real data only: audits run, images analysed, high-risk images, images needing review, average visual-quality score. Empty state before first scan.

New Image Audit screen:
- Marketplace selector: Amazon India / Flipkart / Both.
- Product details form.
- Separate drag/drop boxes for listing images and original reference photos.
- Preview thumbnails with filename and remove action.
- Analyse button.

Results screen:
- Overall status and summary.
- Separate Amazon and Flipkart findings.
- Two proposed gallery sequences with drag-and-drop reorder.
- Image cards showing thumbnail, detected role, confidence, recommended position, quality score, policy risk, product-accuracy finding, issue list, and exact fix.
- Show image-level source citations for policy issues.
- Mark unresolved/seller-confirmation items clearly.
- Quick filter: All / High risk / Needs review / Likely OK / By image role.

History and privacy:
- Do not save uploaded product images permanently by default.
- Give the user an explicit “Save this audit” choice before persistent storage.
- If Firebase is provisioned, use Firebase Authentication and Firestore for audit metadata/history only; store images in private object storage only with explicit consent and deletion controls. Do not make images public.
- Provide delete audit and delete stored files controls.
- If persistent database/storage is not configured, clearly state that audit history is session-only; do not simulate persistence.

### Engineering requirements

- Build a robust React + Node full-stack app with accessible responsive layout for desktop and mobile.
- Use server routes for Gemini calls; the browser must never import `@google/genai` with credentials or call Gemini using a key in client code.
- Use `@google/genai` SDK and `process.env.GEMINI_API_KEY` in server-side code. Let AI Studio Build configure the secret automatically.
- Use file validation: supported image MIME types, maximum size limits, maximum file count, and safe error handling.
- Compress/resize oversized images server-side for model input while preserving readable details. Preserve originals only if user explicitly saves them.
- Add request timeouts, retries for transient errors, rate limits, and clear error messages.
- Validate and sanitize all AI JSON output. Never render raw model HTML.
- Do not log raw image bytes, API keys, or sensitive product uploads.
- Add tests for classification response validation, duplicate/missing image IDs, failed Gemini connection, empty upload, unsupported MIME type, policy `VERIFY` handling, and no false approval fallback.
- Add a visible AI connection status that is backed by a real server health check.
- Do not say online/connected until a real server-side Gemini health request succeeds.
- Add a concise About / Limitations section explaining that this is an advisory tool, not an official marketplace validator.

### Completion checks

Before declaring the app ready:
1. Run the app and fix build/runtime errors.
2. Upload a small set of sample images and verify Gemini actually classifies the image contents (not filenames or upload order).
3. Verify image-role classifications can be manually corrected.
4. Verify the assistant can answer a follow-up question about a specific uploaded image using current session context.
5. Simulate a Gemini API failure and confirm the app displays “Not analysed”, never a pass/approval.
6. Verify policy checks show source links and “VERIFY” when official details are inaccessible.
7. Verify no Gemini key is present in client bundle/network responses.
8. Do not claim deployment is complete until the Publish action returns a live URL.

Build the actual working app now. Do not stop at a plan, wireframe, or static mockup. If any Firebase/database feature requires user permission, ask at the time it is required and keep the rest of the app working without fabricating saved history.

---

## END BUILD PROMPT
