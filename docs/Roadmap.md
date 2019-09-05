Kafka Bus
Connectors

FeatureEngineering Operators
	StreamBased support

- TrainOperators
- PredictOperators
- DeployOperators

- Scalars,
- Transformers
- FeatureEnrichers 
	- Datetime
	- NLP

- DataAnnotators
- Snorkel
- TimeseriesAnnotator


### To be included in DeployOperators !???
1.scalars can  be included
2.Transformers can also be included

## Construct a Pipeline and Deploy 
### Deploy a SklearnPipeline using DeployOperators

- PredictOperators can be used in reqular ETL jobs
- SubDagOperator which trains multiple models in parallel in Dask background
- CombineOperator which uses combines result of multiple models (Stacking and produces the prediction)
	- Which takes Mlflow UUID and runs the specific model

## DeployOperators
	- SparkDeployer
	- DockerDeployer (clipper.ai)
	- TensorflowServingOperator for TensorflowModels
	
## AutoMLOperator
	Using nnictl
	
## Operator API
		EachOperator should take the neccessary configs from the airflow variables
			Handle Naming Conventions for eachoperator
		Each Operator should be able to speak with kafka ,read write its own data
			Handle Topic name efficently
		EachTrain Operator should also able to speak with mlflow backend
		EachFeatureEngOperator should produce UDF in mlflow
			TimeSeriesFeatures
			NLPFeatures
			Log,Power,etc
			
		
		AutoMLOperator should speak with mlflow and nnictl Dashboard
			Log Each model of automl-metric into mlflow and nnictl
			Show leaderboard in nnictl 
			this Operator should Training spec for the alogorithm and trains a model
		LudwigOperator :
				should take YML files and Trains a model
					The featureENricher,Scalar,combiner present in ludwig can be used (with same operator) 
					Deploy/serve using FastAPI for production Grade API deployment
		SubDagOperator or HyperParmaterTunner:
			Try Different Parameters and log the metrics (should be compatable with AutoMLOperator)
		ModelCombineTrainOperator:
			Use Stacking (use master model to control)
			(Applicable Stacking use cases)
		ModelCombinePredictOperator :
			Combine multiple models output and predict 
				VotingClassifier
				AvgRegressor
		DeployOperators:
			Deploy a Workflow in respective Environments (spark,Docker)
				using sklearn Pipeline
			Use Xcomm feature to share the Entire Workflow into DeployOperators
				Deploy a model using this Xcomm Workflow 
					Handle push and pull of xcomm with right Naming conventions
		ExplainOperators 
			USe mlflow UUId load the data and explain a features
			Store the explainers in the backend
		
			

	
### Frameworks To be used under Train and Predict Operators are :
	- Sklearn
	- Catboost
	- H20
	- xgboost
	- Lightgbm
		
### Frameworks To be used under FeatureEngineering Operators :
	- Sklearn
	- Creme
### Frameworks To be used under AutoMLOperators are :
	- nnictl
	- ALLSklearn
	#### To be considered using this	
		- H20 AutoML
		- Tpot
		- MLJar
		- Automl
			
### Frameworks To be used under DeployOperators:
	- SparkDeployer both batch and RestAPI
	- DockerDeployer
	

### ValidationCheck
	- Check the inputs at every operator
	

	
	
