import os


class FileUtil(object):
    @staticmethod
    def createFileIfNotExists(fileName):
        if not os.path.exists(fileName):
            with open(fileName, 'w'):
                pass

    @staticmethod
    def readFile(fileName, ):
        with open(fileName, mode='rt', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def writeFile(fileName, content):
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(content)
