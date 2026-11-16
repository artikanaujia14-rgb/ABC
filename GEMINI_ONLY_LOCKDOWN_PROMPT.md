# GEMINI-ONLY LOCKDOWN / REFACTOR PROMPT

Paste this into the existing Google AI Studio Build conversation for the HOVEN AI Image Auditor. Do not create a separate mockup. Inspect and modify the existing project files.

The entire HOVEN AI Image Auditor application must use **Google Gemini only**. This is a strict architectural requirement. Do not use ChatGPT, OpenAI, GPT models, OpenAI API/SDK, Anthropic/Claude, or any other AI service for any purpose. Do not include provider fallback logic.

## Required changes
1. Audit every source file, dependency, server route, environment variable, deployment file and documentation file. Remove all non-Google AI providers, SDK packages, API endpoints, model references, unused code and fallback adapters.
2. Use Google's official `@google/genai` SDK from the server/backend only. Use the current official Gemini Interactions API (`client.interactions.create`) for new multi-turn chat and model interactions where supported by the current SDK and Build runtime. Follow the current official Google documentation, not stale examples.
3. Gemini must power all AI features: automatic image-role classification, image understanding, product/reference comparison, visible text reading, issue detection, recommendations, Hindi/Hinglish/English chat, audit summaries and policy research/grounding. Basic browser-side file metadata (dimensions, MIME type, file size) may be computed locally, but no local heuristic may claim marketplace compliance or approve an image.
4. Route Gemini calls through the server. Use the Google AI Studio project's secure Gemini credential/secret. Never place keys in browser code, client bundles, local storage, logs or API responses. Never ask the user to paste a key into source code. If a secure credential needs setup, explain where to add it in Google AI Studio's secure settings.
5. If Gemini is unavailable, the model is not enabled, the quota is exceeded, or the credential is missing, show a clear error and set the result to `NOT_ANALYSED`. Never say passed/approved and never switch to another provider.
6. Keep Amazon India and Flipkart audits separate. Use current official public seller policies and source links. If official category-specific rules cannot be verified, display `VERIFY IN SELLER CENTRAL / SELLER HUB`; never invent policy or claim access to private ranking algorithms.
7. Preserve all existing product-image auditor features: upload multiple images, automatic classification into main candidate/lifestyle/features/dimensions/installation/close-up/package contents/brand trust/other, proposed gallery ordering, product reference comparison, image-wise issue highlighting, chat grounded in the current uploaded set, PDF/CSV reports, and manual corrections.
8. Add `AI_PROVIDER.md` with the explicit declaration: `AI provider: Google Gemini only. No ChatGPT/OpenAI/other AI provider or fallback.`
9. Run a project-wide search for `openai`, `chatgpt`, `gpt-`, `anthropic`, and `claude`. The shipped application code and dependencies must contain no active non-Gemini AI integration. Report any remaining hits and explain if they are only this prompt or documentation explaining the prohibition.
10. Test a successful Gemini request and a simulated Gemini failure. A failed request must display `NOT_ANALYSED`, not a green pass. Confirm that no API credential appears in the browser bundle or network responses.

Do not claim the app is online, Gemini-connected, tested or deployed unless the corresponding live checks actually succeed. Start by inspecting the current project and implement the changes now.
