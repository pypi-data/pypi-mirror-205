Swarm GVO datafiles:

SW_OPER_VOBS_1M_2_20131215T000000_20200315T000000_0102.cdf
SW_OPER_VOBS_4M.cdf

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
The GVO processing using the Swarm data are in accordance with the document SW-DS-DTU-GS-005_2-1_GVO_DPA
- GVO model setup:
    -300 globally distributed GVOs using an equal area grid (Leopardi 2006)
    -GVO data search range is 700km around each VO location
    -GVO data are collected for 1 or 4 months ad a time 
    -GVO altitudes are 490km during Swarm period
    -Data along-track differences and sums are used
    -GVO fit using cubic potential description
    -Inversion limit = 30 data points
%==========================================================================
The GVO Swarm cdf files have a format in accordance with GVO Swarm cdf files described in the document SW-DS-DTU-GS-004_2-1_GVO_PDD.

1) 1-month GVOs
    Data used:
    - Swarm Level 1b data, SW_OPER_MAGA_LR_1B, versions 0505/0506, 5 sec data sampling rate
    - No data selection criteria applied
	
    B_OB: observed field time series
    - covers period: 2014-2020

    B_CF: core field time series
    - Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    - PCA denoising applied.
    - SHA denoising applied: external and toroidal terms estimated to SH degree 13. At times of insufficient data for SHA inversion, a linear interpolation was used. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series

2) 4-month GVOs
    Data used
    - Swarm Level 1b data, SW_OPER_MAGA_LR_1B, versions 0505/0506, 5 sec data sampling rate
    - Data selection criteria applied:
    	- The sun is at least 10deg below horizon
    	- Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT)
    	- Estimates of LCS-1 crustal field for SH degree n=14-185 (static part) removed 
    	- Estimates of CIY4 ionopsheric and induced fields removed
	
    B_OB: observed field time series
    - covers period: 2014-2020

    B_CF: core field time series
    - SHA denoising applied: external and toroidal terms estimated to SH degree 13. At times of insufficient data for SHA inversion, a linear interpolation was used. 

    B_SV: core field time series
    - GVO secular variation computed as annual differences of GVO-CORE time series
%==========================================================================




