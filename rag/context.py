def build_context(
        retrieved_chunks:list[dict],
) -> str:
    context_parts = []
    for index, chunk in enumerate(retrieved_chunks, start=1):

        file_path = chunk["file_path"]
        chunk_type = chunk["type"]
        name = chunk["name"]
        start_line = chunk["start_line"]
        end_line = chunk["end_line"]
        content = chunk["content"]

        source = f"{file_path}"

        if start_line !=-1:
            source += f" (lines {start_line}-{end_line})"
        context_parts.append(
            f"""---source {index}---
            File: {source}
Type: {chunk_type}
Name: {name}

Code:
{content}

            """
        )
    return "\n".join(context_parts)