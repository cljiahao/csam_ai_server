import pytest
from sqlalchemy.orm import Session

from db.CRUD.csam import create_lot_detail, get_lot_detail, update_lot_detail


@pytest.mark.parametrize(
    "more_data , with_ai",
    [
        ({}, False),
        ({"no_of_pred": 50}, True),
    ],
)
def test_create_and_get_lot_detail(
    db_session: Session,
    sample_lot_details: dict[str, str],
    sample_chips_batch_details: dict[str, int],
    more_data: dict[str, int],
    with_ai: bool,
) -> None:
    """Test the creation and retrieval of lot detail."""

    # Prepare test data
    sample_lot_details.update(sample_chips_batch_details)
    sample_lot_details.update(more_data)
    sample_lot_details.update({"with_ai": with_ai})
    created_detail = create_lot_detail(db_session, sample_lot_details)

    # Retrieve the detail to verify creation
    lot_detail = get_lot_detail(
        db_session, sample_lot_details["lotNo"], sample_lot_details["plate"], with_ai
    )

    # Ensure the created detail matches the retrieved detail
    assert lot_detail is not None
    assert created_detail == lot_detail

    # Ensure the retrieved detail matches the input data
    for key, value in sample_lot_details.items():
        assert getattr(lot_detail, key) == value


@pytest.mark.parametrize(
    "more_data , with_ai",
    [
        ({}, False),
        ({"no_of_pred": 50}, True),
    ],
)
def test_update_lot_detail(
    db_session: Session,
    sample_lot_details: dict[str, str],
    sample_chips_batch_details: dict[str, int],
    more_data: dict[str, int],
    with_ai: bool,
) -> None:
    """Test the update of lot detail."""

    # Prepare test data
    sample_lot_details.update(sample_chips_batch_details)
    sample_lot_details.update(more_data)
    sample_lot_details.update({"with_ai": with_ai})
    create_lot_detail(db_session, sample_lot_details)

    no_of_real = 10
    updated_detail = update_lot_detail(
        db_session,
        sample_lot_details["lotNo"],
        sample_lot_details["plate"],
        no_of_real,
        with_ai,
    )

    assert updated_detail is not None
    assert updated_detail.no_of_real == no_of_real
