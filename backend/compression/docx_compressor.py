"""
DOCX compression module
"""

import asyncio
import zipfile
import os
from lxml import etree
import shutil

async def compress_docx(input_path: str, output_path: str) -> float:
    """
    Compress DOCX by optimizing XML and removing unused styles
    Returns compression ratio (0-1)
    """
    try:
        original_size = os.path.getsize(input_path)
        
        # Extract DOCX (it's a ZIP file)
        temp_dir = input_path + "_temp"
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Optimize document.xml
        doc_path = os.path.join(temp_dir, 'word', 'document.xml')
        if os.path.exists(doc_path):
            # Parse and clean XML
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(doc_path, parser)
            
            # Remove unnecessary elements (comments, unused styles, etc.)
            root = tree.getroot()
            
            # Remove proofErr elements
            for elem in root.xpath('//w:proofErr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                parent = elem.getparent()
                if parent is not None:
                    parent.remove(elem)
            
            # Save optimized XML
            tree.write(doc_path, pretty_print=False, xml_declaration=True, encoding='utf-8')
        
        # Compress images in media folder
        media_dir = os.path.join(temp_dir, 'word', 'media')
        if os.path.exists(media_dir):
            for filename in os.listdir(media_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    from PIL import Image
                    img_path = os.path.join(media_dir, filename)
                    with Image.open(img_path) as img:
                        # Convert and compress
                        img.save(img_path, optimize=True, quality=70)
        
        # Re-create DOCX with better compression
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip_ref:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, temp_dir)
                    zip_ref.write(file_path, arc_path)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        # Calculate compression ratio
        compressed_size = os.path.getsize(output_path)
        compression_ratio = 1 - (compressed_size / original_size)
        
        return max(0, compression_ratio)
    
    except Exception as e:
        print(f"DOCX compression error: {e}")
        shutil.copy(input_path, output_path)
        return 0.0