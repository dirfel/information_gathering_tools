#!/bin/python3
import sys
import sqlite3

def main():
    if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print("Uso: sqlitereader.py [opções] arquivo.db")
        print()
        print("Opções:")
        print("-t, --tables        Lista todas as tabelas do banco de dados")
        print("-c, --cols          Lista todas as colunas de uma tabela")
        print("-r, --rows          Conta o número de linhas de uma tabela")
        print("-l, --limit N       Exibe as primeiras N linhas de uma tabela")
        print("-i, --indexes       Lista os índices de uma tabela")
        print("-d, --describe      Exibe a descrição de uma tabela")
        print("-h, --help          Exibe esta ajuda")
        return

    database_file = sys.argv[-1]

    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    if sys.argv[1] == '-t' or sys.argv[1] == '--tables':
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for table in tables:
            print(table[0])

    elif sys.argv[1] == '-c' or sys.argv[1] == '--cols':
        table_name = sys.argv[2]
        columns = cursor.execute("PRAGMA table_info('" + table_name + "');")
        for column in columns:
            print(column[1])

    elif sys.argv[1] == '-r' or sys.argv[1] == '--rows':
        table_name = sys.argv[2]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        print(f"Número de linhas em {table_name}: {row_count}")

    elif sys.argv[1] == '-l' or sys.argv[1] == '--limit':
        table_name = sys.argv[3]
        limit = int(sys.argv[2])
        rows = cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
        for row in rows:
            print(row)

    elif sys.argv[1] == '-i' or sys.argv[1] == '--indexes':
        table_name = sys.argv[2]
        indexes = cursor.execute(f"PRAGMA index_list('{table_name}');")
        for index in indexes:
            print(index[1])

    elif sys.argv[1] == '-d' or sys.argv[1] == '--describe':
        table_name = sys.argv[2]
        description = cursor.execute(f"PRAGMA table_info('{table_name}');")
        for column in description:
            print(f"Coluna: {column[1]}, Tipo: {column[2]}, NULL permitido: {column[3] == 0}, Chave Primária: {column[5] == 1}")

if __name__ == "__main__":
    main()
