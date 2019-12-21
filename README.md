# ONNX Runtime on Azure Functions Example

ONNX is so sool. :cool:

See also [my article[Japanese]](https://qiita.com/okajax/items/b85dea2a97b0d82cd340)

## Get started

### Requirements

- Python 3.6
- pipenv
- Azure Blob Storage (for ONNX Model, Labels dictonary JSON)

### Set a environment variable

```
$ cp local.setting.example.json local.setting.json
```

And, set a connect string for your Blob Storage account.

```
    "Values": {
      "BLOB_CONNECTION_STRING": "<your_connect_string>"
    }
```


### Replace codes for your project.

#### HttpTrigger/__init__.py
```HttpTrigger/__init__.py
        container_client = blob_service_client.get_container_client('<your_container>') 
```


#### Pipfile
```Pipfile
deploy = "func azure functionapp publish <your_project> --python"
```

### Run :rocket:

```
$ pipenv install  # if you hav trouble, just do it. $ pipenv --three --python=`which python3`
$ pipenv run start
```

### Deploy to cloud :zap:

```
$ pipenv run deploy
```
