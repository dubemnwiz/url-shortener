from flask import Blueprint, request, jsonify, redirect

from app.services import (
    create_url,
    get_url,
    update_url,
    delete_url,
    get_stats,
)

urls_bp = Blueprint("urls", __name__)

# ---------------------------------------------------------------------------
# POST /shorten
# Accepts JSON {"url": "..."}, creates a new short URL.
# Returns 201 with the new record, 400 on missing/blank input.
# ---------------------------------------------------------------------------
@urls_bp.post("/shorten")
def shorten():
    data = request.get_json()
    original_url = data.get("url")
    if not original_url:
        return jsonify({"error": "URL is required"}), 400
    try:
        url = create_url(original_url)
        return jsonify(url.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ---------------------------------------------------------------------------
# GET /shorten/<code>
# Fetches the record for `code` and increments the click counter.
# Returns 200 with the record, 404 if the code does not exist.
# ---------------------------------------------------------------------------
@urls_bp.get("/shorten/<string:code>")
def get_short_url(code: str):
    try:
        url = get_url(code)
        return jsonify(url.to_dict()), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


# ---------------------------------------------------------------------------
# PUT /shorten/<code>
# Accepts JSON {"url": "..."}, updates the original URL on the record.
# Returns 200 with the updated record, 400 on bad input, 404 if not found.
# ---------------------------------------------------------------------------
@urls_bp.put("/shorten/<string:code>")
def update_short_url(code: str):
    data = request.get_json()
    new_original_url = data.get("url")
    if not new_original_url:
        return jsonify({"error": "URL is required"}), 400
    try:
        url = update_url(code, new_original_url)
        return jsonify(url.to_dict()), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


# ---------------------------------------------------------------------------
# DELETE /shorten/<code>
# Deletes the record for `code`.
# Returns 204 No Content on success, 404 if the code does not exist.
# ---------------------------------------------------------------------------
@urls_bp.delete("/shorten/<string:code>")
def delete_short_url(code: str):
    try:
        delete_url(code)
        return "", 204
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


# ---------------------------------------------------------------------------
# GET /shorten/<code>/stats
# Returns the record + click count without incrementing the counter.
# Returns 200 with the record, 404 if the code does not exist.
# ---------------------------------------------------------------------------
@urls_bp.get("/shorten/<string:code>/stats")
def short_url_stats(code: str):
    try:
        url = get_stats(code)
        return jsonify(url.to_dict()), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


# ---------------------------------------------------------------------------
# GET /<code>
# Browser-facing redirect
# Returns 404 if the code does not exist.
# ---------------------------------------------------------------------------
@urls_bp.get("/<string:code>")
def redirect_to_url(code: str):
    try:
        url = get_url(code)
        return redirect(url.original_url)
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
