from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List


class FlaskAPIEndpoint(BaseModel):
    route: str = Field(..., description="The URL path for the endpoint")
    methods: List[str] = Field(..., description="The HTTP methods supported by the endpoint")
    description: str = Field(..., description="A description of the endpoint")
    function_name: str = Field(..., description="The name of the function that implements the endpoint")
    function_parameters: List[Dict[str, Any]] = Field(
        [], description="A list of parameter sets and their type expected by the function, example. {'name': '', 'type': ''}, allowing for multiple parameter configurations.")
    body_parameters: List[Dict[str, Any]] = Field(
        [], description="A list of parameter sets and their type expected in the body of the request, example. {'name': '', 'type': ''} allowing for multiple parameter configurations.")
    response: Optional[str] = Field(None, description="The expected response from the endpoint")
    status_code: int = Field(..., description="The expected status code from the endpoint")


class ListOfFlaskAPIEndpoints(BaseModel):
    endpoints: List[FlaskAPIEndpoint] = Field([], description="A list of Flask API endpoints")


class FrontendPageDesign(BaseModel):
    name: str = Field(..., description="The name of the HTML page. Should not include the .html extension")
    purpose: str = Field(..., description="The purpose of the HTML page. This should be a very detailed description of what the page is supposed to do.")


class ListOfFrontendPages(BaseModel):
    pages: List[FrontendPageDesign] = Field([], description="A list of JSON objects representing the design of the frontend pages")
