import subprocess

def iniciar_sara():
    try:
        print("Iniciando SARA...")
        subprocess.run(["python", "inicio.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar SARA: {e}")

if __name__ == "__main__":
    iniciar_sara()