@echo off
echo Creating simple server...

echo # -*- coding: utf-8 -*- > backend\app.py
echo from fastapi import FastAPI, File, UploadFile >> backend\app.py
echo from fastapi.responses import FileResponse >> backend\app.py
echo from fastapi.middleware.cors import CORSMiddleware >> backend\app.py
echo import os, uuid, shutil >> backend\app.py
echo. >> backend\app.py
echo app = FastAPI() >> backend\app.py
echo app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]) >> backend\app.py
echo. >> backend\app.py
echo UPLOAD_DIR = "uploads" >> backend\app.py
echo os.makedirs(UPLOAD_DIR, exist_ok=True) >> backend\app.py
echo. >> backend\app.py
echo @app.post("/api/compress") >> backend\app.py
echo async def compress_file(file: UploadFile = File(...)): >> backend\app.py
echo     file_id = str(uuid.uuid4()) >> backend\app.py
echo     ext = file.filename.split('.')[-1].lower() >> backend\app.py
echo     input_path = os.path.join(UPLOAD_DIR, f"{file_id}_input.{ext}") >> backend\app.py
echo     output_path = os.path.join(UPLOAD_DIR, f"{file_id}_compressed.{ext}") >> backend\app.py
echo     with open(input_path, "wb") as f: content = await file.read(); f.write(content) >> backend\app.py
echo     try: >> backend\app.py
echo         from PIL import Image >> backend\app.py
echo         with Image.open(input_path) as img: >> backend\app.py
echo             if ext in ['jpg','jpeg']: img.save(output_path, format='JPEG', quality=60, optimize=True) >> backend\app.py
echo             else: img.save(output_path, format='PNG', optimize=True, compress_level=9) >> backend\app.py
echo     except: shutil.copy(input_path, output_path) >> backend\app.py
echo     os.remove(input_path) >> backend\app.py
echo     return {"fileId": file_id, "originalName": file.filename, "compressedSize": os.path.getsize(output_path), "compressionRatio": 0.3, "downloadUrl": f"/api/download/{file_id}"} >> backend\app.py
echo. >> backend\app.py
echo @app.get("/api/download/{file_id}") >> backend\app.py
echo async def download_file(file_id: str): >> backend\app.py
echo     for file in os.listdir(UPLOAD_DIR): >> backend\app.py
echo         if file.startswith(f"{file_id}_compressed"): >> backend\app.py
echo             return FileResponse(os.path.join(UPLOAD_DIR, file), filename=f"compressed_{file_id}.{file.split('.')[-1]}") >> backend\app.py
echo. >> backend\app.py
echo @app.get("/api/health") >> backend\app.py
echo async def health_check(): return {"status": "healthy"} >> backend\app.py
echo. >> backend\app.py
echo if __name__ == "__main__": import uvicorn; uvicorn.run(app, host="0.0.0.0", port=8000) >> backend\app.py

echo ✅ Server created!
echo 🚀 Starting server...

cd backend
python app.py
pause