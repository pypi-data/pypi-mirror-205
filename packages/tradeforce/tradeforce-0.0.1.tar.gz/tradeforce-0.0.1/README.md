

# -------
# Docker
# -------

# Get bash shell in container
docker exec -it tradeforce bash


# Get requirments.txt
cd /to/path/tradeforce/root
docker build -t tradeforce:build --target build .
docker create --name tradeforce_build tradeforce:build
docker cp tradeforce_build:/opt/tradeforce/requirements.txt ./requirements.txt

# ------------------
# Window Powershell
# ------------------

# Run dedicated market server
$env:RUN_MARKET_SERVER="True"; docker-compose up; Remove-Item Env:\RUN_MARKET_SERVER

# Run JupyterLab
$env:RUN_JUPYTERLAB="True"; docker-compose up; Remove-Item Env:\RUN_JUPYTERLAB

# -----------
# Linux Bash
# -----------

# Run dedicated market server
RUN_MARKET_SERVER="True" docker-compose up

# Run JupyterLab
RUN_JUPYTERLAB="True" docker-compose up
