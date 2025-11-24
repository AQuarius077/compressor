/*
 * C bridge for Assembly LZ77 compression
 * Provides Python-compatible interface
 */

#if defined(__has_include)
#  if __has_include(<Python.h>)
#    include <Python.h>
#  elif __has_include("Python.h")
#    include "Python.h"
#  else

/* Fallback stubs so the file can be parsed/compiled when Python headers are not available.
   These stubs are only intended to suppress editor/compile-time include errors; they do
   not provide a working Python extension at runtime. Adjust your build system to include
   the real Python headers for actual extension builds. */

#include <stddef.h>

/* Minimal stub types and macros */
typedef struct _object { int _private; } PyObject;
typedef struct {
    void *buf;
    size_t len;
    /* other fields omitted */
} Py_buffer;

static inline void PyBuffer_Release(Py_buffer *view) { (void)view; }

static inline PyObject* PyBytes_FromStringAndSize(const char *s, Py_ssize_t n) { (void)s; (void)n; return (PyObject*)1; }
static inline PyObject* PyErr_NoMemory(void) { return (PyObject*)1; }

/* PyArg_ParseTuple fallback returns 0 (failure) to preserve behavior when real header is absent */
static inline int PyArg_ParseTuple(PyObject *args, const char *format, Py_buffer *out) { (void)args; (void)format; (void)out; return 0; }

/* Module definitions stubs */
typedef struct {
    const char *ml_name;
    PyObject *ml_meth;
    int ml_flags;
    const char *ml_doc;
} PyMethodDef;

#define METH_VARARGS 0

typedef struct PyModuleDef {
    void *m_base;
    const char *m_name;
    const char *m_doc;
    int m_size;
    PyMethodDef *m_methods;
} PyModuleDef;

#define PyModuleDef_HEAD_INIT NULL

static inline PyObject* PyModule_Create(PyModuleDef *def) { (void)def; return (PyObject*)1; }
#define PyMODINIT_FUNC PyObject*

/* Provide Py_ssize_t type if missing */
#if !defined(Py_ssize_t)
typedef ssize_t Py_ssize_t;
#endif

#  endif
#else
#  include <Python.h>
#endif

#include <stdlib.h>
#include <string.h>

// External assembly function
extern size_t lz77_compress_asm(const unsigned char* input, size_t input_len, unsigned char* output);

// Python wrapper
static PyObject* py_lz77_compress(PyObject* self, PyObject* args) {
    Py_buffer input_buffer;
    
    if (!PyArg_ParseTuple(args, "y*", &input_buffer)) {
        return NULL;
    }
    
    // Allocate output buffer (worst case: input size + some overhead)
    size_t output_size = input_buffer.len + (input_buffer.len / 8) + 64;
    unsigned char* output = malloc(output_size);
    
    if (!output) {
        PyBuffer_Release(&input_buffer);
        return PyErr_NoMemory();
    }
    
    // Call assembly function
    size_t compressed_size = lz77_compress_asm(
        (const unsigned char*)input_buffer.buf,
        input_buffer.len,
        output
    );
    
    // Create Python bytes object
    PyObject* result = PyBytes_FromStringAndSize((char*)output, compressed_size);
    
    // Cleanup
    free(output);
    PyBuffer_Release(&input_buffer);
    
    return result;
}

// Method definitions
static PyMethodDef module_methods[] = {
    {"lz77_compress", py_lz77_compress, METH_VARARGS, "LZ77 compression"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef lz77_module = {
    PyModuleDef_HEAD_INIT,
    "lz77_core",
    "LZ77 compression core module",
    -1,
    module_methods
};

// Module initialization
PyMODINIT_FUNC PyInit_lz77_core(void) {
    return PyModule_Create(&lz77_module);
}