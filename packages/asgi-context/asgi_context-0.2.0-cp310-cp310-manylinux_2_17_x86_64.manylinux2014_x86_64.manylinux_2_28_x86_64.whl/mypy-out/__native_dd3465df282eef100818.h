#ifndef MYPYC_NATIVE_dd3465df282eef100818_H
#define MYPYC_NATIVE_dd3465df282eef100818_H
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

#ifndef MYPYC_DECLARED_tuple_T0
#define MYPYC_DECLARED_tuple_T0
typedef struct tuple_T0 {
    int empty_struct_error_flag;
} tuple_T0;
static tuple_T0 tuple_undefined_T0 = { CPY_INT_TAG };
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
    PyObject *_err_on_missing;
    PyObject *_err_on_invalid;
    PyObject *_validators;
} asgi_context___headers_extrator___ValidationConfigObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    vectorcallfunc vectorcall;
    PyObject *_ON_MISSING;
    PyObject *_ON_INVALID;
    PyObject *_app;
} asgi_context___headers_extrator___AbstractHeadersExtractorMiddlewareObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
} asgi_context___headers_extrator___HeadersExtractorMiddlewareFactoryObject;

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
    PyObject *___mypyc_temp__4;
    PyObject *_name;
    PyObject *_headers;
    PyObject *___mypyc_temp__5;
    PyObject *___mypyc_temp__6;
    PyObject *_header_value;
    PyObject *___mypyc_temp__7;
    tuple_T3OOO ___mypyc_temp__8;
    PyObject *_validate;
    PyObject *___mypyc_temp__9;
    tuple_T3OOO ___mypyc_temp__10;
    PyObject *___mypyc_temp__11;
    tuple_T3OOO ___mypyc_temp__12;
} asgi_context___headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_envObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_env__;
} asgi_context___headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_genObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_self__;
    PyObject *_send;
    PyObject *_status;
    PyObject *_details;
    PyObject *_type;
    PyObject *_value;
    PyObject *_traceback;
    PyObject *_arg;
    CPyTagged ___mypyc_next_label__;
    PyObject *___mypyc_temp__13;
    tuple_T3OOO ___mypyc_temp__14;
    PyObject *___mypyc_temp__15;
    tuple_T3OOO ___mypyc_temp__16;
} asgi_context___headers_extrator___send_response_AbstractHeadersExtractorMiddleware_envObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_env__;
} asgi_context___headers_extrator___send_response_AbstractHeadersExtractorMiddleware_genObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_self__;
    PyObject *_header_names;
    PyObject *_validation_config;
    PyObject *_base_name;
    PyObject *_header_names_property;
} asgi_context___headers_extrator___build_HeadersExtractorMiddlewareFactory_envObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    vectorcallfunc vectorcall;
    PyObject *___mypyc_env__;
} asgi_context___headers_extrator_____mypyc_lambda__0_build_HeadersExtractorMiddlewareFactory_objObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    vectorcallfunc vectorcall;
    PyObject *___mypyc_env__;
} asgi_context___headers_extrator_____mypyc_lambda__1_build_HeadersExtractorMiddlewareFactory_objObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
} asgi_context___context___RequestContextExceptionObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
} asgi_context___context___ContextObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    vectorcallfunc vectorcall;
    PyObject *_app;
} asgi_context___context___ContextMiddlewareObject;

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
} asgi_context___context___new_context_envObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_env__;
} asgi_context___context___new_context_genObject;

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
} asgi_context___context_____call___3_ContextMiddleware_envObject;

typedef struct {
    PyObject_HEAD
    CPyVTableItem *vtable;
    PyObject *___mypyc_env__;
} asgi_context___context_____call___3_ContextMiddleware_genObject;


