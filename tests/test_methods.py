import unittest
import numpy as np
from rrt_demo.synthetic import generate
from rrt_demo.estimators import aipw_scores, estimate, balance
from rrt_demo.temporal import validate_timeline, observed_early_label


class CausalChecks(unittest.TestCase):
    def test_synthetic_reproducibility_and_observation_window(self):
        a, _ = generate(200, 7)
        b, _ = generate(200, 7)
        self.assertTrue(a.equals(b))
        self.assertTrue((a.followup_days > 0).all())
        self.assertTrue((a.followup_days <= 30).all())
        self.assertTrue((a.event == a.outcome_30d).all())

    def test_double_robustness_in_large_oracle_simulation(self):
        df, truth = generate(150000, 42)
        a, y = df.treatment.to_numpy(), df.outcome_30d.to_numpy()
        target = np.mean(truth["risk1"] - truth["risk0"])
        # Either nuisance may be misspecified when the other is exactly known.
        for e, m0, m1 in [(truth["propensity"], np.zeros(len(df)), np.zeros(len(df))),
                         (np.full(len(df), 0.5), truth["risk0"], truth["risk1"])]:
            self.assertLess(abs(aipw_scores(a, y, e, m0, m1).mean() - target), 0.012)

    def test_fitted_estimator_recovers_known_effect(self):
        df, truth = generate(8000, 11)
        result, _, _, bal = estimate(df, 11)
        self.assertLess(abs(result["aipw_risk_difference"] - np.mean(truth["risk1"] - truth["risk0"])), 0.045)
        self.assertLess(bal.smd_after.abs().max(), 0.12)

    def test_continuous_smd_is_scale_invariant(self):
        df, _ = generate(500, 3)
        a = df.treatment.to_numpy()
        first = balance(df, a, np.ones(len(df)))
        df["severity"] = df.severity * 100 + 500
        second = balance(df, a, np.ones(len(df)))
        np.testing.assert_allclose(first.smd_after, second.smd_after)

    def test_temporal_rejections_and_boundaries(self):
        for args in [(0, 1, None, 10), (0, -1, -1, 10), (0, -1, 20, 10), (0, -1, None, -1)]:
            with self.assertRaises(ValueError):
                validate_timeline(*args)
        validate_timeline(0, -1, 24, 48)
        self.assertEqual(observed_early_label(24), 1)
        self.assertEqual(observed_early_label(24.01), 0)
        self.assertEqual(observed_early_label(None), 0)
        with self.assertRaises(ValueError):
            observed_early_label(-1)


if __name__ == "__main__":
    unittest.main()
