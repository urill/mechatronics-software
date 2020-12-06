import pyamp1394 as ampio
import sys
p = ampio.FirewirePort(0)
a = ampio.AmpIO(0, 10)
p.add_board(a)

print(a.get_motor_current(1))
print(a.get_firmware_version())

import timeit
def time_function(p, a):
    p.read_all_boards()
    a.get_motor_current(1)
t = timeit.timeit(lambda: time_function(p,a), number=1000)
print(t)
