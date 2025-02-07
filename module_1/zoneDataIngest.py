#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine


def main(params) :
    user = params.user
    password = params.password 
    host = params.host
    db = params.db
    table = params.table_name
    port = params.port
    url = params.url
    file_name = 'zoneHomework.csv'

    #downlaod data using url
    os.system(f"wget {url} -O {file_name}")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    print("test1")
    df = pd.read_csv(url)

    print(df.head())

    print(pd.io.sql.get_schema(df , name=table))

    # print(pd.io.sql.get_schema(df , name=table , con=engine))

    df.head(n=0).to_sql(name=table , con=engine , if_exists='replace')
    print("Start inserting data to database")
    chunksize = 100000
    dfLenght = len(df)
    startTime = time()
    for start in range(0 , dfLenght , chunksize) : 
        start_time = time()
        chunk = df[start:start+chunksize]
        chunk.to_sql(name=table , con=engine , if_exists='append')
        end_time = time()
        print("another chunk inserted... took %.3f second" % (end_time - start_time))
    endTime = time()
    print("Finsished at %.3f second" %(endTime - startTime))

    while True:
        time.sleep(60) 

if __name__ == '__main__' : 
    parser = argparse.ArgumentParser(description='ingest parquat data to postgres')
    # user , password , host , port , db , table ,parquatURL 
    parser.add_argument('--user' , help='user name of postgres')
    parser.add_argument('--password' , help='password of postgres')
    parser.add_argument('--host' , help='host name of postgres')
    parser.add_argument('--port' , help='port number')
    parser.add_argument('--db' , help='database name of postgres')
    parser.add_argument('--table_name' , help='table name you want to ingest data in')
    parser.add_argument('--url' , help='url of the data')


    args = parser.parse_args()

    main(args)