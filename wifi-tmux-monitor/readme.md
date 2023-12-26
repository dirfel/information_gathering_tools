# Descrição

Script python para ser executado no aplicativo TERMUX para android.
A execução ocorre em loop infinito (até o usuário interromper com ctrl + C) e a cada execução busca as informações de georeferência e de redes wifi próximas. Quando encontrada uma nova rede, armazena suas informações em wifidump.db, um banco de dados sqlite3. Quando a rede encontrada ja está armazenada no banco de dados, atualiza as coordenadas se o sinal dessa nova captura for mais forte que a anterior.

# Instalação

1. Baixe o aplicativo termux para android
2. Baixe o aplicativo termux:API
3. Execute o aplicativo
4. Instale python3

# Execução

Na linha de comando:

python3 wifimonitor.py

Aceite a permissão de georeferencia caso seja solicitada