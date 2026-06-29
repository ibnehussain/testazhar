"""Faithfulness evaluation harness for the activities knowledge base.

The script searches the local KB for each test query, generates a grounded
answer with a chat model, and then scores the resulting responses with RAGAS
faithfulness.
"""

from __future__ import annotations

import importlib
import os
import sys
import types
from typing import Any

try:
    from src.rag.kb_search import search_kb
except ImportError:
    from kb_search import search_kb


TEST_CASES: list[dict[str, str]] = [
    {
        "query": "how many people can join chess club",
        "expected_context": "12",
    },
    {
        "query": "when does basketball practice run",
        "expected_context": "Monday",
    },
    {
        "query": "which activity allows most participants",
        "expected_context": "30",
    },
    {
        "query": "is there a daily activity",
        "expected_context": "Daily",
    },
]

FAITHFULNESS_THRESHOLD = 0.85
DEFAULT_MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def _build_chat_model():
    """Create a chat model configured from environment variables."""
    try:
        chat_openai_module = importlib.import_module("langchain_openai")
    except ImportError as exc:
        raise RuntimeError(
            "langchain-openai is required to run this evaluation harness."
        ) from exc

    ChatOpenAI = chat_openai_module.ChatOpenAI

    api_key = os.getenv("GITHUB_TOKEN") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set GITHUB_TOKEN or OPENAI_API_KEY before running the evaluation."
        )

    model_kwargs: dict[str, Any] = {
        "model": DEFAULT_MODEL_NAME,
        "temperature": 0,
        "openai_api_key": api_key,
    }
    if os.getenv("GITHUB_TOKEN"):
        model_kwargs["openai_api_base"] = "https://models.inference.ai.azure.com"

    return ChatOpenAI(**model_kwargs)


def _format_context_chunks(kb_entries: list[dict]) -> list[str]:
    """Convert KB entries into compact context strings for prompting and scoring."""
    context_chunks: list[str] = []
    for entry in kb_entries:
        title = str(entry.get("title", "")).strip()
        description = str(entry.get("description", "")).strip()
        if title and description:
            context_chunks.append(f"{title}: {description}")
        elif title:
            context_chunks.append(title)
        elif description:
            context_chunks.append(description)
    return context_chunks


def _generate_grounded_answer(chat_model, query: str, context_chunks: list[str]) -> str:
    """Ask the chat model to answer using only the supplied context."""
    context_block = "\n".join(f"- {chunk}" for chunk in context_chunks) or "- No matching context found."
    prompt = (
        "Answer the question using only the context below. "
        "Keep the answer short, factual, and grounded in the context. "
        "If the context does not contain the answer, say you cannot determine it.\n\n"
        f"Question: {query}\n\n"
        f"Context:\n{context_block}"
    )
    response = chat_model.invoke(prompt)
    return str(getattr(response, "content", response)).strip()


def _extract_faithfulness_scores(evaluation_result: Any) -> list[float]:
    """Normalize the RAGAS result into a list of faithfulness scores."""
    if hasattr(evaluation_result, "to_pandas"):
        frame = evaluation_result.to_pandas()
        return [float(value) for value in frame["faithfulness"].tolist()]

    if isinstance(evaluation_result, dict):
        faithfulness_values = evaluation_result.get("faithfulness")
        if isinstance(faithfulness_values, list):
            return [float(value) for value in faithfulness_values]
        if faithfulness_values is not None:
            return [float(faithfulness_values)]

    raise TypeError("Unsupported RAGAS result format; could not extract faithfulness scores.")


def _install_vertexai_compat_shim() -> None:
    """Provide the legacy vertexai chat model module expected by ragas.

    Some ragas versions still import langchain_community.chat_models.vertexai,
    which is not present in newer langchain-community releases. A lightweight
    placeholder module keeps the import path working without affecting the
    evaluation flow used here.
    """
    module_name = "langchain_community.chat_models.vertexai"
    if module_name in sys.modules:
        return

    shim_module = types.ModuleType(module_name)

    class ChatVertexAI:  # pragma: no cover - compatibility shim only
        """Placeholder for ragas' legacy import path."""

        pass

    shim_module.ChatVertexAI = ChatVertexAI
    sys.modules[module_name] = shim_module

    try:
        chat_models_module = importlib.import_module("langchain_community.chat_models")
        setattr(chat_models_module, "vertexai", shim_module)
    except ImportError:
        return


def run_ragas_eval() -> float:
    """Run the faithfulness evaluation harness and return the overall score."""
    try:
        _install_vertexai_compat_shim()
        datasets_module = importlib.import_module("datasets")
        ragas_module = importlib.import_module("ragas")
        ragas_metrics_module = importlib.import_module("ragas.metrics")
    except ImportError as exc:
        raise RuntimeError(
            "datasets and ragas are required to run this evaluation harness."
        ) from exc

    Dataset = datasets_module.Dataset
    evaluate = ragas_module.evaluate
    faithfulness = ragas_metrics_module.faithfulness

    chat_model = _build_chat_model()
    evaluation_rows: list[dict[str, Any]] = []

    for case in TEST_CASES:
        query = case["query"]
        expected_context = case["expected_context"]
        kb_entries = search_kb(query)
        context_chunks = _format_context_chunks(kb_entries)
        answer = _generate_grounded_answer(chat_model, query, context_chunks)
        context_blob = " ".join(context_chunks)
        expected_hit = expected_context.lower() in context_blob.lower()

        evaluation_rows.append(
            {
                "question": query,
                "answer": answer,
                "contexts": context_chunks,
            }
        )

        print(f"Query: {query}")
        print(f"Retrieved contexts: {context_chunks}")
        print(f"Expected context hit: {expected_hit}")
        print(f"Generated answer: {answer}")
        print()

    dataset = Dataset.from_list(evaluation_rows)
    evaluation_result = evaluate(dataset, metrics=[faithfulness], llm=chat_model)
    faithfulness_scores = _extract_faithfulness_scores(evaluation_result)
    overall_score = sum(faithfulness_scores) / len(faithfulness_scores)

    for case, score in zip(TEST_CASES, faithfulness_scores):
        print(f"Faithfulness for '{case['query']}': {score:.3f}")

    print(f"Overall faithfulness: {overall_score:.3f}")
    return overall_score


if __name__ == "__main__":
    score = run_ragas_eval()
    raise SystemExit(1 if score < FAITHFULNESS_THRESHOLD else 0)