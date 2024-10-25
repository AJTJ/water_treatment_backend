from app.services.database_service import SessionLocal  # SQLAlchemy session
from app.models.users import Roles, UserRoleEnum  # Models and Enums
import logging
from typing import List, Dict

DEFAULT_ROLES: List[Dict[str, UserRoleEnum]] = [{"name": role} for role in UserRoleEnum]


def seed_roles() -> None:
    with SessionLocal() as session:
        for role_data in DEFAULT_ROLES:
            role_name: UserRoleEnum = role_data["name"]
            role: Roles | None = session.query(Roles).filter_by(name=role_name).first()

            if not role:
                logging.info(f"Adding role: {role_name}")
                new_role: Roles = Roles(name=role_name)
                session.add(new_role)

        session.commit()
        logging.info("Seeding completed.")


if __name__ == "__main__":
    try:
        seed_roles()
    except Exception as e:
        logging.error(f"Failed to seed roles: {str(e)}")
