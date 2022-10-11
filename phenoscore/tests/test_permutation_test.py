import unittest
import numpy as np
from random import shuffle
from phenoscore.hpo_phenotype.calc_hpo_sim import SimScorer
from phenoscore.permutationtest.permutation_test import PermutationTester
from phenoscore.phenoscorer import PhenoScorer
import os
# these are both and technical tests in one, although it will sometime fail (so might remove them)
# as p can occasionally be < 0.05 by random chance with the random tests

class SimScorerTester(unittest.TestCase):
    def setUp(self):
        self._simscorer = SimScorer(scoring_method='Resnik', sum_method='BMA')
        self._phenoscorer = PhenoScorer(gene_name='random', mode='both')

    def test_negative_control_permutation(self):
        nodes = list(self._simscorer.hpo_network.nodes())

        N_PATIENTS = 20

        X = []
        y = np.array([0] * int(N_PATIENTS / 2) + [1] * int(N_PATIENTS / 2))
        shuffle(y)

        for p in range(5):  # simulating resampling of controls
            features_rand = np.zeros((N_PATIENTS, 2623), dtype=object)
            for i in range(len(features_rand)):
                face_rand = np.random.uniform(-1, 1, 2622)
                hpo_rand = list(np.random.choice(nodes, size=np.random.randint(3, 30), replace=False))

                features_rand[i, :2622] = face_rand
                features_rand[i, 2622] = hpo_rand
            X.append(features_rand)
        permutation_tester = PermutationTester(self._simscorer, mode='both', bootstraps=100)
        permutation_tester.permutation_test_multiple_X(X, y)
        print("Brier:" + str(np.mean(permutation_tester.classifier_results)))
        print("AUC:" + str(np.mean(permutation_tester.classifier_aucs)))
        print("P value:" + str(permutation_tester.p_value))
        assert permutation_tester.p_value > 0.05

    def test_satb1_data(self):
        try:
            X, y, img_paths, df_data = self._phenoscorer.load_data_from_excel(os.path.join("..", "sample_data",
                                                                                           "satb1_data.xlsx"))
        except:
            X, y, img_paths, df_data = self._phenoscorer.load_data_from_excel(os.path.join("phenoscore", "sample_data",
                                                                                           "satb1_data.xlsx"))
        permutation_tester = PermutationTester(self._simscorer, mode=self._phenoscorer.mode, bootstraps=1000)
        permutation_tester.permutation_test(X, y)
        print("Brier:" + str(np.mean(permutation_tester.classifier_results)));
        print("AUC:" + str(np.mean(permutation_tester.classifier_aucs)));
        print("P value:" + str(permutation_tester.p_value))
        assert permutation_tester.p_value < 0.05

    def test_random_data(self):
        try:
            X, y, img_paths, df_data = self._phenoscorer.load_data_from_excel(os.path.join("..", "sample_data",
                                                                                       "random_generated_sample_data.xlsx"))
        except:
            X, y, img_paths, df_data = self._phenoscorer.load_data_from_excel(os.path.join("phenoscore", "sample_data",
                                                                                           "random_generated_sample_data.xlsx"))
        permutation_tester = PermutationTester(self._simscorer, mode=self._phenoscorer.mode, bootstraps=1000)
        permutation_tester.permutation_test(X, y)
        print("Brier:" + str(np.mean(permutation_tester.classifier_results)));
        print("AUC:" + str(np.mean(permutation_tester.classifier_aucs)));
        print("P value:" + str(permutation_tester.p_value))
        assert permutation_tester.p_value > 0.05