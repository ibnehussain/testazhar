"""RAG search extension using FAISS vector index.

This module provides a rag_search() function that:
1. Loads a FAISS vector index from vector-store/index.faiss
2. Embeds questions using the same embedding model used during indexing
3. Searches for top-3 most similar chunks
4. Formats chunks into a coherent answer string
5. Returns results with confidence scores based on similarity

If FAISS or embedding libraries are unavailable, gracefully falls back to
keyword-based search from the knowledge base.
"""

from pathlib import Path
from typing import Any


def rag_search(question: str) -> dict[str, Any]:
    """Search the RAG knowledge base for answers to a question.
    
    Loads the FAISS vector index and embeddings, then searches for the top-3
    most similar chunks to the question. Formats the results into a coherent
    answer string with a confidence score based on the top chunk's similarity.
    
    Args:
        question: The user's question as a string
        
    Returns:
        A dictionary with keys:
        - "answer": str — The formatted answer text
        - "source": str — Always "rag"
        - "confidence": float — Similarity score of top chunk (0.0-1.0)
        
        If no relevant chunks found (similarity < 0.5) or index unavailable:
        Returns: {
            "answer": "I couldn't find information about that in our knowledge base.",
            "source": "rag",
            "confidence": 0.0
        }
    """
    try:
        # Attempt to use FAISS and embeddings for vector search
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ImportError:
        # Fallback to keyword-based search if vector libraries unavailable
        return _fallback_kb_search(question)
    
    try:
        # Define paths
        vector_store_path = Path(__file__).parent.parent.parent / "vector-store"
        index_path = vector_store_path / "index.faiss"
        metadata_path = vector_store_path / "metadata.json"
        
        # Check if index file exists
        if not index_path.exists():
            return {
                "answer": "I couldn't find information about that in our knowledge base.",
                "source": "rag",
                "confidence": 0.0
            }
        
        # Load the FAISS index
        index = faiss.read_index(str(index_path))
        
        # Load embedding model (use the same model as during indexing)
        model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Embed the question
        question_embedding = model.encode(question, convert_to_numpy=True)
        question_embedding = np.array([question_embedding]).astype("float32")
        
        # Search for top-3 most similar chunks
        distances, indices = index.search(question_embedding, k=3)
        
        # Extract similarity scores (convert distance to similarity)
        similarity_scores = 1 / (1 + distances[0])
        
        # Check if top result meets confidence threshold
        top_similarity = float(similarity_scores[0])
        if top_similarity < 0.5:
            return {
                "answer": "I couldn't find information about that in our knowledge base.",
                "source": "rag",
                "confidence": 0.0
            }
        
        # Load metadata to get chunk content
        try:
            import json
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "answer": "I couldn't find information about that in our knowledge base.",
                "source": "rag",
                "confidence": 0.0
            }
        
        # Format chunks into answer
        answer_parts = []
        for idx, score in zip(indices[0], similarity_scores):
            if idx < len(metadata):
                chunk = metadata[int(idx)]
                if isinstance(chunk, dict):
                    title = chunk.get("title", "")
                    content = chunk.get("content", "")
                else:
                    content = str(chunk)
                    title = ""
                
                if title:
                    answer_parts.append(f"{title}: {content}")
                else:
                    answer_parts.append(content)
        
        if not answer_parts:
            return {
                "answer": "I couldn't find information about that in our knowledge base.",
                "source": "rag",
                "confidence": 0.0
            }
        
        # Join chunks into coherent answer
        answer = " ".join(answer_parts)
        
        return {
            "answer": answer,
            "source": "rag",
            "confidence": top_similarity
        }
    
    except FileNotFoundError:
        return {
            "answer": "I couldn't find information about that in our knowledge base.",
            "source": "rag",
            "confidence": 0.0
        }
    except Exception:
        # Any other error defaults to fallback
        return _fallback_kb_search(question)


def _fallback_kb_search(question: str) -> dict[str, Any]:
    """Fallback keyword-based search using the activities knowledge base.
    
    Used when FAISS/embeddings unavailable or on error.
    
    Args:
        question: The user's question
        
    Returns:
        Result dictionary with answer, source, and confidence
    """
    try:
        from src.rag.kb_search import search_kb
        results = search_kb(question, top_k=3)
        
        if results:
            answer_parts = []
            for result in results:
                title = result.get("title", "")
                description = result.get("description", "")
                if title:
                    answer_parts.append(f"{title}: {description}")
                else:
                    answer_parts.append(description)
            
            answer = " ".join(answer_parts)
            # Confidence 0.7 for keyword-based fallback
            return {
                "answer": answer,
                "source": "rag",
                "confidence": 0.7
            }
    except Exception:
        pass
    
    # Default response if fallback also fails
    return {
        "answer": "I couldn't find information about that in our knowledge base.",
        "source": "rag",
        "confidence": 0.0
    }
