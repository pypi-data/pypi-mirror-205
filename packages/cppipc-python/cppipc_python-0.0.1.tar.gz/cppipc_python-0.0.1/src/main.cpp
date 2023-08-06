#include <pybind11/pybind11.h>
#include <signal.h>
#include <iostream>
#include <string>
#include <thread>
#include <vector>
#include <chrono>
#include <atomic>

#include "libipc/ipc.h"

namespace py = pybind11;

#define send_tm 1000
#define recv_tm 1000

using namespace ipc;

class py_channel: public channel
{
    using channel::channel; // Inherit the constructor
public:
    py::bytes py_recv(std::uint64_t tm = invalid_value) {
        py::gil_scoped_release release;
        buff_t buff = channel::recv(tm);
        py::gil_scoped_acquire acquire;
        if (PyErr_CheckSignals() != 0)
            throw py::error_already_set();
        if (!buff.empty()){
            char const* b = buff.get<char const*>();
            return py::bytes(b, buff.size());
        } 
        else
        {
            return py::bytes("", 0);
        }
    }

    bool py_send(py::bytes bytes, std::uint64_t tm = default_timeout) {
        // 获得数据指针和大小
        char* data = PYBIND11_BYTES_AS_STRING(bytes.ptr());
        size_t size = static_cast<size_t>(PYBIND11_BYTES_SIZE(bytes.ptr()));
        return channel::send(data, size, tm);
    }

    void py_close() {
        return channel::disconnect();
    }

};






class py_route: public route
{
    using route::route; // Inherit the constructor
public:
    py::bytes py_recv(std::uint64_t tm = invalid_value) {
        py::gil_scoped_release release;
        buff_t buff = route::recv(tm);
        py::gil_scoped_acquire acquire;
        if (PyErr_CheckSignals() != 0)
            throw py::error_already_set();
        if (!buff.empty()){
            char const* b = buff.get<char const*>();
            return py::bytes(b, buff.size());
        } 
        else
        {
            return py::bytes("", 0);
        }
    }

    bool py_send(py::bytes bytes, std::uint64_t tm = default_timeout) {
        // 获得数据指针和大小
        char* data = PYBIND11_BYTES_AS_STRING(bytes.ptr());
        size_t size = static_cast<size_t>(PYBIND11_BYTES_SIZE(bytes.ptr()));
        return route::send(data, size, tm);
    }

    void py_close() {
        return route::disconnect();
    }

};





PYBIND11_MODULE(cppipc_python, m) {

    py::class_<py_channel>(m, "py_channel")
        .def(py::init([](std::string channel, std::string role) 
        {
            const char* cstr = channel.c_str();
            if (role=="receiver"){
                return std::unique_ptr<py_channel>(new py_channel(cstr, receiver));
            }
            else if (role=="sender"){
                return std::unique_ptr<py_channel>(new py_channel(cstr, sender));
            }
            else{
                return std::unique_ptr<py_channel>(nullptr);
            }
        }))
        .def("py_recv", &py_channel::py_recv)
        .def("py_send", &py_channel::py_send)
        .def("py_close", &py_channel::py_close);

    py::class_<py_route>(m, "py_route")
        .def(py::init([](std::string channel, std::string role) 
        {
            const char* cstr = channel.c_str();
            if (role=="receiver"){
                return std::unique_ptr<py_route>(new py_route(cstr, receiver));
            }
            else if (role=="sender"){
                return std::unique_ptr<py_route>(new py_route(cstr, sender));
            }
            else{
                return std::unique_ptr<py_route>(nullptr);
            }
        }))
        .def("py_recv", &py_route::py_recv)
        .def("py_send", &py_route::py_send)
        .def("py_close", &py_route::py_close);

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)
#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
