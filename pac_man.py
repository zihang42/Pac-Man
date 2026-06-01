from src.parser import Parser


def main():
    print("Hello from pac-man!")
    parser = Parser("config.json")
    data = parser.load()
    print(data)


if __name__ == "__main__":
    main()
