#ifndef MYPYC_NATIVE_H
#define MYPYC_NATIVE_H
#include <Python.h>
#include <CPy.h>
#ifndef MYPYC_DECLARED_tuple_T3OOO
#define MYPYC_DECLARED_tuple_T3OOO
typedef struct tuple_T3OOO {
    PyObject *f0;
    PyObject *f1;
    PyObject *f2;
} tuple_T3OOO;
static tuple_T3OOO tuple_undefined_T3OOO = { NULL, NULL, NULL };
#endif

#ifndef MYPYC_DECLARED_tuple_T2OO
#define MYPYC_DECLARED_tuple_T2OO
typedef struct tuple_T2OO {
    PyObject *f0;
    PyObject *f1;
} tuple_T2OO;
static tuple_T2OO tuple_undefined_T2OO = { NULL, NULL };
#endif

#ifndef MYPYC_DECLARED_tuple_T1O
#define MYPYC_DECLARED_tuple_T1O
typedef struct tuple_T1O {
    PyObject *f0;
} tuple_T1O;
static tuple_T1O tuple_undefined_T1O = { NULL };
#endif

#ifndef MYPYC_DECLARED_tuple_T5OOOOO
#define MYPYC_DECLARED_tuple_T5OOOOO
typedef struct tuple_T5OOOOO {
    PyObject *f0;
    PyObject *f1;
    PyObject *f2;
    PyObject *f3;
    PyObject *f4;
} tuple_T5OOOOO;
static tuple_T5OOOOO tuple_undefined_T5OOOOO = { NULL, NULL, NULL, NULL, NULL };
#endif

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
} asgi_context___RequestContextExceptionObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
} asgi_context___HeaderValidationExceptionObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
} asgi_context___ContextObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    vectorcallfunc vectorcall;
    PyObject *_app;
} asgi_context___ContextMiddlewareObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    vectorcallfunc vectorcall;
    PyObject *_app;
} asgi_context___AbstractHeadersExtractorMiddlewareObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
} asgi_context___HeadersExtractorMiddlewareFactoryObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_self__;
    PyObject *_type;
    PyObject *_value;
    PyObject *_traceback;
    PyObject *_arg;
    CPyTagged ___mypyc_next_label__;
    PyObject *_token;
} asgi_context___new_context_envObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_env__;
} asgi_context___new_context_genObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_self__;
    PyObject *_self;
    PyObject *_scope;
    PyObject *_receive;
    PyObject *_send;
    PyObject *_type;
    PyObject *_value;
    PyObject *_traceback;
    PyObject *_arg;
    CPyTagged ___mypyc_next_label__;
    PyObject *___mypyc_temp__0;
    tuple_T3OOO ___mypyc_temp__1;
    PyObject *___mypyc_temp__2;
    PyObject *___mypyc_temp__3;
    char ___mypyc_temp__4;
    PyObject *___mypyc_temp__5;
    tuple_T3OOO ___mypyc_temp__6;
    tuple_T3OOO ___mypyc_temp__7;
} asgi_context_____call___3_ContextMiddleware_envObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_env__;
} asgi_context_____call___3_ContextMiddleware_genObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_self__;
    PyObject *_self;
    PyObject *_scope;
    PyObject *_receive;
    PyObject *_send;
    PyObject *_type;
    PyObject *_value;
    PyObject *_traceback;
    PyObject *_arg;
    CPyTagged ___mypyc_next_label__;
    PyObject *___mypyc_temp__8;
    tuple_T3OOO ___mypyc_temp__9;
    PyObject *___mypyc_temp__10;
    PyObject *___mypyc_temp__11;
    PyObject *___mypyc_temp__12;
    PyObject *_name;
    PyObject *_headers;
    PyObject *___mypyc_temp__13;
    PyObject *___mypyc_temp__14;
    PyObject *_header_value;
    PyObject *_validate;
    PyObject *___mypyc_temp__15;
    tuple_T3OOO ___mypyc_temp__16;
} asgi_context_____call___3_AbstractHeadersExtractorMiddleware_envObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_env__;
} asgi_context_____call___3_AbstractHeadersExtractorMiddleware_genObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_self__;
    PyObject *_header_names;
    PyObject *_validators;
    PyObject *_base_name;
    PyObject *_name_parts;
    PyObject *_name_part;
    PyObject *_name;
    PyObject *_header_names_property;
} asgi_context___build_HeadersExtractorMiddlewareFactory_envObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    vectorcallfunc vectorcall;
    PyObject *___mypyc_env__;
} asgi_context_____mypyc_lambda__0_build_HeadersExtractorMiddlewareFactory_objObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    vectorcallfunc vectorcall;
    PyObject *___mypyc_env__;
} asgi_context_____mypyc_lambda__1_build_HeadersExtractorMiddlewareFactory_objObject;

#endif
