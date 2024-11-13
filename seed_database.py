from app.services.database_service import (
    SessionLocal,
)  # SQLAlchemy session
from app.models.users import Roles, UserRoleEnum  # Models and Enums
import logging
from typing import List, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import os

# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql+psycopg2://water_treatment_user:water_treatment_pass@localhost:5432/water_treatment_db",
# )

DATABASE_URL = "postgresql+psycopg2://water_treatment_user:water_treatment_pass@localhost:5432/water_treatment_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


DEFAULT_ROLES: List[Dict[str, UserRoleEnum]] = [{"name": role} for role in UserRoleEnum]


# def seed_roles() -> None:
#     with SessionLocal() as session:
#         for role_data in DEFAULT_ROLES:
#             role_name: UserRoleEnum = role_data["name"]
#             existing_role: Roles | None = (
#                 session.query(Roles).filter_by(name=role_name).first()
#             )

#             if not existing_role:
#                 logging.info(f"Adding role: {role_name}")
#                 new_role: Roles = Roles(name=role_name)
#                 session.add(new_role)

#         session.commit()
#         logging.info("Seeding completed.")


if __name__ == "__main__":
    try:
        seed_roles()
    except Exception as e:
        logging.error(f"Failed to seed roles: {str(e)}")
