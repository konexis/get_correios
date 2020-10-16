import concurrent.futures
import requests
import threading
from bs4 import BeautifulSoup


thread_local = threading.local()


def get_correios(pedidos):
    msgs = []
    try:
        page = requests.post('https://www2.correios.com.br/sistemas/rastreamento/resultado.cfm',
                             data={'objetos': pedidos}, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'html.parser')
        status = soup.find(id='UltimoEvento').strong.text
        data = soup.find(id='UltimoEvento').text.split()[-1]
        msgs.append(f'Pedido nº: {pedidos}, Status: {status} - Data: {data}')
    except Exception as e:
        msgs.append(f'Erro! Código: {pedidos} não foi encontrado! Erro:{e}')
    print(msgs)


def download_pedidos(pedidos):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(get_correios, pedidos)


if __name__ == "__main__":
    # lista com pedidos
    pedidos = ['XXXXXXXXXXXXX', 'XXXXXXXXXXXXX', 'XXXXXXXXXXXXX']
    download_pedidos(pedidos)
