FROM python:3.9
LABEL maintainer="Ailine Lim"

# Copy local code to the container image.
COPY ./ app
WORKDIR /app

# use pip to install any application dependencies 
RUN pip install -U pip && \
	pip install -r ./project/techtrends/requirements.txt

ENV PORT 3111
EXPOSE ${PORT}

# execute command  on the container start
CMD python init_db.py ; python app.py
