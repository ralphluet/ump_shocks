############################################################################################################
# Generate Romer and Romer (2004) shocks for the period 1969 up to latest Tealbook forecast available.
############################################################################################################

# Required packages
import pandas as pd
import requests
import statsmodels.formula.api as smf

# Download the Forecast Data
url = 'https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/greenbook-data/documentation/gbweb_row_format.xlsx?la=en&hash=ADEEBF4E1E339624C8C55B9EAB26B23F'
response = requests.get(url, allow_redirects=True)

open('data/GBweb_Row_Format.xlsx', 'wb').write(response.content)

# Toggles
includeOct1979 = False # If False then it drops the October 6, 1979 meeting which took place before the forecast was released (as in Romer and Romer (2004))
PGDP_PostMay1996 = False # If True then PGDP forecasts are subsituted by gNGDP - gRGDP (as in Wieland and Yang (2020))

# Extract meeting dates from the FOMC_meeting_dates.xlsx file.
# NOTES: Whenever one wants to update the shock series, this file 
# has to be updated manually for each new Forecast available.
meeting_dates = pd.read_excel('data/FOMC_meeting_dates.xlsx')
meeting_dates['MTGDATE'] = pd.to_datetime(meeting_dates[['Year', 'Month', 'Day']])

# Load the Greenbook Data
RGDP_data = pd.read_excel('data/GBweb_Row_Format.xlsx', sheet_name='gRGDP')
NGDP_data = pd.read_excel('data/GBweb_Row_Format.xlsx', sheet_name='gNGDP')
PGDP_data = pd.read_excel('data/GBweb_Row_Format.xlsx', sheet_name='gPGDP')
UNEMP_data = pd.read_excel('data/GBweb_Row_Format.xlsx', sheet_name='UNEMP')

############################################################################################################
# Corrections done by Wieland and Yang (2020) (WY hereafter)
############################################################################################################

# Incorrect relase date in Philadelphia data (double checked in original Greenbook)
RGDP_data.loc[(RGDP_data['GBdate'] == 19910628), 'GBdate'] = 19910626
NGDP_data.loc[(NGDP_data['GBdate'] == 19910628), 'GBdate'] = 19910626
PGDP_data.loc[(PGDP_data['GBdate'] == 19910628), 'GBdate'] = 19910626
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19910628), 'GBdate'] = 19910626

RGDP_data.loc[(RGDP_data['GBdate'] == 19940630), 'GBdate'] = 19940629
NGDP_data.loc[(NGDP_data['GBdate'] == 19940630), 'GBdate'] = 19940629
PGDP_data.loc[(PGDP_data['GBdate'] == 19940630), 'GBdate'] = 19940629
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19940630), 'GBdate'] = 19940629

# For the 1/29/1969 forecast the Greenbooks mention a supplement with additional
# forecasts to be forthcoming, but WY cannot find a record of it. WY augment the 
# data here with data from the Romer Greenbook file.
RGDP_data.loc[(RGDP_data['GBdate'] == 19690129), 'gRGDPF2'] = 1.4
PGDP_data.loc[(PGDP_data['GBdate'] == 19690129), 'gPGDPF2'] = 4.2

# Manual correction of incorrect entries in Philadelphia database. 
# WY checked in the original Greenbooks that the Philadelphia data are incorrect. 
RGDP_data.loc[(RGDP_data['GBdate'] == 19691210), 'gRGDPF2'] = 0.1
RGDP_data.loc[(RGDP_data['GBdate'] == 19870701), 'gRGDPB1'] = 2.2
RGDP_data.loc[(RGDP_data['GBdate'] == 19950322), 'gRGDPB1'] = 4.6

PGDP_data.loc[(PGDP_data['GBdate'] == 19720913), 'gPGDPF2'] = 3.9
PGDP_data.loc[(PGDP_data['GBdate'] == 19720913), 'gPGDPF3'] = 3.4
PGDP_data.loc[(PGDP_data['GBdate'] == 19721011), 'gPGDPF1'] = 3.7
PGDP_data.loc[(PGDP_data['GBdate'] == 19721011), 'gPGDPF2'] = 3.5
PGDP_data.loc[(PGDP_data['GBdate'] == 19721115), 'gPGDPF1'] = 4.1
PGDP_data.loc[(PGDP_data['GBdate'] == 19721115), 'gPGDPF2'] = 3.5
PGDP_data.loc[(PGDP_data['GBdate'] == 19760512), 'gPGDPB1'] = 3.7

