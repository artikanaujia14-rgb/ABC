# Gemini technical notes

- Google announced the Gemini Interactions API as its primary interface for Gemini models and agents and recommends it for new projects.
- The Google AI Studio docs say Interactions API is generally available and recommended for new projects as of June 2026.
- JavaScript example in current docs uses `@google/genai` and `client.interactions.create(...)`.
- Current getting-started docs say Gemini API requests require a project API key; Google AI Studio can automatically create a project and API key for new users. Keep the credential server-side and do not paste it into source code.
- Free-tier access has limits and different data-use terms from paid access. Confirm current model eligibility, quota and data-use terms in AI Studio before uploading confidential product designs.

Official references:
- https://blog.google/innovation-and-ai/technology/developers-tools/interactions-api-general-availability/
- https://aistudio.google.com/docs/interactions-overview
- https://aistudio.google.com/docs/get-started
- https://ai.google.dev/gemini-api/docs/pricing
