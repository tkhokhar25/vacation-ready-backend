from database_utils import fetch_similar_trips

def similar_trips(json_data):
    return fetch_similar_trips(json_data['place_id'])

