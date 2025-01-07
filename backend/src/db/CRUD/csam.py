from sqlalchemy import select
from sqlalchemy.orm.session import Session

from core.exceptions import DatabaseError
from core.logging import logger
from db.models.csam import CSAM_DETAILS


def get_lot_detail(
    db: Session, lot_no: str, plate_no: str, with_ai: bool
) -> CSAM_DETAILS | None:
    """Fetches the detail for a given lot and plate number."""
    try:
        statement = (
            select(CSAM_DETAILS)
            .where(
                CSAM_DETAILS.lotNo == lot_no,
                CSAM_DETAILS.plate == plate_no,
                CSAM_DETAILS.with_ai == with_ai,
            )
            .order_by(CSAM_DETAILS.date_created.desc())
        )
        lot_detail = db.execute(statement).scalars().first()
        return lot_detail
    except Exception as e:
        std_out = f"Error fetching details for {lot_no} : {plate_no} from the database."
        logger.error(std_out, exc_info=True)
        raise DatabaseError(std_out) from e


def create_lot_detail(db: Session, detail_input: dict) -> CSAM_DETAILS | None:
    """Creates a new detail entry in the database."""
    try:
        detail_data = CSAM_DETAILS(**detail_input)
        db.add(detail_data)
        db.commit()
        db.refresh(detail_data)  # Refresh to ensure the object is up-to-date
        return detail_data
    except Exception as e:
        std_out = f"Error creating details for {detail_data.lotNo} : {detail_data.plate} in the database."
        logger.error(std_out, exc_info=True)
        db.rollback()
        raise DatabaseError(std_out) from e


def update_lot_detail(
    db: Session, lot_no: str, plate_no: str, no_of_real: int, with_ai: bool
) -> CSAM_DETAILS | None:
    """Updates an existing detail entry in the database."""
    try:
        statement = select(CSAM_DETAILS).where(
            CSAM_DETAILS.lotNo == lot_no,
            CSAM_DETAILS.plate == plate_no,
            CSAM_DETAILS.with_ai == with_ai,
        )
        lot_detail = db.execute(statement).scalar_one()
        lot_detail.no_of_real = no_of_real
        db.commit()
        return lot_detail
    except Exception as e:
        std_out = f"Error updating details for {lot_no} : {plate_no} in the database."
        logger.error(std_out, exc_info=True)
        db.rollback()
        raise DatabaseError(std_out) from e
