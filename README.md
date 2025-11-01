# Landing AI KYC

> Tool shows how Landing AI can automate bank-grade KYC by turning raw borrower documents into a final lending verdict in minutes.

## Project Structure
```text
landing_ai_kyc/
├── backend/                # FastAPI + LandingAI services
│   ├── requirements.txt    # Python dependencies (FastAPI, landingai-ade, PyMuPDF…)
│   └── src/
│       ├── controller/     # FastAPI routers for uploads and app bootstrap
│       ├── model/          # Pydantic response contracts
│       ├── service/        # Document processing, summariser, utilities
│       └── resources/      # (Generated) Uploaded files and markdown outputs
└── frontend/               # React 19 + Vite single-page app
    ├── package.json        # npm scripts & dependencies
    └── src/
        ├── App.jsx         # Router + global providers
        ├── context/        # Upload state, document metadata
        ├── components/     # Navbar, Toast, Spinner, etc.
        └── pages/          # Home (upload workflow) & Outcomes (results dashboard)
```

## Getting Started

### Prerequisites
- Python 3.10+ (virtual environment recommended)
- Node.js 22+
- npm 10+  
- Optional: Landing AI ADE credentials and pre-generated markdown outputs inside `backend/resources/` for fully automated demos.

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
It expects the FastAPI backend at <http://127.0.0.1:8000>.

### 3. Run the end-to-end demo
1. Start the backend (`uvicorn …`).
2. Start the frontend (`npm run dev`).
3. Visit the Home page, upload the six required document categories, and watch the status badges update.
4. Click **Process Documents** to jump into the Outcomes dashboard, review markdown summaries, and read the final lending verdict.

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

## Frontend Experience
- **Home / Upload Flow**  
  Users work through six responsive cards, each with drag & drop, format hints, and inline status chips. A global progress check ensures all uploads finish before enabling the Outcomes link.

- **Outcomes Dashboard**  
  Tabs for each document type, collapsible markdown summaries (with “Show more” for long content), contextual status badges, and a visually distinct verdict panel. Quick actions let judges retry with different docs or restart the whole flow.

- **UI Core**  
  Built with React 19, React Router v7, Bootstrap 5, and Font Awesome icons. Toast + alert helpers surface copy-to-clipboard events and success/error messages.

## Talking Points
- **Speed to insight**: KYC reviewers jump straight from uploads to AI-curated summaries without waiting for manual compilation.
- **Explainability**: Markdown narratives and document-specific scoring make it clear why a borrower is (or isn’t) approved.
- **Composable architecture**: Swap in alternative parsers or AI models by updating the FastAPI service; the React UI automatically reflects new document types via the shared context.

## Troubleshooting & Tips
- Make sure `backend/resources/` contains mock markdown outputs for every document type when demoing without the full Landing AI pipeline.
- If you change API base URLs, update `API_HOST` inside `frontend/src/context/UserState.jsx`.
- Use the browser dev tools network tab to confirm multipart payloads include both the file and the JSON `metadata`.

