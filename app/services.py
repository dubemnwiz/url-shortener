from app import db
from app.models import Url
from app.utils import unique_short_code


# helpers

def _code_taken(code: str) -> bool:
    """Return True if `code` is already used by an existing Url row."""
    return Url.query.filter_by(short_code=code).first() is not None

# crud operations

def create_url(original_url: str) -> Url:
    """Persist a new Url record with a unique short code and return it.

    Raises ValueError if `original_url` is empty or blank.
    """
    if not original_url or not original_url.strip():
        raise ValueError("Original URL is required")
    
    code = unique_short_code(_code_taken)
    url = Url(original_url=original_url, short_code=code)
    db.session.add(url)
    db.session.commit()
    return url


def get_url(short_code: str) -> Url:
    """Fetch the Url record for `short_code` and increment its click counter.

    Raises LookupError if no matching record exists.
    """
    url = Url.query.filter_by(short_code=short_code).first()
    if not url:
        raise LookupError(f"No URL found for short code: {short_code}")
    url.clicks += 1
    db.session.commit()
    return url

def update_url(short_code: str, new_original_url: str) -> Url:
    """Replace the original URL on an existing record and return it.

    Raises LookupError if `short_code` does not exist.
    Raises ValueError if `new_original_url` is empty or blank.
    """
    if not new_original_url or not new_original_url.strip():
        raise ValueError("Original URL is required")
    
    url = Url.query.filter_by(short_code=short_code).first()
    if not url:
        raise LookupError(f"No URL found for short code: {short_code}")

    url.original_url = new_original_url
    db.session.commit()
    return url

def delete_url(short_code: str) -> None:
    """Delete the Url record for `short_code`.

    Raises LookupError if no matching record exists.
    """
    url = Url.query.filter_by(short_code=short_code).first()
    if not url:
        raise LookupError(f"No URL found for short code: {short_code}")

    db.session.delete(url)
    db.session.commit()
    


def get_stats(short_code: str) -> Url:
    """Return the Url record for `short_code` without touching the click counter.

    Raises LookupError if no matching record exists.
    """
    url = Url.query.filter_by(short_code=short_code).first()
    if not url:
        raise LookupError(f"No URL found for short code: {short_code}")

    return url

