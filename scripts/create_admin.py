import argparse

from sqlalchemy.exc import IntegrityError

import app.models  # noqa: F401
from app.core.security import hash_password
from app.database import SessionLocal
from app.models.user import User, UserRole


def cmd_create_admin(email: str, password: str) -> int:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()

        if user is None:
            user = User(
                email=email,
                hashed_password=hash_password(password),
                role=UserRole.ADMIN,
            )
            db.add(user)
            try:
                db.commit()
            except IntegrityError as e:
                db.rollback()
                user = db.query(User).filter(User.email == email).first()
                if user is None:
                    raise e
                if user.role != UserRole.ADMIN:
                    user.role = UserRole.ADMIN
                    db.commit()

            print(f"Created admin user: {email}")
            return 0

        if user.role == UserRole.ADMIN:
            print(f"User already admin: {email}")
            return 0

        user.role = UserRole.ADMIN
        db.commit()
        print(f"Promoted user to admin: {email}")
        return 0

    finally:
        db.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = subparsers.add_parser("create-admin", help="Create or promote an admin user")
    p.add_argument("--email", required=True)
    p.add_argument("--password", required=True)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "create-admin":
        return cmd_create_admin(email=args.email, password=args.password)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
