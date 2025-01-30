import unittest
import numpy as np
from aya import calculate_absorption, calculate_reflection, update_temperature

class TestAyaFunctions(unittest.TestCase):

    def test_calculate_absorption(self):
        self.assertAlmostEqual(calculate_absorption(0), 0.8)
        self.assertAlmostEqual(calculate_absorption(300), 0.8 * np.exp(-1))
        self.assertAlmostEqual(calculate_absorption(600), 0.8 * np.exp(-2))

    def test_calculate_reflection(self):
        self.assertAlmostEqual(calculate_reflection(0), 0.2)
        self.assertAlmostEqual(calculate_reflection(100), 0.2 + 0.1 * np.sin(1))
        self.assertAlmostEqual(calculate_reflection(200), 0.2 + 0.1 * np.sin(2))

    def test_update_temperature(self):
        global temperature
        initial_temp = np.zeros((40, 40))
        initial_temp[20, 20] = 100
        temperature = initial_temp
        updated_temp = update_temperature(0)
        self.assertEqual(updated_temp.shape, (40, 40))
        self.assertNotEqual(updated_temp[20, 20], 100)  # Температура должна измениться

if __name__ == '__main__':
    unittest.main()
