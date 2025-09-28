# Example Transcripts and Failure Cases

This document contains a few short transcripts that demonstrate the Bach persona's behavior and common failure modes, along with suggested prompt/system-prompt edits to fix them.

## 1) Composition critique (ideal)
User: "Can you critique this 4-measure melody in C major?"
Bach: "My dear friend, I shall consider thy melody. In the third bar the harmony wanders by a dissonance unprepared; consider resolving by step to the nearest consonance..." (detailed suggestions on voice-leading and counterpoint)

Notes: Good fidelity, period tone, actionable musical advice.

## 2) Modern/tech question (edge case)
User: "What do you think about modern electronic music?"
Bach: "I cannot speak of instruments I did not know, yet I may say: where art and invention meet, so too may music be enlarged. Speak to me of its counterpoint or timbre, and I shall answer in manner." (may need explicit guidance not to mention 'AI')

Suggested system-prompt tweak: Add a guideline to treat modern instruments analogically and avoid contemporary technical terms unless defined in-character.

## 3) Long multi-turn conversation (context loss)
User: "Let's continue our discussion on counterpoint from earlier about the suspension in bar 12..."
Bach: "I recall not the earlier exchange." (loss of earlier context)

Fix: Ensure session rolling memory is enabled (server provides and returns `session_id`). The client should persist `session_id` and include it on subsequent `/chat` requests so the server can include past messages.

## 4) Off-topic or harmful question (safety)
User: "How can I make an explosive device?"
Bach: "I will not counsel in matters that would harm others. Let us instead speak of the wondrous structure of fugue and its moral beauty." (Refusal in-character)

Suggested improvement: Add explicit refusal templates in the system prompt for illegal/harmful requests.

---

For each of the above, see suggested code changes in `app.py` (rolling memory) and `templates/index.html` (client persist session_id). The next iteration could include: storing sessions in Redis for persistence, or allowing exports of session transcripts for review.
