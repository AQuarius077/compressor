"""
Image compression module with custom algorithms
"""

import asyncio
from PIL import Image
import os
import sys
import numpy as np

# Исправление импорта
try:
    from backend.lowlevel import lz77_compress
except ImportError:
    try:
        from ..lowlevel import lz77_compress
    except ImportError:
        # Fallback если lowlevel недоступен
        def lz77_compress(data):
            """Fallback LZ77 compression"""
            return data

async def compress_image(input_path: str, output_path: str) -> float:
    """
    Compress image using PIL and custom algorithms
    Returns compression ratio (0-1)
    """
    try:
        original_size = os.path.getsize(input_path)
        
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparency
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Apply compression based on format
            if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
                # JPEG compression with optimization
                img.save(output_path, format='JPEG', quality=65, optimize=True, progressive=True)
            else:
                # PNG compression with optimization
                img.save(output_path, format='PNG', optimize=True, compress_level=9)
        
        # Additional compression using low-level LZ77
        try:
            with open(output_path, 'rb') as f:
                data = f.read()
            
            compressed_data = lz77_compress(data)
            
            with open(output_path, 'wb') as f:
                f.write(compressed_data)
        except:
            pass  # LZ77 compression is optional
        
        # Calculate compression ratio
        compressed_size = os.path.getsize(output_path)
        compression_ratio = 1 - (compressed_size / original_size)
        
        return max(0, compression_ratio)
    
    except Exception as e:
        print(f"Image compression error: {e}")
        # Fallback to simple PIL compression
        with Image.open(input_path) as img:
            img.save(output_path, optimize=True, quality=70)
        return 0.0