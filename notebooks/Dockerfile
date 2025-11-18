FROM jupyter/scipy-notebook:latest

USER root

# Install additional packages
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    plotly \
    scikit-learn \
    xgboost \
    lightgbm \
    transformers \
    sentence-transformers

USER jovyan

WORKDIR /home/jovyan/work

EXPOSE 8888

CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''", "--NotebookApp.allow_origin='*'"]