NGDP_data.loc[(NGDP_data['GBdate'] == 19820623), 'gNGDPF2'] = 8.6
NGDP_data.loc[(NGDP_data['GBdate'] == 19871209), 'gNGDPF0'] = 5.4
NGDP_data.loc[(NGDP_data['GBdate'] == 19871209), 'gNGDPF1'] = 5.1
NGDP_data.loc[(NGDP_data['GBdate'] == 19871209), 'gNGDPF2'] = 5.0
NGDP_data.loc[(NGDP_data['GBdate'] == 19871209), 'gNGDPF3'] = 6.3
NGDP_data.loc[(NGDP_data['GBdate'] == 19871209), 'gNGDPF4'] = 7.0
NGDP_data.loc[(NGDP_data['GBdate'] == 19910626), 'gNGDPF2'] = 7.6

# There is a revised forecast available for 4/6/1970 that is not in the Phildadelphia database.
RGDP_data.loc[(RGDP_data['GBdate'] == 19700401), 'GBdate'] = 19700406
NGDP_data.loc[(NGDP_data['GBdate'] == 19700401), 'GBdate'] = 19700406
PGDP_data.loc[(PGDP_data['GBdate'] == 19700401), 'GBdate'] = 19700406
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19700401), 'GBdate'] = 19700406

NGDP_data.loc[(NGDP_data['GBdate'] == 19700406), 'gNGDPF0'] = 6.7
PGDP_data.loc[(PGDP_data['GBdate'] == 19700406), 'gPGDPF0'] = 5.9

RGDP_data.loc[(RGDP_data['GBdate'] == 19700406), 'gRGDPF1'] = 3.1
NGDP_data.loc[(NGDP_data['GBdate'] == 19700406), 'gNGDPF1'] = 5.0
PGDP_data.loc[(PGDP_data['GBdate'] == 19700406), 'gPGDPF1'] = 2.9
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19700406), 'UNEMPF1'] = 4.6

RGDP_data.loc[(RGDP_data['GBdate'] == 19700406), 'gRGDPF2'] = 3.3
NGDP_data.loc[(NGDP_data['GBdate'] == 19700406), 'gNGDPF2'] = 6.9
PGDP_data.loc[(PGDP_data['GBdate'] == 19700406), 'gPGDPF2'] = 3.6
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19700406), 'UNEMPF2'] = 4.8

# There is a revised forecast available for 2/9/1971 that is not in the Phildadelphia database, but none of the variables we use have changed. */
RGDP_data.loc[(RGDP_data['GBdate'] == 19710203), 'GBdate'] = 19710209
NGDP_data.loc[(NGDP_data['GBdate'] == 19710203), 'GBdate'] = 19710209
PGDP_data.loc[(PGDP_data['GBdate'] == 19710203), 'GBdate'] = 19710209
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19710203), 'GBdate'] = 19710209

# The Philadelphia data quotes a release on 4/15/1977, but the Greenbooks date from 4/13/1977. 
# WY could not find a written record of a forecast for 4/15/1977, so WY use the original 4/13 values.
RGDP_data.loc[(RGDP_data['GBdate'] == 19770415), 'GBdate'] = 19770413
NGDP_data.loc[(NGDP_data['GBdate'] == 19770415), 'GBdate'] = 19770413
PGDP_data.loc[(PGDP_data['GBdate'] == 19770415), 'GBdate'] = 19770413
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19770415), 'GBdate'] = 19770413

RGDP_data.loc[(RGDP_data['GBdate'] == 19770413), 'gRGDPF0'] = 7.2
NGDP_data.loc[(NGDP_data['GBdate'] == 19770413), 'gNGDPF0'] = 13.7 
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19770413), 'UNEMPF0'] = 7.1

RGDP_data.loc[(RGDP_data['GBdate'] == 19770413), 'gRGDPF1'] = 6.4
NGDP_data.loc[(NGDP_data['GBdate'] == 19770413), 'gNGDPF1'] = 12.4
PGDP_data.loc[(PGDP_data['GBdate'] == 19770413), 'gPGDPF1'] = 5.7
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19770413), 'UNEMPF1'] = 7.0

RGDP_data.loc[(RGDP_data['GBdate'] == 19770413), 'gRGDPF2'] = 5.9
NGDP_data.loc[(NGDP_data['GBdate'] == 19770413), 'gNGDPF2'] = 12.8
PGDP_data.loc[(PGDP_data['GBdate'] == 19770413), 'gPGDPF2'] = 6.6
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19770413), 'UNEMPF2'] = 6.9

RGDP_data.loc[(RGDP_data['GBdate'] == 19770413), 'gRGDPF3'] = 5.7
NGDP_data.loc[(NGDP_data['GBdate'] == 19770413), 'gNGDPF3'] = 11.7
PGDP_data.loc[(PGDP_data['GBdate'] == 19770413), 'gPGDPF3'] = 5.7
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19770413), 'UNEMPF3'] = 6.7

