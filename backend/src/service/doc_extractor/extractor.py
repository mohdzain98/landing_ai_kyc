from pathlib import Path
import json

from landingai_ade import LandingAIADE
from landingai_ade.lib import pydantic_to_json_schema
from doc_extractor.logger import get_logger

class DocumentExtractor:
    """Small, simple wrapper for parsing, extracting and saving boxes."""

    def __init__(self, client: LandingAIADE, model="dpt-2-latest"):
        self.logger = get_logger(__name__)
        self.client = client
        self.model = model
        self.document_types = {}

    def add_schema(self, name, schema_model):
        self.logger.info(f"Registering schema '{name}'")
        self.document_types[name] = schema_model

    def parse(self, document_path):
        self.logger.info(f"Parsing document: {document_path} with model: {self.model}")
        resp = self.client.parse(document=Path(document_path), model=self.model)
        self.logger.info("Parsing complete")
        return resp

    def extract(self, markdown, document_type):
        if document_type not in self.document_types:
            self.logger.error(
                f"Unknown document_type: {document_type}. Registered: {list(self.document_types.keys())}"
            )
            raise ValueError(f"Unknown document_type: {document_type}. Registered: {list(self.document_types.keys())}")
        self.logger.info(f"Extracting fields for document_type: {document_type}")
        schema = pydantic_to_json_schema(self.document_types[document_type])
        resp = self.client.extract(schema=schema, markdown=markdown)
        self.logger.info("Extraction complete")
        return resp.extraction, resp.extraction_metadata

    def run(self, document_path, document_type, output_dir):
        # Ensure output directory exists early so we can write markdown
        self.logger.info(
            f"Running extraction | doc: {document_path} | type: {document_type} | out: {output_dir}"
        )
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        parse_resp = self.parse(document_path)
        # Save parsed markdown for reference
        base_name = Path(document_path).stem
        (output_dir / f"{document_type}_parsed.md").write_text(parse_resp.markdown)
        extraction, metadata = self.extract(parse_resp.markdown, document_type)
        self.logger.info("Run complete")
        return extraction,metadata,parse_resp


