# Descrição

Script python para usar em investigação de fontes abertas, com base no CPF, é possível descobrir quais possíveis estados foi gerado e com parte desse número, podemos encontrar todos CPF possíveis.

# Como usar

Verificar informações de CPF:
Basta inserir como argumento um número de 11 dígitos
python3 cpf.py 12345678901

O script retornará se o CPF é válido, caso positivo informa quais possíveis estados de registro e gera links para buscar mais informações na internet

Não para por aí!

Caso você não saiba todos os dígitos de um cpf, basta digitar parte dele (1) ou uma máscara do CPF (2), o stript exibirá todas as possibilidades válidas. Isso pode ser util para descobrir o dígito verificador. Ex:

1. python3 cpf.py 123456789 # observe que aqui faltou os dois ultimos dígitos, dessa forma o script exibirá todos os CPF que possuem o trecho "123456789"

2. python3 cpf.py ???456789?? # nesse caso, o programa exiberá todos os CPF que possuem esse padrão
