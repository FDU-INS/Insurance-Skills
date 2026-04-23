2023 Block Group ADI Files v4.0.1

These files contain a linkage between the Census block group and the ADI score.
The file contains four relevant fields:
- GISJOIN: Key linkage field to the block group shapefile served by NHGIS
- FIPS: The block group Census ID
- ADI_NATRANK: National percentile of block group ADI score 
	Numeric Ranking (1-100) or
	Suppression Codes:
		GQ (Group Quarters) - Greater than 33.3% of Housing Units are Group Quarters
		PH (Population/Housing) - Population less than 100 and/or fewer than 30 housing units
		GQ-PH (Group Quarters and Population Housing) - Both GQ and PH conditions are met (see above)
		QDI (Questionable Data Integrity) - Block Groups missing a key demographic factor for ADI construction (suppressed or missing in the ACS data)
- ADI_STATERNK: State-specific decile of block group ADI score
	Numeric Ranking (1-10) or
	Suppression Codes:
		GQ (Group Quarters) - Greater than 33.3% of Housing Units are Group Quarters
		PH (Population/Housing) - Population less than 100 and/or fewer than 30 housing units
		GQ-PH (Group Quarters and Population Housing) - Both GQ and PH conditions are met (see above)
		QDI (Questionable Data Integrity) - Block Groups missing a key demographic factor for ADI construction (suppressed or missing in the ACS data)


** DO NOT USE EXCEL TO OPEN THE FILES! **
Excel has a record limit of roughly 1.4 million and does not warn you if you exceed
the limit. Truncation of the data may occur!

Upon download of the block group ADI files, please verify the record number count
in your data against the chksum record number below:

  Abbr                 Full    Chksum 
    AL              Alabama   3,925             
    AK               Alaska     504             
    AZ              Arizona   4,773             
    AR             Arkansas   2,294             
    CA           California  25,607             
    CO             Colorado   4,058             
    CT          Connecticut   2,717             
    DE             Delaware     706             
    DC District of Columbia     571             
    FL              Florida  13,388             
    GA              Georgia   7,446             
    HI               Hawaii   1,083             
    ID                Idaho   1,284             
    IL             Illinois   9,898             
    IN              Indiana   5,290             
    IA                 Iowa   2,703             
    KS               Kansas   2,461             
    KY             Kentucky   3,581             
    LA            Louisiana   4,294             
    ME                Maine   1,184             
    MD             Maryland   4,079             
    MA        Massachusetts   5,116             
    MI             Michigan   8,386             
    MN            Minnesota   4,706             
    MS          Mississippi   2,445             
    MO             Missouri   5,031             
    MT              Montana     900             
    NE             Nebraska   1,648             
    NV               Nevada   1,963             
    NH        New Hampshire     997             
    NJ           New Jersey   6,599             
    NM           New Mexico   1,614             
    NY             New York  16,070             
    NC       North Carolina   7,111             
    ND         North Dakota     632             
    OH                 Ohio   9,472             
    OK             Oklahoma   3,374             
    OR               Oregon   2,970             
    PA         Pennsylvania  10,173             
    RI         Rhode Island     792             
    SC       South Carolina   3,408             
    SD         South Dakota     694             
    TN            Tennessee   4,562             
    TX                Texas  18,638             
    UT                 Utah   2,020             
    VT              Vermont     552             
    VA             Virginia   5,963             
    WA           Washington   5,311             
    WV        West Virginia   1,639             
    WI            Wisconsin   4,692             
    WY              Wyoming     457             
    PR          Puerto Rico   2,555             
 	US       United States 	242,336       

US Census data are obtained directly from IPUMS NHGIS, University of Minnesota, www.nhgis.org.

