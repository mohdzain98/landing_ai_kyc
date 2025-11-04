from pathlib import Path
import json

from landingai_ade import LandingAIADE
from landingai_ade.lib import pydantic_to_json_schema
from PIL import Image, ImageDraw
import pymupdf

from src.service.doc_extractor.logger import get_logger

# Define colors for each chunk type
CHUNK_TYPE_COLORS = {
    "chunkText": (40, 167, 69),        # Green
    "chunkTable": (0, 123, 255),       # Blue
    "chunkMarginalia": (111, 66, 193), # Purple
    "chunkFigure": (255, 0, 255),      # Magenta
    "chunkLogo": (144, 238, 144),      # Light green
    "chunkCard": (255, 165, 0),        # Orange
    "chunkAttestation": (0, 255, 255), # Cyan
    "chunkScanCode": (255, 193, 7),    # Yellow
    "chunkForm": (220, 20, 60),        # Red
    "tableCell": (173, 216, 230),      # Light blue
    "table": (70, 130, 180),           # Steel blue
}

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
        (output_dir / f"{document_type}_parsed.txt").write_text(parse_resp.markdown)
        extraction, metadata = self.extract(parse_resp.markdown, document_type)
        self.logger.info("Run complete")
        return extraction,metadata,parse_resp

    def draw_bounding_boxes(self, parse_response, document_path,document_type, output_dir=None):
        """Draw bounding boxes around each chunk."""
        def create_annotated_image(image, groundings, page_num=0):
            """Create an annotated image with grounding boxes and labels."""
            annotated_img = image.copy()
            draw = ImageDraw.Draw(annotated_img)

            img_width, img_height = image.size

            for gid, grounding in groundings.items():
                # Check if grounding belongs to this page (for PDFs)
                if grounding.page != page_num:
                    continue

                box = grounding.box

                # Extract coordinates from box
                left, top, right, bottom = box.left, box.top, box.right, box.bottom

                # Convert to pixel coordinates
                x1 = int(left * img_width)
                y1 = int(top * img_height)
                x2 = int(right * img_width)
                y2 = int(bottom * img_height)

                # Draw bounding box
                color = CHUNK_TYPE_COLORS.get(grounding.type, (128, 128, 128))  # Default to gray
                draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

                # Draw label background and text
                label = f"{grounding.type}:{gid}"
                label_y = max(0, y1 - 20)
                draw.rectangle([x1, label_y, x1 + len(label) * 8, y1], fill=color)
                draw.text((x1 + 2, label_y + 2), label, fill=(255, 255, 255))

            return annotated_img

        document_path = Path(document_path)
        if output_dir is None:
            output_dir = document_path.parent
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        if document_path.suffix.lower() == '.pdf':
            pdf = pymupdf.open(document_path)
            total_pages = len(pdf)
            base_name = document_path.stem

            for page_num in range(total_pages):
                page = pdf[page_num]
                pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))  # 2x scaling
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Create and save annotated image
                annotated_img = create_annotated_image(img, parse_response.grounding, page_num)
                annotated_path = output_dir / f"{document_type}_page_{page_num + 1}.png"
                annotated_img.save(annotated_path)
                self.logger.info(f"Annotated image saved to: {annotated_path}")

            pdf.close()
        else:
            # Load image file directly
            img = Image.open(document_path)
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Create and save annotated image
            annotated_img = create_annotated_image(img, parse_response.grounding)
            base_name = document_path.stem
            annotated_path = output_dir / f"{document_type}_annotated.png"
            annotated_img.save(annotated_path)
            self.logger.info(f"Annotated image saved to: {annotated_path}")

        return annotated_img


