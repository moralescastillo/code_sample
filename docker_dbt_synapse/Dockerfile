FROM python:3.8.13

# Update and install system packages
RUN apt-get update -y && \
  apt-get install --no-install-recommends -y -q \
  git \
  libpq-dev \
  unixodbc-dev \
  python-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# install ODBC Driver 17 for SQL Server
RUN  apt-get update \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install DBT
RUN pip install -U pip
RUN pip install dbt-core==1.0.5
RUN pip install dbt-synapse==1.1.0


ENV DBT_DIR /dbt
ENV DBT_PROFILES_DIR=/dbt/profile/

COPY . /dbt/
WORKDIR /dbt/
RUN dbt run --select invesdor_gender
