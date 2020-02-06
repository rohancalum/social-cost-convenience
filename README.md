# The social cost of commuting convenience: how cities must invest in accessible, public transit-oriented futures to avoid climate catastrophe

[Working draft](https://docs.google.com/document/d/1_nJqh6TF2JJMlkGKWOM8bLRve1uU-IV5rhWL7rGA0qU/edit?usp=sharing).

## Setup 

* Ensure you have the latest environment from the [git repository](https://github.com/rohancalum/social-cost-convenience/tree/master/docs). Install with `conda env create -f docs/environment.yml`
* Ensure you have latest version of [OpenTripPlanner directory](https://drive.google.com/drive/folders/1dpiakMyGko6VMJlpvm_1ocqv_2PX69bZ?usp=sharing) locally. 
* In a new terminal, navigate to the OpenTripPlanner directory. 
* Launch OTP server: `java -Xmx2G -jar otp-1.3.0-shaded.jar --build . --inMemory`
* Activate environment `conda activate geoPython3`
* Restart Jupyter kernel if need be. 

## Methodology for paper: 

1. Basically [this](https://mapmyemissions.com/resources), but on an aggregate city-scale, where you route people to essential services AND their jobs. 
Come up with a rule for people to choose driving over transit (i.e. if transit time is 50% longer than driving to work, then default the person to driving. Perhaps assign some probability that the person is environmentally conscious and would be willing to transit even if it's 50% longer). 

2. Assign a value to each grid cell/census block for the "transit disadvantage factor" -- i.e. the sum of the trips in that block that take 50% longer than driving, weighted by the fraction of how much longer it takes, with an extra term to subtract if the residents are in low-income/high-income to get a measure of "equity". 

3. Perhaps these heatmaps could be overlaid over the existing transit network to show visually where the deficiencies lie, maybe it would be informative enough to suggest completely new route schemes.

4. Calculate the social cost/year of these people driving, and estimate the cost of adding a new route that would service these areas. Justify investment by saying the city would save on social cost... could also look into taxes used to pay for road infrastructure to meet the driving demand generated by poor transit options.

5. Discuss the ["frequency is freedom"](https://pedestrianobservations.com/2018/04/12/buses-in-brooklyn-frequency-is-freedom-but-15-minutes-isnt-frequency/) rule... There is also literature on how frequency isn't enough, it matters where that frequency is going (i.e. should be relevant to the residents of that area). 

6. Do this for a variety of cities that have notoriety for good transit, bad transit, big cities, small towns, etc.

7. Create a reusable python package for any user to calculate accessibility as a function of 'X' geospatial data.


## For routing script: 


1. `python download.py` will download the RAC All file from the [Urban Institute](https://datacatalog.urban.org/dataset/longitudinal-employer-household-dynamics-origin-destination-employment-statistics-lodes) to `/data/raw`.    
2.  `python process.py` contains functions for reading the LODES RAC file, calling the [US Census API](https://cenpy-devs.github.io/cenpy/api.html) for a given city 
   (default at the moment is Seattle, WA) and saves a merged dataframe with the centroids and RAC data for that city to 
    `/data/processed`. 
    
Ensure you have a MyOpenTripPlanner server running on `http://localhost:8080` (i.e. by running `java -Xmx2G -jar otp-[VERSION]-shaded.jar --build <YOUR OTP DIRECTORY> --inMemory` in terminal). See [tutorial](http://docs.opentripplanner.org/en/latest/Basic-Tutorial/) for more details.

3.  `python router.py` will read the processed data for a given city, perform routing and save a matrix of travel times to
    `/data/processed`.
