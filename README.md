# OREFA

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

This file will become your README and also the index of your
documentation.

## Install

``` sh
pip install OREFA
```

## How to use

# Part 1: Data ingestion

## Input Data

- Soil Data
- Agricultural parcel (with crop type)
- Deposition type

from orefa import AOI_creation

parcel_df = AOI_creation(AOI_path, soil_path, parcel_path,
deposition_path)

## Package to calculate the highest Activity (Bq/kg) for agricultural products.

Using prédefined test data from the test_data() function

aoi_parcels = \[\]

from orefa import test_data parcel_df = test_data()

from orefa import Parcel

for input_parcel in parcel_df.itertuples(): parcel =
Parcel(id=input_parcel.id, crop=input_parcel.crop, soil =
input_parcel.soil, deposition=input_parcel.deposition, geom =
input_parcel.geom) parcel.product_conc_prediction(time = 1)
aoi_parcels.append(parcel)

parcel_df\[‘product_concentration’\] = \[parcel.product_concentration
for parcel in aoi_parcels\]

print(‘The highest concetration of Cs-137 found in agricultural products
is’) print(f’{round(parcel_df.product_concentration.max(), 0)} Bq/kg’)
