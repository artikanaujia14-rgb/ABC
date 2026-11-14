# HOVEN Online AI Image Auditor (Cloud AI MVP)

This is an **online-ready web application project**, not an offline HTML checker. The browser sends uploaded listing images to a FastAPI backend. The backend calls a vision-capable OpenAI model through the **Responses API**. The API key stays on the server and is never sent to browser JavaScript.

## What this MVP does

- Upload up to 12 listing images plus up to 8 original product reference photos.
- Select Amazon India, Flipkart, or both.
- Ask the AI to classify every listing image: main-product candidate, lifestyle, feature infographic, dimensions, installation, close-up, package contents, brand/trust, comparison, or other.
- Recommend an image-gallery sequence rather than assuming upload order equals final listing order.
- Review images individually and as a set.
- Compare listing images with original product reference photos for visible differences in shape, colour, finish, handle, joints, threads, and components. This is a visual comparison, not a physical product inspection.
- Produce separate marketplace checks, with uncertain Flipkart rules marked for Seller Hub verification.
- Chat with the AI about the active audit, in Hindi or English.
- Export the structured audit report as JSON.
- Display no offline approval fallback. If the cloud AI key is missing or the API fails, analysis fails visibly; no image is auto-approved.

## What it does NOT claim

- It cannot access Amazon's or Flipkart's private ranking/recommendation algorithms or internal moderation systems.
- It cannot guarantee listing approval, search visibility, sales, or ranking.
- It cannot prove PTMT/brass/plastic grade, thread size, pressure rating, leak-proof performance, durability, or included accessories from an image alone. Supply verified product specifications/test evidence and review seller-confirmation flags.
- The current Flipkart Seller Hub image guide may require seller login. The app therefore avoids inventing category-wide rules and marks inaccessible/current category-specific checks as `verify`.

## Run locally (developer test only)

1. Install Python 3.11+.
2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` with a key from your OpenAI API project. Never paste the key into chat or frontend code.
3. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

4. Load environment variables and start the server:

   ```bash
   # macOS/Linux
   export OPENAI_API_KEY="..."
   uvicorn app:app --host 0.0.0.0 --port 8000

   # Windows PowerShell
   $env:OPENAI_API_KEY="..."
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

5. Open `http://localhost:8000`.

The browser alone is not enough. The FastAPI backend must be running and able to reach the OpenAI API.

## Deploy online (example: Render Web Service using Docker)

1. Create a private Git repository and upload this project folder.
2. In Render, create a **Web Service** connected to that repository and select Docker as the runtime.
3. Add environment variables in the hosting dashboard:
   - `OPENAI_API_KEY` = your API key (server-side secret)
   - `OPENAI_VISION_MODEL` = a vision-capable model available to your API project (default: `gpt-4.1`)
4. Deploy. The container listens on `$PORT`.
5. Open the HTTPS URL from your host. Test `/api/health`; it should show `ai_connected: true`.
6. Upload a small test set and verify that the report is AI-produced. Remove or replace any test image you do not want to retain.

Hosting provider choice, domain, access settings and billing are controlled by the account owner. This project has not been deployed to a public domain.

## Production work still required before staff/business rollout

This is a cloud-connected MVP scaffold. Before using it with a team or sensitive commercial assets, add:

- User login, roles and access controls.
- Persistent database and private object storage with deletion/retention controls.
- Rate limiting, malware/content validation, request-size limits at the reverse proxy, audit logs and backups.
- Background job queue for large catalog batches.
- Policy source update workflow with source date/version, category and country scope, human review and change log.
- Automated tests and monitoring.
- A dedicated review of data processing, vendor terms and image retention settings.

The current MVP stores active audit image data in server process memory for up to the configured session TTL. Restarting the service or running multiple server workers can lose session state. Do not treat this as production-grade persistent storage.

## Policy source notes

The `policy_sources.json` file lists the source URLs and the date they were checked. It is a starting policy snapshot, not a live guarantee. Review the linked Seller Central / Seller Hub pages before each major policy-rule update and before uploading a listing.
