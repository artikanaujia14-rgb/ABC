from __future__ import annotations

import base64
import json
import os
import re
import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
STATIC_DIR = BASE_DIR / "static"
RULES_PATH = BASE_DIR / "policy_sources.json"
MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1")
MAX_IMAGE_BYTES = int(os.getenv("MAX_IMAGE_BYTES", str(15 * 1024 * 1024)))
MAX_IMAGES = int(os.getenv("MAX_IMAGES", "12"))
SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", "7200"))

app = FastAPI(title="HOVEN Online AI Image Auditor", version="0.2.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Prototype session store. Replace with Redis/object storage/database for production.
SESSIONS: dict[str, dict[str, Any]] = {}

SYSTEM_PROMPT = """You are HOVEN's ecommerce product-image auditor and visual listing assistant.
You review images for Amazon India and Flipkart using only the policy information supplied in the request.
Never claim access to private marketplace ranking algorithms, internal moderation systems, or seller account QC.
Never guarantee approval, visibility, ranking, conversion, or sales.
Use three statuses only: HIGH_RISK, NEEDS_REVIEW, LIKELY_OK. LIKELY_OK means no issue was detected in the available checks, not official platform approval.
Separate observed visual facts from inferences and from facts that need seller confirmation.
Do not assert material, fitment, leak-proof performance, durability, dimensions, or included accessories from appearance alone.
Automatically classify every image into exactly one role: MAIN_PRODUCT_CANDIDATE, LIFESTYLE, FEATURE_INFOGRAPHIC, DIMENSIONS, INSTALLATION, CLOSE_UP_DETAIL, PACKAGE_CONTENTS, BRAND_TRUST, COMPARISON, OTHER.
Recommend an order for a typical listing set. Put the best compliant main-product candidate first; then useful supporting images. Do not mistake file upload order for marketplace slot order.
For Amazon India, apply the supplied current public rules precisely. Pay special attention to the MAIN image: pure white RGB 255,255,255 background; entire product visible; product approximately 85% of image; no added text, seller logo, watermark, border, graphics, props/accessories not included; accurately depict colour/scale/quantity. The current Seller Central guide says image longest side 500–10,000 px, JPEG/TIFF/PNG/non-animated GIF, RGB preferred, 1,000+ pixels recommended for zoom. Also apply supplied all-image requirements; if rules conflict or category-specific applicability is unclear, mark as verify in Seller Central.
For Flipkart, do not invent precise current category requirements. The official seller image-guidelines page may require Seller Hub access; rely only on facts explicitly supplied in the policy notes. Mark uncertain points as VERIFY_IN_SELLER_HUB.
Classify infographics and lifestyle images by their visual role, but do not automatically mark them compliant. For Amazon India, the supplied public guide says no text or pricing details on product images (except swatch images); flag overlay/text-heavy secondary graphics for policy verification or high risk according to the supplied source notes. Never assume a common ecommerce practice overrides the platform policy.
Be specific and actionable. Be frank about uncertainty. Respond naturally in Hindi/Hinglish if the user writes that way.
"""

ROLE_LABELS = {
    "MAIN_PRODUCT_CANDIDATE": "Main product candidate",
    "LIFESTYLE": "Lifestyle / in-use",
    "FEATURE_INFOGRAPHIC": "Features / infographic",
    "DIMENSIONS": "Dimensions / measurements",
    "INSTALLATION": "Installation / how-to",
    "CLOSE_UP_DETAIL": "Close-up / product detail",
    "PACKAGE_CONTENTS": "Package contents / accessories",
    "BRAND_TRUST": "Brand / trust image",
    "COMPARISON": "Comparison image",
    "OTHER": "Other",
}


def load_policy_sources() -> dict[str, Any]:
    try:
        return json.loads(RULES_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"checked_date": "not available", "marketplaces": {}}


def get_client() -> OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise HTTPException(status_code=503, detail="AI is not connected yet. Add OPENAI_API_KEY to the server environment, then restart the app.")
    return OpenAI(api_key=key)


def cleanup_sessions() -> None:
    now = time.time()
    expired = [sid for sid, data in SESSIONS.items() if now - data.get("updated", now) > SESSION_TTL_SECONDS]
    for sid in expired:
        SESSIONS.pop(sid, None)


def extract_output_text(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text.strip()
    chunks: list[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            if getattr(content, "type", "") in ("output_text", "text"):
                chunks.append(getattr(content, "text", ""))
    return "\n".join(chunks).strip()


def parse_json_response(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I)
    try:
        obj = json.loads(cleaned)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", cleaned, flags=re.S)
    if match:
        try:
            obj = json.loads(match.group(0))
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
    raise HTTPException(status_code=502, detail="The AI returned an unreadable report. Please retry with fewer or smaller images.")


def image_metadata(raw: bytes, filename: str, content_type: str) -> dict[str, Any]:
    try:
        im = Image.open(BytesIO(raw))
        width, height = im.size
        fmt = (im.format or "unknown").upper()
        mode = im.mode
    except Exception:
        raise HTTPException(status_code=400, detail=f"Cannot read image: {filename}")
    longest = max(width, height)
    return {
        "width": width,
        "height": height,
        "format": fmt,
        "mode": mode,
        "bytes": len(raw),
        "longest_side": longest,
        "content_type": content_type,
    }


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {
        "status": "online",
        "ai_connected": bool(os.getenv("OPENAI_API_KEY")),
        "model": MODEL,
        "policy_checked_date": load_policy_sources().get("checked_date"),
        "note": "If ai_connected is false, image analysis and chat are unavailable. No offline approval fallback is used.",
    }


@app.get("/api/policies")
def policies():
    return load_policy_sources()


@app.post("/api/analyze")
async def analyze(
    files: list[UploadFile] = File(...),
    marketplace: str = Form("both"),
    product_name: str = Form(""),
    sku: str = Form(""),
    brand: str = Form("HOVEN"),
    category: str = Form("Bathroom fittings"),
    product_facts: str = Form(""),
    reference_files: list[UploadFile] = File(default=[]),
):
    cleanup_sessions()
    if len(files) < 1 or len(files) > MAX_IMAGES:
        raise HTTPException(status_code=400, detail=f"Upload between 1 and {MAX_IMAGES} images per audit.")
    allowed = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/tiff"}
    image_items: list[dict[str, Any]] = []
    input_content: list[dict[str, Any]] = []
    for index, upload in enumerate(files, start=1):
        content_type = upload.content_type or "application/octet-stream"
        if content_type not in allowed:
            raise HTTPException(status_code=400, detail=f"Unsupported image format for {upload.filename}. Use JPEG, PNG, WEBP, GIF or TIFF.")
        raw = await upload.read()
        if not raw or len(raw) > MAX_IMAGE_BYTES:
            raise HTTPException(status_code=400, detail=f"{upload.filename} is empty or exceeds the {MAX_IMAGE_BYTES // (1024*1024)} MB limit.")
        meta = image_metadata(raw, upload.filename or f"image-{index}", content_type)
        mime = content_type if content_type != "image/tiff" else "image/png"
        if content_type == "image/tiff":
            # TIFF decoding is handled by Pillow and converted to PNG for vision input.
            im = Image.open(BytesIO(raw)).convert("RGB")
            buf = BytesIO(); im.save(buf, format="PNG")
            raw_for_ai = buf.getvalue(); mime = "image/png"
        else:
            raw_for_ai = raw
        data_url = f"data:{mime};base64," + base64.b64encode(raw_for_ai).decode("ascii")
        item_id = str(uuid.uuid4())
        image_items.append({
            "id": item_id,
            "filename": upload.filename or f"image-{index}",
            "metadata": meta,
            "data_url": data_url,
            "manual": False,
        })
        input_content.append({"type": "input_text", "text": f"IMAGE_ID={item_id}; FILE={upload.filename}; METADATA={json.dumps(meta)}"})
        input_content.append({"type": "input_image", "image_url": data_url, "detail": "high"})

    reference_items: list[dict[str, Any]] = []
    if len(reference_files) > 8:
        raise HTTPException(status_code=400, detail="Upload no more than 8 original reference photos.")
    for index, upload in enumerate(reference_files, start=1):
        content_type = upload.content_type or "application/octet-stream"
        if content_type not in allowed:
            raise HTTPException(status_code=400, detail=f"Unsupported reference image format for {upload.filename}.")
        raw = await upload.read()
        if not raw or len(raw) > MAX_IMAGE_BYTES:
            raise HTTPException(status_code=400, detail=f"Reference photo {upload.filename} is empty or exceeds the size limit.")
        meta = image_metadata(raw, upload.filename or f"reference-{index}", content_type)
        mime = content_type if content_type != "image/tiff" else "image/png"
        if content_type == "image/tiff":
            im = Image.open(BytesIO(raw)).convert("RGB")
            buf = BytesIO(); im.save(buf, format="PNG")
            raw_for_ai = buf.getvalue(); mime = "image/png"
        else:
            raw_for_ai = raw
        data_url = f"data:{mime};base64," + base64.b64encode(raw_for_ai).decode("ascii")
        ref_id = str(uuid.uuid4())
        reference_items.append({"id": ref_id, "filename": upload.filename or f"reference-{index}", "metadata": meta, "data_url": data_url})
        input_content.append({"type": "input_text", "text": f"ORIGINAL_REFERENCE_ID={ref_id}; FILE={upload.filename}; METADATA={json.dumps(meta)}. This is genuine reference photography, not a listing image."})
        input_content.append({"type": "input_image", "image_url": data_url, "detail": "high"})

    rules = load_policy_sources()
    requested = marketplace.lower()
    market_context = rules.get("marketplaces", {})
    prompt = f"""Audit this product image set for marketplace={requested}.
Product name: {product_name or 'not provided'}
SKU: {sku or 'not provided'}
Brand: {brand or 'not provided'}
Category: {category or 'not provided'}
Seller-provided product facts/specifications (treat as seller claims, do not infer beyond them): {product_facts or 'not provided'}
Current policy source notes: {json.dumps(market_context, ensure_ascii=False)}

The listing image entries are each labelled with IMAGE_ID and metadata, followed by the image itself. Original reference photos, if present, are labelled ORIGINAL_REFERENCE_ID. Include only listing images in the items array and recommended_gallery_order; reference photos are comparison inputs, not listing slots. Compare listing images with original reference photos for visible differences in shape, colour, finish, handle, joints, threads and components. Describe only visible differences; never claim technical performance or exact material from appearance alone. Analyse the full listing set collectively and each listing image individually. Detect which file is the main-product candidate, lifestyle, infographic/features, dimensions, installation, close-up, package contents, brand/trust, comparison, or other. Recommend a sequence number for a listing gallery, and explain why.
Return ONLY valid JSON with this exact top-level shape:
{{
  "overall_status":"HIGH_RISK|NEEDS_REVIEW|LIKELY_OK",
  "overall_summary":"short plain-language summary",
  "recommended_gallery_order":[{{"image_id":"...","position":1,"reason":"..."}}],
  "missing_image_types":["..."],
  "items":[{{
    "image_id":"...",
    "filename":"...",
    "role":"one exact role key from the system prompt",
    "role_confidence":0.0,
    "recommended_position":1,
    "status":"HIGH_RISK|NEEDS_REVIEW|LIKELY_OK",
    "observations":["visible facts only"],
    "issues":[{{"severity":"critical|high|medium|low|info","title":"...","evidence":"what is visible or measured","why_it_matters":"...","fix":"specific corrective action","marketplaces":["amazon","flipkart"]}}],
    "platform_checks":{{
      "amazon":{{"status":"HIGH_RISK|NEEDS_REVIEW|LIKELY_OK|NOT_SELECTED","checks":[{{"rule":"...","result":"pass|fail|verify","evidence":"...","source_key":"..."}}]}},
      "flipkart":{{"status":"HIGH_RISK|NEEDS_REVIEW|LIKELY_OK|NOT_SELECTED","checks":[{{"rule":"...","result":"pass|fail|verify","evidence":"...","source_key":"..."}}]}}
    }},
    "improvement_suggestions":["..."],
    "seller_confirmation_needed":["..."]
  }}],
  "important_caveats":["..."],
  "policy_last_checked":"{rules.get('checked_date','unknown')}"
}}
Do not fabricate IDs. Include every uploaded image exactly once in items and recommended_gallery_order. If the evidence is insufficient, use verify / NEEDS_REVIEW. Do not issue blanket passes. In particular, don't claim technical claims such as 15mm fit, PTMT material, leak-proof, or durability are validated merely from the image."""
    input_content.insert(0, {"type": "input_text", "text": prompt})
    client = get_client()
    try:
        response = client.responses.create(
            model=MODEL,
            input=[
                {"role": "system", "content": [{"type": "input_text", "text": SYSTEM_PROMPT}]},
                {"role": "user", "content": input_content},
            ],
        )
        report = parse_json_response(extract_output_text(response))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {str(exc)[:350]}")

    sid = str(uuid.uuid4())
    SESSIONS[sid] = {
        "created": time.time(), "updated": time.time(),
        "images": image_items, "reference_images": reference_items, "report": report,
        "context": {"marketplace": requested, "product_name": product_name, "sku": sku, "brand": brand, "category": category, "product_facts": product_facts},
        "history": [],
    }
    # Do not return the base64 source images to the browser; preview is created client-side.
    sanitized = []
    for item in image_items:
        sanitized.append({"id": item["id"], "filename": item["filename"], "metadata": item["metadata"]})
    return {"session_id": sid, "report": report, "images": sanitized, "model": MODEL, "policy_sources": rules.get("sources", {})}


@app.post("/api/chat")
async def chat(payload: dict[str, Any]):
    cleanup_sessions()
    sid = str(payload.get("session_id", ""))
    message = str(payload.get("message", "")).strip()
    if not message:
        raise HTTPException(status_code=400, detail="Enter a question for the AI assistant.")
    if len(message) > 4000:
        raise HTTPException(status_code=400, detail="Question is too long (maximum 4,000 characters).")
    session = SESSIONS.get(sid)
    if not session:
        raise HTTPException(status_code=404, detail="This audit session has expired. Please upload and analyse the images again.")
    client = get_client()
    rules = load_policy_sources()
    context = session.get("context", {})
    report_text = json.dumps(session.get("report", {}), ensure_ascii=False)[:28000]
    content: list[dict[str, Any]] = [{"type": "input_text", "text": f"Audit report context: {report_text}\nProduct context: {json.dumps(context, ensure_ascii=False)}\nPolicy notes: {json.dumps(rules.get('marketplaces', {}), ensure_ascii=False)}\nUser question: {message}"}]
    # Attach the analyzed images again so the assistant can discuss exact visual details.
    for item in session.get("images", [])[:MAX_IMAGES]:
        content.append({"type": "input_text", "text": f"Listing image reference {item['id']} / {item['filename']} / {json.dumps(item['metadata'])}"})
        content.append({"type": "input_image", "image_url": item["data_url"], "detail": "high"})
    for item in session.get("reference_images", [])[:8]:
        content.append({"type": "input_text", "text": f"Original product reference photo {item['id']} / {item['filename']} / {json.dumps(item['metadata'])}"})
        content.append({"type": "input_image", "image_url": item["data_url"], "detail": "high"})
    history = session.get("history", [])[-8:]
    input_messages = [{"role": "system", "content": [{"type": "input_text", "text": SYSTEM_PROMPT + "\nYou are also a conversational consultant. Answer follow-up questions grounded in this audit and supplied policy notes. If the user asks which image to change, reference filename and image role. Clearly separate observed facts, suggestions, and seller confirmations."}]}]
    for msg in history:
        input_messages.append({"role": msg["role"], "content": msg["content"]})
    input_messages.append({"role": "user", "content": content})
    try:
        response = client.responses.create(model=MODEL, input=input_messages)
        answer = extract_output_text(response)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI chat failed: {str(exc)[:350]}")
    session["history"].append({"role": "user", "content": [{"type": "input_text", "text": message}]})
    session["history"].append({"role": "assistant", "content": [{"type": "output_text", "text": answer}]})
    session["updated"] = time.time()
    return {"answer": answer, "model": MODEL}


@app.get("/api/session/{session_id}/report")
def get_report(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Audit session not found or expired.")
    return JSONResponse({"report": session.get("report"), "context": session.get("context")})
