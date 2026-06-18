from dataclasses import dataclass
from pathlib import Path


@dataclass
class DocumentChunk:
    document_name: str
    chunk_id: str
    text: str


def chunk_markdown_file(
    file_path: Path,
    max_chars: int = 800,
) -> list[DocumentChunk]:
    content = file_path.read_text(encoding="utf-8")

    sections = [
        section.strip()
        for section in content.split("\n## ")
        if section.strip()
    ]

    chunks: list[DocumentChunk] = []

    for index, section in enumerate(sections):
        text = section

        if index > 0:
            text = "## " + text

        if len(text) <= max_chars:
            chunks.append(
                DocumentChunk(
                    document_name=file_path.name,
                    chunk_id=f"{file_path.stem}-{index}",
                    text=text,
                )
            )
        else:
            for part_index in range(0, len(text), max_chars):
                chunks.append(
                    DocumentChunk(
                        document_name=file_path.name,
                        chunk_id=f"{file_path.stem}-{index}-{part_index}",
                        text=text[part_index : part_index + max_chars],
                    )
                )

    return chunks


def load_knowledge_base_chunks(
    knowledge_base_dir: Path,
) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []

    for file_path in knowledge_base_dir.glob("*.md"):
        chunks.extend(chunk_markdown_file(file_path))

    return chunks