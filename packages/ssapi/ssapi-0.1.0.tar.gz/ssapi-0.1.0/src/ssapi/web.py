from bottle import get, post, request, response

from ssapi.entities import Sale
from ssapi.env import get_env_database
from ssapi.web_decorators import accepts_json, returns_json


@get("/shops")
@returns_json
def get_shops():
    return list(get_env_database().get_shops())


@get("/sales")
@returns_json
def get_sales():
    return [
        dict(sale.as_map()) for sale in get_env_database().get_sales()
    ]


@post("/sales")
@accepts_json
@returns_json
def post_sales():
    try:
        new_sale = Sale(**request.adapted_json)
    except TypeError as exc:
        response.status = 400
        outcome = (
            f"creation failed: "
            f"invalid parameters for type 'sale': "
            f"{request.json} {exc}"
        )
    else:
        db = get_env_database()
        count = db.add_sales(new_sale)
        outcome = f"creation ({count}) succeeded in database at: {db.name}"

    return {"outcome": outcome}


@post("/drop")
@accepts_json
@returns_json
def drop():
    # FIXME: add security
    db = get_env_database()
    db.drop()
    db.open()
    return {"outcome": f"Database dropped at: {db.name}"}
