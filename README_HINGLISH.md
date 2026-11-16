# HOVEN AI Auditor — Gemini-only AI Studio starter pack

## Is pack mein kya hai?
- `HOVEN_GEMINI_AI_STUDIO_BUILD_PROMPT.md` — complete Gemini-only prompt jo Google AI Studio Build mode mein paste karna hai.
- `GEMINI_ONLY_LOCKDOWN_PROMPT.md` — agar app pehle se AI Studio mein ban chuki hai, toh usi Build chat mein ye prompt paste karke project ka audit/refactor karwayein.
- `reference/policy_sources_2026-11-14.json` — pehle project ka policy starting snapshot; ise current final policy na samjhein. App ko official sources se re-verify karna chahiye.

## Kaise use karein
1. Google AI Studio kholein: https://aistudio.google.com/
2. Build mode select karein.
3. `HOVEN_GEMINI_AI_STUDIO_BUILD_PROMPT.md` open karein.
4. `BUILD PROMPT` section ke andar ka poora prompt copy karke AI Studio ke prompt box mein paste karein.
5. Build run karein. AI Studio ko React frontend aur Node.js server ke saath app banana chahiye.
6. AI Studio project ke Gemini credentials/usage ko use karein. Google ke current getting-started guide ke mutabik naye users ke liye AI Studio project aur API key automatically create kar sakta hai; app ke source code mein key paste na karein. Agar Build Mode secret configuration maange, toh sirf AI Studio ke secure Secrets/credential controls use karein.
7. App ke andar image analysis, classification, comparison, chat aur reports ke liye sirf Gemini hoga—ChatGPT/OpenAI ya kisi doosre AI provider ka code/fallback nahi hoga.
8. Preview mein actual image set upload karke test karein, phir build errors aur audit output verify karein.
9. Jab testing theek ho, Publish se live app deploy karein. Deployment availability aur billing Google account eligibility par depend kar sakti hai.

## Important
- Ye starter pack/prompt hai; ye khud se aapke Google account mein app create ya publish nahi karta.
- Google AI Studio Build mode mein prompt chalana aur Publish click karna user ko apne Google account se karna hoga.
- Gemini-only hone ka matlab unlimited/free usage nahi hai. AI Studio/Gemini ke free-tier quotas, model availability aur data-use terms apply hote hain; free tier par uploaded content ke data-use terms ko dhyan se padhein. Paid tier mein usage charges lag sakte hain.
- Gemini AI public marketplace policy information ko audit kar sakta hai, lekin Amazon/Flipkart ke private ranking algorithms ya internal approval systems access nahi kar sakta.
- Flipkart ke category-specific rules agar Seller Hub login ke peeche hon, toh app ko `VERIFY IN SELLER HUB` dikhana chahiye; guess karke pass nahi dena chahiye.


## AI provider lock
- Is software mein sirf Google Gemini hoga. ChatGPT/OpenAI API, SDK, model, ya fallback kabhi use nahi hoga.
- Google ka current recommended interface Gemini Interactions API hai; Build prompt ko latest official Google SDK/docs follow karne ko kaha gaya hai.
- Google documents ke mutabik Gemini API authentication ke liye project key/credential hota hai. “Manual key paste nahi karna” ka matlab secure Google AI Studio credential setup use karna hai—not that authentication is unnecessary.
