import os
import json
import sqlite3
import time

def db_conn(db_path):
    try:
        return sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        return False

def checar_ou_criar_tabela(db_path, table_name, conn):
    cursor = conn.cursor()

    # Verifica se a tabela existe.

    cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    count = cursor.fetchone()[0]

    if count > 0:
        return True

    print('')
    create_table_query = f"""
      CREATE TABLE {table_name} (
      bssid TEXT,
      frequency_mhz INTEGER,
      rssi INTEGER,
      ssid TEXT,
      channel_bandwidth_mhz TEXT,
      latitude FLOAT,
      longitude FLOAT,
      altitude FLOAT,
      accuracy FLOAT
      );
    """
    cursor.execute(create_table_query)
    conn.commit()

    return True


def examinar_redes():
    wifiDump = os.popen('termux-wifi-scaninfo').read()
    y = json.loads(wifiDump)
    return y

def obter_geolocalizacao():
    georef = os.popen('termux-location').read()
    y = json.loads(georef)
    return y

def armazenar_dados_db(bssid):
    # verifica se o mac ja esta no db
    # reescreve caso o novo sinal seja mais forte
    # atualiza informacoes para as mais recentes
    return 0

def atualizar_melhor_local(table, bssid, conn, cursor, latitude, longitude, altitude, rssi):
    cursor.execute(f'''UPDATE {table} SET latitude = "{latitude}",
    longitude = "{longitude}", altitude = "{altitude}", rssi = {rssi}
    WHERE bssid = "{bssid}";''')
    conn.commit()
    return True

def main():
    # parte 1: definir algumas variáveis
    sistema_versao = 1.0
    arquivo_db = 'wifidump.db'
    table = "redeswifi"
    # parte 2: conectar ao banco de dados
    conn = db_conn(arquivo_db)
    if not conn:
        print('Não foi possível conectar ao banco de dados')
        exit()
    else:
        print('Carregando Banco de Dados...')
    cursor = conn.cursor()
    # parte 3: varificar se a tabela existe, caso contrario criar
    tabela_criada = checar_ou_criar_tabela(arquivo_db, table, conn)
    if not tabela_criada:
        exit()
    # parte 4: iniciar o loop
    while True:
        # parte 4.1: obtenho as informacoes das redes
        redes = examinar_redes()
        # parte 4.2: obtenho geolocalizacao
        georef = obter_geolocalizacao()
        # parte 4.3: para cada rede salvo no banco de dados
        for rede in redes:
            cursor.execute(f'SELECT * FROM {table} WHERE bssid = "{rede["bssid"]}";')
            ultimo_check = cursor.fetchall()
            if len(ultimo_check) < 1:
                cursor.execute(f'''INSERT INTO {table}
                (bssid, frequency_mhz, rssi, ssid, channel_bandwidth_mhz,
                latitude, longitude, altitude, accuracy)
                values("{rede["bssid"]}", "{rede["frequency_mhz"]}",
                {rede["rssi"]}, "{rede["ssid"]}",
                {rede["channel_bandwidth_mhz"]}, {georef["latitude"]},
                {georef["longitude"]}, {georef["altitude"]}, {georef["accuracy"]});''')
                conn.commit()
                print('Inseriu nova rede: ', rede['bssid'])
            elif int(rede['rssi']) > int(ultimo_check[0][2]):
                atualizado = atualizar_melhor_local(table, rede["bssid"], conn, cursor,
                georef["latitude"], georef["longitude"], georef["altitude"], rede["rssi"])
                if atualizado:
                    print("Informacoes de ", rede['bssid'], " atualizadas")
            else:
                print("Não foi necessário atualizar dados de ", rede['bssid'])

       # parte 4.4: aguardo proxima execucao
        time.sleep(10)


main()