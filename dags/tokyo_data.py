from datetime import datetime
import json
from airflow.operators.python import PythonOperator
from kafka import KafkaProducer
from bs4 import BeautifulSoup
import requests
import pandas as pd
from airflow import DAG
import logging

def scraping_data():
    url = 'https://en.wikipedia.org/wiki/2020_Summer_Olympics_medal_table'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    table_index = None
    # Find the correct table by class name
    for index, table in enumerate(tables):
        if 'sortable' in table.get('class', []) and 'sticky-header-multi' in table.get('class', []):
            table_index = index
            break
    if table_index is None:
        raise ValueError("Could not find the correct table on the page.")
    Tokyo_olympics = pd.DataFrame(columns=["Rank", "Noc", "Gold", "Silver", "Bronze", "Total"])
    past_rank = None

    for row in tables[table_index].tbody.find_all("tr"):
        col = row.find_all("td")
        if col:
            if len(col) == 5:
                Rank = col[0].get_text(strip=True)
                past_rank = Rank
                Gold = col[1].get_text(strip=True)
                Silver = col[2].get_text(strip=True)
                Bronze = col[3].get_text(strip=True)
                Total = col[4].get_text(strip=True)
            else:
                Rank = past_rank
                Gold = col[0].get_text(strip=True)
                Silver = col[1].get_text(strip=True)
                Bronze = col[2].get_text(strip=True)
                Total = col[3].get_text(strip=True)

        col1 = row.find_all("th")
        anchor_tag = col1[0].find("a")
        if anchor_tag:
            Noc = anchor_tag.get_text(strip=True)
            Tokyo_olympics = pd.concat([Tokyo_olympics, pd.DataFrame(
                [{"Rank": Rank, "Noc": Noc, "Gold": Gold, "Silver": Silver, "Bronze": Bronze, "Total": Total}])],
                                       ignore_index=True)
    return Tokyo_olympics

def stream_data():
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000,
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    df = scraping_data()
    for _, row in df.iterrows():
        message = row.to_dict()
        producer.send('olympic_games_results', value=message)
        logging.info(f"Sent message: {message}")
    producer.flush()  # Ensure all messages are sent

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 7, 25, 1, 35),
    'retries': 0
}

with DAG('tokyo_data', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    streaming_task = PythonOperator(
        task_id='stream_data_from_scrap',
        python_callable=stream_data
    )


