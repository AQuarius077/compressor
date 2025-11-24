"""
Compression module initialization
"""

from .pdf_compressor import compress_pdf
from .docx_compressor import compress_docx
from .image_compressor import compress_image
from .text_compressor import compress_text
from .video_compressor import compress_video

__all__ = [
    'compress_pdf', 'compress_docx', 'compress_image',
    'compress_text', 'compress_video'
]