struct export_table_dd3465df282eef100818 {
    PyObject **CPyStatic_headers_extrator___asgi_context___headers_extrator___HeadersExtractorMiddlewareFactory___build___validation_config;
    PyTypeObject **CPyType_headers_extrator___ValidationConfig;
    PyObject *(*CPyDef_headers_extrator___ValidationConfig)(PyObject *cpy_r_args, PyObject *cpy_r_kwargs);
    PyTypeObject **CPyType_headers_extrator___AbstractHeadersExtractorMiddleware;
    PyObject *(*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware)(PyObject *cpy_r_app);
    PyTypeObject **CPyType_headers_extrator___HeadersExtractorMiddlewareFactory;
    PyObject *(*CPyDef_headers_extrator___HeadersExtractorMiddlewareFactory)(void);
    PyTypeObject **CPyType_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_env;
    PyObject *(*CPyDef_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_env)(void);
    PyTypeObject **CPyType_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_gen;
    PyObject *(*CPyDef_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_gen)(void);
    PyTypeObject **CPyType_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_env;
    PyObject *(*CPyDef_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_env)(void);
    PyTypeObject **CPyType_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_gen;
    PyObject *(*CPyDef_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_gen)(void);
    PyTypeObject **CPyType_headers_extrator___build_HeadersExtractorMiddlewareFactory_env;
    PyObject *(*CPyDef_headers_extrator___build_HeadersExtractorMiddlewareFactory_env)(void);
    PyTypeObject **CPyType_headers_extrator_____mypyc_lambda__0_build_HeadersExtractorMiddlewareFactory_obj;
    PyObject *(*CPyDef_headers_extrator_____mypyc_lambda__0_build_HeadersExtractorMiddlewareFactory_obj)(void);
    PyTypeObject **CPyType_headers_extrator_____mypyc_lambda__1_build_HeadersExtractorMiddlewareFactory_obj;
    PyObject *(*CPyDef_headers_extrator_____mypyc_lambda__1_build_HeadersExtractorMiddlewareFactory_obj)(void);
    char (*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware_____init__)(PyObject *cpy_r_self, PyObject *cpy_r_app);
    char (*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware_____init___3__AbstractHeadersExtractorMiddleware_glue)(PyObject *cpy_r_self, PyObject *cpy_r_app);
    PyObject *(*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware___header_names)(PyObject *cpy_r_self);
    PyObject *(*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware___header_names__AbstractHeadersExtractorMiddleware_glue)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware___validation_config)(PyObject *cpy_r_self);
    PyObject *(*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware___validation_config__AbstractHeadersExtractorMiddleware_glue)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_gen_____mypyc_generator_helper__)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_type, PyObject *cpy_r_value, PyObject *cpy_r_traceback, PyObject *cpy_r_arg);
    PyObject *(*CPyDef_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_gen_____next__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_gen___send)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_arg);
    PyObject *(*CPyDef_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_gen_____iter__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_gen___throw)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_type, PyObject *cpy_r_value, PyObject *cpy_r_traceback);
    PyObject *(*CPyDef_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_gen___close)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_headers_extrator_____call___3_AbstractHeadersExtractorMiddleware_gen_____await__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware_____call__)(PyObject *cpy_r_self, PyObject *cpy_r_scope, PyObject *cpy_r_receive, PyObject *cpy_r_send);
    PyObject *(*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware_____call___3__AbstractHeadersExtractorMiddleware_glue)(PyObject *cpy_r_self, PyObject *cpy_r_scope, PyObject *cpy_r_receive, PyObject *cpy_r_send);
    PyObject *(*CPyDef_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_gen_____mypyc_generator_helper__)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_type, PyObject *cpy_r_value, PyObject *cpy_r_traceback, PyObject *cpy_r_arg);
    PyObject *(*CPyDef_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_gen_____next__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_gen___send)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_arg);
    PyObject *(*CPyDef_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_gen_____iter__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_gen___throw)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_type, PyObject *cpy_r_value, PyObject *cpy_r_traceback);
    PyObject *(*CPyDef_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_gen___close)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_headers_extrator___send_response_AbstractHeadersExtractorMiddleware_gen_____await__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware___send_response)(PyObject *cpy_r_send, PyObject *cpy_r_status, PyObject *cpy_r_details);
    PyObject *(*CPyDef_headers_extrator___AbstractHeadersExtractorMiddleware___send_response__AbstractHeadersExtractorMiddleware_glue)(PyObject *cpy_r_send, PyObject *cpy_r_status, PyObject *cpy_r_details);
    PyObject *(*CPyDef_headers_extrator_____mypyc_lambda__0_build_HeadersExtractorMiddlewareFactory_obj_____get__)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_instance, PyObject *cpy_r_owner);
    PyObject *(*CPyDef_headers_extrator_____mypyc_lambda__0_build_HeadersExtractorMiddlewareFactory_obj_____call__)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_self);
    PyObject *(*CPyDef_headers_extrator_____mypyc_lambda__1_build_HeadersExtractorMiddlewareFactory_obj_____get__)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_instance, PyObject *cpy_r_owner);
    PyObject *(*CPyDef_headers_extrator_____mypyc_lambda__1_build_HeadersExtractorMiddlewareFactory_obj_____call__)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_self);
    PyObject *(*CPyDef_headers_extrator___HeadersExtractorMiddlewareFactory___build)(PyObject *cpy_r_base_name, PyObject *cpy_r_header_names, PyObject *cpy_r_validation_config);
    PyObject *(*CPyDef_headers_extrator___HeadersExtractorMiddlewareFactory____build_name)(PyObject *cpy_r_base_name);
    char (*CPyDef_headers_extrator_____top_level__)(void);
    char (*CPyDef_protocol_____top_level__)(void);
    PyTypeObject **CPyType_context___RequestContextException;
    PyTypeObject **CPyType_context___Context;
    PyObject *(*CPyDef_context___Context)(void);
    PyTypeObject **CPyType_context___ContextMiddleware;
    PyObject *(*CPyDef_context___ContextMiddleware)(PyObject *cpy_r_app);
    PyTypeObject **CPyType_context___new_context_env;
    PyObject *(*CPyDef_context___new_context_env)(void);
    PyTypeObject **CPyType_context___new_context_gen;
    PyObject *(*CPyDef_context___new_context_gen)(void);
    PyTypeObject **CPyType_context_____call___3_ContextMiddleware_env;
    PyObject *(*CPyDef_context_____call___3_ContextMiddleware_env)(void);
    PyTypeObject **CPyType_context_____call___3_ContextMiddleware_gen;
    PyObject *(*CPyDef_context_____call___3_ContextMiddleware_gen)(void);
    char (*CPyDef_context___Context_____init__)(PyObject *cpy_r_self);
    PyObject *(*CPyDef_context___Context___data)(PyObject *cpy_r_self);
    PyObject *(*CPyDef_context___new_context_gen_____mypyc_generator_helper__)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_type, PyObject *cpy_r_value, PyObject *cpy_r_traceback, PyObject *cpy_r_arg);
    PyObject *(*CPyDef_context___new_context_gen_____next__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_context___new_context_gen___send)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_arg);
    PyObject *(*CPyDef_context___new_context_gen_____iter__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_context___new_context_gen___throw)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_type, PyObject *cpy_r_value, PyObject *cpy_r_traceback);
    PyObject *(*CPyDef_context___new_context_gen___close)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_context___new_context)(void);
    char (*CPyDef_context___ContextMiddleware_____init__)(PyObject *cpy_r_self, PyObject *cpy_r_app);
    PyObject *(*CPyDef_context_____call___3_ContextMiddleware_gen_____mypyc_generator_helper__)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_type, PyObject *cpy_r_value, PyObject *cpy_r_traceback, PyObject *cpy_r_arg);
    PyObject *(*CPyDef_context_____call___3_ContextMiddleware_gen_____next__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_context_____call___3_ContextMiddleware_gen___send)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_arg);
    PyObject *(*CPyDef_context_____call___3_ContextMiddleware_gen_____iter__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_context_____call___3_ContextMiddleware_gen___throw)(PyObject *cpy_r___mypyc_self__, PyObject *cpy_r_type, PyObject *cpy_r_value, PyObject *cpy_r_traceback);
    PyObject *(*CPyDef_context_____call___3_ContextMiddleware_gen___close)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_context_____call___3_ContextMiddleware_gen_____await__)(PyObject *cpy_r___mypyc_self__);
    PyObject *(*CPyDef_context___ContextMiddleware_____call__)(PyObject *cpy_r_self, PyObject *cpy_r_scope, PyObject *cpy_r_receive, PyObject *cpy_r_send);
    char (*CPyDef_context_____top_level__)(void);
    char (*CPyDef_asgi_context_____top_level__)(void);
};
#endif
