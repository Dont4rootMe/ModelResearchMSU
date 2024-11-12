FROM pytorch/pytorch AS backend

# install packages
RUN pip install uvicorn fastapi pydentic

# run server
COPY ./src /src
EXPOSE 8000
CMD ["python", "/src/api.py"]