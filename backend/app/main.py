from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import  department
from app.routers import  classroom
from app.routers import  faculty
from app.routers import  role
from app.routers import  subject
from app.routers import auth
from app.routers import user
from app.routers import dashboard
from app.middleware import add_timing_middleware  
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Timing middleware added first so CORS wraps it (last-added = outermost)
add_timing_middleware(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables at startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["User"])
app.include_router(department.router, prefix="/department", tags=["Department"])
app.include_router(classroom.router, prefix="/classroom", tags=["classroom"])
app.include_router(faculty.router, prefix="/faculty", tags=["Faculty"])
app.include_router(role.router, prefix="/roles", tags=["Roles"])
app.include_router(subject.router, prefix="/subject", tags=["Subject"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(dashboard.router)