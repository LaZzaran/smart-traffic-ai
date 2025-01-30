"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from .config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

# SQLAlchemy model base class
Base = declarative_base()

def get_engine(database_url: str = None):
    """Create database engine"""
    return create_engine(
        database_url or settings.DATABASE_URL_VALUE,
        pool_pre_ping=True,  # Bağlantı kontrolü
        pool_size=5,  # Bağlantı havuzu boyutu
        max_overflow=10  # Maksimum ek bağlantı
    )

try:
    engine = get_engine()
    # Test connection
    with engine.connect() as conn:
        conn.execute("SELECT 1")
    logger.info("Successfully connected to PostgreSQL database")
except OperationalError as e:
    logger.error(f"Could not connect to database: {e}")
    raise

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Database session generator"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise 
