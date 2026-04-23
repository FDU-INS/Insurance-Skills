"""Git LFS detection and handling for HealthSim database files.

The healthsim.duckdb file is stored in Git LFS due to its size.
When Git LFS is not installed or configured, the file appears as a
small (~130 byte) pointer file instead of the actual database.

This module provides utilities to detect and handle this situation.
"""

import os
from pathlib import Path


# LFS pointer files start with this header
LFS_POINTER_HEADER = b"version https://git-lfs.github.com/spec/v1"

# Expected minimum size for actual DuckDB file (pointer files are ~130 bytes)
MIN_DUCKDB_SIZE = 1024  # 1KB minimum for any real database


def is_lfs_pointer(file_path: str | Path) -> bool:
    """Check if a file is a Git LFS pointer instead of actual content.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if the file is an LFS pointer, False if it's actual content
    """
    path = Path(file_path)
    
    if not path.exists():
        return False
    
    # Check file size first - LFS pointers are tiny
    size = path.stat().st_size
    if size > 500:  # LFS pointers are ~130 bytes
        return False
    
    # Check for LFS header
    try:
        with open(path, "rb") as f:
            header = f.read(len(LFS_POINTER_HEADER))
            return header == LFS_POINTER_HEADER
    except Exception:
        return False


def check_duckdb_file(db_path: str | Path | None = None) -> dict:
    """Check the status of the HealthSim DuckDB file.
    
    Args:
        db_path: Path to database file. If None, uses default location.
        
    Returns:
        Dict with keys:
        - exists: bool
        - is_lfs_pointer: bool
        - size_bytes: int
        - status: 'ok' | 'missing' | 'lfs_pointer'
        - message: Human-readable status message
    """
    if db_path is None:
        # Find workspace root
        db_path = _find_default_db_path()
    
    path = Path(db_path)
    
    if not path.exists():
        return {
            "exists": False,
            "is_lfs_pointer": False,
            "size_bytes": 0,
            "status": "missing",
            "message": f"Database file not found: {path}",
            "path": str(path),
        }
    
    size = path.stat().st_size
    is_pointer = is_lfs_pointer(path)
    
    if is_pointer:
        return {
            "exists": True,
            "is_lfs_pointer": True,
            "size_bytes": size,
            "status": "lfs_pointer",
            "message": (
                f"Database file is a Git LFS pointer ({size} bytes). "
                "Git LFS is not installed or not configured. "
                "Run 'git lfs pull' or copy the actual database file."
            ),
            "path": str(path),
        }
    
    if size < MIN_DUCKDB_SIZE:
        return {
            "exists": True,
            "is_lfs_pointer": False,
            "size_bytes": size,
            "status": "invalid",
            "message": f"Database file exists but is too small ({size} bytes). May be corrupted.",
            "path": str(path),
        }
    
    return {
        "exists": True,
        "is_lfs_pointer": False,
        "size_bytes": size,
        "status": "ok",
        "message": f"Database file OK ({size:,} bytes)",
        "path": str(path),
    }


def _find_default_db_path() -> Path:
    """Find the default database path by searching up from current location."""
    # Try common locations
    candidates = [
        Path.cwd() / "healthsim.duckdb",
        Path.cwd() / "data" / "healthsim.duckdb",
        Path(__file__).parent.parent.parent.parent.parent.parent.parent / "healthsim.duckdb",
    ]
    
    # Also check HEALTHSIM_DB_PATH environment variable
    env_path = os.environ.get("HEALTHSIM_DB_PATH")
    if env_path:
        candidates.insert(0, Path(env_path))
    
    for candidate in candidates:
        if candidate.exists():
            return candidate
    
    # Return the workspace root default even if it doesn't exist
    return Path.cwd() / "healthsim.duckdb"


def require_duckdb(db_path: str | Path | None = None) -> Path:
    """Ensure DuckDB file is available and valid.
    
    Args:
        db_path: Path to database file. If None, uses default location.
        
    Returns:
        Path to the valid database file
        
    Raises:
        FileNotFoundError: If database file is missing
        ValueError: If database file is an LFS pointer or invalid
    """
    status = check_duckdb_file(db_path)
    
    if status["status"] == "missing":
        raise FileNotFoundError(status["message"])
    
    if status["status"] == "lfs_pointer":
        raise ValueError(
            f"{status['message']}\n\n"
            "To fix this:\n"
            "1. Install Git LFS: https://git-lfs.github.com/\n"
            "2. Run: git lfs install\n"
            "3. Run: git lfs pull\n\n"
            "Or set HEALTHSIM_DB_PATH to point to a valid database file."
        )
    
    if status["status"] == "invalid":
        raise ValueError(status["message"])
    
    return Path(status["path"])


class LFSError(Exception):
    """Raised when a Git LFS file is not properly downloaded."""
    pass


def get_db_connection(db_path: str | Path | None = None):
    """Get a DuckDB connection, with LFS validation.
    
    Args:
        db_path: Path to database file. If None, uses default location.
        
    Returns:
        DuckDB connection
        
    Raises:
        LFSError: If database file is an LFS pointer
        FileNotFoundError: If database file is missing
    """
    import duckdb
    
    path = require_duckdb(db_path)
    return duckdb.connect(str(path), read_only=True)
