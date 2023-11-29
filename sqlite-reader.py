import sys
import sqlite3

def main():
    database_file = sys.argv[1]

    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    if len(sys.argv) == 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print("Uso: sqlitereader.py [opções] arquivo.db")
        print()
        print("Opções:")
        print("-t, --tables     Lista todas as tabelas do banco de dados")
        print("-c, --cols      Lista todas as colunas de uma tabela")
        print("-h, --help      Exibe esta ajuda")
    else:
        if sys.argv[2] == '-t' or sys.argv[2] == '--tables':
            tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            for table in tables:
                print(table[0])
        else:
            if sys.argv[2] == '--cols':
                table_name = sys.argv[3]
                columns = cursor.execute("PRAGMA table_info('" + table_name + "');")
                for column in columns:
                    print(column[1])
            else:
                query = sys.argv[2]
                cursor.execute(query)

                for row in cursor:
                    print(row)

if __name__ == "__main__":
    main()
