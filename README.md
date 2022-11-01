# Publisher
![Python](https://img.shields.io/badge/Python-3.10-green?style=for-the-badge)

> An in-progress implementation of a publishing platform intended to mimic the **[CommunityWrites project](https://github.com/MarvinKweyu/CommunityWrites)**


![Preview](./image/publisher.gif)

## Key Features

:white_check_mark: Article tagging

:white_check_mark: Comments

:white_check_mark: Email sharing

:white_check_mark: Full-text search

## Setup 

### Bare metal
**Note:** 

**Install postgresql on your host machine**

Setup a virtual environment, install requirements , run migrations and run the server

```bash
bash develop.sh
```

### It just works(Docker)

(Documentation in progress)

With *docker* and *docker-compose* installed , clone the repo and run the following command at teh root of the project.
```bash
docker-compose up -d --build
```

Access the project via: 1**27.0.0.1:8000/home**