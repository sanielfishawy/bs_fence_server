from typing import Set
import unittest
from threading import Thread
from saw_state import SawState
import time

class TestFenceState(unittest.TestCase):

    def test_max_position_limit(self):
        max = 50
        SawState.set_max_position(max)
        self.assertEqual(SawState.get_max_position(), max)
        SawState.set_position(max + 10)
        self.assertEqual(SawState.get_position(), max)
        SawState.set_position(max - 10)
        self.assertEqual(SawState.get_position(), max - 10)
        SawState.change_position(20)
        self.assertEqual(SawState.get_position(), max)

    def test_min_position_limit(self):
        min = -50
        SawState.set_min_position(min)
        self.assertEqual(SawState.get_min_position(), min)
        SawState.set_position(min - 10)
        self.assertEqual(SawState.get_position(), min)
        SawState.set_position(min + 10)
        self.assertEqual(SawState.get_position(), min + 10)
        SawState.change_position(-20)
        self.assertEqual(SawState.get_position(), min)

    def test_set_min_max(self):
        SawState.set_limits_set(False)
        self.assertFalse(SawState.get_limits_set())
        SawState.set_min_and_max_position(-29, 30)
        self.assertEqual(SawState.get_min_position(), -29)
        self.assertEqual(SawState.get_max_position(), 30)

    def test_set_and_get_position_inches(self):
        rpi = 10
        zp = 25
        SawState.set_min_and_max_position(-150, 100)
        SawState.set_revolutions_per_inch(rpi)
        self.assertEqual(SawState.get_revolutions_per_inch(), rpi)
        SawState.set_zero_position(zp)
        self.assertEqual(SawState.get_zero_position(), zp)
        SawState.set_position_inches(0)
        self.assertEqual(SawState.get_position(), zp)
        SawState.set_position_inches(2)
        self.assertEqual(SawState.get_position(), 2*rpi + zp)

    def test_control_from_multiple_threads(self):
        SawState.set_position(0)
        self.assertEqual(SawState.get_position(), 0)
        SetPositionThread().start()
        time.sleep(.001)
        self.assertEqual(SawState.get_position(), SetPositionThread.POS)



class SetPositionThread(Thread):
    POS = 30

    def run(self):
        SawState.set_position(self.__class__.POS)

if __name__ == '__main__':
    unittest.main()