RGDP_data.loc[(RGDP_data['GBdate'] == 19770413), 'gRGDPF4'] = 5.6
NGDP_data.loc[(NGDP_data['GBdate'] == 19770413), 'gNGDPF4'] = 11.3
PGDP_data.loc[(PGDP_data['GBdate'] == 19770413), 'gPGDPF4'] = 5.4
UNEMP_data.loc[(UNEMP_data['GBdate'] == 19770413), 'UNEMPF4'] = 6.6

if PGDP_PostMay1996 == True:
    PGDP_data.loc[(PGDP_data['GBdate'] >= 19960516), 'gPGDPB1'] = NGDP_data.loc[(NGDP_data['GBdate'] >= 19960516), 'gNGDPB1'] - RGDP_data.loc[(RGDP_data['GBdate'] >= 19960516), 'gRGDPB1']
    PGDP_data.loc[(PGDP_data['GBdate'] >= 19960516), 'gPGDPF0'] = NGDP_data.loc[(NGDP_data['GBdate'] >= 19960516), 'gNGDPF0'] - RGDP_data.loc[(RGDP_data['GBdate'] >= 19960516), 'gRGDPF0']
    PGDP_data.loc[(PGDP_data['GBdate'] >= 19960516), 'gPGDPF1'] = NGDP_data.loc[(NGDP_data['GBdate'] >= 19960516), 'gNGDPF1'] - RGDP_data.loc[(RGDP_data['GBdate'] >= 19960516), 'gRGDPF1']
    PGDP_data.loc[(PGDP_data['GBdate'] >= 19960516), 'gPGDPF2'] = NGDP_data.loc[(NGDP_data['GBdate'] >= 19960516), 'gNGDPF2'] - RGDP_data.loc[(RGDP_data['GBdate'] >= 19960516), 'gRGDPF2']
    PGDP_data.loc[(PGDP_data['GBdate'] >= 19960516), 'gPGDPF3'] = NGDP_data.loc[(NGDP_data['GBdate'] >= 19960516), 'gNGDPF3'] - RGDP_data.loc[(RGDP_data['GBdate'] >= 19960516), 'gRGDPF3']


############################################################################################################
# Construct dataset like in the Romer and Romer (2004)
############################################################################################################

# Variable GBdate transformed to datetime
RGDP_data['GBdate'] = pd.to_datetime(RGDP_data['GBdate'], format='%Y%m%d')
PGDP_data['GBdate'] = pd.to_datetime(PGDP_data['GBdate'], format='%Y%m%d')
UNEMP_data['GBdate'] = pd.to_datetime(UNEMP_data['GBdate'], format='%Y%m%d')

# Obtain only relevant columns
RGDP = RGDP_data[['GBdate', 'gRGDPB1','gRGDPF0','gRGDPF1','gRGDPF2','gRGDPF3']]
PGDP = PGDP_data[['GBdate', 'gPGDPB1','gPGDPF0','gPGDPF1','gPGDPF2','gPGDPF3']]
UNEMP = UNEMP_data[['GBdate', 'UNEMPF0']]

# Merge the Greenbook data into a single DataFrame 
GB_data = pd.merge(RGDP, PGDP, how='outer', on='GBdate')
GB_data = pd.merge(GB_data, UNEMP, how='outer', on='GBdate')

# Match Greenbook forecast release date with FOMC meeting date
meeting_dates = meeting_dates.sort_values('MTGDATE')
GB_data = GB_data.sort_values('GBdate')
GB_data = pd.merge_asof(meeting_dates['MTGDATE'], GB_data, left_on='MTGDATE', right_on='GBdate', direction='nearest')

# Generate an auxiliary variables for the quarter to correctly calculate the forecast innovation
GB_data['Quarter'] = GB_data['GBdate'].dt.quarter
GB_data_prev = GB_data.shift(1)

# Create a boolean mask for the condition
mask = GB_data['Quarter'] == GB_data_prev['Quarter']

# Columns for RGDP Forecast Change
GB_data.loc[mask, 'gRGDPB1_change'] = GB_data.loc[mask, 'gRGDPB1'] - GB_data_prev.loc[mask, 'gRGDPB1']
GB_data.loc[~mask, 'gRGDPB1_change'] = GB_data.loc[~mask, 'gRGDPB1'] - GB_data_prev.loc[~mask, 'gRGDPF0']

