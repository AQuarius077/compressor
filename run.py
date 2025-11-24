#!/usr/bin/env python3
"""
Корректный запуск сервера Universal File Compressor
"""

import sys
import os
import uvicorn

# Добавляем backend в Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    print("🚀 Starting Universal File Compressor server...")
    print("📡 Server running on http://localhost:8000")
    print("📝 API documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )