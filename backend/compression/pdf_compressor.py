"""
PDF compression module using PyPDF2 and PIL
"""

import asyncio
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io
import os

async def compress_pdf(input_path: str, output_path: str) -> float:
    """
    Compress PDF by reducing image quality and removing unnecessary elements
    Returns compression ratio (0-1)
    """
    try:
        # Get original size
        original_size = os.path.getsize(input_path)
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            # Compress images in the page
            if '/Resources' in page and '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
                
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        # Get image data
                        size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                        data = xObject[obj]._data
                        
                        # Convert and compress image
                        image = Image.open(io.BytesIO(data))
                        
                        # Reduce quality for JPEG compression
                        output = io.BytesIO()
                        image.save(output, format='JPEG', quality=60, optimize=True)
                        xObject[obj]._data = output.getvalue()
            
            writer.add_page(page)
        
        # Write compressed PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Calculate compression ratio
        compressed_size = os.path.getsize(output_path)
        compression_ratio = 1 - (compressed_size / original_size)
        
        return max(0, compression_ratio)
    
    except Exception as e:
        print(f"PDF compression error: {e}")
        # If compression fails, just copy the file
        import shutil
        shutil.copy(input_path, output_path)
        return 0.0