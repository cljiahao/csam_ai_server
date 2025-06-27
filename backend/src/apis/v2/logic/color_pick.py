from sqlalchemy.orm import Session
from uuid import uuid4

from apis.v2.schemas.color_pick import DotColors
from constants.colors import BGRColors
from constants.tensorflow_model import DatasetModes
from core.logging import logger
from db.services.dot_colors import DotColorsService


def get_dot_colors_by_item(item: str, db: Session) -> list[DotColors]:
    """Retrieve dot colors for a given item from the database."""
    dot_colors_service = DotColorsService(db)
    dot_colors_data = dot_colors_service.read_all_dot_colors(item)

    if dot_colors_data:
        return [
            DotColors(
                uuid=dot_colors.uuid,
                label=dot_colors.defect_label,
                color=dot_colors.hex_color,
            )
            for dot_colors in dot_colors_data
        ]
    return [
        DotColors(uuid=uuid4(), label=DatasetModes.NG, color=BGRColors.YELLOW.value)
    ]


# TODO: build db dict inside the service instead
def save_dot_colors_by_item(
    item: str, dot_colors: list[DotColors], db: Session
) -> None:
    """Synchronize dot colors for an item: create, update, or delete as needed."""

    incoming_uuids = {dot_color.uuid: dot_color for dot_color in dot_colors}

    dot_colors_service = DotColorsService(db)
    existing_dot_colors = dot_colors_service.read_all_dot_colors(item)
    existing_uuids = {dot_color.uuid: dot_color for dot_color in existing_dot_colors}

    to_create = [
        {
            "uuid": uuid,
            "defect_label": incoming_uuids[uuid].label,
            "hex_color": incoming_uuids[uuid].color,
            "item": item,
        }
        for uuid in incoming_uuids.keys() - existing_uuids.keys()
    ]

    to_update = []
    for uuid, new_data in incoming_uuids.items():
        if uuid in existing_uuids:
            existing_data = existing_uuids[uuid]

            # Check if any value has changed before updating
            update_data = {}
            if existing_data.defect_label != new_data.label:
                update_data["defect_label"] = new_data.label
            if existing_data.hex_color != new_data.color:
                update_data["hex_color"] = new_data.color

            if update_data:  # Only add if there's a change
                to_update.append(
                    {
                        "filter_conditions": {"uuid": uuid},
                        "update_data": update_data,
                    }
                )

    to_delete = [k for k in existing_uuids.keys() - incoming_uuids.keys()]

    create_res = dot_colors_service.bulk_create_dot_colors(to_create)
    logger.info(f"Created {len(create_res)} new dot colors.")

    update_res = dot_colors_service.bulk_update_dot_colors(to_update)
    logger.info(f"Updated {update_res} existing dot colors.")

    delete_res = dot_colors_service.bulk_delete_dot_colors(to_delete)
    logger.info(f"Deleted {delete_res} existing dot colors.")
