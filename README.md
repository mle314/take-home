### The Directory Structure
- app: contains python code for a FastAPI model deployment
- data: contains raw and processed data
- Docs: reference and supporting project material
- models: trained models
- notebooks: Jupyter nobtebooks
- take_home: A python module for etl, modeling and data visualization
- tests: Test python functions

### Install instructions
This project was built using `python 3.8.10` using `pyenv` and `poetry`.   
To install the dependencies using poetry, cd into the project directory and   
then run the following command:
```
poetry install
```
Using pip:
```
pip install -r requirements.txt
```

### Deploying a model using FastAPI
*This example uses a scikit-learn random forest classifier trained on the COVID
data sets.*   
Change directories to `take-home` and build the docker image    
```
docker build -t rfapi .
```
Run the docker container   
```
docker run -d --name rfapicontainer -p 80:80 rfapi
```
Request predictions using the python example script `test_predictions.py`      
```
python test_predictions.py 
```
Also, you can test the deployed model using the web browser by going to 
[localhost/docs](http://localhost/docs)   
