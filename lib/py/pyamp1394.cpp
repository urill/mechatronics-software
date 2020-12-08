#include <pybind11/pybind11.h>
#include "AmpIO.h"
#include "FirewirePort.h"

namespace py = pybind11;

PYBIND11_MODULE(pyamp1394, m)
{
    py::class_<BoardIO>(m, "BoardIO");
    py::class_<AmpIO, BoardIO> ampio(m, "AmpIO");
    ampio.def(py::init<AmpIO_UInt8, unsigned int>())
        .def("get_firmware_version", &AmpIO::GetFirmwareVersion)
        .def("get_motor_current", &AmpIO::GetMotorCurrent)
        .def("write_current_loop_parameters", &AmpIO::WriteCurrentLoopParameters)
        .def("write_motor_control_mode", &AmpIO::WriteMotorControlMode)
        .def("set_motor_current", &AmpIO::SetMotorCurrent);
    py::enum_<AmpIO::MotorControlMode>(ampio, "MotorControlMode")
        .value("PWM_DUTY_CYCLE", AmpIO::MotorControlMode::PWM_DUTY_CYCLE)
        .value("CURRENT", AmpIO::MotorControlMode::CURRENT)
        .export_values();

    py::class_<FirewirePort>(m, "FirewirePort")
        .def(py::init(
            [](int port) {
                return new FirewirePort(port);
            }))
        .def("add_board", &FirewirePort::AddBoard)
        .def("read_all_boards", &FirewirePort::ReadAllBoards)
        .def("write_all_boards", &FirewirePort::WriteAllBoards);
}
