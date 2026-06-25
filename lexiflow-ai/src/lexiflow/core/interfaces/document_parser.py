# src/lexiflow/core/interfaces/document_parser.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any


class DocumentParser(ABC):
    """Abstract interface for parsing documents into text chunks with metadata."""
    
    @abstractmethod
    def parse(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse a document and return a list of chunks.
        
        Args:
            file_path: Path to the document (e.g., PDF, TXT).
            
        Returns:
            List of dictionaries, each containing:
                - "text": str (the chunk content)
                - "metadata": dict (e.g., {"page": 1, "source": "filename.pdf"})
        """
        pass
    
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """Return a list of supported file extensions (e.g., ['.pdf', '.txt'])."""
        pass