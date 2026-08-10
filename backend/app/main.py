from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.database import engine, Base
from app.api.routes import auth, predict, history, dashboard

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Uploads Directory
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Register Routers (Both /api/v1 prefix and root fallback for maximum API compatibility)
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Authentication"])
app.include_router(auth.router, tags=["Authentication Root Fallback"])

app.include_router(predict.router, prefix=settings.API_V1_STR, tags=["Prediction Engine"])
app.include_router(predict.router, tags=["Prediction Engine Root Fallback"])

app.include_router(history.router, prefix=settings.API_V1_STR, tags=["Prediction History"])
app.include_router(history.router, tags=["Prediction History Root Fallback"])

app.include_router(dashboard.router, prefix=settings.API_V1_STR, tags=["Analytics & Dashboard"])
app.include_router(dashboard.router, tags=["Analytics & Dashboard Root Fallback"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "online", "project": settings.PROJECT_NAME, "version": settings.VERSION}
