import requests
import pandas as pd
import os
import numpy as np
from process import get_city_names 
my_path = os.path.abspath(os.path.dirname(__file__))

def read_processed_data(city_name: str, year: int):
    fname = '{}_{}_rac_all.pkl'.format(city_name, str(year))
    df = pd.read_pickle('../data/processed/'+fname)
    return df

def route(df: pd.DataFrame, time = '8:00am', date = '03-5-2019',
          mode = 'TRANSIT,WALK', arriveBy = 'false') -> np.ndarray:
    
    origins = df['coord'].values
    destinations = df['coord'].values
    travelTimes = np.zeros([len(origins), len(destinations)])

    for i, origin in enumerate(origins):
        for j, destination in enumerate(destinations):
            url = 'http://localhost:8080/otp/routers/default/plan?fromPlace={}&'\
            'toPlace={}&time={}&date={}&mode={}&'\
            'maxWalkDistance=500&arriveBy={}'.format(origin, destination, time,
                                                     date, mode, arriveBy)
            response = requests.get(url)
            
            try:
                
                time = response.json()['plan']['itineraries'][0]['duration']
                print(time/60)
                travelTimes[i,j] = time/60
                
            except KeyError:
                
                travelTimes[i,j] = 0
                print(response.json()['error']['msg'])
                
    return travelTimes


def main(default: bool, year: int, time = '8:00am', date = '03-5-2019',
         mode = 'TRANSIT,WALK', arriveBy = 'false'):
    
    if default:
        # This corresponds to Seattle
        i = -3
        j = -2
    else:
        # All cities
        i = 0
        j = None 
        
    city_names = get_city_names()
    for city in city_names[i:j]:
        df = read_processed_data(city[:-4], year = year)
        print(df['coord'])
        m = route(df = df, time = time, date = date,
              mode = mode, arriveBy = arriveBy)
        np.savetxt('../data/processed/'+"{}_{}_traveltime_matrix.csv".format(city[:-4], year), m, 
                   delimiter=",")

if __name__ == '__main__':
    main(default = False, year = 2017)