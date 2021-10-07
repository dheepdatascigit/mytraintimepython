# mytraintimepython
can I buy coffee before my train in the morning at craigieburn station

## Setup
- Virtual environment = venv_mytrainpython
- pip run = pip install -r requirements.txt
- Environment variables
    - PTVAPI_DEVID = [developer id]
    - PTVAPI_SIG = [signature of the api call]
    - AZURE_STORAGE_CONNECTION_STRING = []

## how tos
### how to get connection string to azure blob storage
az storage account show-connection-string --resource-group RG-traintime --query connectionString --name trainstoreacc01