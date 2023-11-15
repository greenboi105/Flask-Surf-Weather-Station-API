# SQLAlchemy Challenge

## Part 1: Analyze and Explore the Climate Data

In this section, we use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, we use SQLAlchemy ORM queries, Pandas, and Matplotlib.

1. Use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete the climate analysis and data exploration. 

2. Use the SQLAlchemy create_engine() function to connect to the SQLite database. 

3. Use the SQLAlchemy automap_base() function to reflect your tables into classes and then save references to the classes named station and measurement.

4. Link Python to the database by creating a SQLAlchemy session.

5. Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

### Precipitation Analysis 

1. Find the most recent date in the dataset. 

2. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data. 

3. Select only the 'date' and 'prcp' values. 

4. Load the query results into a Pandas DataFrame. Explicitly set the column names. 

5. Sort the DataFrame values by 'date'.

6. Plot the results by using the DataFrame plot method.

7. Use pandas to print the summary statistics for the precipitation data.

### Station Analysis

1. Design a query to calculate the total number of stations in the dataset.

2. Design a query to find the most-active stations.

    - List the stations and observation counts in descending order. 

    - Answer the following question: which station id has the greatest number of observations.

3. Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.

4. Design a query to get the previous 12 months of temperature observation (TOBS) data.

    - Filter by the station that has the greatest number of observations. 

    - Query the previous 12 months of TOBS data for that station. 

    - Plot the results as a histogram with bins=12.

## Part 2: Design the Climate App 

We now want to design a Flask API based on the queries we have developed. 

