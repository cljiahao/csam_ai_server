import pytest
from sqlalchemy.orm import Session

from db.CRUD.csam import create_lot_detail, get_lot_detail, update_lot_detail
from db.models.CDC import CDC_DETAILS
from db.models.CAI import CAI_DETAILS


@pytest.mark.parametrize(
    "mock_model, more_data",
    [
        (CDC_DETAILS, {}),
        (CAI_DETAILS, {"no_of_pred": 50}),
    ],
)
def test_create_and_get_lot_detail(
    db_session: Session,
    sample_lot_details: dict[str, str],
    sample_chips_batch_details: dict[str, int],
    mock_model: type,
    more_data: dict[str, int],
) -> None:
    """Test the creation and retrieval of lot detail."""

    # Prepare test data
    sample_lot_details.update(sample_chips_batch_details)
    sample_lot_details.update(more_data)
    created_detail = create_lot_detail(mock_model, db_session, sample_lot_details)

    # Retrieve the detail to verify creation
    lot_detail = get_lot_detail(
        mock_model, db_session, sample_lot_details["lotNo"], sample_lot_details["plate"]
    )

    # Ensure the created detail matches the retrieved detail
    assert lot_detail is not None
    assert created_detail == lot_detail

    # Ensure the retrieved detail matches the input data
    for key, value in sample_lot_details.items():
        assert getattr(lot_detail, key) == value


@pytest.mark.parametrize(
    "mock_model, more_data",
    [
        (CDC_DETAILS, {}),
        (CAI_DETAILS, {"no_of_pred": 50}),
    ],
)
def test_update_lot_detail(
    db_session: Session,
    sample_lot_details: dict[str, str],
    sample_chips_batch_details: dict[str, int],
    mock_model: type,
    more_data: dict[str, int],
) -> None:
    """Test the update of lot detail."""

    # Prepare test data
    sample_lot_details.update(sample_chips_batch_details)
    sample_lot_details.update(more_data)
    create_lot_detail(mock_model, db_session, sample_lot_details)

    no_of_real = 10
    updated_detail = update_lot_detail(
        mock_model,
        db_session,
        sample_lot_details["lotNo"],
        sample_lot_details["plate"],
        no_of_real,
    )

    assert updated_detail is not None
    assert updated_detail.no_of_real == no_of_real
