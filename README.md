# How does it work 
- once a day the script searches for swagger files in the master branch of all repositories in gitlab
- then it gets the swagger specification from services where it is generated dynamically  
- therefor it gets all services from the Kong Admin API 
- and checks for the endpoint /doc

# Requirements
```shell
pip install requirements.txt
```

# Run 
- needed environmental variables:
- TOKEN: Gitlab access token for private repositories
- LADON: internal URL to Ladon service 
- DB_HOST
- DB_PORT

# Notes
- if you want to re read the swagger files manually, just reload the service, it will delete all previous swagger files 