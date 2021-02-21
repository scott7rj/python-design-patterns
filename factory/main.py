import json
import xml.etree.ElementTree as etree

class NoneExistentExtractor:
    def __init__(self, filepath):
        self.data = None
    @property
    def parsedData(self):
        return self.data

class JSONDataExtractor:
    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r', encoding='utf-8') as f:
            self.data = json.load(f)

    @property
    def parsedData(self):
        return self.data

class XMLDataExtractor:
    def __init__(self, filepath):
        self.tree = etree.parse(filepath)
        
    @property
    def parsedData(self):
        return self.tree

class DataExtractorFactory:

    def __init__(self, filepath):
        self.filepath = filepath

    def getExtractor(self):
        if self.filepath.endswith('json'):
            extractor = JSONDataExtractor
        elif self.filepath.endswith('xml'):
            extractor = XMLDataExtractor
        else:
            extractor = NoneExistentExtractor
        return extractor(self.filepath)


def main():
    sqliteExtractor = DataExtractorFactory('person.sq3').getExtractor()
    sqliteData = sqliteExtractor.parsedData
    print(sqliteData)

    jsonExtractor = DataExtractorFactory('movies.json').getExtractor()
    jsonData = jsonExtractor.parsedData
    print(f'Found: {len(jsonData)} movies')
    for movie in jsonData:
        print(f"Title: {movie['title']}")
        year = movie['year']
        if year:
            print(f"Year: {year}")
        director = movie['director']
        if director:
            print(f"Director: {director}")
        genre = movie['genre']
        if genre:
            print(f"Genre: {genre}")
        print()

    xmlExtractor = DataExtractorFactory('persons.xml').getExtractor()
    xmlData = xmlExtractor.parsedData
    liars = xmlData.findall(f".//person[lastName='Liar']")
    print(f'found: {len(liars)} persons')
    for liar in liars:
        firstname = liar.find('firstName').text
        print(f'first name: {firstname}')
        lastname = liar.find('lastName').text
        print(f'last name: {lastname}')
        [print(f"phone number ({p.attrib['type']}):", p.text) 
              for p in liar.find('phoneNumbers')]
        print()
    print()


if __name__ == '__main__':
    main()