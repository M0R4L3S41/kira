import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
from tqdm import tqdm
import concurrent.futures
import time
import os
import shutil

def limpiar_pantalla():
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
def mostrar_marca_agua():
    marca_agua = """
  _  _______ _____            
 | |/ /_   _|  __ \     /\    
 | ' /  | | | |__) |   /  \   
 |  <   | | |  _  /   / /\ \  
 | . \ _| |_| | \ \  / ____ \ 
 |_|\_\_____|_|  \_\/_/    \_\
    """
    terminal_width = shutil.get_terminal_size().columns
    
    marca_agua_centrada = "\n".join(line.center(terminal_width) for line in marca_agua.split("\n"))
    
    print(marca_agua_centrada)
    print("Bienvenido al buscador de URLs de KIRA".center(terminal_width))
    print("=" * terminal_width)


class URLFinder:
    def __init__(self, base_url, max_depth=2, max_workers=5):
        self.base_url = base_url
        self.max_depth = max_depth
        self.max_workers = max_workers
        self.urls_encontradas = set()
        self.urls_fallidas = set()
        self.session = requests.Session()
        
        parsed_url = urlparse(base_url)
        self.domain = parsed_url.netloc

        self.rutas_adicionales = [
            '/admin', '/admin/login', '/administrator', '/login',
            '/dashboard', '/backend', '/wp-admin', '/manager'
        ]

    def es_url_valida(self, url):
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc == self.domain and
                parsed.scheme in ['http', 'https'] and
                '#' not in url and
                'javascript' not in url.lower()
            )
        except Exception:
            return False

    def obtener_urls_pagina(self, url):
        urls = set()
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/91.0.4472.124 Safari/537.36'
            }
            response = self.session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for tag in soup.find_all(['a', 'link', 'img', 'script', 'iframe']):
                link = tag.get('href') or tag.get('src')
                if link:
                    absolute_url = urljoin(url, link)
                    if self.es_url_valida(absolute_url):
                        urls.add(absolute_url)
            
        except Exception as e:
            print(f"⚠️ Error al procesar {url}: {str(e)}")
            self.urls_fallidas.add(url)
            
        return urls

    def buscar_pagina_admin(self, rutas):
        admin_urls = set()
        for ruta in rutas:
            url = urljoin(self.base_url, ruta)
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    admin_urls.add(url)
                    print(f"Posible página de administración encontrada: {url}")
            except:
                pass
        return admin_urls

    def crawl(self):
        urls_pendientes = {self.base_url}
        profundidad = 0
        
        print(f"🔍 Iniciando búsqueda de URLs en {self.base_url}")
        print(f"📊 Profundidad máxima: {self.max_depth}")
        
        while urls_pendientes and profundidad < self.max_depth:
            nuevas_urls = set()
            
            with tqdm(total=len(urls_pendientes), desc=f"Nivel {profundidad + 1}/{self.max_depth}", unit="url") as pbar:
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    future_to_url = {executor.submit(self.obtener_urls_pagina, url): url for url in urls_pendientes}
                    
                    for future in concurrent.futures.as_completed(future_to_url):
                        urls = future.result()
                        nuevas_urls.update(urls)
                        pbar.update(1)
            
            self.urls_encontradas.update(urls_pendientes)
            urls_pendientes = nuevas_urls - self.urls_encontradas
            profundidad += 1
            
            print(f" URLs encontradas hasta ahora: {len(self.urls_encontradas)}")
            
        return sorted(list(self.urls_encontradas))

    def guardar_resultados(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for url in sorted(self.urls_encontradas):
                f.write(f"{url}\n")
        
        print(f" Resultados guardados en {filename}")

def main():
    limpiar_pantalla()
    mostrar_marca_agua()
    parser = argparse.ArgumentParser(description='Encuentra todas las URLs en un sitio web')
    parser.add_argument('url', help='URL del sitio web a analizar')
    parser.add_argument('--depth', type=int, default=2, help='Profundidad máxima de búsqueda')
    parser.add_argument('--workers', type=int, default=5, help='Número de workers paralelos')
    
    args = parser.parse_args()
    
    try:
        tiempo_inicio = time.time()
        finder = URLFinder(args.url, args.depth, args.workers)

        
        buscar_admin = input("¿Deseas intentar encontrar la página del administrador? (s/n): ").strip().lower()
        if buscar_admin.startswith('s'):
            usar_diccionario = input("¿Tienes un diccionario personalizado? (s/n): ").strip().lower()
            if usar_diccionario.startswith('s'):
                ruta_diccionario = input("Ingresa la ruta del archivo de diccionario: ").strip()
                if os.path.exists(ruta_diccionario):
                    with open(ruta_diccionario, 'r') as f:
                        rutas_admin = [line.strip() for line in f if line.strip()]
                    print(f"Diccionario cargado exitosamente: {len(rutas_admin)} rutas")
                else:
                    print("El archivo no existe. Usando rutas predeterminadas.")
                    rutas_admin = finder.rutas_adicionales
            else:
                print("Usando rutas predeterminadas.")
                rutas_admin = finder.rutas_adicionales
            
            admin_urls = finder.buscar_pagina_admin(rutas_admin)
            if admin_urls:
                print(f"Se encontraron {len(admin_urls)} posibles páginas de administración.")
                finder.urls_encontradas.update(admin_urls)
            else:
                print("No se encontraron páginas de administración.")

        urls = finder.crawl()
        
        
        base_nombre = urlparse(args.url).netloc.replace("www.", "")
        contador = 1
        while True:
            nombre_archivo = f"{base_nombre}_{contador}.txt"
            if not os.path.exists(nombre_archivo):
                break
            contador += 1
        
        finder.guardar_resultados(nombre_archivo)
        
        tiempo_total = time.time() - tiempo_inicio
        print(f" Búsqueda completada en {tiempo_total:.2f} segundos")
        print(f" Total URLs encontradas: {len(urls)}")
        if finder.urls_fallidas:
            print(f"⚠️ URLs con error: {len(finder.urls_fallidas)}")
            
    except Exception as e:
        print(f" Error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
    
