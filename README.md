# How does it work 
- gets all services from the Kong Admin API 
- and checks for the endpoint /doc

# Requirements
```shell
pip install requirements.txt
```

# Run 
- needed environmental variables:
- TOKEN: Gitlab access token for private repositories
- LADON_URL: internal URL to Ladon service 
- DB_HOST
- DB_PORT
- KONG_HOST (publicly available kong host)
- KONG_INTERNAL_URL (internally available kong url, ends with /api)
- KONG_INTERNAL_BASIC_USER (username for basic auth)
- KONG_INTERNAL_BASIC_PW (password for basic auth)


# Notes
- if you want to re read the swagger files manually, just reload the service, it will delete all previous swagger files 
