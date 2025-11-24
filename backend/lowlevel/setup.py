"""
Setup script for building the LZ77 extension module
"""

from setuptools import setup, Extension
import subprocess
import os

# Build the assembly file
def build_assembly():
    """Build the assembly file using NASM"""
    try:
        subprocess.run([
            'nasm', '-f', 'elf64', 'lz77_core.asm', '-o', 'lz77_core.o'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not build assembly module: {e}")
        print("Falling back to pure Python implementation")
        return False
    return True

# Try to build assembly
assembly_built = build_assembly()

# Define extension
lz77_extension = Extension(
    'lz77_core',
    sources=['lz77_bridge.c'] + (['lz77_core.o'] if assembly_built else []),
    extra_compile_args=['-O3', '-march=native'] if assembly_built else []
)

setup(
    name='lz77-core',
    version='1.0.0',
    description='LZ77 compression core with assembly optimization',
    ext_modules=[lz77_extension] if assembly_built else []
)