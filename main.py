import socket
import configparser

# # Dados da etiqueta
# material = "PS Bege 3mm"
# fornecedor = "Fornecedor: Cicoplast"
# id_material = "id: 5895"

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, 'utf-8')
    return config

def consultar_horas_turno(self,TOKEN, LOGIN, SENHA, NUMERO_CNC, url):
        parametros = {
            'TOKEN': TOKEN,
            'LOGIN': LOGIN,
            'SENHA': SENHA,

        }

        try:
            resposta = requests.get(url, params=parametros)
            if resposta.status_code == 200:        
                return resposta.text
            else:            
                resposta.raise_for_status()
        except requests.exceptions.RequestException as e:        
            print("Erro durante a solicitação:", e)

def main():
    try:
        
        config = read_config('config.conf')

        # Endereço IP da impressora Zebra
        printer_ip = config['CONFIG']['ipimpressora']
        printer_port = config['CONFIG']['porta']
        url = config['API']['urlimpressao']
        # Comando ZPL para criar a etiqueta
        zpl = f"""
        ^XA
        ^FO50,50^A0N,50,50^FD{material}^FS
        ^FO50,120^A0N,50,50^FD{fornecedor}^FS
        ^FO50,190^A0N,50,50^FD{id_material}^FS
        ^XZ
        """

        # Enviando o comando ZPL para a impressora
        def send_zpl_to_printer(zpl, ip, port):
            try:
                # Cria uma conexão com a impressora
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((ip, port))
                    s.sendall(zpl.encode())
                    print("Etiqueta enviada para impressão.")
            except Exception as e:
                print(f"Erro ao enviar a etiqueta: {e}")

        # Enviar a etiqueta para a impressora
        send_zpl_to_printer(zpl, printer_ip, printer_port)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()