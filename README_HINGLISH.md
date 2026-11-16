# HOVEN AI Auditor — Gemini AI Studio starter pack

## Is pack mein kya hai?
- `HOVEN_GEMINI_AI_STUDIO_BUILD_PROMPT.md` — complete prompt jo Google AI Studio Build mode mein paste karna hai.
- `reference/policy_sources_2026-11-14.json` — pehle project ka policy starting snapshot; ise current final policy na samjhein. App ko official sources se re-verify karna chahiye.

## Kaise use karein
1. Google AI Studio kholein: https://aistudio.google.com/
2. Build mode select karein.
3. `HOVEN_GEMINI_AI_STUDIO_BUILD_PROMPT.md` open karein.
4. `BUILD PROMPT` section ke andar ka poora prompt copy karke AI Studio ke prompt box mein paste karein.
5. Build run karein. AI Studio ko React frontend aur Node.js server ke saath app banana chahiye.
6. AI Studio Build mein Gemini API key ko server-side secret ke roop mein automatically configure kiya jata hai; aapko manually key paste nahi karni chahiye.
7. Preview mein actual image set upload karke test karein, phir build errors aur audit output verify karein.
8. Jab testing theek ho, Publish se live app deploy karein. Deployment availability aur billing Google account eligibility par depend kar sakti hai.

## Important
- Ye starter pack/prompt hai; ye khud se aapke Google account mein app create ya publish nahi karta.
- Google AI Studio Build mode mein prompt chalana aur Publish click karna user ko apne Google account se karna hoga.
- API key automatically manage hone ka matlab AI usage unlimited/free hona nahi hai. Usage quotas and possible charges apply.
- Gemini AI public marketplace policy information ko audit kar sakta hai, lekin Amazon/Flipkart ke private ranking algorithms ya internal approval systems access nahi kar sakta.
- Flipkart ke category-specific rules agar Seller Hub login ke peeche hon, toh app ko `VERIFY IN SELLER HUB` dikhana chahiye; guess karke pass nahi dena chahiye.
