#include <pybind11/pybind11.h>
#include "AmpIO.h"
#include "FirewirePort.h"

namespace py = pybind11;

PYBIND11_MODULE(pyamp1394, m)
{
    py::class_<BoardIO>(m, "BoardIO");
    py::class_<AmpIO, BoardIO>(m, "AmpIO")
        .def(py::init<AmpIO_UInt8, unsigned int>())
        .def("get_firmware_version", &AmpIO::GetFirmwareVersion)
        .def("get_motor_current", &AmpIO::GetMotorCurrent);
    py::class_<FirewirePort>(m, "FirewirePort")
        .def(py::init(
            [](int port) {
                return new FirewirePort(port);
            }))
        .def("add_board", &FirewirePort::AddBoard)
        .def("read_all_boards", &FirewirePort::ReadAllBoards);
}
