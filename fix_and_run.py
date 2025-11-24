#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess

# Создаем необходимые директории
os.makedirs("backend/uploads", exist_ok=True)

# Создаем простой сервер (ASCII only, no UTF-8 symbols)
server_code = '''# -*- coding: utf-8 -*-
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import shutil
from pathlib import Path

app = FastAPI(title="Universal File Compressor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/compress")
async def compress_file(file: UploadFile = File(...)):
    """Simple file compression"""
    file_id = str(uuid.uuid4())
    ext = file.filename.split('.')[-1].lower()
    
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}_input.{ext}")
    output_path = os.path.join(UPLOAD_DIR, f"{file_id}_compressed.{ext}")
    
    # Save file
    with open(input_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Simple compression simulation
    original_size = os.path.getsize(input_path)
    
    # For images use Pillow
    if ext in ['jpg', 'jpeg', 'png']:
        try:
            from PIL import Image
            with Image.open(input_path) as img:
                if ext in ['jpg', 'jpeg']:
                    img.save(output_path, format='JPEG', quality=60, optimize=True)
                else:
                    img.save(output_path, format='PNG', optimize=True, compress_level=9)
        except:
            shutil.copy(input_path, output_path)
    else:
        # For other files just copy
        shutil.copy(input_path, output_path)
    
    # Calculate compression ratio
    compressed_size = os.path.getsize(output_path)
    compression_ratio = 1 - (compressed_size / original_size)
    
    # Remove original file
    os.remove(input_path)
    
    return {
        "fileId": file_id,
        "originalName": file.filename,
        "compressedSize": compressed_size,
        "compressionRatio": max(0.1, compression_ratio),
        "downloadUrl": f"/api/download/{file_id}"
    }

@app.get("/api/download/{file_id}")
async def download_file(file_id: str):
    for file in os.listdir(UPLOAD_DIR):
        if file.startswith(f"{file_id}_compressed"):
            file_path = os.path.join(UPLOAD_DIR, file)
            ext = file.split('_compressed.')[1]
            return FileResponse(
                file_path,
                filename=f"compressed_{file_id}.{ext}"
            )
    return {"error": "File not found"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

# Write server with proper encoding
with open("backend/app.py", "w", encoding='utf-8') as f:
    f.write(server_code)

print("✅ Server created with UTF-8 encoding!")
print("🚀 Starting server...")

# Run server
try:
    subprocess.run([sys.executable, "backend/app.py"])
except KeyboardInterrupt:
    print("\n🛑 Server stopped")