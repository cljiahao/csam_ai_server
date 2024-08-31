from src.db.CRUD.base import get_lot_plate_detail

from src.db.models.CDC import CDC_DETAILS

# from src.db.models.CAI import CAI_DETAILS


def test_lot_plate_detail(db_session):
    detail_input = {"lotNo": 1234567890, "plate": "temp", "item": "test123"}
    # detail_data = CDC_DETAILS(detail_input)
    # lot_plate_detail = get_lot_plate_detail(CDC_DETAILS, db_session, 1234567890, "temp")
    # print(detail_data)
    # print(lot_plate_detail)


# def test_create_detail(db_session):
