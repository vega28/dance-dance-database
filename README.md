# dancenerd app

## local setup

### 1. clone the repo
  ```
  git clone https://github.com/vega28dance-dance-database.git
  cd dance-dance-database
  ```

### 2. python setup

- `uv sync`
    - creates virtual environment
    - installs the appropriate python version and dependencies

- enter the virtual environment: `source .venv/bin/activate`
    (leave the virtual env using `deactivate`)

### 3. switch to the correct node version
- `nvm use 25`

### 4. install JS dependencies
- `npm install`


## run server

start the react app:
- `npm run dev`

start the flask app:
- `npm run api`