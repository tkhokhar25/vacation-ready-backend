from database_utils import upsert_into_database
from table_names import kPLACE_REVIEWS_TABLE

def review_place(json_data):
    keys = '(' + 'place_id' + ', ' + json_data['action'] + 's)'
    values = "('" + json_data['place_id'] + "', " + "1)"

    return upsert_into_database(kPLACE_REVIEWS_TABLE, keys, values, 'place_id', json_data['action'] + 's')