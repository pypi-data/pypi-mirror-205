#include <Python.h>

PyMODINIT_FUNC
PyInit_context(void)
{
    PyObject *tmp;
    if (!(tmp = PyImport_ImportModule("17a8d88ade6453be006f__mypyc"))) return NULL;
    Py_DECREF(tmp);
    void *init_func = PyCapsule_Import("17a8d88ade6453be006f__mypyc.init_asgi_context___context", 0);
    if (!init_func) {
        return NULL;
    }
    return ((PyObject *(*)(void))init_func)();
}

// distutils sometimes spuriously tells cl to export CPyInit___init__,
// so provide that so it chills out
PyMODINIT_FUNC PyInit___init__(void) { return PyInit_context(); }
