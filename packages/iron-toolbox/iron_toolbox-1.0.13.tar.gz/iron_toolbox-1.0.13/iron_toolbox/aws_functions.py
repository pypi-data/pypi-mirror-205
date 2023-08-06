import datetime
import pandas as pd
from datetime import datetime, timedelta
import boto3
import awswrangler as wr
import time
import os


import warnings
warnings.simplefilter("ignore")
# aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
# aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

session = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name="us-east-1")


def get_timestamp():
    timestamp = datetime.utcnow() - timedelta(hours=3)
    return timestamp


def send_file_to_s3(local_file, s3_path, file_name):
    wr.s3.upload(local_file, f's3://{s3_path}/{file_name}')
    print('Arquivo enviado para S3 com sucesso!')


def send_dataset_to_s3(dataset, file_name, bucket_folder, folder_name):
    if 'csv' in file_name:
        dataset.to_csv(f"s3://{bucket_folder}/{folder_name}/{file_name}", sep=';', encoding='utf-8',
                       storage_options={'key': os.environ['AWS_ACCESS_KEY_ID'],
                                        'secret': os.environ['AWS_SECRET_ACCESS_KEY']})
    else:
        dataset.to_excel(f"s3://{bucket_folder}/{folder_name}/{file_name}", index=False,
                         storage_options={'key': os.environ['AWS_ACCESS_KEY_ID'],
                                          'secret': os.environ['AWS_SECRET_ACCESS_KEY']})

    print(f'{file_name} adicionado ao S3\n')
    return


def download_file_from_s3_to_dataset(arquivo, bucket_name, folder_name):
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(bucket_name)

    files = []
    df_final = pd.DataFrame()
    for object_summary in my_bucket.objects.filter(Prefix=folder_name):
        if arquivo in object_summary.key:
            print(object_summary.key)
            if 'homologacao' in object_summary.key:
                continue
                files.pop(-1)
                files.append(object_summary.key)
            else:
                files.append(object_summary.key)
            if 'xlsx' in object_summary.key:
                df = wr.s3.read_excel(f's3://{bucket_name}/{object_summary.key}', dtype={'CPF': str, 'cpf': str},
                                      boto3_session=session, use_threads=True, engine='openpyxl')
            elif 'json' in object_summary.key:
                df = wr.s3.read_json(f's3://{bucket_name}/{object_summary.key}', dtype={'CPF': str, 'cpf': str},
                                      boto3_session=session, use_threads=True)
            else:
                df = wr.s3.read_csv(f's3://{bucket_name}/{object_summary.key}', dtype={'CPF': str, 'cpf': str},
                                    boto3_session=session, use_threads=True, sep=',', encoding='latin')
                # df = pd.read_csv(f's3://{bucket_name}/{object_summary.key}', sep=',', encoding='latin',
                #                  dtype={'cpf': str},
                #                  storage_options={'key': os.environ['AWS_ACCESS_KEY_ID'],
                #                                   'secret': os.environ['AWS_SECRET_ACCESS_KEY']})
            df['origem'] = object_summary.key.removeprefix(f'{folder_name}/')
            df_final = pd.concat([df_final, df], ignore_index=True, sort=True)
            time.sleep(2)
    print(f'Finalizado! {df_final["origem"].nunique()} arquivo (s) foi/foram carregados!\n')
    return df_final


# def send_parquet_to_s3(dataset, bucket_name, folder_name, database, mode="append", table_name=None):
#
#     dataset['timestamp'] = get_timestamp()
#
#     wr.s3.to_parquet(
#         df=dataset,
#         path=f's3://{bucket_name}/{folder_name}/{table_name}',
#         index=False,
#         dataset=True,
#         max_rows_by_file=10000,
#         database=database,
#         table=table_name,
#         # dtype=dict
#         mode=mode,
#         # partition_cols=['_updated_at'],
#         use_threads=True,
#         boto3_session=session)
#
#     print(f'{table_name} adicionado ao S3\n')
#     return


def send_json_to_s3(df, bucket_name, foler_name, file_name=None):

    df['DT_ENVIO'] = get_timestamp()

    wr.s3.to_json(
        df=df,
        path=f's3://{bucket_name}/{foler_name}/{file_name}.json',
        dataset=False,
        concurrent_partitioning=True,
        use_threads=True,
        boto3_session=session,
        orient='records',
        date_format='iso')

    print(f'Tabela {foler_name} adicionada ao S3\n')
    return


