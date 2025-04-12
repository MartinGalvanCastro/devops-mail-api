from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def setup_custom_openapi(app: FastAPI, title: str, version: str):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=title,
            version=version,
            routes=app.routes,
        )

        # Replace 422 responses with 400 in all endpoints
        for path in openapi_schema["paths"].values():
            for method in path.values():
                responses = method.get("responses", {})
                if "422" in responses:
                    responses["400"] = {
                        **responses.pop("422"),
                        "content": {
                            "application/problem+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                            }
                        },
                    }

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return custom_openapi
