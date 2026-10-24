"""Behaviour checks for the Lab 5 fixes."""

import contextlib
import importlib
import io
import sqlite3
import unittest

import wildlife_sightings as wildlife


class SightingsTests(unittest.TestCase):
    """Check normal results and cases that the original program missed."""

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.connection.execute(
            "CREATE TABLE sightings "
            "(id INTEGER PRIMARY KEY, species TEXT, zone TEXT, count INTEGER)"
        )

    def test_sample_totals(self):
        totals = wildlife.log_sighting(self.connection, "Leopard", "North", 1)
        wildlife.log_sighting(self.connection, "Chital", "North", 24, totals)
        wildlife.log_sighting(self.connection, "Hornbill", "East", 3, totals)
        self.assertEqual(totals, {"Leopard": 1, "Chital": 24, "Hornbill": 3})
        self.assertEqual(wildlife.zone_summary(self.connection, "North"), 25)
        self.assertEqual(wildlife.rarest(self.connection), "Leopard")

    def test_defaults_are_independent(self):
        first = wildlife.log_sighting(self.connection, "Leopard", "North", 1)
        second = wildlife.log_sighting(self.connection, "Chital", "North", 2)
        self.assertIsNot(first, second)
        self.assertEqual(first, {"Leopard": 1})
        self.assertEqual(second, {"Chital": 2})

    def test_explicit_totals_are_updated(self):
        totals = {}
        result = wildlife.log_sighting(
            self.connection, "Leopard", "North", 1, totals
        )
        wildlife.log_sighting(self.connection, "Leopard", "East", 2, totals)
        self.assertIs(result, totals)
        self.assertEqual(totals, {"Leopard": 3})

    def test_quotes_are_stored_as_data(self):
        species = "Pallas's cat"
        zone = "North'); DROP TABLE sightings; --"
        wildlife.log_sighting(self.connection, species, zone, 2)
        row = self.connection.execute(
            "SELECT species, zone, count FROM sightings"
        ).fetchone()
        self.assertEqual(row, (species, zone, 2))
        self.assertEqual(wildlife.zone_summary(self.connection, zone), 2)

    def test_invalid_counts_leave_data_unchanged(self):
        totals = {}
        for count in (0, -1, 1.5, "2", True, None):
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    wildlife.log_sighting(
                        self.connection, "Leopard", "North", count, totals
                    )
        self.assertEqual(totals, {})
        self.assertEqual(wildlife.zone_summary(self.connection, "North"), 0)

    def test_invalid_names_are_rejected(self):
        for species, zone in (("", "N"), ("A", " "), (None, "N"), ("A", 5)):
            with self.subTest(species=species, zone=zone):
                with self.assertRaises(ValueError):
                    wildlife.log_sighting(self.connection, species, zone, 1)
        self.assertIsNone(wildlife.rarest(self.connection))

    def test_empty_database(self):
        self.assertEqual(wildlife.zone_summary(self.connection, "Unknown"), 0)
        self.assertIsNone(wildlife.rarest(self.connection))

    def test_rarest_uses_species_totals(self):
        wildlife.log_sighting(self.connection, "Leopard", "North", 1)
        wildlife.log_sighting(self.connection, "Leopard", "East", 10)
        wildlife.log_sighting(self.connection, "Hornbill", "East", 3)
        self.assertEqual(wildlife.rarest(self.connection), "Hornbill")

    def test_observer_label(self):
        expected = (
            "e753d3a08b7608e542a9ae2a0107bedf"
            "5dc548dadb1fe51b7d6f923a44431e69"
        )
        self.assertEqual(wildlife.observer_id("Arun"), expected)
        self.assertNotEqual(wildlife.observer_id("Arun"),
                            wildlife.observer_id("Meera"))

    def test_import_does_not_run_demo(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            importlib.reload(wildlife)
        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
