from math import radians, sin, cos, sqrt, atan2

class HarversineCalculator:

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        # Radius der Erde in Kilometern
        R = 6371.0

        # Umrechnung der Breiten- und Längengrade von Grad in Radian
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Deltas der Breiten- und Längengrade
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Haversine-Formel
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Entfernung berechnen
        distance = R * c

        return distance