<p align="center">
  <a  href="https://github.com/NoeCruzMW/zpy-flask-msc-docs"><img width="150" src="https://lh3.googleusercontent.com/a-/AOh14GjLO5qYYR5nQl5hgavUKz4Dv3LVzWDvGtV4xNam=s600-k-no-rp-mo" alt="Zurck'z"></a>
</p>
<p align="center">
    <em>Zkt for API Test Automation </em>
</p>
<p align="center"></p>

---

# Zkt

> Zurck'z Testing Tool

This package contains some helpers features for api test automation

ZPy use the following packages:

- zpy-api-core

## Requirements

- Python 3.10+

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install py flask micro service core .

```bash
pip install zkt
```

## Features

Contains some helper features.

- Stage
  - Step

## Basic Usage

```python



    test_scenario = Stepexecutor(
        scenario="Create a Generic Order PROD",
        steps=[
            FullRequestTest("Prepare token request", data_request),
            PostHttpRequest("Get Token"),
            HttpResponseVerifier("Tooken Response Verifier"),
            DictValueExtract("Extract Data Tokens", key="result"),
            StoreTransactData("Store Auth Data", key="auth")
        ],
    )

    result = test_scenario.execute()
    print(result)

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

[Noé Cruz](https://www.linkedin.com/in/zurckz/)