def get_last_last_modified_file(bucket_name, folder_name):
    s3_client = boto3.client('s3')
    all_files = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)['Contents']
    latest_file = max(all_files, key=lambda x: x['LastModified'])
    file_path = latest_file['Key']
    file_name = latest_file['Key'].removeprefix(f'{folder_name}/')
    print(f'\nBaixando arquivo {file_name}!')

    if 'xlsx' in file_name:
        df = wr.s3.read_excel(f's3://{bucket_name}/{file_path}', dtype={'CPF': str, 'cpf': str},
                              boto3_session=session, use_threads=True, engine='openpyxl')
    elif 'json' in file_name:
        df = wr.s3.read_json(f's3://{bucket_name}/{file_path}', dtype={'CPF': str, 'cpf': str},
                             boto3_session=session, use_threads=True)
    elif 'csv' in file_name:
        df = wr.s3.read_csv(f's3://{bucket_name}/{file_path}', dtype={'CPF': str, 'cpf': str},
                            boto3_session=session, use_threads=True, sep=',', encoding='latin')

    print(f'Arquivo {file_name} carregado com sucesso!')
    return df


''' Funções para enviar arquivo parquet e criar tabela no Glue Catalogue '''


def send_parquet_partioned_to_s3(dataset, bucket_name, folder_name, database, mode="append",
                                 table_name=None, partition_cols=None):

    dataset['envio_domo'] = get_timestamp()

    wr.s3.to_parquet(
        df=dataset,
        path=f's3://{bucket_name}/{folder_name}/{table_name}',
        index=False,
        dataset=True,
        # max_rows_by_file=10000,
        database=database,
        table=table_name,
        # dtype=dict
        mode=mode,
        catalog_versioning=True,
        partition_cols=partition_cols,
        concurrent_partitioning=True,
        use_threads=True,
        boto3_session=session)

    print(f'{table_name} adicionado ao S3\n')
    return


def send_parquet_to_s3(dataset, bucket_name, folder_name, mode="append", database=None, table_name=None,
                       partition_cols=None):

    dataset['envio_s3'] = get_timestamp()

    wr.s3.to_parquet(
        df=dataset,
        path=f's3://{bucket_name}/{folder_name}/{table_name}',
        index=False,
        dataset=True,
        max_rows_by_file=10000,
        database=database,
        table=table_name,
        # dtype=dict
        mode=mode,
        catalog_versioning=True,
        partition_cols=partition_cols,
        concurrent_partitioning=True,
        use_threads=True,
        boto3_session=session)

    print(f'{table_name} adicionado ao S3\n')
    return


def send_csv_to_s3(dataset, bucket_name, folder_name, mode=None, database=None, table_name=None,
                   partition_cols=None, sep=';'):

    if database is not None:
        dataset['envio_domo'] = get_timestamp()
        wr.s3.to_csv(
            df=dataset,
            path=f's3://{bucket_name}/{folder_name}/{table_name}',
            index=False,
            sep=sep,
            dataset=True,
            database=database,
            table=table_name,
            mode=mode,
            catalog_versioning=True,
            partition_cols=partition_cols,
            concurrent_partitioning=True,
            use_threads=True,
            boto3_session=session)
    else:
        wr.s3.to_csv(
            df=dataset,
            path=f's3://{bucket_name}/{folder_name}/{table_name}',
            index=False,
            index_label=False,
            use_threads=True,
            sep=sep,
            boto3_session=session)

    print(f'{table_name} adicionado ao S3\n')
    return


def download_csv_from_s3(path, filename):
    dataset = wr.s3.read_csv(f'{path}/{filename}', sep=';')
    print(f'Arquivo {filename} carregado com sucesso!')
    return dataset


def read_parquet_from_s3(bucket_folder, folder_name, file_name, columns=None):
    dataset = wr.s3.read_parquet(path=f's3://{bucket_folder}/{folder_name}/{file_name}',
                                 path_suffix='.parquet',
                                 use_threads=True,
                                 boto3_session=session,
                                 columns=columns)
    return dataset


