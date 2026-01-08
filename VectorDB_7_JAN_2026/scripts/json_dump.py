import json
from app.chroma import collection


def dump_vectordb(output_file="vectordb_dump.json"):
    data = collection.get(
        include=["documents", "metadatas", "embeddings"]
    )

    dump = []
    for i in range(len(data["ids"])):
        dump.append({
            "id": data["ids"][i],
            "document": data["documents"][i],
            "metadata": data["metadatas"][i],
            "embedding": data["embeddings"][i],
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dump, f, indent=2)

    print(f"Dumped {len(dump)} vectors to {output_file}")


if __name__ == "__main__":
    dump_vectordb()
