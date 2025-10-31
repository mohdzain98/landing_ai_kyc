from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..controller.upload_controller import router as search_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(search_router, prefix="/api/upload")
