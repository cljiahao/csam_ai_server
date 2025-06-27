from sqlalchemy.orm import Session

from apis.v2.schemas.stats_data import CountResult
from db.services.lot_details import LotDetailsService


def get_lot_details_count(lot_details_id: str, is_ai: bool, db: Session) -> CountResult:
    lot_details_service = LotDetailsService(db)
    lot_detail = lot_details_service.read_lot_details_by_id(lot_details_id)
    return CountResult(
        result=lot_detail.no_of_pred if is_ai else lot_detail.no_of_chips
    )
