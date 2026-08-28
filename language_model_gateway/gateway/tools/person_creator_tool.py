import uuid

from datetime import datetime

import httpx
from httpx import Response, Headers
from pydantic import BaseModel, Field
from typing import Any, Literal, Optional, Tuple, Type

from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool

META = {
    "meta": {
        "versionId": "1",
        "lastUpdated": datetime.now().isoformat(),
        "source": "https://www.icanbwell.com",
        "security": [
            {"system": "https://www.icanbwell.com/owner", "code": "FHIR-samsung-demo"},
            {"system": "https://www.icanbwell.com/access", "code": "FHIR-samsung-demo"},
            {"system": "https://www.icanbwell.com/vendor", "code": "FHIR-samsung-demo"},
            {
                "system": "https://www.icanbwell.com/sourceAssigningAuthority",
                "code": "FHIR-samsung-demo",
            },
        ],
    }
}


class PersonCreatorAgentInput(BaseModel):
    """
    Input model for configuring new PersonCreatorAgent.
    """

    patient_id: Optional[str] = Field(
        default=None,
        description=(
            "Patient ID to create an encounter for"
            "PARSING INSTRUCTION: Extract exact patient id from the query.  "
            "If no patient_id is found, ask user for it. This ID should be used to populate the `patient` reference in any subsequent resource."
        ),
    )

    resource: Optional[dict[str, Any]] = Field(
        default=None,
        description=(
            "FHIR resource to be used as the payload for the POST request.  User should be prompted for to either provider a resource or have you create one."
            f"All resources must include `meta.security` and `meta.source` fields.  If meta is not provided in a resource, then this default can be added: {META}"
        ),
    )

    resource_type: Optional[str] = Field(
        default=None,
        description=(
            "FHIR resource type to determine which payload to use for the POST request."
            "PARSING INSTRUCTION: Extract exact resource type from the query, something like 'Encounter'.  If it cannot be found, ask user for it."
        ),
    )


