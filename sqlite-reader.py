#!/bin/python3
import sys
import sqlite3

def print_help():
    print("Uso: sqlitereader.py [opções] arquivo.db")
    print()
    print("Opções:")
    print("-t, --tables        Lista todas as tabelas do banco de dados")
    print("-c, --cols          Lista todas as colunas de uma tabela")
    print("-r, --rows          Conta o número de linhas de uma tabela")
    print("-l, --limit N       Exibe as primeiras N linhas de uma tabela")
    print("-i, --indexes       Lista os índices de uma tabela")
    print("-d, --describe      Exibe a descrição de uma tabela")
    print("-sa, --search-all   Pesquisa um valor em todas as colunas de uma tabela")
    print("-h, --help          Exibe esta ajuda")

def connect_db(database_file):
    """Estabelece a conexão com o banco de dados SQLite."""
    return sqlite3.connect(database_file)

def list_tables(cursor):
    """Lista todas as tabelas no banco de dados."""
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in tables:
        print(table[0])

def list_columns(cursor, table_name):
    """Lista todas as colunas de uma tabela."""
    columns = cursor.execute(f"PRAGMA table_info('{table_name}');")
    for column in columns:
        print(column[1])

def count_rows(cursor, table_name):
    """Conta o número de linhas de uma tabela."""
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    row_count = cursor.fetchone()[0]
    print(f"Número de linhas em {table_name}: {row_count}")

def limit_rows(cursor, table_name, limit):
    """Exibe as primeiras N linhas de uma tabela."""
    rows = cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
    for row in rows:
        print(row)

def list_indexes(cursor, table_name):
    """Lista todos os índices de uma tabela."""
    indexes = cursor.execute(f"PRAGMA index_list('{table_name}');")
    for index in indexes:
        print(index[1])

def describe_table(cursor, table_name):
    """Exibe a descrição de uma tabela."""
    description = cursor.execute(f"PRAGMA table_info('{table_name}');")
    for column in description:
        print(f"Coluna: {column[1]}, Tipo: {column[2]}, NULL permitido: {column[3] == 0}, Chave Primária: {column[5] == 1}")

def search_all_columns(cursor, table_name, search_value):
    """Pesquisa um valor em todas as colunas de uma tabela."""
    cursor.execute(f"PRAGMA table_info('{table_name}');")
    columns = [column[1] for column in cursor.fetchall()]

    # Montar a consulta para pesquisar em todas as colunas
    query = f"SELECT * FROM {table_name} WHERE " + " OR ".join([f"{col} LIKE ?" for col in columns])
    search_term = f"%{search_value}%"

    # Executar a consulta com a busca parcial
    rows = cursor.execute(query, [search_term] * len(columns))

    results_found = False
    for row in rows:
        print(row)
        results_found = True
    
    if not results_found:
        print(f"Nenhum resultado encontrado para '{search_value}' em '{table_name}'.")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print_help()
        return

    database_file = sys.argv[-1]
    connection = connect_db(database_file)
    cursor = connection.cursor()

    if sys.argv[1] == '-t' or sys.argv[1] == '--tables':
        list_tables(cursor)

    elif sys.argv[1] == '-c' or sys.argv[1] == '--cols':
        table_name = sys.argv[2]
        list_columns(cursor, table_name)

    elif sys.argv[1] == '-r' or sys.argv[1] == '--rows':
        table_name = sys.argv[2]
        count_rows(cursor, table_name)

    elif sys.argv[1] == '-l' or sys.argv[1] == '--limit':
        limit = int(sys.argv[2])
        table_name = sys.argv[3]
        limit_rows(cursor, table_name, limit)

    elif sys.argv[1] == '-i' or sys.argv[1] == '--indexes':
        table_name = sys.argv[2]
        list_indexes(cursor, table_name)

    elif sys.argv[1] == '-d' or sys.argv[1] == '--describe':
        table_name = sys.argv[2]
        describe_table(cursor, table_name)

    elif sys.argv[1] == '-sa' or sys.argv[1] == '--search-all':
        search_value = sys.argv[2]
        table_name = sys.argv[3]
        search_all_columns(cursor, table_name, search_value)

if __name__ == "__main__":
    main()
