from pymongo import MongoClient
# Зростання бази даних помісячно по кількості наданих послуг

client = MongoClient('mongodb://localhost:27017/')
result = client['Cluster0']['raw_report'].aggregate([
        {
            '$group': {
                '_id': '$file',
                'count': {
                    '$sum': 1
                }
            }
        }, {
        '$sort': {
            '_id': 1
        }
    }
    ])

for document in result:
    print(document)