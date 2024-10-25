from app.models.plants import Plants
from app.services.database_service import SessionLocal  # SQLAlchemy session
from app.models.users import Roles, UserRoleEnum  # Models and Enums
import logging

DEFAULT_ROLES: list[dict[str, UserRoleEnum]] = [{"name": role} for role in UserRoleEnum]


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


def seed_plant() -> None:
    with SessionLocal() as session:
        plant_name = "Plant 1"
        new_plant: Plants = Plants(name=plant_name)
        session.add(new_plant)
        session.commit()
        logging.info("Seeding completed.")


def seed_database() -> None:
    seed_roles()
    seed_plant()


if __name__ == "__main__":
    try:
        seed_roles()
    except Exception as e:
        logging.error(f"Failed to seed roles: {str(e)}")
