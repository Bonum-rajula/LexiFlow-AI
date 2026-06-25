# src/lexiflow/infrastructure/parsers/pypdf_parser.py
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ...core.interfaces import DocumentParser
from ...core.config import settings


class PyPDFParser(DocumentParser):
    """Concrete PDF parser using PyMuPDF (fitz) with recursive character chunking."""

    def __init__(
        self,
        chunk_size: int = settings.max_chunk_size,
        chunk_overlap: int = settings.chunk_overlap,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def parse(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract text page-by-page, then split into overlapping chunks."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        doc = fitz.open(file_path)
        all_chunks = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            if not text.strip():
                continue
                
            # Split this page's text into chunks
            page_chunks = self.text_splitter.split_text(text)
            
            for chunk_text in page_chunks:
                all_chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        "source": file_path.name,
                        "page": page_num + 1,
                        "total_pages": len(doc),
                    }
                })
        
        doc.close()
        return all_chunks

    def supported_extensions(self) -> List[str]:
        return [".pdf"]