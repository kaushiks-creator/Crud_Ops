import pandas as pd
from app.chroma import collection

def main():
    data = collection.get(
        include=["documents", "metadata"]
    )

    if not data["documents"]:
        raise RuntimeError("No vectors found in Chroma DB")

    rows = []
    for i, doc in enumerate(data["documents"]):
        rows.append({
            "chunk_id": i,
            "text": doc,
            "metadata": data["metadatas"][i]
        })

    df = pd.DataFrame(rows)
    df.to_excel("vector_chunks.xlsx", index=False)
    print(f"Exported {len(df)} chunks")

if __name__ == "__main__":
    main()
