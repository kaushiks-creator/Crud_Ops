from app.db.qdrant import get_qdrant_client, COLLECTION_NAME
from qdrant_client.models import Filter
from datetime import datetime, timedelta
from qdrant_client.models import Filter, FieldCondition, Range

def last_24h_filter():
    since = (datetime.utcnow() - timedelta(hours=24)).isoformat()

    return Filter(
        must=[
            FieldCondition(
                key="published_at",
                range=Range(gte=since)
            )
        ]
    )

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