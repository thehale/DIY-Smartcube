class Logger:
    def __init__(self, file_name: str):
        self.file_name = f"./logs/{file_name}_log.txt"
        self.file = open(self.file_name, "a")

    def __log(self, msg):
        print(msg)
        self.file.write(f"{msg}\n")

    def info(self, msg):
        self.__log(f"[INFO] {msg}")

    def warn(self, msg):
        self.__log(f"[WARN] {msg}")

    def error(self, msg):
        self.__log(f"[ERROR] {msg}")

    def debug(self, msg):
        self.__log(f"[DEBUG] {msg}")

    def save_to_disk(self):
        self.file.flush()

    def __del__(self):
        self.file.close()
