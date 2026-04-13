from datetime import datetime, timezone

from app import db


class Url(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    clicks = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "clicks": self.clicks,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Url {self.short_code!r} -> {self.original_url!r}>"
