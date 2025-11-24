"""
Text compression using Huffman coding
"""

import asyncio
import heapq
from collections import Counter, defaultdict
import os

class HuffmanNode:
    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    """Build Huffman tree from text"""
    frequency = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = HuffmanNode()
        merged.freq = left.freq + right.freq
        merged.left = left
        merged.right = right
        
        heapq.heappush(heap, merged)
    
    return heap[0]

def build_codes(root):
    """Build Huffman codes from tree"""
    codes = {}
    
    def _build_codes_helper(node, current_code):
        if node is None:
            return
        
        if node.char is not None:
            codes[node.char] = current_code
            return
        
        _build_codes_helper(node.left, current_code + "0")
        _build_codes_helper(node.right, current_code + "1")
    
    _build_codes_helper(root, "")
    return codes

async def compress_text(input_path: str, output_path: str) -> float:
    """
    Compress text using Huffman coding
    Returns compression ratio (0-1)
    """
    try:
        original_size = os.path.getsize(input_path)
        
        # Read text
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Build Huffman tree
        root = build_huffman_tree(text)
        codes = build_codes(root)
        
        # Encode text
        encoded = ""
        for char in text:
            encoded += codes[char]
        
        # Pad to make it byte-aligned
        padding = 8 - len(encoded) % 8
        encoded += "0" * padding
        
        # Convert to bytes
        byte_array = bytearray()
        for i in range(0, len(encoded), 8):
            byte = encoded[i:i+8]
            byte_array.append(int(byte, 2))
        
        # Create header with tree structure
        header = str(padding) + "\n"
        
        # Serialize tree
        def serialize_tree(node):
            if node.char is not None:
                return f"1{node.char}"
            return "0" + serialize_tree(node.left) + serialize_tree(node.right)
        
        header += serialize_tree(root) + "\n"
        
        # Write compressed data
        with open(output_path, 'wb') as f:
            f.write(header.encode('utf-8'))
            f.write(bytes(byte_array))
        
        # Calculate compression ratio
        compressed_size = os.path.getsize(output_path)
        compression_ratio = 1 - (compressed_size / original_size)
        
        return max(0, compression_ratio)
    
    except Exception as e:
        print(f"Text compression error: {e}")
        # Fallback: just copy the file
        with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
            f_out.write(f_in.read())
        return 0.0