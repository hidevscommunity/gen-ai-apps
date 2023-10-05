
from geopy.distance import great_circle
from Supabase.Extractor import SupabaseExtractor

class GeoCalculator:
    """Class for calculating distance between two points coordinates lat and lng"""
    supplier_info = SupabaseExtractor.extractAllSupplierInfo()
    @classmethod
    def calculateDistance(cls, coordinate1: tuple[float, float], coordinate2: tuple[float, float]) -> float:
        """
        Returns distance between two points in kilometers using geopy's great_circle method.
        """
        # Create geopy points from the coordinates
        point1 = (coordinate1[0], coordinate1[1])
        point2 = (coordinate2[0], coordinate2[1])

        # Calculate the distance using great_circle method
        distance = great_circle(point1, point2).kilometers

        return distance
    
    @classmethod
    def calculateDistanceFromSupplier(cls, coordinate: tuple[float, float]) -> dict:
        """
        Purpose: Given the location coordinates of a disruptuon event (lat, lng), calculate the distance from the event to all the suppliers.
        Returns: Sorted dictionary of suppliers by distance from the event.
        """
        distance_from_supplier = {}
        for supplier in cls.supplier_info:
            supplier_coordinate = (supplier['lat'], supplier['lng'])
            distance = cls.calculateDistance(coordinate, supplier_coordinate)
            distance_from_supplier[supplier['Name']] = distance

        # Sort the dictionary by increasing order of distance
        distance_from_supplier = dict(sorted(distance_from_supplier.items(), key=lambda item: item[1]))
        # print('distance_from_supplier top5: ', list(distance_from_supplier.items())[:5])

        return distance_from_supplier

class DisruptionEventRanker:
    """Ranks the disruption events by distance from the suppliers"""

    def addRiskScore(disruption_event: dict) -> dict:
        """Given a disruption event, add a risk score to the event based on the distance from the event to it's nearest supplier.
        Returns:
            > disruption_event: dict
                with 'risk_score' key added
        '"""
        # Add risk score "Low","Medium","High"
        # At least one supplier in the top 10 is within 50km 
        coordinate = (disruption_event['lat'], disruption_event['lng'])
        distance_from_supplier = GeoCalculator.calculateDistanceFromSupplier(coordinate)
        if min(list(distance_from_supplier.values())[:10]) <= 50:
            disruption_event['risk_score'] = 'High'
        # At least one supplier in the top 10 is within 150km
        elif min(list(distance_from_supplier.values())[:10]) <= 150:
            disruption_event['risk_score'] = 'Medium'
        else:
            disruption_event['risk_score'] = 'Low'

        return disruption_event
    def addSupplierMapping(disruption_event:dict) -> dict:
        """"Addes the 'supplier' and the 'avg_distance_top_10' keys to the disruption event"""
        try:
            coordinate = (disruption_event['lat'], disruption_event['lng'])
            distance_from_supplier = GeoCalculator.calculateDistanceFromSupplier(coordinate)
            # Calculate the average distance from the event to the nearest 10 suppliers
            avg_distance_top_10 = sum(list(distance_from_supplier.values())[:10]) / 10
            disruption_event['avg_distance_top_10(km)'] = avg_distance_top_10
            # Add the list of suppliers sorted by distance from the event
            disruption_event['suppliers'] = [{'Name': supplier_name, 'distance': distance} for supplier_name, distance in distance_from_supplier.items()]
            # Sort the list of suppliers by increasing order of distance
            disruption_event['suppliers'] = sorted(disruption_event['suppliers'], key=lambda k: k['distance'])
            return disruption_event
        except Exception as e:
            print(f'Error calculating distance from supplier: {e},returing the event without the distance from supplier')
            return disruption_event

    @classmethod
    def rankDisruptionEvents(cls, all_disruption_events: list[dict]) -> list[dict]:
        """
        Purpose: Rank the disruption events by calculating the average distance from the event to nearest 10 suppliers.
        disruption_event = {
            'id': 1,
            'Title': 'Title',
            ...,
            'avg_distance_top_10': 123.123
            'suppliers' : sorted list of suppliers by distance from event {
                [{'Name': 'Supplier1', 'distance': 123.123}, {'Name': 'Supplier2', 'distance': 123.123}, ...}]
            }
        }
        Returns:
            > Sorted list of disruption events by increasing order of average distance to top 10 suppliers
        """
        for disruption_event in all_disruption_events:
            disruption_event = cls.addSupplierMapping(disruption_event)
            disruption_event = cls.addRiskScore(disruption_event)
            
        # Sort the list of disruption events by increasing order of average distance to top 10 suppliers
        all_disruption_events = sorted(all_disruption_events, key=lambda k: k['avg_distance_top_10(km)'])
        return all_disruption_events