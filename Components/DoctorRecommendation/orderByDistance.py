import pandas as pd
import requests
from geopy.distance import geodesic

def orderByDistance(doctors_info_df,doctorsID_df, patientCity):
    df=doctors_info_df[doctors_info_df['Doctor_ID'].isin(doctorsID_df[0].values)]
    # this function obtains the latitude and longitude points of a location from GeoDB API
    def get_lat_long(location):
        url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/cities?namePrefix={location.split(',')[0]}"
        headers = {
            'x-rapidapi-key': 'b9cfcb04ffmshf71fdcb719a66dfp1a2547jsn9c7baa131119', 
            'x-rapidapi-host': 'wft-geo-db.p.rapidapi.com'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                return data['data'][0]['latitude'], data['data'][0]['longitude']
        return None, None

    patient_lat, patient_long = get_lat_long(patientCity)

    distances = []
    for location in df['City']:
        location_lat, location_long = get_lat_long(location)
        if location_lat and location_long:
            distance = geodesic((patient_lat, patient_long), (location_lat, location_long)).km
            distances.append(distance)
        else:
            distances.append(None)

    df['Distance_from_Patient'] = distances

    #sorting the dataFrame based on distance
    df_sorted = df.sort_values(by='Distance_from_Patient').reset_index(drop=True)

    return df_sorted