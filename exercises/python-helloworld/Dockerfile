FROM python:3.9
LABEL maintainer="Ailine Lim"

COPY ./ app
WORKDIR /app
# use pip to install any application dependencies 
RUN pip install -r requirements.txt

# execute command  on the container start
CMD [ "python", "app.py" ]