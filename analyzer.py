# analyzer.py

from openai import OpenAI
client = OpenAI()

ANALYSIS_PROMPT = """
Eres un sistema avanzado de análisis de contenido con enfoque en:
- geopolítica
- inteligencia artificial
- conspiraciones verificables
- amenazas reales
- islam (con respeto y precisión)
- finanzas y negocios
- detección de estafas
- detección de manipulación o control social
- identificación de patrones psicológicos
- advertencias de desinformación
- detección de mensajes ocultos o agendas

Evalúa objetivamente el contenido entregado.

Entregas SIEMPRE un JSON con esta estructura:

{
  "summary": "...",
  "key_points": [...],
  "risk_flags": {
    "disinformation": false,
    "manipulation": false,
    "psychological_patterns": false,
    "hidden_messages": false,
    "scam_risk": false
  },
  "categories": {
    "geopolitics": false,
    "ai": false,
    "conspiracy": false,
    "islam": false,
    "threats": false,
    "finance": false,
    "educational": false
  },
  "source_reliability_score": 0.0,
  "importance_score": 0.0,
  "should_watch": false,
  "urgency": "baja"
}

No hagas texto fuera del JSON.
"""

def analyze_transcript(transcript_text: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": ANALYSIS_PROMPT},
            {"role": "user", "content": transcript_text}
        ]
    )

    return response.choices[0].message["content"]
