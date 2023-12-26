# E-RETAIL

[![E-RETAIL CI](https://github.com/greatlaki/test-task-rocketdata-electronic-retail/actions/workflows/ci.yml/badge.svg)](https://github.com/greatlaki/test-task-rocketdata-electronic-retail/actions/workflows/ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/f96f7167d5e96fa9ef0c/maintainability)](https://codeclimate.com/github/greatlaki/test-task-rocketdata-electronic-retail/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f96f7167d5e96fa9ef0c/test_coverage)](https://codeclimate.com/github/greatlaki/test-task-rocketdata-electronic-retail/test_coverage)

### About
Implement a network model for the sale of electronics. The network have a hierarchical structure of 5 levels:
- Factory;
- Distributor;
- Dealership;
- Large retail chain;
- An individual entrepreneur.

Each link in the network refers to only one hardware supplier (not
necessarily the previous one in the hierarchy). It is important to note that the hierarchy level
is determined not by the name of the link, but by the relationship to the other elements of the network, i.e.
the plant is always at level 0, and if the retail network refers directly to
the plant, bypassing the other links, its level is 1.

## Configuration
Configuration is stored in `backend/.env`, for examples see `default.env`

## Installing on a local machine
This project requires python 3.11. Python virtual environment should be installed and activated.
 Dependencies are managed by [poetry](https://python-poetry.org/) with requirements stored in `pyproject.toml`.

Install requirements:

```bash
make install
```

## Docker
Then run the following command in the same directory as the `docker-compose.yml` file to start the container.
`docker compose up -d`

Testing:
```bash
# run lint
make lint

# run unit tests
make test
```

### Features: 

- Admin site:
  - a link to the "Provider";
  - filter by city name;
  - "admin action", clearing debts to the provider of selected objects;
  - Admin site - {{domain}}/admin;

- API:
  - Information about all network objects;
  - Filters: by country, by product ids;
  - CRUD (Provider objects, Product objects);
  - Output of statistics on objects whose debt exceeds the average debt of all objects;
  - API is available only to authorized users;
  - API description - {{domain}}/docs;

- The ability to fill the database (users have a password - "Y530-15ICH")
  ```bash
  make init-data
  ```

- The processes of changing the debt are automated
