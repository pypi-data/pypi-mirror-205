Ground observatory cdf files:

GObs_1M_19970115T000000_20201215T000000_0101.cdf
GObs_4M_19970301T000000_20201101T000000_0101.cdf


Variables:
Timestamp    - time in milliseconds since 01-Jan-0000 00:00:00.000 of B_OB and B_CF 
Latitude     - latitude in degrees of GO
Longitude    - longitude in degrees of GO
Radius       - radius in metres of GO
B_OB         - estimated observed field in nT
sigma_OB     - error estimate of observed field in nT
B_CF         - estimated core field in nT
sigma_CF     - error estimate of core field in nT
Timestamp_SV - time in milliseconds since 01-Jan-0000 00:00:00.000 of B_SV
B_SV         - SV field in nT/yr
sigma_SV     - error estimate of SV field in nT/yr
bias_crust   - Estimated observatory bias [nT]
Obs          - IAGA Ground observatory code

%==========================================================================
The GObs time series are derived from version 0122 of the ground observatory hourly means between 1997 and 2020 from the database
AUX_OBS prepared by the British Geological Survey (BGS): ftp://ftp.nerc-murchison.ac.uk/geomag/Swarm/AUX_OBS/hour/ 


Any papers published using these data are requested to include the following acknowledgement

"The staff of the geomagnetic observatories and INTERMAGNET are thanked for supplying high-quality observatory data."
and to consider referencing the following article

Macmillan S, Olsen N (2013) Observatory data and the Swarm mission. Earth
Planets Space 65:1355–1362. https ://doi.org/10.5047/eps.2013.07.011

%==========================================================================
The GO composite cdf files have a format in accordance with GVO Swarm cdf files described in the document SW-DS-DTU-GS-004_2-1_GVO_PDD.
In addition to this they contain extra variables bias_crust (containing the estimated observatory bias) and Obs containing the IAGA observatory code.

1) 1-month GObs
    B_OB: observed field time series
    - Robust 1 monthly means from HMV, computed in 1 month bins, no corrections or data selection applied

    B_CF: core field time series
    -  Robust 1 monthly means from HMV, after subtracting CM4 SQ field predictions and CHAOS-7.2 external field predictions, with input from RC index RC_1997-2020_Aug_v4.dat. In the literature these are revered to as revised monthly means - see Olsen et al. (2014) for details. 

    B_SV: core field time series
    - Secular variation computed as annual differences of B_CF time series i.e. annual differences of revised monthly means

    sigma_OB, sigma_CF, sigma_SV: error estimates
    - Derived from variances calculated from detrended residuals from CHAOS observed/core/secular variation field

    bias_crust: 
    - observatory bias computed as the median of residuals between B_CF and CHAOS-7.2 field predictions to SH degree 14 for each component at each observatory

4) 4-month GObs
    B_OB: observed field time series
    - Robust 4 monthly means from HMV, computed in 4 month bins 

    B_CF: core field time series
    -  Robust 4 monthly means from HMV, after subtracting CM4 SQ predictions and CHAOS-7.2 external field model, with input from RC index RC_1997-2020_Aug_v4.dat. These are  4-monthly versions of the revised monthly means of Olsen et al. (2014). 

    B_SV: core field time series
    - Secular variation computed as annual differences of B_CF time series

    sigma_OB, sigma_CF, sigma_SV: error estimates
    - Derived from variances derived from detrended residuals from CHAOS observed/core/secular variation field

    bias_crust: 
    - estimated observatory bias (mostly from the crust) computed as median of residuals between B_CF and CHAOS-7.2 field predictions to SH degree 14 for each component at each observatory
%==========================================================================

