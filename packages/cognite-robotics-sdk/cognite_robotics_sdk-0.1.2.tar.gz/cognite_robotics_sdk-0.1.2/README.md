# Cognite Robotics SDK


### Build stubs from OpenAPI spec in `robotics_local.yml`

Run the following command from root in the repo
```sh
make generate-openapi-python
```

### Build the SDK

Navigate to the `sdks/robotics-sdk-python` directory and run the following command
```sh
make poetry-install
```

To run all the tests, run the following command
```sh
poetry run pytest
```

If you want to run a single test `<mytest>.py`, run the following command
```sh
poetry run pytest tests/<mytest>.py
```

`mypy` is used to check the type annotations. To run `mypy`, run the following command
```sh
make poetry-mypy
```

Finally, to build the package, run the following command
```sh
poetry build
```
