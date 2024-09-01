import pytest
from sqlalchemy.orm import Session

from db.CRUD.csam import get_lot_plate_detail
from db.models.CDC import CDC_DETAILS
from db.models.CAI import CAI_DETAILS


@pytest.mark.parametrize(
    "model, more_data",
    [
        (CDC_DETAILS, {}),
        (CAI_DETAILS, {"no_of_pred": 50}),
    ],
)
def test_lot_plate_detail(db_session: Session, detail_input, model, more_data):
    detail_input.update(more_data)
    detail_data = model(**detail_input)
    db_session.add(detail_data)
    db_session.commit()
    db_session.refresh(detail_data)

    lot_plate_detail = get_lot_plate_detail(model, db_session, 1234567890, "temp")

    assert detail_data == lot_plate_detail
