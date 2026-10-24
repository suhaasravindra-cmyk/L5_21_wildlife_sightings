"""Record wildlife sightings and summarise them by zone and species.

Lab 5 - R Suhaas, PES2UG24CS389, Section G.
"""

from contextlib import closing
import hashlib
import sqlite3


def log_sighting(connection, species, zone, count, extras=None):
    """Store a sighting and update supplied totals, or create fresh ones."""
    if not isinstance(species, str) or not species.strip():
        raise ValueError("Species must be a non-empty string.")
    if not isinstance(zone, str) or not zone.strip():
        raise ValueError("Zone must be a non-empty string.")
    if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
        raise ValueError("Count must be a positive integer.")
    if extras is None:
        extras = {}
    connection.execute(
        "INSERT INTO sightings (species, zone, count) VALUES (?, ?, ?)",
        (species, zone, count),
    )
    extras[species] = extras.get(species, 0) + count
    return extras


def observer_id(observer):
    """Return a stable SHA-256 label, not an authentication credential."""
    return hashlib.sha256(observer.encode("utf-8")).hexdigest()


def zone_summary(connection, zone):
    """Return the total animal count for a zone, or zero if it is empty."""
    row = connection.execute(
        "SELECT SUM(count) FROM sightings WHERE zone = ?", (zone,)
    ).fetchone()
    if row[0] is None:
        return 0
    return row[0]


def rarest(connection):
    """Return a species with the lowest total count, or None if empty."""
    rows = connection.execute(
        "SELECT species, SUM(count) FROM sightings GROUP BY species"
    ).fetchall()
    if not rows:
        return None
    rarest_sighting = min(rows, key=lambda row: row[1])
    return rarest_sighting[0]


def main():
    """Run the sample sightings log and close its temporary database."""
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.execute(
            "CREATE TABLE sightings "
            "(id INTEGER PRIMARY KEY, species TEXT, zone TEXT, count INTEGER)"
        )
        totals = log_sighting(connection, "Leopard", "North", 1)
        log_sighting(connection, "Chital", "North", 24, totals)
        log_sighting(connection, "Hornbill", "East", 3, totals)
        if len(totals) != 3:
            raise RuntimeError("The demonstration should contain 3 species.")
        print(
            observer_id("Arun"),
            zone_summary(connection, "North"),
            rarest(connection),
        )


if __name__ == "__main__":
    main()
