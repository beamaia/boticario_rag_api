from abc import ABC

import codecs
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document


class ChunkSplitter(ABC):
    separators = ["\n\n", "\n", " ", "", ".", "!", "?", ")"]
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
        separators=separators
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=540,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
        separators=separators
    )
    
    def __init__(self, content, file_path):
        self.file_path = file_path
        self.content = content
    
    def _parse_text(self):
        parsed_text = re.sub(r'(?<=[\s.,;])n(?=[\s.,;])', '\n', str(self.content)) # Remove the leading b and misplaced "n"s that are newsline
        parsed_text = re.sub(r'\\n', ' ', parsed_text) # Removes literal "\n" (not newlines char)
        parsed_text = re.sub(r"[\t\n\r]|^\s+|\s{2,}", " ", parsed_text, flags=re.MULTILINE).strip() # Remove tab and unecessary chars
        decoded_text = codecs.escape_decode(parsed_text)[0].decode('utf-8', 'ignore') # Decode any charcters to utf-8
        parsed_text = re.sub(r"[^\w\s.,!?;:'\"()\[\]{}_-]",'', decoded_text) # Substitute any non-word/paragraph char not previously captured

        return parsed_text

    def create_chunks(self):
        chunks = []

        metadata = dict()
        metadata.update({
            "s3_path": self.file_path
        })

        parsed_text = self._parse_text()
        parent_chunks = self.parent_splitter.split_text(parsed_text)
        
        for chunk in parent_chunks:
            metadata.update({
                "parent_chunk": chunk,
            })

            child_chunks = self.child_splitter.split_text(chunk)
            chunks.extend([
                Document(
                    page_content=child,
                    metadata=metadata,
                    child_num= i+1
                ) for i, child in enumerate(child_chunks)
            ])
    
        return chunks
    