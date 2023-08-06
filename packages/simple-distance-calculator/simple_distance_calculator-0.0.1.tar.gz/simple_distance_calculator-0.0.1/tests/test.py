import unittest

from simple_distance_calculator.distance import haversine_distance, get_coordinates, spherical_law_of_cosines_distance, get_address, equirectangular_approximation

class TestDistanceFunctions(unittest.TestCase):

    def test_haversine_distance(self):
        # Atstumas tarp tu paciu koordinaciu
        self.assertAlmostEqual(haversine_distance(54.6872, 25.2797, 54.6872, 25.2797), 0.0, places=2)

        # Atstumas tarp Studentu g. 50 ir studentu g. 48
        self.assertAlmostEqual(haversine_distance(54.9037, 23.9578, 54.9057, 23.9562), 0.24, places=2)

    def test_get_coordinates(self):
        # Gedimino pilies koordinates
        self.assertEqual(get_coordinates("Gedimino pilis"), (54.686758350000005, 25.29068448063221))

        # test getting coordinates of a location that does not exist
        with self.assertRaises(IndexError):
            get_coordinates("This location does not exist")

    def test_spherical_law_of_cosines_distance(self):
        # Atstumas tarp tu paciu koordinaciu
        self.assertAlmostEqual(spherical_law_of_cosines_distance(54.6872, 25.2797, 54.6872, 25.2797), 0.0, places=3)

        # Atstumas tarp Studentu g. 50 ir studentu g. 48
        self.assertAlmostEqual(spherical_law_of_cosines_distance(54.9037, 23.9578, 54.9057, 23.9562), 0.24, places=2)

    def test_get_address(self):
        # Gedimino pilies koordinates
        self.assertEqual(get_address(54.686758350000005, 25.29068448063221), ("Gedimino pilis, 5, Arsenalo g., Senamiestis, Senamiesčio seniūnija, Vilnius, Vilniaus miesto savivaldybė, Vilniaus apskritis, 01143, Lietuva"))

    def test_equirectangular_approximation(self):
        # Atstumas tarp tu paciu koordinaciu
        self.assertAlmostEqual(equirectangular_approximation(54.6872, 25.2797, 54.6872, 25.2797), 0.0, places=2)

        # Atstumas tarp Studentu g. 50 ir studentu g. 48
        self.assertAlmostEqual(equirectangular_approximation(54.9037, 23.9578, 54.9057, 23.9562), 0.24, places=2)

if __name__ == '__main__':
    unittest.main()