"""
Low-level compression module
"""

try:
    # Try to import the compiled extension
    from .lz77_core import lz77_compress # type: ignore
except ImportError:
    # Fallback to pure Python implementation
    def lz77_compress(data):
        """Pure Python LZ77 compression fallback"""
        # Simple RLE-like compression for demonstration
        if not data:
            return b''
        
        result = bytearray()
        i = 0
        
        while i < len(data):
            # Look for repeated sequences
            best_len = 1
            best_dist = 0
            
            # Search backwards (limited window)
            start = max(0, i - 4096)
            for j in range(start, i):
                # Check match length
                match_len = 0
                while (match_len < 18 and 
                       i + match_len < len(data) and 
                       j + match_len < i and
                       data[i + match_len] == data[j + match_len]):
                    match_len += 1
                
                if match_len > best_len:
                    best_len = match_len
                    best_dist = i - j
            
            if best_len >= 3:
                # Encode as (distance, length)
                result.extend([0, best_dist & 0xFF, (best_dist >> 8) & 0xFF, best_len])
                i += best_len
            else:
                # Encode as literal
                result.append(data[i])
                i += 1
        
        return bytes(result)

__all__ = ['lz77_compress']