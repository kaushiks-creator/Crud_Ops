from app.db.qdrant import get_qdrant_client, COLLECTION_NAME
from qdrant_client.models import Filter

def semantic_search(
    query_vector: list[float],
    top_k: int = 5,
    metadata_filter: Filter | None = None,
):
    client = get_qdrant_client()

    response = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=top_k,
    with_payload=True,
)

    results = []
    for scored_point in response.points:   # ✅ THIS IS THE FIX
        results.append({
            "score": scored_point.score,
            **scored_point.payload
    })
    return results