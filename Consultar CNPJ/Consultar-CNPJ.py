import requests 
import json
import re 

while True:
    print("\n" + "="*30)
    cnpj = input("Digite seu CNPJ (ou digite 'sair' para encerrar): ") 
    
    # Condição extra para caso você queira fechar o programa manualmente
    if cnpj.lower() == 'sair':
        print("Programa encerrado.")
        break
        
    cnpj = re.sub(r'[.\-/]', '', cnpj) 
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"

    requisicao = requests.get(url)

    if requisicao.status_code == 200: 
        respostas = requisicao.json() 

        # === LISTAS DOS SÓCIOS ===
        lista_socios = []        
        lista_qualificacoes = [] 

        for socio in respostas.get("qsa", []):
            lista_socios.append(socio.get("nome_socio"))                  
            lista_qualificacoes.append(socio.get("qualificacao_socio"))   

        # === LISTAS DO CNAE PRINCIPAL ===
        lista_cnae_principal_codigo = []    
        lista_cnae_principal_descricao = [] 

        codigo_principal = respostas.get("cnae_fiscal")             
        descricao_principal = respostas.get("cnae_fiscal_descricao") 

        if codigo_principal:                                         
            lista_cnae_principal_codigo.append(codigo_principal)
            lista_cnae_principal_descricao.append(descricao_principal)

        # === LISTAS DOS CNAEs SECUNDÁRIOS ===
        lista_cnae_secundario_codigo = []    
        lista_cnae_secundario_descricao = [] 

        for cnae in respostas.get("cnaes_secundarios", []): 
            lista_cnae_secundario_codigo.append(cnae.get("codigo"))    
            lista_cnae_secundario_descricao.append(cnae.get("descricao")) 

        empresa_organizada = { 
            "CNPJ": respostas.get("cnpj"),
            "Razão Social": respostas.get("razao_social"),
            "Nome Fantasia": respostas.get("nome_fantasia"),
            "Situação Cadastral": respostas.get("descricao_situacao_cadastral"),
            "Porte": respostas.get("porte"),                     
            "Estado": respostas.get("uf"),
            "Cidade": respostas.get("municipio"),
            "Bairro": respostas.get("bairro"),
            "Logradouro": respostas.get("logradouro"),
            "Número": respostas.get("numero"),
            "CEP": respostas.get("cep"),
            "Sócios": lista_socios,
            "Qualificações dos Sócios": lista_qualificacoes,     
            "CNAE Principal Código": lista_cnae_principal_codigo,       
            "CNAE Principal Descrição": lista_cnae_principal_descricao, 
            "CNAEs Secundários Códigos": lista_cnae_secundario_codigo,       
            "CNAEs Secundários Descrições": lista_cnae_secundario_descricao, 
            "Simples": respostas.get("opcao_pelo_simples") 
        }

        optante_simples = "OPTANTE"
        if empresa_organizada["Simples"] == None:
            optante_simples = "NÃO OPTANTE"

        print("\n=== DADOS DA EMPRESA ===")
        print("CNPJ:", empresa_organizada["CNPJ"])
        print("Razão Social:", empresa_organizada["Razão Social"])
        print("Nome Fantasia:", empresa_organizada["Nome Fantasia"])
        print("Situação:", empresa_organizada["Situação Cadastral"])
        print("Porte:", empresa_organizada["Porte"])              
        print("Cidade:", empresa_organizada["Cidade"])
        print("Estado:", empresa_organizada["Estado"])
        print("Simples Nacional:", optante_simples)

        print("\n=== LISTA DE SÓCIOS ===")
        for i in range(len(empresa_organizada["Sócios"])):
            print(f"- {empresa_organizada['Sócios'][i]} | {empresa_organizada['Qualificações dos Sócios'][i]}")

        print("\n=== CNAEs ===")
        print("-- CNAE Principal --")
        for i in range(len(empresa_organizada["CNAE Principal Código"])):
            print(f"  Código: {empresa_organizada['CNAE Principal Código'][i]}")
            print(f"  O que é: {empresa_organizada['CNAE Principal Descrição'][i]}")

        print("-- CNAEs Secundários --")
        for i in range(len(empresa_organizada["CNAEs Secundários Códigos"])): 
            print(f"  Código: {empresa_organizada['CNAEs Secundários Códigos'][i]}")
            print(f"  O que é: {empresa_organizada['CNAEs Secundários Descrições'][i]}")
            
        break # <--- Aqui encerramos o loop após o sucesso!

    else:
        print("❌ CNPJ Inválido ou não encontrado! Tente novamente.")