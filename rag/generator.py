import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(query: str, context_docs: list, user_id: str) -> str:
    context = "\n\n---\n".join(
        f"[Source: {d.metadata['source']} | Dept: {d.metadata['department']}]\n{d.page_content}"
        for d in context_docs
    )
    return f"""You are a secure enterprise assistant. Answer ONLY using the context below.
If the answer is not in the context, say "I don't have access to that information."
Never reveal data from departments the user hasn't been granted access to.

USER: {user_id}

CONTEXT:
{context}

QUESTION: {query}

ANSWER (cite sources):"""


def generate_answer(query: str, context_docs: list, user_id: str,
                    llm_client=None) -> dict:
    if not context_docs:
        return {
            "answer": "❌ Access denied or no relevant data found.",
            "sources": [],
            "user_id": user_id
        }

    prompt = build_prompt(query, context_docs, user_id)

    # ✅ Groq API call
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    sources = list({d.metadata["source"] for d in context_docs})

    return {
        "answer": answer,
        "sources": sources,
        "user_id": user_id
    }
