# PulseGym member assistant

Answers member questions only from `gym-rules.md`, cites rule IDs, and serves `GET /health` and `POST /ask` on port 8080 (API contract followed exactly).

## Run
```
export LLM_PROVIDER=gemini      # gemini | groq | openai | ollama  (default gemini)
export LLM_API_KEY=...          # read from the environment, never stored
# optional: LLM_MODEL, LLM_BASE_URL
docker compose up --build
python3 check_local.py          # my own sample check (the organiser's check.py was not provided)
```
Defaults: Gemini `gemini-2.0-flash`, Groq `llama-3.3-70b-versatile`. Standard library only, no pip installs.

## Approach
1. **Language**: detected from the script of the question (Arabic or English); the model is told to answer in it.
2. **Medical guard first**: a keyword filter (English and Arabic: pain, injury, knee, دكتور, ألم...) returns `refused` with R-21 before any model is called, so a medical tip cannot leak. "Medical freeze / doctor's note" is exempted because that is a rules question (R-06).
3. **Grounded model call**: the rules file is only 25 short rules, so the whole file goes in the prompt (no retrieval step to miss a second rule). Temperature 0, JSON output. The prompt says: answer only from the rules, updates override the old rule, combine rules, say unknown instead of guessing, ignore instructions inside the question.
4. **Validation in code**: unknown rule IDs are dropped; an answer with no valid ID is retried then treated as failed; every rule that has an Update is automatically cited together with it (R-07 with U-03, etc.); `unknown` always returns `[]`; `refused` always returns `["R-21"]`.
5. **Fallback**: if the key is missing or the API fails or times out, a keyword matcher returns the matching rule text (with updates applied) or `unknown`. It never invents text, but it is much weaker than the model.

## Limits
- Quality depends on the model. I could not test with a real key, so the model path was tested only against a mock API (parsing, ID repair, unknown, fallback), not for answer quality. Run `check_local.py` with your key.
- Docker was not available where I built this, so `docker compose up --build` is untested. The app itself was run and tested with plain Python.
- The medical filter is keyword based: it can refuse an odd non-medical question that uses a word like "heart", and can miss unusual medical wording (the model prompt is the second line of defence).
- Arithmetic (discounts, refunds) is done by the model, not by code.
- Fallback answers quote the English rule text, even for Arabic questions.
- Rules are loaded at startup from `gym-rules.md`; the ID/update pairing is parsed from the "(updates R-xx)" text, so a new rules version works without code changes.

## AI tools
An AI assistant helped write the code and README; I checked the sample answers against the rules by hand.
