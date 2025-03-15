from sqlalchemy.orm import Session

from apis.v2.schemas.colors import ItemDotColors, DotColors
from core.logging import logger
from db.services.dot_colors import DotColorsService


def get_dot_colors_by_item(item: str, db: Session) -> ItemDotColors:
    """Retrieve dot colors for a given item from the database."""
    dot_colors_service = DotColorsService(db)
    dot_colors_data = dot_colors_service.read_all_dot_colors(item)

    dot_color_list = [
        DotColors(
            uuid=dot_colors.uuid,
            defect_label=dot_colors.defect_label,
            hex_color=dot_colors.hex_color,
        )
        for dot_colors in dot_colors_data
    ]

    return ItemDotColors(item=item, dot_colors_list=dot_color_list)


def save_dot_colors_by_item(item_dot_colors: ItemDotColors, db: Session) -> None:
    """Synchronize dot colors for an item: create, update, or delete as needed."""

    dot_colors_service = DotColorsService(db)

    incoming_uuids = {
        dot_colors.uuid: dot_colors for dot_colors in item_dot_colors.dot_colors_list
    }

    existing_dot_colors = dot_colors_service.read_all_dot_colors(item_dot_colors.item)
    existing_uuids = {dot_colors.uuid: dot_colors for dot_colors in existing_dot_colors}

    to_create = [
        {
            **incoming_uuids[uuid].model_dump(exclude_none=True),
            "item": item_dot_colors.item,
        }
        for uuid in incoming_uuids.keys() - existing_uuids.keys()
    ]

    to_update = []
    for uuid, new_data in incoming_uuids.items():
        if uuid in existing_uuids:
            existing_data = existing_uuids[uuid]

            # Check if any value has changed before updating
            update_data = {}
            if existing_data.defect_label != new_data.defect_label:
                update_data["defect_label"] = new_data.defect_label
            if existing_data.hex_color != new_data.hex_color:
                update_data["hex_color"] = new_data.hex_color

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
