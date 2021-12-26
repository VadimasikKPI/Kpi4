from api import app, db
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.queries import *
from api.mutations import *

query = ObjectType("Query")
mutation = ObjectType("Mutation")
query.set_field("listPackages", listPackages_resolver)
query.set_field("getPackage", getPackage_resolver)
query.set_field("listClients", listClients_resolver)
query.set_field("getClient", getClient_resolver)
query.set_field("listOrders", listOrders_resolver)
query.set_field("getOrder", getOrder_resolver)

mutation.set_field("createPackage", create_package_resolver)
mutation.set_field("updatePackage", update_package_resolver)
mutation.set_field("deletePackage", delete_package_resolver)
mutation.set_field("createClient", create_client_resolver)
mutation.set_field("updateClient", update_client_resolver)
mutation.set_field("deleteClient", delete_client_resolver)
mutation.set_field("createOrder", create_order_resolver)
mutation.set_field("updateOrder", update_order_resolver)
mutation.set_field("deleteOrder", delete_order_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code