from flask import Blueprint


ads_bl = Blueprint('asd', 'ads')


@ads_bl.post('/create')
def create_ads():
    return {'result': 'in develop...'}


@ads_bl.get('/get')
def get_ads():
    return {'result': 'in develop...'}


@ads_bl.put('/edit')
def edit_ads():
    return {'result': 'in develop...'}


@ads_bl.delete('/delete')
def delete_ads():
    return {'result': 'in develop...'}