class PersonCreatorTool(ResilientBaseTool):
    """
    A LangChain-compatible tool for creating a new Person on the bwell FHIR Server.

    This tool can be used to:
    - Create a new person with a specified first name.

    """

    name: str = "person_creator"
    description: str = (
        "BWell Fhir Person Creator Tool. "
        "USAGE TIPS: "
        "- Specify a patient id to  create a new Encounter for that patient."
        "- Example queries: "
        "'Create a new encounter for patient id f7a75623-afd3-481b-aa22-b57dc472225c', "
    )

    args_schema: Type[BaseModel] = (
        PersonCreatorAgentInput  # Should be the input parameters class you created above
    )
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"

    async def _arun(
        self,
        patient_id: str,
        resource_type: Optional[str] = None,
        resource: Optional[dict[str, Any]] = None,
    ) -> Tuple[str, str]:
        try:
            # TODO: Implement the logic for creating a new person
            # TODO: get access token from env???
            access_token = "active_token_to_FHIR_server"
            headers = Headers(
                {
                    "Content-Type": "application/fhir+json",
                    "Authorization": f"Bearer {access_token}",
                    "content-type": "application/json",
                }
            )
            payload: dict[str, Any] = {}
            if resource_type == "Encounter":
                payload = {
                    "resourceType": "Encounter",
                    "id": f"{uuid.uuid4()}",
                    "meta": {
                        "versionId": "1",
                        "lastUpdated": datetime.now().isoformat(),
                        "source": "https://www.icanbwell.com",
                        "security": [
                            {
                                "system": "https://www.icanbwell.com/owner",
                                "code": "FHIR-samsung-demo",
                            },
                            {
                                "system": "https://www.icanbwell.com/access",
                                "code": "FHIR-samsung-demo",
                            },
                            {
                                "system": "https://www.icanbwell.com/vendor",
                                "code": "FHIR-samsung-demo",
                            },
                            {
                                "system": "https://www.icanbwell.com/sourceAssigningAuthority",
                                "code": "FHIR-samsung-demo",
                            },
                        ],
                    },
                    "status": "finished",
                    "class": {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                        "code": "AMB",
                        "display": "Ambulatory",
                    },
                    "type": [
                        {
                            "coding": [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "11687002",
                                    "display": "Emergency room admission",
                                }
                            ],
                            "text": "Emergency Room Admission",
                        }
                    ],
                    "subject": {
                        "extension": [
                            {
                                "id": "sourceId",
                                "url": "https://www.icanbwell.com/sourceId",
                                "valueString": f"Patient/{patient_id}",
                            },
                            {
                                "id": "uuid",
                                "url": "https://www.icanbwell.com/uuid",
                                "valueString": f"Patient/{patient_id}",
                            },
                            {
                                "id": "sourceAssigningAuthority",
                                "url": "https://www.icanbwell.com/sourceAssigningAuthority",
                                "valueString": "FHIR-samsung-demo",
                            },
                        ],
                        "reference": f"Patient/{patient_id}",
                    },
                }
            elif resource_type == "Immunization":
                payload = {
                    "resourceType": "Immunization",
                    "id": f"{uuid.uuid4()}",
                    "meta": {
                        "versionId": "1",
                        "lastUpdated": datetime.now().isoformat(),
                        "source": "https://www.icanbwell.com",
                        "security": [
                            {
                                "system": "https://www.icanbwell.com/owner",
                                "code": "FHIR-samsung-demo",
                            },
                            {
                                "system": "https://www.icanbwell.com/access",
                                "code": "FHIR-samsung-demo",
                            },
                            {
                                "system": "https://www.icanbwell.com/vendor",
                                "code": "FHIR-samsung-demo",
                            },
                            {
                                "system": "https://www.icanbwell.com/sourceAssigningAuthority",
                                "code": "FHIR-samsung-demo",
                            },
                        ],
                    },
                    "status": "completed",
                    "vaccineCode": {
                        "coding": [
                            {
                                "system": "http://hl7.org/fhir/sid/cvx",
                                "code": "140",
                                "display": "Influenza, seasonal, injectable",
                            }
                        ]
                    },
                    "patient": {
                        "reference": f"Patient/{patient_id}",
                        "display": "John Doe",
                    },
                    "occurrenceDateTime": "2023-11-15T10:30:00Z",
                    "recorded": "2023-11-15T10:35:00Z",
                    "primarySource": True,
                    "location": {"reference": "Location/health-clinic"},
                    "manufacturer": {"reference": "Organization/vaccine-manufacturer"},
                    "lotNumber": "BATCH2023-A",
                    "expirationDate": "2024-12-31",
                    "site": {
                        "coding": [
                            {
                                "system": "http://hl7.org/fhir/v3/ActSite",
                                "code": "LA",
                                "display": "Left Arm",
                            }
                        ]
                    },
                    "route": {
                        "coding": [
                            {
                                "system": "http://hl7.org/fhir/v3/RouteOfAdministration",
                                "code": "IM",
                                "display": "Intramuscular",
                            }
                        ]
                    },
                    "doseQuantity": {
                        "value": 0.5,
                        "unit": "mL",
                        "system": "http://unitsofmeasure.org",
                        "code": "mL",
                    },
                    "performer": [
                        {
                            "actor": {
                                "reference": "Practitioner/nurse-jones",
                                "display": "Nurse Jones",
                            },
                            "function": {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/v2-0443",
                                        "code": "AP",
                                        "display": "Administering Provider",
                                    }
                                ]
                            },
                        }
                    ],
                }
            url = f"https://fhir.dev.icanbwell.com/4_0_0/{resource_type}"

            async with httpx.AsyncClient(
                headers=headers, follow_redirects=True
            ) as client:
                response: Response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json(), response.json()

        except Exception as e:
            error_msg = f"Failed to create Encounter: {str(e)}"
            error_artifact = f"PersonCreatorAgent: Failed to create Encounter: {str(e)}"
            return error_msg, error_artifact

    def _run(
        self,
        # add parameters here that mirror the fields in your input parameters class
        # For example:
        patient_id: str,
        resource_type: str,
        resource: Optional[dict[str, Any]] = None,
    ) -> Tuple[str, str]:
        """
        Synchronous version of the tool (falls back to async implementation).

        Raises:
            NotImplementedError: Always raises to enforce async usage
        """
        raise NotImplementedError("Use async version of this tool")
