Composite GVO datafiles:

OR_OPER_VOBS_4M.cdf


Variables:
Timestamp    - time in milliseconds since 01-Jan-0000 00:00:00.000 of B_OB and B_CF 
Latitude     - latitude in degrees of GVO
Longitude    - longitude in degrees of GVO
Radius       - radius in metres of GVO
B_OB         - observed field in nT
sigma_OB     - error estimate of observed field in nT
B_CF         - core field in nT
sigma_CF     - error estimate of core field in nT
Timestamp_SV - time in milliseconds since 01-Jan-0000 00:00:00.000 of B_SV
B_SV         - SV field in nT/yr
sigma_SV     - error estimate of SV field in nT/yr

%==========================================================================
The GVO processing using the Oersted, CHAMP, CryoSat-2 and Swarm data are in accordance with the document SW-DS-DTU-GS-005_2-1_GVO_DPA
- GVO model setup:
    -300 globally distributed GVOs using an equal area grid (Leopardi 2006)
    -GVO data search range is 700km around each VO location
    -GVO data are collected for 1 or 4 months ad a time 
    -Data along-track differences and sums are used
    -GVO fit using cubic potential description
    -Inversion limit = 30 data points

For Oersted GVOs the error estimates for the core field and SV have been computed in a modified way due to the large number of gaps 

sigma_CF error estimates of the GVO CORE field are computed based on the residuals with respect to internal CHAOS-7-2 field predictions (deg 1-20). The residuals are computed for two latitude bands: a) 50N-90N degrees together with 50S-90S degrees and b) 50S-50N deg.
Using all residual within each band, the error estimates are computed as the square root of the residual robust mean squared plus the residual robust standard deviation squared.

sigma_SV error estimates of the GVO SV field are computed based on the residuals with respect to internal CHAOS-7-2 field SV predictions (deg 1-20).  The residuals are computed for two latitude bands: a) 50N-90N degrees together with 50S-90S degrees and b) 50S-50N deg. Using all residual within each band, the error estimates are computed as the square root of the residual robust mean squared plus the residual robust standard deviation squared.

%==========================================================================
The GVO composite cdf files have a format in accordance with GVO Swarm cdf files described in the document SW-DS-DTU-GS-004_2-1_GVO_PDD.

1) 4-month GVOs
    Data used
    - Oersted data (available from ftp://ftp.spacecenter.dk/data/magnetic-satellites/Oersted/), 5 sec data sampling rate
    - Data selection criteria applied:
    	- The sun is at least 10deg below horizon
    	- Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT)
    	- Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    	- Estimates of CIY4 ionopsheric and induced fields removed
	
    B_OB: observed field time series
    - covers period: 1999-2004

    B_CF: core field time series
    - SHA denoising applied: external and toroidal terms estimated to SH degree 13. At times of insufficient data for SHA inversion, a linear interpolation was used. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series
%==========================================================================

