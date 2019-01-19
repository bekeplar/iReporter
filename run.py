from api import create_app

app = create_app("Development")

"""Api entry point for my application"""

if __name__ == "__main__":
    app.run()