GB_data.loc[mask, 'gRGDPF0_change'] = GB_data.loc[mask, 'gRGDPF0'] - GB_data_prev.loc[mask, 'gRGDPF0']
GB_data.loc[~mask, 'gRGDPF0_change'] = GB_data.loc[~mask, 'gRGDPF0'] - GB_data_prev.loc[~mask, 'gRGDPF1']

GB_data.loc[mask, 'gRGDPF1_change'] = GB_data.loc[mask, 'gRGDPF1'] - GB_data_prev.loc[mask, 'gRGDPF1']
GB_data.loc[~mask, 'gRGDPF1_change'] = GB_data.loc[~mask, 'gRGDPF1'] - GB_data_prev.loc[~mask, 'gRGDPF2']

GB_data.loc[mask, 'gRGDPF2_change'] = GB_data.loc[mask, 'gRGDPF2'] - GB_data_prev.loc[mask, 'gRGDPF2']
GB_data.loc[~mask, 'gRGDPF2_change'] = GB_data.loc[~mask, 'gRGDPF2'] - GB_data_prev.loc[~mask, 'gRGDPF3']

# Columns for CPI Forecast Change.
GB_data.loc[mask, 'gPGDPB1_change'] = GB_data.loc[mask, 'gPGDPB1'] - GB_data_prev.loc[mask, 'gPGDPB1']
GB_data.loc[~mask, 'gPGDPB1_change'] = GB_data.loc[~mask, 'gPGDPB1'] - GB_data_prev.loc[~mask, 'gPGDPF0']

GB_data.loc[mask, 'gPGDPF0_change'] = GB_data.loc[mask, 'gPGDPF0'] - GB_data_prev.loc[mask, 'gPGDPF0']
GB_data.loc[~mask, 'gPGDPF0_change'] = GB_data.loc[~mask, 'gPGDPF0'] - GB_data_prev.loc[~mask, 'gPGDPF1']

GB_data.loc[mask, 'gPGDPF1_change'] = GB_data.loc[mask, 'gPGDPF1'] - GB_data_prev.loc[mask, 'gPGDPF1']
GB_data.loc[~mask, 'gPGDPF1_change'] = GB_data.loc[~mask, 'gPGDPF1'] - GB_data_prev.loc[~mask, 'gPGDPF2']

GB_data.loc[mask, 'gPGDPF2_change'] = GB_data.loc[mask, 'gPGDPF2'] - GB_data_prev.loc[mask, 'gPGDPF2']
GB_data.loc[~mask, 'gPGDPF2_change'] = GB_data.loc[~mask, 'gPGDPF2'] - GB_data_prev.loc[~mask, 'gPGDPF3']

# Drop columns not relevant anymore
GB_data.drop('Quarter', axis=1, inplace=True)
GB_data.drop('gRGDPF3', axis=1, inplace=True)
GB_data.drop('gPGDPF3', axis=1, inplace=True)

# Load Federal Funds Rate Data
# NOTES: Whenever one wants to update the shock series, this file 
# has to be updated manually for each new Forecast available.
FFR_data = pd.read_excel('data/target_ffr.xlsx')
FFR_data['MTGDATE'] = pd.to_datetime(FFR_data['MTGDATE'])

# Merge with Greenbook data to generate Romer and Romer (2004) data file
RR_data = pd.merge(FFR_data, GB_data, on='MTGDATE')

# Reorder the columns
columns_ordered = ['MTGDATE', 'GBdate'] + [col for col in RR_data.columns if col != 'MTGDATE' and col != 'GBdate']
RR_data = RR_data[columns_ordered]

if includeOct1979 == False:
    RR_data = RR_data[RR_data['MTGDATE'] != '1979-10-06']

# Download the Wu-Xia Shadow Rate Data
url = 'https://www.atlantafed.org/-/media/documents/datafiles/cqer/research/wu-xia-shadow-federal-funds-rate/WuXiaShadowRate.xlsx'
response = requests.get(url, allow_redirects=True)

open('data/WuXiaShadowRate.xlsx', 'wb').write(response.content)

# Load Shadow Rate
shadow_rate_data = pd.read_excel('data/WuXiaShadowRate.xlsx', usecols=[0, 2])
shadow_rate_data = shadow_rate_data.rename(columns={'Unnamed: 0': 'Date', 'Wu-Xia shadow federal funds rate (last business day of month)': 'WX_rate'})

# Greenbook Data for ZLB period
start_date = '2008-11-01' # Need to start one month before the first ZLB meeting to calculate shadow rate change for January 2009
end_date = '2015-12-31'

