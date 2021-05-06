# Data Dictionary
This file explains both the data that was obtained and used to build our models, and the data produced from our models.

### Data Sources
- **[Distances.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/Distances.csv) list of distances between the census blocks and the POD sites (Size: 1100 x 47)**\
The data for this file was generated using [shapefiles](https://www.census.gov/cgi-bin/geo/shapefiles/index.php) for Allegheny County census block groups provided to the public via the U.S. Census Bureau. These shapefiles were uploaded to ArcGIS Pro and then the "Feature to Point" tool to calculate the centroid for each census block. We then also uploaded a list of 47 POD sites provided by our CMU professor and used the "Geocode Addresses" tool in ArcGIS Pro to generate a point for each POD. The "OD Cost Matrix" tool in ArcgIS online was then used to calculate the straight-line distance between each pair of census block group centroid and POD site, generating the resulting matrix.
- **[Labor.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/Labor.csv) list of cost of labor at each POD site per hour of operation (Size: 47 x 1)**\
These estimates were based on the expected operational size/scale of each POD (i.e., the number of loading sites at each POD), and friends and family members who work in the healthcare sector provided insight to help us determine how many staff with each experience level would be required to operate PODs of various sizes.
- **[LoadingSites.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/LoadingSites.csv) list of available loading spots at each POD site (Size: 47 x 1)**\
A loading spot is a designated place within a parking lot where a recipient can momentarily park their car to receive the necessary supplies and/or receive medical attention and administration of vaccines. It is assumed that at any given point in time, each of these loading sites will be occupied. Consulting literature about POD layout, traffic flow, and space requirements, combined with our use of Google Maps to visually inspect and make measurements of parking lots surrounding POD sites enabled us to make these estimates.
- **[Populations.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/Populations.csv) list of population in each census block (Size: 1100 x 1)**\
The data for this file was generated using [Table B01003 ("Total Population")](https://data.census.gov/cedsci/table?text=B01003&g=0500000US42003.150000&tid=ACSDT5Y2019.B01003) from the U.S. Census Bureau. In order to generate an appropriate order for the individual rows in this file, the csv was uploaded to ArcGIS and joined to the census block shapefile. Then, an excel document was exported with the population estimates in the same order as all of our other files.
- **[Supplies.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/Supplies.csv) list of cost of supplies that are given to the population (Size: 9 x 1)**\
Ultimately, our team omitted this variable from our model because it was determined that our assumption that all residents would be receiving supplies in all scenarios leads to this parameters having no impact on the model optimality in its current state.
- **[pgh_blocks.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/pgh_blocks.csv) list of population in each block specifically within Pittsburgh (Size: 361 x 1)**\ This file was generated using ArcGIS and the original Populations.csv file. In ArcGIS, we restricted the Populations file to include only census blocks located within the boundary of the City of Pittsburgh.
- **[pgh_pods.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/pgh_pods.csv) list of POD capacities within Pittsburgh (Size: 11 x 1)**\
This file includes all PODs located inside of the City of Pittsburgh boundary and any PODs that are outside the boundary but within 1 mile of it. This file does not necessarily need to be used in Model 2 (the original POD file should suffice), but limiting the number of POD options may boost copmutational performance.
- **[popDens.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/popDens.csv) dataframe of population and population density of each census block (Size: 1100 x 3)**\
This file was ultimately omitted from our model as we decided not to weight distances by population density (which would follow a density-dependent model of virulence where individuals living in greater population-dense areas are prioritized with closer PODs, on average). These values were calculated by dividing the estimated population size by the land area of the census block group and multiplied by 100. Thus, the units are in "people per 100 square meters."

### Model-Generated Data [(Output Files)](https://github.com/sormehyazdi/dabpGroupProject2021/tree/main/Final_DABP/OutputFiles)
blockDistances =\
optimalVals =\
podDays =\
- [s1_m1_blockDistances.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s1_m1_blockDistances.csv) lists budget, cost, block, distances traveled (miles), and designated POD for each budget simulation (9899 x 5)
- [s1_m1_optimalVals.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s1_m1_optimalVals.csv) lists budget, cost, and optimal total distance traveled (miles) (9 x 3)
- [s1_m1_podDays.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s1_m1_podDays.csv) lists budget, cost, POD #, number of days the POD remains open (422 x 4)
- [s1_m2_blockDistances.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s1_m2_blockDistances.csv)
- [s1_m2_optimalVals.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s1_m2_optimalVals.csv)
- [s1_m2_podDays.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s1_m2_podDays.csv)
- [s2_m1_blockDistances.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s2_m1_blockDistances.csv)
- [s2_m1_optimalVals.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s2_m1_optimalVals.csv)
- [s2_m1_podDays.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s2_m1_podDays.csv)
- [s2_m2_blockDistances.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s2_m2_blockDistances.csv)
- [s2_m2_optimalVals.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s2_m2_optimalVals.csv)
- [s2_m2_podDays.csv](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/OutputFiles/s2_m2_podDays.csv)
