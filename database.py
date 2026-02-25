from tinydb import TinyDB , Query

class Database:
    def __init__(self , dbName: str) -> None:
        self.dbName = dbName
        self.db = TinyDB(self.dbName)

    def saveScore(self , wpm: float , correct: int) -> None:
        
