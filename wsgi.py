from app import create_app

wsgi = create_app()

if __name__ == "__main__":
    wsgi.run(port=5000, debug=True)
