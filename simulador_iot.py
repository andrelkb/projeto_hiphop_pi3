import requests

# A URL oficial da sua API na nuvem (a porta invisível que acabamos de criar)
URL_NUVEM = "https://projeto-hiphop-pi3.onrender.com/api/iot/presenca/"

def simular_leitura_cartao():
    print("\n" + "="*40)
    print("   SIMULADOR DE CATRACA / LEITOR IoT   ")
    print("="*40)
    
    # Simula a ação física de passar um cartão ou tag
    identificador = input("\n[BIP!] Passe o cartão (Digite um ID ou CPF de teste): ")

    # Monta o pacote de dados exatamente como um chip ESP32 faria
    dados_para_enviar = {
        "identificador": identificador
    }

    print("\nEnviando dados via Wi-Fi para a nuvem...")

    try:
        # Faz o disparo do POST para o servidor Render
        resposta = requests.post(URL_NUVEM, json=dados_para_enviar)

        # Analisa a resposta que voltou do servidor
        if resposta.status_code == 200:
            print("\n✅ SUCESSO! O servidor da nuvem respondeu:")
            print("Mensagem:", resposta.json())
        else:
            print(f"\n❌ ERRO! O servidor rejeitou. Código HTTP: {resposta.status_code}")
            print("Detalhes:", resposta.text)

    except Exception as erro:
        print(f"\n⚠️ Falha na conexão com a internet: {erro}")
        
    print("="*40 + "\n")

if __name__ == "__main__":
    simular_leitura_cartao()