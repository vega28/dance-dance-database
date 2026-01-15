# dancenerd app

## local setup

### 1. clone the repo
  ```
  git clone https://github.com/vega28/dance-dance-database.git
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

### 5. database setup
- create a dancenerd postgres database
- add configuration in a `.env` file in the root of the project
- seed db: `flask --app api.api seed`

## run server

start the react app:
- `npm run dev`

start the flask app:
- `npm run api`