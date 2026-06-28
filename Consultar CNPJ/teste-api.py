# Aqui é apenas para mostrar os dados que mostra quando você puxa a API e o CNPJ

import requests

resposta = requests.get("https://brasilapi.com.br/api/cnpj/v1/{cnpj}").json()

print(resposta)