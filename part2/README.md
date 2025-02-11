## Initial Code Refactor

Given that we have only have a jupyter notebook [here](../notebooks/01DSNotebook.ipynb), we will need to first break down the notebook into training components.


```shell
datalake:
    - landing_zone:
    - raw_zone:
    - feature_store

```
`datalake/raw_zone` will store the data coming from a data engineering pipeline. Our pipeline will not change this data at this location but will merely read this data.

`datalake/landing_zone` will store data validated by our data validation component.

`feature_store`: will contain data prepared by our feature engineering component. Our training component will consume data from here


### Training pipeline components
We have created 3 components

1. [Data validation](./datavalidation/)

This contains the code to validate data on datalake. For a basic introduction to data validation see this [notebook](../notebooks/02DoingDataValidation.ipynb)

To run this component follow the following commands

```shell
cd datavalidation
conda env create --name conda.yaml
conda activate datavalidation
python run.py --train_path gs://examplemlops/raw-zone/train.csv --test_path gs://examplemlops/raw-zone/test.csv --landing_zone_path gs://examplemlops/landing-zone/
```

2. [Feature engineering](./dataengineering/)

This component does feature engineering on validated data created by the previous component. It also saves the features created back to s3 in to form of numpy arrays on a block of s3 designated as landing zone.

Run the following commands

```shell
cd featureengineering
conda env create -f conda.yaml
conda activate featureengineering
python run.py --validated_train_path gs://examplemlops/landing-zone/train.csv --feature_store_path gs://examplemlops/feature-store
```
You will need to change the s3 paths with paths relevant to your data

3. [Model Training Component](./training/)

This component does model training. It pulls data from the feature store on s3 and does model training.

Run the following commands to use this component.

```shell
python run.py --x_path gs://examplemlops/feature-store/X.npy --y_path gs://examplemlops/feature-store/y.npy --n_estimators 120 --max_depth 15 --n_jobs -1
```

You will need to change the s3 paths accordingly
