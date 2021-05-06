## Data Dictionary
This file explains both the data that was obtained and used to build our models, and the data produced from our models.

**Data Sources**
- [Distances.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/Distances.csv) list of distances between the census blocks and the POD sites (1100 x 47)
  The data for this file was generated using [shapefiles](https://www.census.gov/cgi-bin/geo/shapefiles/index.php) for Allegheny County census block groups provided to the public via the U.S. Census Bureau. These shapefiles were uploaded to ArcGIS Pro and then the "Feature to Point" tool to calculate the centroid for each census block. We then also uploaded a list of 47 POD sites provided by our CMU professor and used the "Geocode Addresses" tool in ArcGIS Pro to generate a point for each POD. The "OD Cost Matrix" tool in ArcgIS online was then used to calculate the straight-line distance between each pair of census block group centroid and POD site, generating the resulting matrix.
- [Labor.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/Labor.csv) list of cost of labor at each POD site (47 x 1)
- [LoadingSites.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/LoadingSites.csv) list of available loading spots at each POD site (47 x 1)
- [Populations.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/Populations.csv) list of population in each census block (1100 x 1)
- [Supplies.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/Supplies.csv) list of cost of supplies that are given to the population (9 x 1)
- [pgh_blocks.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/pgh_blocks.csv) list of population in each block specifically within Pittsburgh (361 x 1)
- [pgh_pods.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/pgh_pods.csv) list of POD capacities within Pittsburgh (11 x 1)
- [popDens.csv:](https://github.com/sormehyazdi/dabpGroupProject2021/blob/main/Final_DABP/popDens.csv) dataframe of population and population density of each census block (1100 x 3)

**Model-Generated Data [(Output Files)](https://github.com/sormehyazdi/dabpGroupProject2021/tree/main/Final_DABP/OutputFiles)**
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
