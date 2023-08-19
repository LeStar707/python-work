from pymongo import MongoClient
# Кількість пацієнтів по віку

client = MongoClient('mongodb://localhost:27017/')
result = client['Cluster0']['raw_report'].aggregate([
    {
        '$group': {
            '_id': {'patient': '$Пацієнт', 'birthday': '$Дата народження пацієнта', 'date': '$Дата', 'number': '$Номер замовлення'}
        }
    },
    {
        '$project': {
            'patient': '$_id.patient',
            'birthday': '$_id.birthday',
            'date': '$_id.date',
            '_id': 0
        }
    },
    {
        '$group': {
            '_id': '$patient',
            'dates': {'$push': '$date'}
            #'fields': {'$push': '$$ROOT'}
        }
    },
    {
        '$project': {
            '_id': 0,
            'Пацієнт': '$_id',
            #'Дата народження пацієнта': '$fields.birthday',
            'Дати звернення': {
                '$reduce': {
                    'input': '$dates',
                    'initialValue': '',
                    'in': {'$concat': ['$$value', ', ', '$$this']}
                }
            }
        }
    }
])

for document in result:
    print(document)
