""" модуль тестування  методів класу BinarySearchPrefix
"""
import unittest
import time
from  Prefix import BinarySearchPrefix, BinarySearchPrefixMultiProcessing, BinarySearchPrefixMultiThreding,\
    Param, Result
from  testset import read_list_from_file, FILE_NAME


class PrefixTest(unittest.TestCase):
    list_1 = ['0asdf',  '1assdf',  "2bfg", "3bfga", "4bfgb", "5cdf", "6edf"]

    def setUp(self) -> None:
        self.test_list = read_list_from_file(FILE_NAME)
        self.binary_srch=BinarySearchPrefix()
        self.res = {'': (0, 9_999_999),
               'i': (3078925, 3463572),
               'ix': (3419156, 3433966),
               'ixv': (3431186, 3431744),
               'ixve': (3431265, 3431282),
               'ixvec': (3431267, 3431269),
               'ixveca': (3431267, 3431267),
               'ixvecad': (3431267, 3431267),
               'ixvecady': (3431267, 3431267),
               'ixvecadyk': (3431267, 3431267),
               'ixvecadykd': (3431267, 3431267),
               'ixvecadykdz': (3431267, 3431267),
               'ixvecadykdzg': (3431267, 3431267),
               'ixvecadykdzgm': (3431267, 3431267),
               'ixvecadykdzgmx': (3431267, 3431267)
               }


    def test_get_safety_neighborhood(self):
        """

        :return:
        тестування функції безпечного пошуку сусідніх елементів та його індексу
        """

        res=[]
        wait_left_res=[(None,1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, None)]
        for mid in range(0, len(self.list_1)):
            res.append(self.binary_srch.get_safety_neighborhoods(self.list_1, mid))
        self.assertListEqual(res, wait_left_res)

    def  test_get_safety_neighborhood_raises(self):
        """

        :return:
        тестування генерації виключення у функції безпечного пошуку сусідніх елементів
        """
        for mid in [-1, len(self.list_1), len(self.list_1)+1]:
            with self.assertRaises(ValueError):
                self.binary_srch.get_safety_neighborhoods(self.list_1, mid)



    def test_find_prefix(self):


        pref = 'aaaaceigqmeqoll'
        idx_left, idx_right = self.binary_srch.find_prefix(self.test_list, pref)
        self.assertEqual((0,0), (idx_left, idx_right))

        pref = 'zzzzxgcihzacyzt'
        idx_left, idx_right = self.binary_srch.find_prefix(self.test_list, pref)
        self.assertEqual((9_999_999, 9_999_999), (idx_left, idx_right))


        pref = 'aaaaceigqmeqollz'
        idx_left, idx_right = self.binary_srch.find_prefix(self.test_list, pref)
        self.assertEqual(Result.notfind, idx_left)
        self.assertEqual(Result.notfind, idx_right)

    def test_find_prefix_2(self):

        pref = "ixvecadykdzgmxq"
        start_time = time.time()
        for i in range(len(pref)):
            sub_pref = pref[0:i]
            idx_left, idx_right = self.binary_srch.find_prefix(self.test_list, sub_pref)
            self.assertEqual(self.res[sub_pref],(idx_left, idx_right))
        print(f" single process--- {time.time() - start_time} seconds ---")

    def test_find_prefix_multiprocesing(self):
        pref = "ixvecadykdzgmxq"
        inst = BinarySearchPrefixMultiProcessing()
        start_time = time.time()
        for i in range(len(pref)):
            sub_pref = pref[0:i]
            idx_left, idx_right = inst.find_prefix(self.test_list, sub_pref)
            self.assertEqual(self.res[sub_pref], (idx_left, idx_right))
        print(f" multi process--- {time.time() - start_time} seconds ---")

    def testtest_find_prefix_multithreding(self):
        pref = "ixvecadykdzgmxq"
        inst = BinarySearchPrefixMultiThreding()
        start_time = time.time()
        for i in range(len(pref)):
            sub_pref = pref[0:i]
            idx_left, idx_right = inst.find_prefix(self.test_list, sub_pref)
            self.assertEqual(self.res[sub_pref], (idx_left, idx_right))
        print(f" multi threding--- {time.time() - start_time} seconds ---")

    def test_clasic(self):
        pref = "ixvecadykdzgmxq"
        start_time = time.time()
        for i in range(len(pref)):
            sub_pref = pref[0:i]
            res = [s for s in self.test_list if s.startswith(sub_pref)]
        print(f"clasic method--- {time.time() - start_time} seconds ---")


if __name__ == "__main__":
    unittest.main()
