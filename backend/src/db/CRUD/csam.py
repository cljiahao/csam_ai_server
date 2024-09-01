from datetime import datetime as dt
from sqlalchemy import select, update
from sqlalchemy.orm.session import Session

from db.models.CDC import CDC_DETAILS
from db.models.CAI import CAI_DETAILS
from core.exceptions import DatabaseError
from core.logging import logger


def get_lot_plate_detail(
    model: CAI_DETAILS | CDC_DETAILS, db: Session, lot_no: str, plate_no: str
):
    """Fetches the detail for a given lot and plate number."""
    try:
        statement = (
            select(model)
            .where(model.lotNo == lot_no, model.plate == plate_no)
            .order_by(model.date_created.desc())
        )
        lot_plate_detail = db.execute(statement).scalars().first()

    except Exception as e:
        std_out = f"Error fetching details for {lot_no} : {plate_no} from database."
        logger.error(std_out, exc_info=True)
        db.rollback()
        raise DatabaseError(std_out) from e

    return lot_plate_detail


def create_detail(
    model: CAI_DETAILS | CDC_DETAILS, db: Session, detail_input: dict
) -> None:
    """Creates a new detail entry in the database."""
    try:
        detail_data = model(**detail_input)
        db.add(detail_data)
        db.commit()
    except Exception as e:
        std_out = f"Error creating details for {detail_data.lotNo} : {detail_data.plate} in database."
        logger.error(std_out, exc_info=True)
        db.rollback()
        raise DatabaseError(std_out) from e


def update_lot_plate_detail(
    model: CAI_DETAILS | CDC_DETAILS,
    db: Session,
    lot_no: str,
    plate_no: str,
    no_of_real: dict,
) -> None:
    """Updates an existing detail entry in the database."""
    try:
        statement = (
            update(model)
            .where(model.lotNo == lot_no, model.plate == plate_no)
            .values(no_of_real)
        )
        db.execute(statement)
        db.commit()
    except Exception as e:
        std_out = f"Error updating details for {lot_no} : {plate_no} in database."
        logger.error(std_out, exc_info=True)
        db.rollback()
        raise DatabaseError(std_out) from e
