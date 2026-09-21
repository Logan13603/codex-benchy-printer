"""Analytical checks independent of the generated printer toolpaths."""
import math, unittest
from path_model import Move, duration, AF

def line(length, direction=(1.,0.,0.), e=0.):
    return Move(length,direction,e,1.,1000.,'test',.5)

class Kinematics(unittest.TestCase):
    def test_triangle(self):
        self.assertAlmostEqual(duration([line(10)],vmax=1000,accel=100)['seconds'],2*math.sqrt(.1))
    def test_trapezoid(self):
        self.assertAlmostEqual(duration([line(100)],vmax=10,accel=100)['seconds'],10.1)
    def test_collinear_partition_invariant(self):
        a=duration([line(100)],vmax=100,accel=1000)['seconds']
        b=duration([line(1)]*100,vmax=100,accel=1000)['seconds']
        self.assertAlmostEqual(a,b)
    def test_reverse_full_stop(self):
        a=duration([line(10)],accel=100)['seconds']
        b=duration([line(10),line(10,(-1.,0.,0.))],accel=100)['seconds']
        self.assertAlmostEqual(2*a,b)
    def test_flow_lower_bound(self):
        t=duration([line(100,e=100/AF)],flow=10,accel=1000)['seconds']
        self.assertGreaterEqual(t,10.)
    def test_corner_slower_than_straight(self):
        straight=duration([line(10),line(10)],accel=1000)['seconds']
        corner=duration([line(10),line(10,(0.,1.,0.))],accel=1000)['seconds']
        self.assertGreater(corner,straight)
    def test_external_axis_acceleration_cap(self):
        t=duration([line(10)],vmax=1000,accel=100,axis_caps=[(1000,25)])['seconds']
        self.assertAlmostEqual(t,2*math.sqrt(10/25))

if __name__=='__main__': unittest.main()
