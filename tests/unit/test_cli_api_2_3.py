import asyncio
from cli.command_router import CommandRouter
from cli.product_commands import ProductCommands
from api.routes.runtime import router_for as runtime_router

def test_command_router_parse_and_execute():
    router=CommandRouter();router.register("echo",lambda value="":value,aliases=("e",));assert router.parse('e value="hello world"')==("echo",{"value":"hello world"});assert asyncio.run(router.execute_line("e value=x"))=="x"
def test_product_commands_returns_envelope(db,settings):
    from app.dependency_container import build_container
    container=build_container(settings);row=ProductCommands(container).execute("candidates");assert row["ok"] and row["command"]=="products.candidates"
def test_runtime_router_has_routes(db,settings):
    from app.dependency_container import build_container
    container=build_container(settings);paths={route.path for route in runtime_router(container).routes};assert "/runtime/liveness" in paths and "/runtime/readiness" in paths
