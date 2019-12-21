# ONNX Runtime on Azure Functions Example

ONNX with Severless is so sool :sunglasses:

See also [my article[Japanese]](https://qiita.com/okajax/items/b85dea2a97b0d82cd340)

## 1. Requirements

- Python 3.6
- pipenv
- Azure Blob Storage (for ONNX Model, Labels dictonary JSON)

### Files
- [MobileNet ONNX Model](https://github.com/onnx/models/tree/master/vision/classification/mobilenet)
- [Labels dictonary](https://gist.github.com/PonDad/4dcb4b242b9358e524b4ddecbee385e9)

## 2. Set an environment variable

### For local development

```
$ cp local.setting.example.json local.setting.json
```

And, set a connect string for your Blob Storage account.

```local.setting.json
    "Values": {
      "BLOB_CONNECTION_STRING": "<your_connect_string>"
    }
```

### For cloud

Edit settings on Azure.


## 3. Replace codes for your project

### HttpTrigger/__init__.py
```HttpTrigger/__init__.py
        container_client = blob_service_client.get_container_client('<your_container>') 
```


### Pipfile
```Pipfile
deploy = "func azure functionapp publish <your_project> --python"
```

## 4. Run :rocket:

```
$ pipenv install  # if you hav trouble, just do it. $ pipenv --three --python=`which python3`
$ pipenv run start
```

POST a image to endpoint :+1:

## 5. Deploy to cloud :zap:

```
$ pipenv run deploy
```
