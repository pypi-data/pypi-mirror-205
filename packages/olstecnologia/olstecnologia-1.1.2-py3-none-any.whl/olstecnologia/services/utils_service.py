import os, time, random as rd, requests
from tqdm import tqdm

def colors(color, value=""):

        if color == "red":
            color = "\033[1;31m"

        if color == "blue":
            color = "\033[1;34m"
        
        if color == "cyan":
            color = "\033[1;36m"
        
        if color == "green":
            color = "\033[0;32m"

        if color == "reset":
            color = "\033[0;0m"
        
        if color == "gold":
            color = "\033[33m"
        
        if color == "reverse":
            color = "\033[;7m"

        if value:
            return color + value + "\033[0;0m"
        else:
            return color
        
def abort_system(clean=True):
    x = rd.randint(0,6)

    for i in range(6):
        if i == 0:
            print(colors("red", "saindo"), end="", flush=True)
        print(colors("red", "."), end="", flush=True)
        if i == x:
            if clean:
                os.system('cls' if os.name == 'nt' else 'clear')
            os.abort()

        time.sleep(0.5)

def get_ibge(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        ibge_code = data['ibge']

        return ibge_code
    
    else:
        return None
    
def get_ibges(ceps):
    ibge_codes = []

    for cep in tqdm(ceps, desc =f"Pegando o cod-ibge => "):
        if not cep:
            ibge_codes.append(None)
        
        else:
            try:
                # url = f'https://viacep.com.br/ws/{cep}/json/'
                url = f'https://api.postmon.com.br/v1/cep/{cep}'
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    ibge_code = data['cidade_info']['codigo_ibge']
                    ibge_codes.append(ibge_code)
                else:
                    ibge_codes.append(None)
            except:
                ibge_codes.append(None)

    return ibge_codes