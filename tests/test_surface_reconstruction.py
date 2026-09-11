import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'paper_output/code/modeling'))
from core_solver import reconstruct_surface, sample_and_interpolate_fixed, sample_and_interpolate_moving


class SurfaceReconstructionTests(unittest.TestCase):
    def test_robin_flux_balance(self):
        times = np.array([60.0, 120.0])
        T = np.array([310.0, 315.0])
        C = np.array([1.5, 0.2])
        delta = np.array([0.000125, 0.000075])
        te = np.array([0.0, 120.0])
        Ta = np.array([320.0, 325.0])
        Ca = np.array([0.04, 0.05])
        coefficients = [
            (0.36, 7e-9 * np.exp(-0.89 / C)),
            (0.21 + 0.38 * C / (C + 1), 2.4e-3 * np.exp(-0.45 / C - 3850 / T)),
            (0.12 + 0.20 * C / (C + 1), 4.2e-4 * np.exp(-0.30 / C - 3850 / T)),
        ]
        for mode, (k, D) in enumerate(coefficients, 1):
            Ts, Cs = reconstruct_surface(times, T, C, delta, te, Ta, Ca, mode, 25.0, 8e-7)
            np.testing.assert_allclose(k * (T - Ts) / delta, 25 * (Ts - np.interp(times, te, Ta)), atol=1e-9)
            np.testing.assert_allclose(D * (C - Cs) / delta, 8e-7 * (Cs - np.interp(times, te, Ca)), atol=1e-18)
            self.assertTrue(np.all(Ts > T))
            self.assertTrue(np.all(Cs < C))

    def test_fixed_and_moving_surface_sampling(self):
        times = np.array([0.0, 60.0])
        T = np.array([[301.15, 301.15], [310.0, 315.0]])
        C = np.array([[2.55, 2.55], [1.5, 1.0]])
        te = np.array([0.0, 60.0])
        Ta = np.array([301.15, 323.15])
        Ca = np.array([0.02, 0.05])
        radii = np.array([0.0, 1.5, 1.75, 2.0])
        _, Cf = sample_and_interpolate_fixed(times, T, C, 2, 0.02, radii, te, Ta, Ca, 3)
        Cm, Cs = sample_and_interpolate_moving(times, np.full(2, 0.02), T, C, 2, radii, te, Ta, Ca)
        np.testing.assert_allclose(Cf, Cm)
        np.testing.assert_allclose(Cf[:, -1], Cs)
        np.testing.assert_allclose(Cf[:, 1], C[:, -1])
        np.testing.assert_allclose(Cf[:, 2], (C[:, -1] + Cs) / 2)
        np.testing.assert_allclose(Cf[0], 2.55)
        Cm, Cs = sample_and_interpolate_moving(times, np.array([0.02, 0.015]), T, C, 2, radii, te, Ta, Ca)
        self.assertEqual(Cm[1, 1], Cs[1])
        self.assertTrue(np.isnan(Cm[1, 2:]).all())


if __name__ == '__main__':
    unittest.main()
