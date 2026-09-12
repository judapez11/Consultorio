from app import App
from db import init_db


def main():
    init_db()
    App().mainloop()


if __name__ == "__main__":
    main()