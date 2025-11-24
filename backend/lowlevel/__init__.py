"""
Low-level compression module - fallback implementation
"""

def lz77_compress(data):
    """
    Fallback LZ77 compression - просто возвращает данные без изменений
    Это позволит приложению работать без assembly модулей
    """
    if not data:
        return b''
    return data

def xor_delta_preprocess(data):
    """Fallback XOR дельта препроцессинг"""
    if len(data) < 2:
        return data
    
    result = bytearray([data[0]])
    for i in range(1, len(data)):
        result.append(data[i] ^ data[i-1])
    
    return bytes(result)

__all__ = ['lz77_compress', 'xor_delta_preprocess']