# Extract the data for the period of interest
GB_ZLB = GB_data[(GB_data['MTGDATE'] >= start_date) & (GB_data['MTGDATE'] <= end_date)]
shadow_rate = shadow_rate_data[(shadow_rate_data['Date'] >= start_date) & (shadow_rate_data['Date'] <= end_date)]

# Convert the dates to datetime format if they aren't already
shadow_rate['Date'] = pd.to_datetime(shadow_rate['Date'])
GB_ZLB['MTGDATE'] = pd.to_datetime(GB_ZLB['MTGDATE'])

# Extract year and month
shadow_rate['YearMonth'] = shadow_rate['Date'].dt.to_period('M')
GB_ZLB['YearMonth'] = GB_ZLB['MTGDATE'].dt.to_period('M')

# Match Shadow Rate with FOMC meeting dates
matching_dates = shadow_rate[shadow_rate['YearMonth'].isin(GB_ZLB['YearMonth'])]
GB_ZLB = GB_ZLB.merge(matching_dates[['WX_rate', 'YearMonth']], on='YearMonth', how='inner')

# Drop columns not relevant anymore
GB_ZLB = GB_ZLB.drop(columns=['YearMonth'])

# Dates for the shadow rate before the FOMC meeting
GB_ZLB['prev_dates'] = GB_ZLB['MTGDATE'] - pd.DateOffset(months=1)
GB_ZLB['prev_dates'] = pd.to_datetime(GB_ZLB['prev_dates'])

# Extract year and month for shadow rate before the FOMC meeting
shadow_rate['YearMonth'] = shadow_rate['Date'].dt.to_period('M')
GB_ZLB['YearMonth'] = GB_ZLB['prev_dates'].dt.to_period('M')

# Match previous shadow rate with FOMC meeting dates
matching_dates_prev = shadow_rate[shadow_rate['YearMonth'].isin(GB_ZLB['YearMonth'])]
matching_dates_prev = matching_dates_prev.rename(columns={'WX_rate': 'Old_rate'})

# Merge all the data into a single DataFrame
GB_ZLB = GB_ZLB.merge(matching_dates_prev[['Old_rate', 'YearMonth']], on='YearMonth', how='inner')

# Generate a shadow rate change variable
GB_ZLB['Rate_change'] = GB_ZLB['WX_rate'] - GB_ZLB['Old_rate']

# Generate Romer and Romer dataset for ZLB period
RR_ZLB = GB_ZLB.drop(columns=['WX_rate', 'prev_dates', 'YearMonth'])
RR_ZLB = RR_ZLB[(RR_ZLB['MTGDATE'] >= '2009-01-01')]

# Substitute shadow rate into the Romer and Romer dataset
columns_ordered = ['MTGDATE','GBdate','Rate_change','Old_rate'] + [col for col in RR_ZLB.columns if col != 'MTGDATE' and col != 'GBdate' and col != 'Rate_change' and col != 'Old_rate']
RR_ZLB = RR_ZLB[columns_ordered]
RR_data[(RR_data['MTGDATE'] >= '2009-01-01') & (RR_data['MTGDATE'] <= '2016-01-01')] = RR_ZLB.values

# Save the data
RR_data.to_csv('output/RR_data.csv', index=True)


############################################################################################################
# Generate monthly shocks
############################################################################################################
# Set MTGDATE as index
RR_data = RR_data.set_index('MTGDATE')

# Create a formula string that specifies the regression model
formula = 'Rate_change ~ ' + ' + '.join([col for col in RR_data.columns if col != 'Rate_change' and col != 'GBdate'])

# Fit the regression model using the formula and the RR_Data DataFrame
model = smf.ols(formula=formula, data=RR_data).fit()

# Get the residuals from the regression
shocks = model.resid

# Resample the Series by month and fill missing values with 0
shocks = shocks.resample('M').sum().fillna(0)

# .sum() is just used in case that there is a month that for some reason they met more than once. This is extremly
# unlikely, but if somehow it was the case, then we just sum up the shocks in that month.

# Original RR series starts in January 1969 but there is only a shock starting in March 1969
shocks.loc[pd.Timestamp('1969-02-01')] = 0
shocks.loc[pd.Timestamp('1969-01-01')] = 0

shocks = shocks.sort_index()
shocks.index = shocks.index.to_period('M').to_timestamp()

# Save the 1969-2008 shocks
shocks = shocks.to_frame('RESID')
shocks.to_csv('output/monthly/RR_shocks.csv')

############################################################################################################
# Transform into quarterly shocks
############################################################################################################

shocks_Q = shocks.resample('Q').sum().fillna(0)
shocks_Q.index = shocks_Q.index.to_period('Q').to_timestamp()

shocks_Q.to_csv('output/quarterly/RR_shocks.csv')