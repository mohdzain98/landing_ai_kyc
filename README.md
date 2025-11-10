# LoanLens

LoanLens AI is an intelligent, end-to-end underwriting assistant that automates financial document analysis, fraud detection, and credit decisioning with speed, accuracy, and transparency..

## Project Structure
```text
landing_ai_kyc/
├── backend/                # FastAPI + LandingAI services
│   ├── requirements.txt    # Python dependencies (FastAPI, landingai-ade, PyMuPDF…)
│   └── src/
│       ├── controller/     # FastAPI routers (upload, evaluate, search, app bootstrap)
│       ├── model/          # Pydantic response contracts
│       ├── service/        # Document extraction, KPI engines, RAG, fraud, summaries
│       └── resources/      # (Generated) Uploaded files, KPIs, markdown, final outputs
└── frontend/               # React 19 + Vite single-page app
    ├── package.json        # npm scripts & dependencies
    └── src/
        ├── App.jsx         # Router + global providers
        ├── context/        # Upload state, document metadata
        ├── components/     # Navbar, Toast, Spinner, etc.
        └── pages/          # Home (upload workflow) & Outcomes (results dashboard)
```

## Key Capabilities
- **Document extraction pipeline** powered by LandingAI ADE schemas, per-document KPIs, and annotated bounding boxes.
- **Automated underwriting** that blends KPI scoring, decisioning, and fraud detection across all uploaded documents.
- **RAG-powered follow-ups** via Bedrock (Nova) for question answering against the case dossier and final decision files.
- **Fraud analysis** for identity documnets using landing ai agentic object detection components and configurable thresholds.
- **Interactive frontend** that drives uploads, monitors progress, and surfaces the final verdict plus fraud warnings.

## Getting Started

### Prerequisites
- Python 3.10+ (virtual environment recommended)
- Node.js 22+
- npm 10+
- Landing AI ADE credentials (for document parsing/extraction)
- AWS Bedrock credentials (for RAG Q&A and intent detection)


### Environment Variables
Create a `.env` file in `backend/` (or any ancestor directory) with the keys consumed by the services:

```bash
AWS_ACCESS_KEY=<your_bedrock_access_key>
AWS_SECRET_KEY=<your_bedrock_secret_key>
VISION_AGENT_API_KEY=<vision_fraud_service_key>   
```


### 1. Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Run the API
uvicorn src.controller.main_controller:app --host 0.0.0.0 --port 8000 --reload
```

By default the upload pipeline persists every document to `backend/resources/<case_id>/<document_type>/`.  


### 2. Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
This launches the development server on <http://localhost:5173>.  
Pass the backend base URL (defaults to `http://127.0.0.1:8000/api`) to the `UserState` provider in `frontend/src/App.jsx` if you deviate from defaults.

### 3. Run the end-to-end demo
1. Start the backend (`uvicorn …`).
2. Start the frontend (`npm run dev`).
3. Visit the Home page, upload the six required document categories, and watch the status badges update.
4. Click **Process Documents** to jump into the Outcomes dashboard, review markdown summaries, and read the final lending verdict.

## Document Flow
1. **Upload** – Each POST to `/api/upload/<document_type>` stores the raw file, extracts structured data with LandingAI ADE, and generates KPIs plus markdown summaries under `backend/resources/<case_id>/<document_type>/output/`.
2. **Fraud checks** – Identity uploads trigger the passport fraud detector. Findings surface in the API response and dashboard warnings.
3. **Evaluation** – `GET /api/evaluate/evaluate-doc` aggregates KPIs, runs fraud heuristics, writes `final_output/kpis_final.json` and `final_output/final_decision.json`, and kicks off RAG indexing.
4. **Search & Q&A** – `/api/search/search-doc` returns a consolidated view of per-document markdown plus the final verdict. `/api/search/ask` lets reviewers query the case using the Bedrock-backed RAG agent.

## Backend API Surface
All endpoints accept multipart form submissions with a `metadata` JSON string and a single file field whose name matches the document type.

| Method | Endpoint | Description | Expected file field |
| ------ | -------- | ----------- | ------------------- |
| POST | `/api/upload/bank_statement` | Upload and process borrower bank statements | `bank_statements` |
| POST | `/api/upload/identity_document` | Verify identity documents (passport, ID, DL) | `identity_documents` |
| POST | `/api/upload/credit_report` | Analyze credit bureau data | `credit_reports` |
| POST | `/api/upload/income_proof` | Inspect income verification proofs | `income_proof` |
| POST | `/api/upload/tax_statement` | Review the latest tax filings | `tax_statements` |
| POST | `/api/upload/utility_bill` | Confirm residency using utility bills | `utility_bills` |
| GET | `/api/evaluate/evaluate-doc?uuid=<case_id>` | Aggregate KPIs, compute underwriting score, build RAG index | — |
| GET | `/api/search/search-doc?uuid=<case_id>` | Retrieve per-document markdown and final verdict | — |
| POST | `/api/search/ask` | Query the case dossier via RAG (`{"case_id": "...", "query": "..."}`) | — |

Successful uploads return:
```json
{
  "status": 200,
  "message": "Documents uploaded successfully.",
  "data": {
    "folderId": "<case-id>",
    "content": "## Under Development"
  },
  "errors": null
}
```

The `errors` field surfaces fraud warnings (for identity documents) or search/evaluation issues. After evaluation, `final_output/` contains downstream artefacts consumed by the RAG agent.

## Frontend Experience
- **Home / Upload Flow**  
  Users work through six responsive cards, each with drag & drop, format hints, and inline status chips. A global progress check ensures all uploads finish before enabling the Outcomes link.

- **Outcomes Dashboard**  
  Tabs for each document type, collapsible markdown summaries (with “Show more” for long content), contextual status badges, and a visually distinct verdict panel. Quick actions let judges retry with different docs or restart the whole flow. Fraud alerts from the identity pipeline surface alongside the verdict.

- **Ask This Case**  
  The backend RAG agent indexes all generated markdown, KPI JSON, and the final decision. Call `/api/search/ask` from the UI (or REST clients) to power contextual Q&A once evaluation succeeds.

- **UI Core**  
  Built with React 19, React Router v7, Bootstrap 5, and Font Awesome icons. Toast + alert helpers surface copy-to-clipboard events and success/error messages.

## Talking Points
- **Speed to insight**: KYC reviewers jump straight from uploads to AI-curated summaries without waiting for manual compilation.
- **Explainability**: Markdown narratives and document-specific scoring make it clear why a borrower is (or isn’t) approved.
- **Composable architecture**: Swap in alternative parsers or AI models by updating the FastAPI service; the React UI automatically reflects new document types via the shared context.

## Troubleshooting & Tips
- Make sure `backend/resources/` contains mock markdown outputs for every document type when demoing without the full Landing AI pipeline.
- Missing `.env` keys cause the extractor, Bedrock RAG, or passport fraud modules to raise errors—double-check credentials before running `uvicorn`.
- The RAG agent persists FAISS indices under `backend/rag_index/<case_id>/`; delete a folder to force re-indexing.
- The search service expects a case UUID present under `backend/resources/`. Ensure uploads completed (or mock data exists) before calling `/api/search/search-doc`.
- If you change API base URLs, update the `host` prop passed into `UserState` (see `frontend/src/App.jsx`).
- Use the browser dev tools network tab to confirm multipart payloads include both the file and the JSON `metadata`.