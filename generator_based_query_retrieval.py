'''
A generator based python code to fetch 10,000 rows at a time
from ms-sql server to a csv. This saves memory.
'''

import csv
from sqlalchemy.engine import URL
import pyodbc
from sqlalchemy import create_engine


def con_string(db_name):
    """
    Method that gives you connection string
    """
    return (
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
            + server
            + ";DATABASE="
            + db_name
            + ";UID="
            + username
            + ";PWD="
            + pw
    )


def con_url(constring):
    """
    Method to create the connection URL
    """
    return URL.create("mssql+pyodbc", query={"odbc_connect": constring})


def _generate_chunks(sql):
    """
    Method to generate chunks from the results
    """
    with sourceengine.begin() as conn:
        conn = conn.execution_options(stream_results=True)
        results = conn.execute(sql)
        while True:
            chunk = results.fetchmany(10000)
            if not chunk:
                break
            yield chunk


if __name__ == '__main__':

    server = ''
    username=''
    pw=''
    port = 1433
    db=''
    query = ""
    csv_file = 'test.csv'

    # creating sqlalchemy's engine which can be used later to fetch 10k rows
    sourceengine = create_engine(con_url(con_string(db)))

    try:
        chunks = _generate_chunks(query)

        with open(csv_file, "a") as file:
            for chunk in chunks:
                csv_writer = csv.writer(file, delimiter=",")
                csv_writer.writerows(chunk)

        print("Finished downloading to csv: ", csv_file.name)

    except Exception as exp:
        raise Exception(exp)
