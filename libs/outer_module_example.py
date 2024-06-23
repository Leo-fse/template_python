def hello():
    print("Hello, I'm outer module!")
    raise Exception("Error in outer module")


if __name__ == "__main__":
    hello()
