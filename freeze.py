from app.generator import app, freezer
import sys

if __name__ == '__main__':
    try:
        freezer.freeze()
    except Exception as e:
        print(f"Error durante el proceso de congelamiento: {str(e)}", file=sys.stderr)
        sys.exit(1)
    print("Sitio estático generado exitosamente en el directorio 'build'")