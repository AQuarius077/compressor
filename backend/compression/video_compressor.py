"""
Video compression using FFmpeg
"""

import asyncio
import subprocess
import os

async def compress_video(input_path: str, output_path: str) -> float:
    """
    Compress video using FFmpeg
    Returns compression ratio (0-1)
    """
    try:
        original_size = os.path.getsize(input_path)
        
        # FFmpeg compression command
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-vcodec', 'libx264',
            '-crf', '28',  # Quality setting (lower = better quality)
            '-preset', 'medium',  # Compression speed
            '-acodec', 'aac',
            '-b:a', '128k',  # Audio bitrate
            '-y',  # Overwrite output
            output_path
        ]
        
        # Run FFmpeg
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"FFmpeg error: {stderr.decode()}")
        
        # Calculate compression ratio
        compressed_size = os.path.getsize(output_path)
        compression_ratio = 1 - (compressed_size / original_size)
        
        return max(0, compression_ratio)
    
    except Exception as e:
        print(f"Video compression error: {e}")
        # Fallback: copy file
        import shutil
        shutil.copy(input_path, output_path)
        return 0.0