def read_parquet_from_s3_with_filter(bucket_folder, folder_name, file_name, columns=None):
    dataset = wr.s3.read_parquet(path=f's3://{bucket_folder}/{folder_name}/{file_name}',
                                 path_suffix='.parquet',
                                 # chunked=True,
                                 dataset=True,
                                 use_threads=True,
                                 boto3_session=session,
                                 columns=columns,
                                 pyarrow_additional_kwargs={"filters": ('corporacao', '=', 'Saúde Petrobras')})
    return dataset


def get_max_updated_date_from_table(database, table, column):
    print(f"SELECT MAX({column}) FROM {table} AS max_date")
    max_updates_date = wr.athena.read_sql_query(boto3_session=session,
                                                database=database,
                                                max_cache_seconds=900,
                                                max_cache_query_inspections=500,
                                                use_threads=True,
                                                sql=f"SELECT MAX({column}) AS max_date FROM {table}")
    return max_updates_date.iloc[0, 0]


def remove_duplicates_from_table(database, table, table_view, column, order_by):
    sql = f'''CREATE OR REPLACE VIEW {table_view} AS
                WITH agendamentos_duplicados AS
                    (SELECT
                        *,
                        ROW_NUMBER() OVER(PARTITION BY {column} ORDER BY {order_by} DESC) AS registro_duplicado 
                    FROM {table})
                SELECT
                    *
                FROM
                    agendamentos_duplicados
                WHERE
                    registro_duplicado = 1'''
    retorno = wr.athena.start_query_execution(sql=sql,
                                              boto3_session=session,
                                              database=database,
                                              max_cache_seconds=900,
                                              max_cache_query_inspections=500)
    print(f'Duplicados Removidos e Tabela {table_view} criada')
    return retorno


def run_query_in_athena(sql, database):
    query = wr.athena.read_sql_query(boto3_session=session,
                                     database=database,
                                     sql=sql,
                                     use_threads=True,
                                     max_cache_seconds=900,
                                     max_cache_query_inspections=500)
    return query


def create_view_athena(sql, database):
    query = wr.athena.start_query_execution(boto3_session=session,
                                            database=database,
                                            sql=sql,
                                            max_cache_seconds=900,
                                            max_cache_query_inspections=500)
    return query


def check_table_length(database, table):
    table_length = wr.athena.read_sql_query(boto3_session=session,
                                            database=database,
                                            use_threads=True,
                                            max_cache_seconds=900,
                                            max_cache_query_inspections=500,
                                            sql=f"SELECT count(*) AS table_legnth FROM {table}")
    return table_length.iloc[0, 0]


# def create_table_to_updadate(database, table, new_table, column, order_by):
def create_table_to_update(database, bucket, folder_name, table, update_table, col_update, col_drop,
                           partition_cols=None):

    try:
        dt_ultimo_registro = str(get_max_updated_date_from_table(database, update_table, col_update))[0:23]
        table_to_update = run_query_in_athena(f'SELECT * FROM {table}_update', database)
        data_to_update = wr.athena.read_sql_query(boto3_session=session,
                                                  database=database,
                                                  max_cache_seconds=900,
                                                  max_cache_query_inspections=500,
                                                  use_threads=True,
                                                  sql=f''' SELECT
                                                                *
                                                             FROM
                                                                {table}
                                                             where 
                                                                {table}.{col_update} > timestamp '{dt_ultimo_registro}' 
                                                                ''')
    except Exception as e:
        dt_ultimo_registro = datetime.datetime(2015, 1, 1)
        table_to_update = pd.DataFrame()
        data_to_update = wr.athena.read_sql_query(boto3_session=session,
                                                  database=database,
                                                  max_cache_seconds=900,
                                                  max_cache_query_inspections=500,
                                                  use_threads=True,
                                                  sql=f'''SELECT
                                                              *
                                                          FROM
                                                              {table}''')
        print(f'Tabela para update vazia, error: {e}')

    table_to_update = pd.concat([table_to_update, data_to_update], ignore_index=True)
    table_to_update.sort_values(by=[col_drop], ascending=False, inplace=True)
    table_to_update.drop_duplicates([col_drop], keep='last', inplace=True)
    table_to_update.drop(columns=['envio_s3'], inplace=True)

    send_parquet_to_s3(table_to_update, bucket,
                       folder_name=folder_name,
                       database=database,
                       table_name=update_table,
                       mode='overwrite',
                       partition_cols=partition_cols)

    return dt_ultimo_registro, table_to_update, data_to_update
