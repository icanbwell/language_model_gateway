import httpx

from pydantic import BaseModel, Field
from typing import Type, Tuple, Literal, Dict, Any, cast

from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool


class FhirConverterServiceToolInput(BaseModel):
    ccda_xml: str = Field(
        description="CCDA XML string to be converted to FHIR using fhir-converter-service",
    )


class FhirConverterServiceTool(ResilientBaseTool):
    name: str = "fhir_converter_service"
    description: str = "Accepts CCDA as an xml string and converts it to FHIR"
    args_schema: Type[BaseModel] = FhirConverterServiceToolInput
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"
    api_url: str = "https://fhir-converter-service.dev-ue1.bwell.zone/api/convert-data"

    # noinspection PyMethodMayBeStatic
    def _prepare_request_payload(self, ccda_xml: str) -> Dict[str, Any]:
        return {
            "resourceType": "Parameters",
            "parameter": [
                {"name": "inputData", "valueString": ccda_xml},
                {"name": "inputDataType", "valueString": "Ccda"},
                {"name": "templateCollectionReference", "valueString": "default"},
                {"name": "rootTemplate", "valueString": "CCD"},
            ],
        }

    # noinspection PyMethodMayBeStatic
    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Process and validate the API response"""
        if response.status_code != 200:
            raise Exception(
                f"API request failed with status {response.status_code}: {response.text}"
            )
        return cast(Dict[str, Any], response.json())

    def _run(
        self,
        ccda_xml: str,
    ) -> Dict[str, Any]:
        """Synchronous execution"""
        raise NotImplementedError("Use async version of this tool")

    async def _arun(
        self,
        ccda_xml: str,
    ) -> Tuple[Dict[str, Any], str]:
        """Asynchronous execution"""

        payload = self._prepare_request_payload(ccda_xml)

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "accept": "*/*",
        }

        async_client: httpx.AsyncClient = httpx.AsyncClient(headers=headers)

        try:
            response = await async_client.post(self.api_url, json=payload, timeout=60.0)
            artifact: str = "FhirConverterServiceAgent: Running"
            return self._handle_response(response), artifact

        except httpx.TimeoutException:
            raise Exception("Request timed out")
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {str(e)}")
