from typing import Tuple, Literal
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool


class GraphqlSchemaProviderTool(ResilientBaseTool):
    """
    A tool for providing FHIR GraphQL schema.
    """

    name: str = "fhir_graphql_schema_provider"
    description: str = (
        "This is a FHIR GraphQL schema provider that provides the GraphQL SDL for needed for generating correct query"
        "Example queries: "
        "'Make query for getting all patients with ids 1,2', "
        "'Get conditions for patients whose name is John'"
    )

    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"

    async def _arun(self) -> Tuple[str, str]:
        graphql_schema = '''
directive @key(fields: _FieldSet!, resolvable: Boolean = true) on OBJECT | INTERFACE

directive @requires(fields: _FieldSet!) on FIELD_DEFINITION

directive @provides(fields: _FieldSet!) on FIELD_DEFINITION

directive @external(reason: String) on OBJECT | FIELD_DEFINITION

directive @tag(name: String!) on FIELD_DEFINITION | OBJECT | INTERFACE | UNION | ARGUMENT_DEFINITION | SCALAR | ENUM | ENUM_VALUE | INPUT_OBJECT | INPUT_FIELD_DEFINITION

directive @extends on OBJECT | INTERFACE

"""
Indicates exactly one field must be supplied and this field must not be `null`.
"""
directive @oneOf on INPUT_OBJECT

enum TotalType {
  accurate
  estimate
}

type Query {
  id: String
  accounts(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, identifier: SearchToken, name: SearchString, owner: SearchReference, patient: SearchReference, period: SearchDate, status: SearchToken, subject: SearchReference, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): AccountBundle
  activityDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, composed_of: SearchReference, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, depends_on: SearchReference, derived_from: SearchReference, description: SearchString, effective: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, predecessor: SearchReference, publisher: SearchString, status: SearchToken, successor: SearchReference, title: SearchString, topic: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ActivityDefinitionBundle
  administrableProductDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, device: SearchReference, dose_form: SearchToken, form_of: SearchReference, identifier: SearchToken, ingredient: SearchToken, manufactured_item: SearchReference, route: SearchToken, target_species: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): AdministrableProductDefinitionBundle
  adverseEvents(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, actuality: SearchToken, category: SearchToken, date: SearchDate, event: SearchToken, location: SearchReference, recorder: SearchReference, resultingcondition: SearchReference, seriousness: SearchToken, severity: SearchToken, study: SearchReference, subject: SearchReference, substance: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): AdverseEventBundle
  allergyIntolerances(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, asserter: SearchReference, category: SearchToken, clinical_status: SearchToken, code: SearchToken, criticality: SearchToken, date: SearchDate, identifier: SearchToken, last_date: SearchDate, manifestation: SearchToken, onset: SearchDate, patient: SearchReference, recorder: SearchReference, route: SearchToken, severity: SearchToken, type: SearchToken, verification_status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): AllergyIntoleranceBundle
  appointments(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, actor: SearchReference, appointment_type: SearchToken, based_on: SearchReference, date: SearchDate, identifier: SearchToken, location: SearchReference, part_status: SearchToken, patient: SearchReference, practitioner: SearchReference, reason_code: SearchToken, reason_reference: SearchReference, service_category: SearchToken, service_type: SearchToken, slot: SearchReference, specialty: SearchToken, status: SearchToken, supporting_info: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): AppointmentBundle
  appointmentResponses(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, actor: SearchReference, appointment: SearchReference, identifier: SearchToken, location: SearchReference, part_status: SearchToken, patient: SearchReference, practitioner: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): AppointmentResponseBundle
  auditEvents(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, action: SearchToken, address: SearchString, agent: SearchReference, agent_name: SearchString, agent_role: SearchToken, altid: SearchToken, date: SearchDate, entity: SearchReference, entity_name: SearchString, entity_role: SearchToken, entity_type: SearchToken, outcome: SearchToken, patient: SearchReference, policy: SearchString, site: SearchToken, source: SearchReference, subtype: SearchToken, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): AuditEventBundle
  basics(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, author: SearchReference, code: SearchToken, created: SearchDate, identifier: SearchToken, patient: SearchReference, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): BasicBundle
  binaries(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): BinaryBundle
  biologicallyDerivedProducts(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): BiologicallyDerivedProductBundle
  bodyStructures(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, identifier: SearchToken, location: SearchToken, morphology: SearchToken, patient: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): BodyStructureBundle
  bundles(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, composition: SearchReference, identifier: SearchToken, message: SearchReference, timestamp: SearchDate, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): BundleBundle
  capabilityStatements(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, fhirversion: SearchToken, format: SearchToken, guide: SearchReference, jurisdiction: SearchToken, mode: SearchToken, name: SearchString, publisher: SearchString, resource: SearchToken, resource_profile: SearchReference, security_service: SearchToken, software: SearchString, status: SearchToken, supported_profile: SearchReference, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CapabilityStatementBundle
  carePlans(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, activity_code: SearchToken, activity_date: SearchDate, activity_reference: SearchReference, based_on: SearchReference, care_team: SearchReference, category: SearchToken, condition: SearchReference, date: SearchDate, encounter: SearchReference, goal: SearchReference, identifier: SearchToken, instantiates_canonical: SearchReference, instantiates_uri: SearchString, intent: SearchToken, part_of: SearchReference, patient: SearchReference, performer: SearchReference, replaces: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CarePlanBundle
  careTeams(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, category: SearchToken, date: SearchDate, encounter: SearchReference, identifier: SearchToken, participant: SearchReference, patient: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CareTeamBundle
  catalogEntries(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CatalogEntryBundle
  chargeItems(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, account: SearchReference, code: SearchToken, context: SearchReference, entered_date: SearchDate, enterer: SearchReference, factor_override: SearchNumber, identifier: SearchToken, occurrence: SearchDate, patient: SearchReference, performer_actor: SearchReference, performer_function: SearchToken, performing_organization: SearchReference, price_override: SearchQuantity, quantity: SearchQuantity, requesting_organization: SearchReference, service: SearchReference, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ChargeItemBundle
  chargeItemDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, effective: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, publisher: SearchString, status: SearchToken, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ChargeItemDefinitionBundle
  citations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, effective: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, publisher: SearchString, status: SearchToken, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CitationBundle
  claims(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, care_team: SearchReference, created: SearchDate, detail_udi: SearchReference, encounter: SearchReference, enterer: SearchReference, facility: SearchReference, identifier: SearchToken, insurer: SearchReference, item_udi: SearchReference, patient: SearchReference, payee: SearchReference, priority: SearchToken, procedure_udi: SearchReference, provider: SearchReference, status: SearchToken, subdetail_udi: SearchReference, use: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ClaimBundle
  claimResponses(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, created: SearchDate, disposition: SearchString, identifier: SearchToken, insurer: SearchReference, outcome: SearchToken, patient: SearchReference, payment_date: SearchDate, request: SearchReference, requestor: SearchReference, status: SearchToken, use: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ClaimResponseBundle
  clinicalImpressions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, assessor: SearchReference, date: SearchDate, encounter: SearchReference, finding_code: SearchToken, finding_ref: SearchReference, identifier: SearchToken, investigation: SearchReference, patient: SearchReference, previous: SearchReference, problem: SearchReference, status: SearchToken, subject: SearchReference, supporting_info: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ClinicalImpressionBundle
  clinicalUseDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, contraindication: SearchToken, contraindication_reference: SearchReference, effect: SearchToken, effect_reference: SearchReference, identifier: SearchToken, indication: SearchToken, indication_reference: SearchReference, interaction: SearchToken, product: SearchReference, subject: SearchReference, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ClinicalUseDefinitionBundle
  codeSystems(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, code: SearchToken, content_mode: SearchToken, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, identifier: SearchToken, jurisdiction: SearchToken, language: SearchToken, name: SearchString, publisher: SearchString, status: SearchToken, supplements: SearchReference, system: SearchString, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CodeSystemBundle
  communications(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, based_on: SearchReference, category: SearchToken, encounter: SearchReference, identifier: SearchToken, instantiates_canonical: SearchReference, instantiates_uri: SearchString, medium: SearchToken, part_of: SearchReference, patient: SearchReference, received: SearchDate, recipient: SearchReference, sender: SearchReference, sent: SearchDate, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CommunicationBundle
  communicationRequests(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, authored: SearchDate, based_on: SearchReference, category: SearchToken, encounter: SearchReference, group_identifier: SearchToken, identifier: SearchToken, medium: SearchToken, occurrence: SearchDate, patient: SearchReference, priority: SearchToken, recipient: SearchReference, replaces: SearchReference, requester: SearchReference, sender: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CommunicationRequestBundle
  compartmentDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, code: SearchToken, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, name: SearchString, publisher: SearchString, resource: SearchToken, status: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CompartmentDefinitionBundle
  compositions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, attester: SearchReference, author: SearchReference, category: SearchToken, confidentiality: SearchToken, context: SearchToken, date: SearchDate, encounter: SearchReference, entry: SearchReference, identifier: SearchToken, patient: SearchReference, period: SearchDate, related_id: SearchToken, related_ref: SearchReference, section: SearchToken, status: SearchToken, subject: SearchReference, title: SearchString, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CompositionBundle
  conceptMaps(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, dependson: SearchString, description: SearchString, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, other: SearchReference, product: SearchString, publisher: SearchString, source: SearchReference, source_code: SearchToken, source_system: SearchString, source_uri: SearchReference, status: SearchToken, target: SearchReference, target_code: SearchToken, target_system: SearchString, target_uri: SearchReference, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ConceptMapBundle
  conditions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, abatement_age: SearchQuantity, abatement_date: SearchDate, abatement_string: SearchString, asserter: SearchReference, body_site: SearchToken, category: SearchToken, clinical_status: SearchToken, code: SearchToken, encounter: SearchReference, evidence: SearchToken, evidence_detail: SearchReference, identifier: SearchToken, onset_age: SearchQuantity, onset_date: SearchDate, onset_info: SearchString, patient: SearchReference, recorded_date: SearchDate, severity: SearchToken, stage: SearchToken, subject: SearchReference, verification_status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ConditionBundle
  consents(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, action: SearchToken, actor: SearchReference, category: SearchToken, consentor: SearchReference, data: SearchReference, date: SearchDate, identifier: SearchToken, organization: SearchReference, patient: SearchReference, period: SearchDate, purpose: SearchToken, scope: SearchToken, security_label: SearchToken, source_reference: SearchReference, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ConsentBundle
  contracts(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, authority: SearchReference, domain: SearchReference, identifier: SearchToken, instantiates: SearchString, issued: SearchDate, patient: SearchReference, signer: SearchReference, status: SearchToken, subject: SearchReference, url: SearchString, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ContractBundle
  coverages(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, beneficiary: SearchReference, class_type: SearchToken, class_value: SearchString, dependent: SearchString, identifier: SearchToken, patient: SearchReference, payor: SearchReference, policy_holder: SearchReference, status: SearchToken, subscriber: SearchReference, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CoverageBundle
  coverageEligibilityRequests(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, created: SearchDate, enterer: SearchReference, facility: SearchReference, identifier: SearchToken, patient: SearchReference, provider: SearchReference, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CoverageEligibilityRequestBundle
  coverageEligibilityResponses(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, created: SearchDate, disposition: SearchString, identifier: SearchToken, insurer: SearchReference, outcome: SearchToken, patient: SearchReference, request: SearchReference, requestor: SearchReference, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): CoverageEligibilityResponseBundle
  detectedIssues(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, author: SearchReference, code: SearchToken, identified: SearchDate, identifier: SearchToken, implicated: SearchReference, patient: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): DetectedIssueBundle
  devices(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, device_name: SearchString, identifier: SearchToken, location: SearchReference, manufacturer: SearchString, model: SearchString, organization: SearchReference, patient: SearchReference, status: SearchToken, type: SearchToken, udi_carrier: SearchString, udi_di: SearchString, url: SearchString, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): DeviceBundle
  deviceDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, identifier: SearchToken, parent: SearchReference, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): DeviceDefinitionBundle
  deviceMetrics(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, category: SearchToken, identifier: SearchToken, parent: SearchReference, source: SearchReference, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): DeviceMetricBundle
  deviceRequests(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, authored_on: SearchDate, based_on: SearchReference, code: SearchToken, device: SearchReference, encounter: SearchReference, event_date: SearchDate, group_identifier: SearchToken, identifier: SearchToken, instantiates_canonical: SearchReference, instantiates_uri: SearchString, insurance: SearchReference, intent: SearchToken, patient: SearchReference, performer: SearchReference, prior_request: SearchReference, requester: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): DeviceRequestBundle
  deviceUseStatements(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, device: SearchReference, identifier: SearchToken, patient: SearchReference, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): DeviceUseStatementBundle
  diagnosticReports(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, based_on: SearchReference, category: SearchToken, code: SearchToken, conclusion: SearchToken, date: SearchDate, encounter: SearchReference, identifier: SearchToken, issued: SearchDate, media: SearchReference, patient: SearchReference, performer: SearchReference, result: SearchReference, results_interpreter: SearchReference, specimen: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): DiagnosticReportBundle
  documentManifests(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, author: SearchReference, created: SearchDate, description: SearchString, identifier: SearchToken, item: SearchReference, patient: SearchReference, recipient: SearchReference, related_id: SearchToken, related_ref: SearchReference, source: SearchString, status: SearchToken, subject: SearchReference, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): DocumentManifestBundle
  documentReferences(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, authenticator: SearchReference, author: SearchReference, category: SearchToken, contenttype: SearchToken, custodian: SearchReference, date: SearchDate, description: SearchString, encounter: SearchReference, event: SearchToken, facility: SearchToken, format: SearchToken, identifier: SearchToken, language: SearchToken, location: SearchString, patient: SearchReference, period: SearchDate, related: SearchReference, relatesto: SearchReference, relation: SearchToken, security_label: SearchToken, setting: SearchToken, status: SearchToken, subject: SearchReference, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): DocumentReferenceBundle
  encounters(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, account: SearchReference, appointment: SearchReference, based_on: SearchReference, class: SearchToken, date: SearchDate, diagnosis: SearchReference, episode_of_care: SearchReference, identifier: SearchToken, length: SearchQuantity, location: SearchReference, location_period: SearchDate, part_of: SearchReference, participant: SearchReference, participant_type: SearchToken, patient: SearchReference, practitioner: SearchReference, reason_code: SearchToken, reason_reference: SearchReference, service_provider: SearchReference, special_arrangement: SearchToken, status: SearchToken, subject: SearchReference, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): EncounterBundle
  endpoints(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, connection_type: SearchToken, identifier: SearchToken, name: SearchString, organization: SearchReference, payload_type: SearchToken, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): EndpointBundle
  enrollmentRequests(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, identifier: SearchToken, patient: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): EnrollmentRequestBundle
  enrollmentResponses(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, identifier: SearchToken, request: SearchReference, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): EnrollmentResponseBundle
  episodesOfCare(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, care_manager: SearchReference, condition: SearchReference, date: SearchDate, identifier: SearchToken, incoming_referral: SearchReference, organization: SearchReference, patient: SearchReference, status: SearchToken, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): EpisodeOfCareBundle
  eventDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, composed_of: SearchReference, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, depends_on: SearchReference, derived_from: SearchReference, description: SearchString, effective: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, predecessor: SearchReference, publisher: SearchString, status: SearchToken, successor: SearchReference, title: SearchString, topic: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): EventDefinitionBundle
  evidences(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, identifier: SearchToken, publisher: SearchString, status: SearchToken, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): EvidenceBundle
  evidenceReports(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, identifier: SearchToken, publisher: SearchString, status: SearchToken, url: SearchString, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): EvidenceReportBundle
  evidenceVariables(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, identifier: SearchToken, name: SearchString, publisher: SearchString, status: SearchToken, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): EvidenceVariableBundle
  exampleScenarios(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, publisher: SearchString, status: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ExampleScenarioBundle
  explanationOfBenefits(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, care_team: SearchReference, claim: SearchReference, coverage: SearchReference, created: SearchDate, detail_udi: SearchReference, disposition: SearchString, encounter: SearchReference, enterer: SearchReference, facility: SearchReference, identifier: SearchToken, item_udi: SearchReference, patient: SearchReference, payee: SearchReference, procedure_udi: SearchReference, provider: SearchReference, status: SearchToken, subdetail_udi: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ExplanationOfBenefitBundle
  familyMemberHistories(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, code: SearchToken, date: SearchDate, identifier: SearchToken, instantiates_canonical: SearchReference, instantiates_uri: SearchString, patient: SearchReference, relationship: SearchToken, sex: SearchToken, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): FamilyMemberHistoryBundle
  flags(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, author: SearchReference, date: SearchDate, encounter: SearchReference, identifier: SearchToken, patient: SearchReference, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): FlagBundle
  goals(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, achievement_status: SearchToken, category: SearchToken, identifier: SearchToken, lifecycle_status: SearchToken, patient: SearchReference, start_date: SearchDate, subject: SearchReference, target_date: SearchDate, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): GoalBundle
  graphDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, jurisdiction: SearchToken, name: SearchString, publisher: SearchString, start: SearchToken, status: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): GraphDefinitionBundle
  groups(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, actual: SearchToken, characteristic: SearchToken, code: SearchToken, exclude: SearchToken, identifier: SearchToken, managing_entity: SearchReference, member: SearchReference, type: SearchToken, value: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): GroupBundle
  guidanceResponses(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, identifier: SearchToken, patient: SearchReference, request: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): GuidanceResponseBundle
  healthcareServices(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, active: SearchToken, characteristic: SearchToken, coverage_area: SearchReference, endpoint: SearchReference, identifier: SearchToken, location: SearchReference, name: SearchString, organization: SearchReference, program: SearchToken, service_category: SearchToken, service_type: SearchToken, specialty: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): HealthcareServiceBundle
  imagingStudies(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, basedon: SearchReference, bodysite: SearchToken, dicom_class: SearchToken, encounter: SearchReference, endpoint: SearchReference, identifier: SearchToken, instance: SearchToken, interpreter: SearchReference, modality: SearchToken, patient: SearchReference, performer: SearchReference, reason: SearchToken, referrer: SearchReference, series: SearchToken, started: SearchDate, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ImagingStudyBundle
  immunizations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, date: SearchDate, identifier: SearchToken, location: SearchReference, lot_number: SearchString, manufacturer: SearchReference, patient: SearchReference, performer: SearchReference, reaction: SearchReference, reaction_date: SearchDate, reason_code: SearchToken, reason_reference: SearchReference, series: SearchString, status: SearchToken, status_reason: SearchToken, target_disease: SearchToken, vaccine_code: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ImmunizationBundle
  immunizationEvaluations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, date: SearchDate, dose_status: SearchToken, identifier: SearchToken, immunization_event: SearchReference, patient: SearchReference, status: SearchToken, target_disease: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ImmunizationEvaluationBundle
  immunizationRecommendations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, date: SearchDate, identifier: SearchToken, information: SearchReference, patient: SearchReference, status: SearchToken, support: SearchReference, target_disease: SearchToken, vaccine_type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ImmunizationRecommendationBundle
  implementationGuides(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, depends_on: SearchReference, description: SearchString, experimental: SearchToken, global: SearchReference, jurisdiction: SearchToken, name: SearchString, publisher: SearchString, resource: SearchReference, status: SearchToken, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ImplementationGuideBundle
  ingredients(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, for: SearchReference, function: SearchToken, identifier: SearchToken, manufacturer: SearchReference, role: SearchToken, substance: SearchReference, substance_code: SearchToken, substance_definition: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): IngredientBundle
  insurancePlans(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, address: SearchString, address_city: SearchString, address_country: SearchString, address_postalcode: SearchString, address_state: SearchString, address_use: SearchToken, administered_by: SearchReference, endpoint: SearchReference, identifier: SearchToken, name: SearchString, owned_by: SearchReference, phonetic: SearchString, status: SearchToken, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): InsurancePlanBundle
  invoices(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, account: SearchReference, date: SearchDate, identifier: SearchToken, issuer: SearchReference, participant: SearchReference, participant_role: SearchToken, patient: SearchReference, recipient: SearchReference, status: SearchToken, subject: SearchReference, totalgross: SearchQuantity, totalnet: SearchQuantity, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): InvoiceBundle
  libraries(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, composed_of: SearchReference, content_type: SearchToken, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, depends_on: SearchReference, derived_from: SearchReference, description: SearchString, effective: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, predecessor: SearchReference, publisher: SearchString, status: SearchToken, successor: SearchReference, title: SearchString, topic: SearchToken, type: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): LibraryBundle
  linkages(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, author: SearchReference, item: SearchReference, source: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): LinkageBundle
  lists(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, code: SearchToken, date: SearchDate, empty_reason: SearchToken, encounter: SearchReference, identifier: SearchToken, item: SearchReference, notes: SearchString, patient: SearchReference, source: SearchReference, status: SearchToken, subject: SearchReference, title: SearchString, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ListBundle
  locations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, address: SearchString, address_city: SearchString, address_country: SearchString, address_postalcode: SearchString, address_state: SearchString, address_use: SearchToken, endpoint: SearchReference, identifier: SearchToken, name: SearchString, near: String, operational_status: SearchToken, organization: SearchReference, partof: SearchReference, status: SearchToken, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): LocationBundle
  manufacturedItemDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, dose_form: SearchToken, identifier: SearchToken, ingredient: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ManufacturedItemDefinitionBundle
  measures(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, composed_of: SearchReference, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, depends_on: SearchReference, derived_from: SearchReference, description: SearchString, effective: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, predecessor: SearchReference, publisher: SearchString, status: SearchToken, successor: SearchReference, title: SearchString, topic: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MeasureBundle
  measureReports(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, date: SearchDate, evaluated_resource: SearchReference, identifier: SearchToken, measure: SearchReference, patient: SearchReference, period: SearchDate, reporter: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MeasureReportBundle
  media(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, based_on: SearchReference, created: SearchDate, device: SearchReference, encounter: SearchReference, identifier: SearchToken, modality: SearchToken, operator: SearchReference, patient: SearchReference, site: SearchToken, status: SearchToken, subject: SearchReference, type: SearchToken, view: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MediaBundle
  medications(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, code: SearchToken, expiration_date: SearchDate, form: SearchToken, identifier: SearchToken, ingredient: SearchReference, ingredient_code: SearchToken, lot_number: SearchToken, manufacturer: SearchReference, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MedicationBundle
  medicationAdministrations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, code: SearchToken, context: SearchReference, device: SearchReference, effective_time: SearchDate, identifier: SearchToken, medication: SearchReference, patient: SearchReference, performer: SearchReference, reason_given: SearchToken, reason_not_given: SearchToken, request: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MedicationAdministrationBundle
  medicationDispenses(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, code: SearchToken, context: SearchReference, destination: SearchReference, identifier: SearchToken, medication: SearchReference, patient: SearchReference, performer: SearchReference, prescription: SearchReference, receiver: SearchReference, responsibleparty: SearchReference, status: SearchToken, subject: SearchReference, type: SearchToken, whenhandedover: SearchDate, whenprepared: SearchDate, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MedicationDispenseBundle
  medicationKnowledges(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, classification: SearchToken, classification_type: SearchToken, code: SearchToken, doseform: SearchToken, ingredient: SearchReference, ingredient_code: SearchToken, manufacturer: SearchReference, monitoring_program_name: SearchToken, monitoring_program_type: SearchToken, monograph: SearchReference, monograph_type: SearchToken, source_cost: SearchToken, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MedicationKnowledgeBundle
  medicationRequests(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, authoredon: SearchDate, category: SearchToken, code: SearchToken, date: SearchDate, encounter: SearchReference, identifier: SearchToken, intended_dispenser: SearchReference, intended_performer: SearchReference, intended_performertype: SearchToken, intent: SearchToken, medication: SearchReference, patient: SearchReference, priority: SearchToken, requester: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MedicationRequestBundle
  medicationStatements(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, category: SearchToken, code: SearchToken, context: SearchReference, effective: SearchDate, identifier: SearchToken, medication: SearchReference, part_of: SearchReference, patient: SearchReference, source: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MedicationStatementBundle
  medicinalProductDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, characteristic: SearchToken, characteristic_type: SearchToken, contact: SearchReference, domain: SearchToken, identifier: SearchToken, ingredient: SearchToken, master_file: SearchReference, name: SearchString, name_language: SearchToken, product_classification: SearchToken, status: SearchToken, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MedicinalProductDefinitionBundle
  messageDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, category: SearchToken, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, event: SearchToken, focus: SearchToken, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, parent: SearchReference, publisher: SearchString, status: SearchToken, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MessageDefinitionBundle
  messageHeaders(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, author: SearchReference, code: SearchToken, destination: SearchString, destination_uri: SearchString, enterer: SearchReference, event: SearchToken, focus: SearchReference, receiver: SearchReference, response_id: SearchToken, responsible: SearchReference, sender: SearchReference, source: SearchString, source_uri: SearchString, target: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MessageHeaderBundle
  molecularSequences(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, chromosome: SearchToken, identifier: SearchToken, patient: SearchReference, referenceseqid: SearchToken, type: SearchToken, variant_end: SearchNumber, variant_start: SearchNumber, window_end: SearchNumber, window_start: SearchNumber, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): MolecularSequenceBundle
  namingSystems(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, contact: SearchString, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, id_type: SearchToken, jurisdiction: SearchToken, kind: SearchToken, name: SearchString, period: SearchDate, publisher: SearchString, responsible: SearchString, status: SearchToken, telecom: SearchToken, type: SearchToken, value: SearchString, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): NamingSystemBundle
  nutritionOrders(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, additive: SearchToken, datetime: SearchDate, encounter: SearchReference, formula: SearchToken, identifier: SearchToken, instantiates_canonical: SearchReference, instantiates_uri: SearchString, oraldiet: SearchToken, patient: SearchReference, provider: SearchReference, status: SearchToken, supplement: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): NutritionOrderBundle
  nutritionProducts(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, identifier: SearchToken, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): NutritionProductBundle
  observations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, based_on: SearchReference, category: SearchToken, code: SearchToken, combo_code: SearchToken, combo_data_absent_reason: SearchToken, combo_value_concept: SearchToken, combo_value_quantity: SearchQuantity, component_code: SearchToken, component_data_absent_reason: SearchToken, component_value_concept: SearchToken, component_value_quantity: SearchQuantity, data_absent_reason: SearchToken, date: SearchDate, derived_from: SearchReference, device: SearchReference, encounter: SearchReference, focus: SearchReference, has_member: SearchReference, identifier: SearchToken, method: SearchToken, part_of: SearchReference, patient: SearchReference, performer: SearchReference, specimen: SearchReference, status: SearchToken, subject: SearchReference, value_concept: SearchToken, value_date: SearchDate, value_quantity: SearchQuantity, value_string: SearchString, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ObservationBundle
  observationDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ObservationDefinitionBundle
  operationDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, base: SearchReference, code: SearchToken, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, input_profile: SearchReference, instance: SearchToken, jurisdiction: SearchToken, kind: SearchToken, name: SearchString, output_profile: SearchReference, publisher: SearchString, status: SearchToken, system: SearchToken, title: SearchString, type: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): OperationDefinitionBundle
  operationOutcomes(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): OperationOutcomeBundle
  organizations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, active: SearchToken, address: SearchString, address_city: SearchString, address_country: SearchString, address_postalcode: SearchString, address_state: SearchString, address_use: SearchToken, endpoint: SearchReference, identifier: SearchToken, name: SearchString, partof: SearchReference, phonetic: SearchString, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): OrganizationBundle
  organizationAffiliations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, active: SearchToken, date: SearchDate, email: SearchToken, endpoint: SearchReference, identifier: SearchToken, location: SearchReference, network: SearchReference, participating_organization: SearchReference, phone: SearchToken, primary_organization: SearchReference, role: SearchToken, service: SearchReference, specialty: SearchToken, telecom: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): OrganizationAffiliationBundle
  packagedProductDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, biological: SearchReference, contained_item: SearchReference, device: SearchReference, identifier: SearchToken, manufactured_item: SearchReference, medication: SearchReference, name: SearchToken, nutrition: SearchReference, package: SearchReference, package_for: SearchReference, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): PackagedProductDefinitionBundle
  parameters(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ParametersBundle
  patients(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, active: SearchToken, address: SearchString, address_city: SearchString, address_country: SearchString, address_postalcode: SearchString, address_state: SearchString, address_use: SearchToken, birthdate: SearchDate, death_date: SearchDate, deceased: SearchToken, email: SearchToken, family: SearchString, gender: SearchToken, general_practitioner: SearchReference, given: SearchString, identifier: SearchToken, language: SearchToken, link: SearchReference, name: SearchString, organization: SearchReference, phone: SearchToken, phonetic: SearchString, telecom: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): PatientBundle
  paymentNotices(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, created: SearchDate, identifier: SearchToken, payment_status: SearchToken, provider: SearchReference, request: SearchReference, response: SearchReference, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): PaymentNoticeBundle
  paymentReconciliations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, created: SearchDate, disposition: SearchString, identifier: SearchToken, outcome: SearchToken, payment_issuer: SearchReference, request: SearchReference, requestor: SearchReference, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): PaymentReconciliationBundle
  persons(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, address: SearchString, address_city: SearchString, address_country: SearchString, address_postalcode: SearchString, address_state: SearchString, address_use: SearchToken, birthdate: SearchDate, email: SearchToken, family: SearchString, gender: SearchToken, given: SearchString, identifier: SearchToken, link: SearchReference, name: SearchString, organization: SearchReference, patient: SearchReference, phone: SearchToken, phonetic: SearchString, practitioner: SearchReference, relatedperson: SearchReference, telecom: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): PersonBundle
  planDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, composed_of: SearchReference, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, definition: SearchReference, depends_on: SearchReference, derived_from: SearchReference, description: SearchString, effective: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, predecessor: SearchReference, publisher: SearchString, status: SearchToken, successor: SearchReference, title: SearchString, topic: SearchToken, type: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): PlanDefinitionBundle
  practitioners(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, active: SearchToken, address: SearchString, address_city: SearchString, address_country: SearchString, address_postalcode: SearchString, address_state: SearchString, address_use: SearchToken, communication: SearchToken, email: SearchToken, family: SearchString, gender: SearchToken, given: SearchString, identifier: SearchToken, name: SearchString, phone: SearchToken, phonetic: SearchString, telecom: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): PractitionerBundle
  practitionerRoles(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, active: SearchToken, date: SearchDate, email: SearchToken, endpoint: SearchReference, identifier: SearchToken, location: SearchReference, organization: SearchReference, phone: SearchToken, practitioner: SearchReference, role: SearchToken, service: SearchReference, specialty: SearchToken, telecom: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): PractitionerRoleBundle
  procedures(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, based_on: SearchReference, category: SearchToken, code: SearchToken, date: SearchDate, encounter: SearchReference, identifier: SearchToken, instantiates_canonical: SearchReference, instantiates_uri: SearchString, location: SearchReference, part_of: SearchReference, patient: SearchReference, performer: SearchReference, reason_code: SearchToken, reason_reference: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ProcedureBundle
  provenances(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, agent: SearchReference, agent_role: SearchToken, agent_type: SearchToken, entity: SearchReference, location: SearchReference, patient: SearchReference, recorded: SearchDate, signature_type: SearchToken, target: SearchReference, when: SearchDate, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ProvenanceBundle
  questionnaires(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, code: SearchToken, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, definition: SearchString, description: SearchString, effective: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, publisher: SearchString, status: SearchToken, subject_type: SearchToken, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): QuestionnaireBundle
  questionnaireResponses(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, author: SearchReference, authored: SearchDate, based_on: SearchReference, encounter: SearchReference, identifier: SearchToken, part_of: SearchReference, patient: SearchReference, questionnaire: SearchReference, source: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): QuestionnaireResponseBundle
  regulatedAuthorizations(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, case: SearchToken, case_type: SearchToken, holder: SearchReference, identifier: SearchToken, region: SearchToken, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): RegulatedAuthorizationBundle
  relatedPersons(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, active: SearchToken, address: SearchString, address_city: SearchString, address_country: SearchString, address_postalcode: SearchString, address_state: SearchString, address_use: SearchToken, birthdate: SearchDate, email: SearchToken, gender: SearchToken, identifier: SearchToken, name: SearchString, patient: SearchReference, phone: SearchToken, phonetic: SearchString, relationship: SearchToken, telecom: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): RelatedPersonBundle
  requestGroups(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, author: SearchReference, authored: SearchDate, code: SearchToken, encounter: SearchReference, group_identifier: SearchToken, identifier: SearchToken, instantiates_canonical: SearchReference, instantiates_uri: SearchString, intent: SearchToken, participant: SearchReference, patient: SearchReference, priority: SearchToken, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): RequestGroupBundle
  researchDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, composed_of: SearchReference, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, depends_on: SearchReference, derived_from: SearchReference, description: SearchString, effective: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, predecessor: SearchReference, publisher: SearchString, status: SearchToken, successor: SearchReference, title: SearchString, topic: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ResearchDefinitionBundle
  researchElementDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, composed_of: SearchReference, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, depends_on: SearchReference, derived_from: SearchReference, description: SearchString, effective: SearchDate, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, predecessor: SearchReference, publisher: SearchString, status: SearchToken, successor: SearchReference, title: SearchString, topic: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ResearchElementDefinitionBundle
  researchStudies(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, category: SearchToken, date: SearchDate, focus: SearchToken, identifier: SearchToken, keyword: SearchToken, location: SearchToken, partof: SearchReference, principalinvestigator: SearchReference, protocol: SearchReference, site: SearchReference, sponsor: SearchReference, status: SearchToken, title: SearchString, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ResearchStudyBundle
  researchSubjects(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, date: SearchDate, identifier: SearchToken, individual: SearchReference, patient: SearchReference, status: SearchToken, study: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ResearchSubjectBundle
  riskAssessments(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, condition: SearchReference, date: SearchDate, encounter: SearchReference, identifier: SearchToken, method: SearchToken, patient: SearchReference, performer: SearchReference, probability: SearchNumber, risk: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): RiskAssessmentBundle
  schedules(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, active: SearchToken, actor: SearchReference, date: SearchDate, identifier: SearchToken, service_category: SearchToken, service_type: SearchToken, specialty: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ScheduleBundle
  searchParameters(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, base: SearchToken, code: SearchToken, component: SearchReference, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, derived_from: SearchReference, description: SearchString, jurisdiction: SearchToken, name: SearchString, publisher: SearchString, status: SearchToken, target: SearchToken, type: SearchToken, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SearchParameterBundle
  serviceRequests(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, authored: SearchDate, based_on: SearchReference, body_site: SearchToken, category: SearchToken, code: SearchToken, encounter: SearchReference, identifier: SearchToken, instantiates_canonical: SearchReference, instantiates_uri: SearchString, intent: SearchToken, occurrence: SearchDate, patient: SearchReference, performer: SearchReference, performer_type: SearchToken, priority: SearchToken, replaces: SearchReference, requester: SearchReference, requisition: SearchToken, specimen: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ServiceRequestBundle
  slots(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, appointment_type: SearchToken, identifier: SearchToken, schedule: SearchReference, service_category: SearchToken, service_type: SearchToken, specialty: SearchToken, start: SearchDate, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SlotBundle
  specimens(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, accession: SearchToken, bodysite: SearchToken, collected: SearchDate, collector: SearchReference, container: SearchToken, container_id: SearchToken, identifier: SearchToken, parent: SearchReference, patient: SearchReference, status: SearchToken, subject: SearchReference, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SpecimenBundle
  specimenDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, container: SearchToken, identifier: SearchToken, type: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SpecimenDefinitionBundle
  structureDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, abstract: SearchToken, base: SearchReference, base_path: SearchToken, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, derivation: SearchToken, description: SearchString, experimental: SearchToken, ext_context: SearchToken, identifier: SearchToken, jurisdiction: SearchToken, keyword: SearchToken, kind: SearchToken, name: SearchString, path: SearchToken, publisher: SearchString, status: SearchToken, title: SearchString, type: SearchString, url: SearchString, valueset: SearchReference, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): StructureDefinitionBundle
  structureMaps(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, publisher: SearchString, status: SearchToken, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): StructureMapBundle
  subscriptions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, contact: SearchToken, criteria: SearchString, payload: SearchToken, status: SearchToken, type: SearchToken, url: SearchString, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SubscriptionBundle
  subscriptionStatuses(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SubscriptionStatusBundle
  subscriptionTopics(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, date: SearchDate, derived_or_self: SearchString, identifier: SearchToken, resource: SearchString, status: SearchToken, title: SearchString, trigger_description: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SubscriptionTopicBundle
  substances(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, category: SearchToken, code: SearchToken, container_identifier: SearchToken, expiry: SearchDate, identifier: SearchToken, quantity: SearchQuantity, status: SearchToken, substance_reference: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SubstanceBundle
  substanceDefinitions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, classification: SearchToken, code: SearchToken, domain: SearchToken, identifier: SearchToken, name: SearchString, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SubstanceDefinitionBundle
  supplyDeliveries(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, identifier: SearchToken, patient: SearchReference, receiver: SearchReference, status: SearchToken, supplier: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SupplyDeliveryBundle
  supplyRequests(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, category: SearchToken, date: SearchDate, identifier: SearchToken, requester: SearchReference, status: SearchToken, subject: SearchReference, supplier: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): SupplyRequestBundle
  tasks(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, authored_on: SearchDate, based_on: SearchReference, business_status: SearchToken, code: SearchToken, encounter: SearchReference, focus: SearchReference, group_identifier: SearchToken, identifier: SearchToken, intent: SearchToken, modified: SearchDate, owner: SearchReference, part_of: SearchReference, patient: SearchReference, performer: SearchToken, period: SearchDate, priority: SearchToken, requester: SearchReference, status: SearchToken, subject: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): TaskBundle
  terminologyCapabilities(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, jurisdiction: SearchToken, name: SearchString, publisher: SearchString, status: SearchToken, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): TerminologyCapabilitiesBundle
  testReports(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, identifier: SearchToken, issued: SearchDate, participant: SearchString, result: SearchToken, tester: SearchString, testscript: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): TestReportBundle
  testScripts(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, publisher: SearchString, status: SearchToken, testscript_capability: SearchString, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): TestScriptBundle
  valueSets(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, code: SearchToken, context: SearchToken, context_quantity: SearchQuantity, context_type: SearchToken, date: SearchDate, description: SearchString, expansion: SearchString, identifier: SearchToken, jurisdiction: SearchToken, name: SearchString, publisher: SearchString, reference: SearchString, status: SearchToken, title: SearchString, url: SearchString, version: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): ValueSetBundle
  verificationResults(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, target: SearchReference, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): VerificationResultBundle
  visionPrescriptions(id: SearchString, _lastUpdated: SearchDate, _profile: SearchString, _security: SearchToken, _source: SearchString, _tag: SearchToken, extension: SearchExtension, datewritten: SearchDate, encounter: SearchReference, identifier: SearchToken, patient: SearchReference, prescriber: SearchReference, status: SearchToken, _total: TotalType, _sort: [String], _count: Int, _getpagesoffset: Int, _debug: Boolean, _explain: Boolean, _setIndexHint: String): VisionPrescriptionBundle
  _entities(representations: [_Any!]!): [_Entity]!
  _service: _Service!
}

type AccountCoverageCoverageReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Coverage
  type: URI
  identifier: Identifier
  display: String
}

type AccountCoverage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  coverage: AccountCoverageCoverageReference
  priority: Int
}

union AccountGuarantorParty = Patient | RelatedPerson | Organization

type AccountGuarantorPartyReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AccountGuarantorParty
  type: URI
  identifier: Identifier
  display: String
}

type AccountGuarantor {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  party: AccountGuarantorPartyReference
  onHold: Boolean
  period: Period
}

type ActivityDefinitionDynamicValue {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  path: String
  expression: Expression
}

type ActivityDefinitionParticipant {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  role: CodeableConcept
}

type AdministrableProductDefinitionProperty {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueCodeableConcept: CodeableConcept
  valueQuantity: Quantity
  valueDate: Date
  valueBoolean: Boolean
  valueAttachment: Attachment
  status: CodeableConcept
}

type AdministrableProductDefinitionRouteOfAdministration {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  firstDose: Quantity
  maxSingleDose: Quantity
  maxDosePerDay: Quantity
  maxDosePerTreatmentPeriod: Ratio
  maxTreatmentPeriod: Quantity
  targetSpecies: [AdministrableProductDefinitionTargetSpecies]
}

type AdministrableProductDefinitionTargetSpecies {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  withdrawalPeriod: [AdministrableProductDefinitionWithdrawalPeriod]
}

type AdministrableProductDefinitionWithdrawalPeriod {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  tissue: CodeableConcept
  value: Quantity
  supportingInformation: String
}

union AdverseEventCausalityAuthor = Practitioner | PractitionerRole

type AdverseEventCausalityAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AdverseEventCausalityAuthor
  type: URI
  identifier: Identifier
  display: String
}

type AdverseEventCausality {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  assessment: CodeableConcept
  productRelatedness: String
  author: AdverseEventCausalityAuthorReference
  method: CodeableConcept
}

union AdverseEventSuspectEntityInstance = Immunization | Procedure | Substance | Medication | MedicationAdministration | MedicationStatement | Device

type AdverseEventSuspectEntityInstanceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AdverseEventSuspectEntityInstance
  type: URI
  identifier: Identifier
  display: String
}

type AdverseEventSuspectEntity {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  instance: AdverseEventSuspectEntityInstanceReference
  causality: [AdverseEventCausality]
}

type AllergyIntoleranceReaction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  substance: CodeableConcept
  manifestation: [CodeableConcept]
  description: String
  onset: DateTime
  severity: Code
  exposureRoute: CodeableConcept
  note: [Annotation]
}

union AppointmentParticipantActor = Patient | Practitioner | PractitionerRole | RelatedPerson | Device | HealthcareService | Location

type AppointmentParticipantActorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AppointmentParticipantActor
  type: URI
  identifier: Identifier
  display: String
}

type AppointmentParticipant {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: [CodeableConcept]
  actor: AppointmentParticipantActorReference
  required: Code
  status: Code
  period: Period
}

union AuditEventAgentWho = PractitionerRole | Practitioner | Organization | Device | Patient | RelatedPerson

type AuditEventAgentWhoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AuditEventAgentWho
  type: URI
  identifier: Identifier
  display: String
}

type AuditEventAgentLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type AuditEventAgent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  role: [CodeableConcept]
  who: AuditEventAgentWhoReference
  altId: String
  name: String
  requestor: Boolean
  location: AuditEventAgentLocationReference
  policy: [URI]
  media: Coding
  network: AuditEventNetwork
  purposeOfUse: [CodeableConcept]
}

type AuditEventDetail {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: String
  valueString: String
  valueBase64Binary: Base64Binary
}

type AuditEventEntityWhatReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type AuditEventEntity {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  what: AuditEventEntityWhatReference
  type: Coding
  role: Coding
  lifecycle: Coding
  securityLabel: [Coding]
  name: String
  description: String
  query: Base64Binary
  detail: [AuditEventDetail]
}

type AuditEventNetwork {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  address: String
  type: Code
}

union AuditEventSourceObserver = PractitionerRole | Practitioner | Organization | Device | Patient | RelatedPerson

type AuditEventSourceObserverReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AuditEventSourceObserver
  type: URI
  identifier: Identifier
  display: String
}

type AuditEventSource {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  site: String
  observer: AuditEventSourceObserverReference
  type: [Coding]
}

union BiologicallyDerivedProductCollectionCollector = Practitioner | PractitionerRole

type BiologicallyDerivedProductCollectionCollectorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: BiologicallyDerivedProductCollectionCollector
  type: URI
  identifier: Identifier
  display: String
}

union BiologicallyDerivedProductCollectionSource = Patient | Organization

type BiologicallyDerivedProductCollectionSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: BiologicallyDerivedProductCollectionSource
  type: URI
  identifier: Identifier
  display: String
}

type BiologicallyDerivedProductCollection {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  collector: BiologicallyDerivedProductCollectionCollectorReference
  source: BiologicallyDerivedProductCollectionSourceReference
  collectedDateTime: DateTime
  collectedPeriod: Period
}

type BiologicallyDerivedProductManipulation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  timeDateTime: DateTime
  timePeriod: Period
}

type BiologicallyDerivedProductProcessingAdditiveReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Substance
  type: URI
  identifier: Identifier
  display: String
}

type BiologicallyDerivedProductProcessing {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  procedure: CodeableConcept
  additive: BiologicallyDerivedProductProcessingAdditiveReference
  timeDateTime: DateTime
  timePeriod: Period
}

type BiologicallyDerivedProductStorage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  temperature: Float
  scale: Code
  duration: Period
}

type BundleEntry {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  link: [BundleLink]
  fullUrl: URI
  resource: Resource
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type BundleLink {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  relation: String
  url: URI
}

type BundleRequest {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  method: Code
  url: URI
  ifNoneMatch: String
  ifModifiedSince: Instant
  ifMatch: String
  ifNoneExist: String
}

type BundleResponse {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  status: String
  location: URI
  etag: String
  lastModified: Instant
  outcome: Resource
}

type BundleSearch {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  mode: Code
  score: Float
}

type CapabilityStatementDocument {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  mode: Code
  documentation: Markdown
  profile: Canonical
}

type CapabilityStatementEndpoint {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  protocol: Coding
  address: URL
}

type CapabilityStatementImplementationCustodianReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type CapabilityStatementImplementation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  url: URL
  custodian: CapabilityStatementImplementationCustodianReference
}

type CapabilityStatementInteraction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  documentation: Markdown
}

type CapabilityStatementInteraction1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  documentation: Markdown
}

type CapabilityStatementMessaging {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  endpoint: [CapabilityStatementEndpoint]
  reliableCache: Int
  documentation: Markdown
  supportedMessage: [CapabilityStatementSupportedMessage]
}

type CapabilityStatementOperation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  definition: Canonical
  documentation: Markdown
}

type CapabilityStatementResource {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  profile: Canonical
  supportedProfile: [Canonical]
  documentation: Markdown
  interaction: [CapabilityStatementInteraction]
  versioning: Code
  readHistory: Boolean
  updateCreate: Boolean
  conditionalCreate: Boolean
  conditionalRead: Code
  conditionalUpdate: Boolean
  conditionalDelete: Code
  referencePolicy: [Code]
  searchInclude: [String]
  searchRevInclude: [String]
  searchParam: [CapabilityStatementSearchParam]
  operation: [CapabilityStatementOperation]
}

type CapabilityStatementRest {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  mode: Code
  documentation: Markdown
  security: CapabilityStatementSecurity
  resource: [CapabilityStatementResource]
  interaction: [CapabilityStatementInteraction1]
  searchParam: [CapabilityStatementSearchParam]
  operation: [CapabilityStatementOperation]
  compartment: [Canonical]
}

type CapabilityStatementSearchParam {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  definition: Canonical
  type: Code
  documentation: Markdown
}

type CapabilityStatementSecurity {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  cors: Boolean
  service: [CodeableConcept]
  description: Markdown
}

type CapabilityStatementSoftware {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  version: String
  releaseDate: DateTime
}

type CapabilityStatementSupportedMessage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  mode: Code
  definition: Canonical
}

type CarePlanActivityOutcomeReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union CarePlanActivityReference = Appointment | CommunicationRequest | DeviceRequest | MedicationRequest | NutritionOrder | Task | ServiceRequest | VisionPrescription | RequestGroup

type CarePlanActivityReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CarePlanActivityReference
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanActivity {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  outcomeCodeableConcept: [CodeableConcept]
  outcomeReference: [CarePlanActivityOutcomeReferenceReference]
  progress: [Annotation]
  reference: CarePlanActivityReferenceReference
  detail: CarePlanDetail
}

union CarePlanDetailReasonReference = Condition | Observation | DiagnosticReport | DocumentReference

type CarePlanDetailReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CarePlanDetailReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanDetailGoalReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Goal
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanDetailLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

union CarePlanDetailPerformer = Practitioner | PractitionerRole | Organization | RelatedPerson | Patient | CareTeam | HealthcareService | Device

type CarePlanDetailPerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CarePlanDetailPerformer
  type: URI
  identifier: Identifier
  display: String
}

union CarePlanDetailProductReference = Medication | Substance

type CarePlanDetailProductReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CarePlanDetailProductReference
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanDetail {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  kind: Code
  instantiatesCanonical: [Canonical]
  instantiatesUri: [URI]
  code: CodeableConcept
  reasonCode: [CodeableConcept]
  reasonReference: [CarePlanDetailReasonReferenceReference]
  goal: [CarePlanDetailGoalReference]
  status: Code
  statusReason: CodeableConcept
  doNotPerform: Boolean
  scheduledTiming: Timing
  scheduledPeriod: Period
  scheduledString: String
  location: CarePlanDetailLocationReference
  performer: [CarePlanDetailPerformerReference]
  productCodeableConcept: CodeableConcept
  productReference: CarePlanDetailProductReferenceReference
  dailyAmount: Quantity
  quantity: Quantity
  description: String
}

union CareTeamParticipantMember = Practitioner | PractitionerRole | RelatedPerson | Patient | Organization | CareTeam

type CareTeamParticipantMemberReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CareTeamParticipantMember
  type: URI
  identifier: Identifier
  display: String
}

type CareTeamParticipantOnBehalfOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type CareTeamParticipant {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  role: [CodeableConcept]
  member: CareTeamParticipantMemberReference
  onBehalfOf: CareTeamParticipantOnBehalfOfReference
  period: Period
}

type CatalogEntryRelatedEntryItemReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CatalogEntry
  type: URI
  identifier: Identifier
  display: String
}

type CatalogEntryRelatedEntry {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  relationtype: Code
  item: CatalogEntryRelatedEntryItemReference
}

type ChargeItemDefinitionApplicability {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  language: String
  expression: String
}

type ChargeItemDefinitionPriceComponent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  code: CodeableConcept
  factor: Float
  amount: Money
}

type ChargeItemDefinitionPropertyGroup {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  applicability: [ChargeItemDefinitionApplicability]
  priceComponent: [ChargeItemDefinitionPriceComponent]
}

union ChargeItemPerformerActor = Practitioner | PractitionerRole | Organization | CareTeam | Patient | Device | RelatedPerson

type ChargeItemPerformerActorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ChargeItemPerformerActor
  type: URI
  identifier: Identifier
  display: String
}

type ChargeItemPerformer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  function: CodeableConcept
  actor: ChargeItemPerformerActorReference
}

type CitationAbstract {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  language: CodeableConcept
  text: Markdown
  copyright: Markdown
}

type CitationAffiliationInfo {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  affiliation: String
  role: String
  identifier: [Identifier]
}

type CitationCitedArtifact {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  relatedIdentifier: [Identifier]
  dateAccessed: DateTime
  version: CitationVersion
  currentState: [CodeableConcept]
  statusDate: [CitationStatusDate1]
  title: [CitationTitle]
  abstract: [CitationAbstract]
  part: CitationPart
  relatesTo: [CitationRelatesTo1]
  publicationForm: [CitationPublicationForm]
  webLocation: [CitationWebLocation]
  classification: [CitationClassification1]
  contributorship: CitationContributorship
  note: [Annotation]
}

type CitationClassification {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  classifier: [CodeableConcept]
}

type CitationClassification1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  classifier: [CodeableConcept]
  whoClassified: CitationWhoClassified
}

type CitationContributionInstance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  time: DateTime
}

type CitationContributorship {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  complete: Boolean
  entry: [CitationEntry]
  summary: [CitationSummary1]
}

type CitationDateOfPublication {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  date: Date
  year: String
  month: String
  day: String
  season: String
  text: String
}

type CitationEntry {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: HumanName
  initials: String
  collectiveName: String
  identifier: [Identifier]
  affiliationInfo: [CitationAffiliationInfo]
  address: [Address]
  telecom: [ContactPoint]
  contributionType: [CodeableConcept]
  role: CodeableConcept
  contributionInstance: [CitationContributionInstance]
  correspondingContact: Boolean
  listOrder: Int
}

type CitationPartBaseCitationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Citation
  type: URI
  identifier: Identifier
  display: String
}

type CitationPart {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  value: String
  baseCitation: CitationPartBaseCitationReference
}

type CitationPeriodicRelease {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  citedMedium: CodeableConcept
  volume: String
  issue: String
  dateOfPublication: CitationDateOfPublication
}

type CitationPublicationForm {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  publishedIn: CitationPublishedIn
  periodicRelease: CitationPeriodicRelease
  articleDate: DateTime
  lastRevisionDate: DateTime
  language: [CodeableConcept]
  accessionNumber: String
  pageString: String
  firstPage: String
  lastPage: String
  pageCount: String
  copyright: Markdown
}

type CitationPublishedInPublisherReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type CitationPublishedIn {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  identifier: [Identifier]
  title: String
  publisher: CitationPublishedInPublisherReference
  publisherLocation: String
}

type CitationRelatesToTargetReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CitationRelatesTo {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  relationshipType: CodeableConcept
  targetClassifier: [CodeableConcept]
  targetUri: URI
  targetIdentifier: Identifier
  targetReference: CitationRelatesToTargetReferenceReference
  targetAttachment: Attachment
}

type CitationRelatesTo1TargetReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CitationRelatesTo1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  relationshipType: CodeableConcept
  targetClassifier: [CodeableConcept]
  targetUri: URI
  targetIdentifier: Identifier
  targetReference: CitationRelatesTo1TargetReferenceReference
  targetAttachment: Attachment
}

type CitationStatusDate {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  activity: CodeableConcept
  actual: Boolean
  period: Period
}

type CitationStatusDate1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  activity: CodeableConcept
  actual: Boolean
  period: Period
}

type CitationSummary {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  style: CodeableConcept
  text: Markdown
}

type CitationSummary1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  style: CodeableConcept
  source: CodeableConcept
  value: Markdown
}

type CitationTitle {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: [CodeableConcept]
  language: CodeableConcept
  text: Markdown
}

type CitationVersionBaseCitationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Citation
  type: URI
  identifier: Identifier
  display: String
}

type CitationVersion {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  value: String
  baseCitation: CitationVersionBaseCitationReference
}

type CitationWebLocation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  url: URI
}

union CitationWhoClassifiedPerson = Person | Practitioner

type CitationWhoClassifiedPersonReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CitationWhoClassifiedPerson
  type: URI
  identifier: Identifier
  display: String
}

type CitationWhoClassifiedOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type CitationWhoClassifiedPublisherReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type CitationWhoClassified {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  person: CitationWhoClassifiedPersonReference
  organization: CitationWhoClassifiedOrganizationReference
  publisher: CitationWhoClassifiedPublisherReference
  classifierCopyright: String
  freeToShare: Boolean
}

type ClaimAccidentLocationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type ClaimAccident {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  date: Date
  type: CodeableConcept
  locationAddress: Address
  locationReference: ClaimAccidentLocationReferenceReference
}

union ClaimCareTeamProvider = Practitioner | PractitionerRole | Organization

type ClaimCareTeamProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimCareTeamProvider
  type: URI
  identifier: Identifier
  display: String
}

type ClaimCareTeam {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  provider: ClaimCareTeamProviderReference
  responsible: Boolean
  role: CodeableConcept
  qualification: CodeableConcept
}

type ClaimDetailUdiReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type ClaimDetail {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  revenue: CodeableConcept
  category: CodeableConcept
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  programCode: [CodeableConcept]
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  udi: [ClaimDetailUdiReference]
  subDetail: [ClaimSubDetail]
}

type ClaimDiagnosisDiagnosisReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Condition
  type: URI
  identifier: Identifier
  display: String
}

type ClaimDiagnosis {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  diagnosisCodeableConcept: CodeableConcept
  diagnosisReference: ClaimDiagnosisDiagnosisReferenceReference
  type: [CodeableConcept]
  onAdmission: CodeableConcept
  packageCode: CodeableConcept
}

type ClaimInsuranceCoverageReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Coverage
  type: URI
  identifier: Identifier
  display: String
}

type ClaimInsuranceClaimResponseReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimResponse
  type: URI
  identifier: Identifier
  display: String
}

type ClaimInsurance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  focal: Boolean
  identifier: Identifier
  coverage: ClaimInsuranceCoverageReference
  businessArrangement: String
  preAuthRef: [String]
  claimResponse: ClaimInsuranceClaimResponseReference
}

type ClaimItemLocationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type ClaimItemUdiReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type ClaimItemEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

type ClaimItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  careTeamSequence: [Int]
  diagnosisSequence: [Int]
  procedureSequence: [Int]
  informationSequence: [Int]
  revenue: CodeableConcept
  category: CodeableConcept
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  programCode: [CodeableConcept]
  servicedDate: Date
  servicedPeriod: Period
  locationCodeableConcept: CodeableConcept
  locationAddress: Address
  locationReference: ClaimItemLocationReferenceReference
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  udi: [ClaimItemUdiReference]
  bodySite: CodeableConcept
  subSite: [CodeableConcept]
  encounter: [ClaimItemEncounterReference]
  detail: [ClaimDetail]
}

union ClaimPayeeParty = Practitioner | PractitionerRole | Organization | Patient | RelatedPerson

type ClaimPayeePartyReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimPayeeParty
  type: URI
  identifier: Identifier
  display: String
}

type ClaimPayee {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  party: ClaimPayeePartyReference
}

type ClaimProcedureProcedureReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Procedure
  type: URI
  identifier: Identifier
  display: String
}

type ClaimProcedureUdiReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type ClaimProcedure {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  type: [CodeableConcept]
  date: DateTime
  procedureCodeableConcept: CodeableConcept
  procedureReference: ClaimProcedureProcedureReferenceReference
  udi: [ClaimProcedureUdiReference]
}

type ClaimRelatedClaimReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Claim
  type: URI
  identifier: Identifier
  display: String
}

type ClaimRelated {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  claim: ClaimRelatedClaimReference
  relationship: CodeableConcept
  reference: Identifier
}

union ClaimResponseAddItemProvider = Practitioner | PractitionerRole | Organization

type ClaimResponseAddItemProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimResponseAddItemProvider
  type: URI
  identifier: Identifier
  display: String
}

type ClaimResponseAddItemLocationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type ClaimResponseAddItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  itemSequence: [Int]
  detailSequence: [Int]
  subdetailSequence: [Int]
  provider: [ClaimResponseAddItemProviderReference]
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  programCode: [CodeableConcept]
  servicedDate: Date
  servicedPeriod: Period
  locationCodeableConcept: CodeableConcept
  locationAddress: Address
  locationReference: ClaimResponseAddItemLocationReferenceReference
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  bodySite: CodeableConcept
  subSite: [CodeableConcept]
  noteNumber: [Int]
  adjudication: [ClaimResponseAdjudication]
  detail: [ClaimResponseDetail1]
}

type ClaimResponseAdjudication {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  category: CodeableConcept
  reason: CodeableConcept
  amount: Money
  value: Float
}

type ClaimResponseDetail {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  detailSequence: Int
  noteNumber: [Int]
  adjudication: [ClaimResponseAdjudication]
  subDetail: [ClaimResponseSubDetail]
}

type ClaimResponseDetail1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  noteNumber: [Int]
  adjudication: [ClaimResponseAdjudication]
  subDetail: [ClaimResponseSubDetail1]
}

type ClaimResponseError {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  itemSequence: Int
  detailSequence: Int
  subDetailSequence: Int
  code: CodeableConcept
}

type ClaimResponseInsuranceCoverageReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Coverage
  type: URI
  identifier: Identifier
  display: String
}

type ClaimResponseInsuranceClaimResponseReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimResponse
  type: URI
  identifier: Identifier
  display: String
}

type ClaimResponseInsurance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  focal: Boolean
  coverage: ClaimResponseInsuranceCoverageReference
  businessArrangement: String
  claimResponse: ClaimResponseInsuranceClaimResponseReference
}

type ClaimResponseItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  itemSequence: Int
  noteNumber: [Int]
  adjudication: [ClaimResponseAdjudication]
  detail: [ClaimResponseDetail]
}

type ClaimResponsePayment {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  adjustment: Money
  adjustmentReason: CodeableConcept
  date: Date
  amount: Money
  identifier: Identifier
}

type ClaimResponseProcessNote {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  number: Int
  type: Code
  text: String
  language: CodeableConcept
}

type ClaimResponseSubDetail {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  subDetailSequence: Int
  noteNumber: [Int]
  adjudication: [ClaimResponseAdjudication]
}

type ClaimResponseSubDetail1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  noteNumber: [Int]
  adjudication: [ClaimResponseAdjudication]
}

type ClaimResponseTotal {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  category: CodeableConcept
  amount: Money
}

type ClaimSubDetailUdiReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type ClaimSubDetail {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  revenue: CodeableConcept
  category: CodeableConcept
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  programCode: [CodeableConcept]
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  udi: [ClaimSubDetailUdiReference]
}

type ClaimSupportingInfoValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ClaimSupportingInfo {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  category: CodeableConcept
  code: CodeableConcept
  timingDate: Date
  timingPeriod: Period
  valueBoolean: Boolean
  valueString: String
  valueQuantity: Quantity
  valueAttachment: Attachment
  valueReference: ClaimSupportingInfoValueReferenceReference
  reason: CodeableConcept
}

union ClinicalImpressionFindingItemReference = Condition | Observation | Media

type ClinicalImpressionFindingItemReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalImpressionFindingItemReference
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalImpressionFinding {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  itemCodeableConcept: CodeableConcept
  itemReference: ClinicalImpressionFindingItemReferenceReference
  basis: String
}

union ClinicalImpressionInvestigationItem = Observation | QuestionnaireResponse | FamilyMemberHistory | DiagnosticReport | RiskAssessment | ImagingStudy | Media

type ClinicalImpressionInvestigationItemReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalImpressionInvestigationItem
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalImpressionInvestigation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  item: [ClinicalImpressionInvestigationItemReference]
}

type ClinicalUseDefinitionContraindicationDiseaseSymptomProcedureReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionContraindicationDiseaseStatusReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionContraindicationComorbidityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionContraindicationIndicationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalUseDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionContraindication {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  diseaseSymptomProcedure: ClinicalUseDefinitionContraindicationDiseaseSymptomProcedureReference
  diseaseStatus: ClinicalUseDefinitionContraindicationDiseaseStatusReference
  comorbidity: [ClinicalUseDefinitionContraindicationComorbidityReference]
  indication: [ClinicalUseDefinitionContraindicationIndicationReference]
  otherTherapy: [ClinicalUseDefinitionOtherTherapy]
}

type ClinicalUseDefinitionIndicationDiseaseSymptomProcedureReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionIndicationDiseaseStatusReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionIndicationComorbidityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionIndicationIntendedEffectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionIndicationUndesirableEffectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalUseDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionIndication {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  diseaseSymptomProcedure: ClinicalUseDefinitionIndicationDiseaseSymptomProcedureReference
  diseaseStatus: ClinicalUseDefinitionIndicationDiseaseStatusReference
  comorbidity: [ClinicalUseDefinitionIndicationComorbidityReference]
  intendedEffect: ClinicalUseDefinitionIndicationIntendedEffectReference
  durationRange: Range
  durationString: String
  undesirableEffect: [ClinicalUseDefinitionIndicationUndesirableEffectReference]
  otherTherapy: [ClinicalUseDefinitionOtherTherapy]
}

union ClinicalUseDefinitionInteractantItemReference = MedicinalProductDefinition | Medication | Substance | ObservationDefinition

type ClinicalUseDefinitionInteractantItemReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalUseDefinitionInteractantItemReference
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionInteractant {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  itemReference: ClinicalUseDefinitionInteractantItemReferenceReference
  itemCodeableConcept: CodeableConcept
}

type ClinicalUseDefinitionInteractionEffectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionInteraction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  interactant: [ClinicalUseDefinitionInteractant]
  type: CodeableConcept
  effect: ClinicalUseDefinitionInteractionEffectReference
  incidence: CodeableConcept
  management: [CodeableConcept]
}

union ClinicalUseDefinitionOtherTherapyTherapy = MedicinalProductDefinition | Medication | Substance | SubstanceDefinition | ActivityDefinition

type ClinicalUseDefinitionOtherTherapyTherapyReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalUseDefinitionOtherTherapyTherapy
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionOtherTherapy {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  relationshipType: CodeableConcept
  therapy: ClinicalUseDefinitionOtherTherapyTherapyReference
}

type ClinicalUseDefinitionUndesirableEffectSymptomConditionEffectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionUndesirableEffect {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  symptomConditionEffect: ClinicalUseDefinitionUndesirableEffectSymptomConditionEffectReference
  classification: CodeableConcept
  frequencyOfOccurrence: CodeableConcept
}

type ClinicalUseDefinitionWarning {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: Markdown
  code: CodeableConcept
}

type CodeSystemConcept {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  display: String
  definition: String
  designation: [CodeSystemDesignation]
  property: [CodeSystemProperty1]
  concept: [CodeSystemConcept]
}

type CodeSystemDesignation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  language: Code
  use: Coding
  value: String
}

type CodeSystemFilter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  description: String
  operator: [Code]
  value: String
}

type CodeSystemProperty {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  uri: URI
  description: String
  type: Code
}

type CodeSystemProperty1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  valueCode: Code
  valueCoding: Coding
  valueString: String
  valueInteger: Int
  valueBoolean: Boolean
  valueDateTime: DateTime
  valueDecimal: Float
}

type CommunicationPayloadContentReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CommunicationPayload {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  contentString: String
  contentAttachment: Attachment
  contentReference: CommunicationPayloadContentReferenceReference
}

type CommunicationRequestPayloadContentReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CommunicationRequestPayload {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  contentString: String
  contentAttachment: Attachment
  contentReference: CommunicationRequestPayloadContentReferenceReference
}

type CompartmentDefinitionResource {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  param: [String]
  documentation: String
}

union CompositionAttesterParty = Patient | RelatedPerson | Practitioner | PractitionerRole | Organization

type CompositionAttesterPartyReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CompositionAttesterParty
  type: URI
  identifier: Identifier
  display: String
}

type CompositionAttester {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  mode: Code
  time: DateTime
  party: CompositionAttesterPartyReference
}

type CompositionEventDetailReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CompositionEvent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: [CodeableConcept]
  period: Period
  detail: [CompositionEventDetailReference]
}

type CompositionRelatesToTargetReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Composition
  type: URI
  identifier: Identifier
  display: String
}

type CompositionRelatesTo {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  targetIdentifier: Identifier
  targetReference: CompositionRelatesToTargetReferenceReference
}

union CompositionSectionAuthor = Practitioner | PractitionerRole | Device | Patient | RelatedPerson | Organization

type CompositionSectionAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CompositionSectionAuthor
  type: URI
  identifier: Identifier
  display: String
}

type CompositionSectionFocusReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CompositionSectionEntryReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CompositionSection {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  title: String
  code: CodeableConcept
  author: [CompositionSectionAuthorReference]
  focus: CompositionSectionFocusReference
  text: Narrative
  mode: Code
  orderedBy: CodeableConcept
  entry: [CompositionSectionEntryReference]
  emptyReason: CodeableConcept
  section: [CompositionSection]
}

type ConceptMapDependsOn {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  property: URI
  system: Canonical
  value: String
  display: String
}

type ConceptMapElement {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  display: String
  target: [ConceptMapTarget]
}

type ConceptMapGroup {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  source: URI
  sourceVersion: String
  target: URI
  targetVersion: String
  element: [ConceptMapElement]
  unmapped: ConceptMapUnmapped
}

type ConceptMapTarget {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  display: String
  equivalence: Code
  comment: String
  dependsOn: [ConceptMapDependsOn]
  product: [ConceptMapDependsOn]
}

type ConceptMapUnmapped {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  mode: Code
  code: Code
  display: String
  url: Canonical
}

type ConditionEvidenceDetailReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ConditionEvidence {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: [CodeableConcept]
  detail: [ConditionEvidenceDetailReference]
}

union ConditionStageAssessment = ClinicalImpression | DiagnosticReport | Observation

type ConditionStageAssessmentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ConditionStageAssessment
  type: URI
  identifier: Identifier
  display: String
}

type ConditionStage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  summary: CodeableConcept
  assessment: [ConditionStageAssessmentReference]
  type: CodeableConcept
}

union ConsentActorReference = Device | Group | CareTeam | Organization | Patient | Practitioner | RelatedPerson | PractitionerRole

type ConsentActorReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ConsentActorReference
  type: URI
  identifier: Identifier
  display: String
}

type ConsentActor {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  role: CodeableConcept
  reference: ConsentActorReferenceReference
}

type ConsentDataReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ConsentData {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  meaning: Code
  reference: ConsentDataReferenceReference
}

type ConsentPolicy {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  authority: URI
  uri: URI
}

type ConsentProvision {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  period: Period
  actor: [ConsentActor]
  action: [CodeableConcept]
  securityLabel: [Coding]
  purpose: [Coding]
  class: [Coding]
  code: [CodeableConcept]
  dataPeriod: Period
  data: [ConsentData]
  provision: [ConsentProvision]
}

union ConsentVerificationVerifiedWith = Patient | RelatedPerson

type ConsentVerificationVerifiedWithReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ConsentVerificationVerifiedWith
  type: URI
  identifier: Identifier
  display: String
}

type ConsentVerification {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  verified: Boolean
  verifiedWith: ConsentVerificationVerifiedWithReference
  verificationDate: DateTime
}

union ContractActionContext = Encounter | EpisodeOfCare

type ContractActionContextReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractActionContext
  type: URI
  identifier: Identifier
  display: String
}

union ContractActionRequester = Patient | RelatedPerson | Practitioner | PractitionerRole | Device | Group | Organization

type ContractActionRequesterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractActionRequester
  type: URI
  identifier: Identifier
  display: String
}

union ContractActionPerformer = RelatedPerson | Patient | Practitioner | PractitionerRole | CareTeam | Device | Substance | Organization | Location

type ContractActionPerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractActionPerformer
  type: URI
  identifier: Identifier
  display: String
}

union ContractActionReasonReference = Condition | Observation | DiagnosticReport | DocumentReference | Questionnaire | QuestionnaireResponse

type ContractActionReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractActionReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type ContractAction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  doNotPerform: Boolean
  type: CodeableConcept
  subject: [ContractSubject]
  intent: CodeableConcept
  linkId: [String]
  status: CodeableConcept
  context: ContractActionContextReference
  contextLinkId: [String]
  occurrenceDateTime: DateTime
  occurrencePeriod: Period
  occurrenceTiming: Timing
  requester: [ContractActionRequesterReference]
  requesterLinkId: [String]
  performerType: [CodeableConcept]
  performerRole: CodeableConcept
  performer: ContractActionPerformerReference
  performerLinkId: [String]
  reasonCode: [CodeableConcept]
  reasonReference: [ContractActionReasonReferenceReference]
  reason: [String]
  reasonLinkId: [String]
  note: [Annotation]
  securityLabelNumber: [Int]
}

type ContractAnswerValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ContractAnswer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  valueBoolean: Boolean
  valueDecimal: Float
  valueInteger: Int
  valueDate: Date
  valueDateTime: DateTime
  valueTime: Time
  valueString: String
  valueUri: URI
  valueAttachment: Attachment
  valueCoding: Coding
  valueQuantity: Quantity
  valueReference: ContractAnswerValueReferenceReference
}

type ContractAssetTypeReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ContractAsset {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  scope: CodeableConcept
  type: [CodeableConcept]
  typeReference: [ContractAssetTypeReferenceReference]
  subtype: [CodeableConcept]
  relationship: Coding
  context: [ContractContext]
  condition: String
  periodType: [CodeableConcept]
  period: [Period]
  usePeriod: [Period]
  text: String
  linkId: [String]
  answer: [ContractAnswer]
  securityLabelNumber: [Int]
  valuedItem: [ContractValuedItem]
}

union ContractContentDefinitionPublisher = Practitioner | PractitionerRole | Organization

type ContractContentDefinitionPublisherReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractContentDefinitionPublisher
  type: URI
  identifier: Identifier
  display: String
}

type ContractContentDefinition {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  subType: CodeableConcept
  publisher: ContractContentDefinitionPublisherReference
  publicationDate: DateTime
  publicationStatus: Code
  copyright: Markdown
}

type ContractContextReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ContractContext {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  reference: ContractContextReferenceReference
  code: [CodeableConcept]
  text: String
}

union ContractFriendlyContentReference = Composition | DocumentReference | QuestionnaireResponse

type ContractFriendlyContentReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractFriendlyContentReference
  type: URI
  identifier: Identifier
  display: String
}

type ContractFriendly {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  contentAttachment: Attachment
  contentReference: ContractFriendlyContentReferenceReference
}

union ContractLegalContentReference = Composition | DocumentReference | QuestionnaireResponse

type ContractLegalContentReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractLegalContentReference
  type: URI
  identifier: Identifier
  display: String
}

type ContractLegal {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  contentAttachment: Attachment
  contentReference: ContractLegalContentReferenceReference
}

type ContractOfferTopicReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ContractOffer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  party: [ContractParty]
  topic: ContractOfferTopicReference
  type: CodeableConcept
  decision: CodeableConcept
  decisionMode: [CodeableConcept]
  answer: [ContractAnswer]
  text: String
  linkId: [String]
  securityLabelNumber: [Int]
}

union ContractPartyReference = Patient | RelatedPerson | Practitioner | PractitionerRole | Device | Group | Organization

type ContractPartyReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractPartyReference
  type: URI
  identifier: Identifier
  display: String
}

type ContractParty {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  reference: [ContractPartyReferenceReference]
  role: CodeableConcept
}

type ContractRuleContentReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReference
  type: URI
  identifier: Identifier
  display: String
}

type ContractRule {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  contentAttachment: Attachment
  contentReference: ContractRuleContentReferenceReference
}

type ContractSecurityLabel {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  number: [Int]
  classification: Coding
  category: [Coding]
  control: [Coding]
}

union ContractSignerParty = Organization | Patient | Practitioner | PractitionerRole | RelatedPerson

type ContractSignerPartyReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractSignerParty
  type: URI
  identifier: Identifier
  display: String
}

type ContractSigner {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Coding
  party: ContractSignerPartyReference
  signature: [Signature]
}

union ContractSubjectReference = Patient | RelatedPerson | Practitioner | PractitionerRole | Device | Group | Organization

type ContractSubjectReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractSubjectReference
  type: URI
  identifier: Identifier
  display: String
}

type ContractSubject {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  reference: [ContractSubjectReferenceReference]
  role: CodeableConcept
}

type ContractTermTopicReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ContractTerm {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  issued: DateTime
  applies: Period
  topicCodeableConcept: CodeableConcept
  topicReference: ContractTermTopicReferenceReference
  type: CodeableConcept
  subType: CodeableConcept
  text: String
  securityLabel: [ContractSecurityLabel]
  offer: ContractOffer
  asset: [ContractAsset]
  action: [ContractAction]
  group: [ContractTerm]
}

type ContractValuedItemEntityReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union ContractValuedItemResponsible = Organization | Patient | Practitioner | PractitionerRole | RelatedPerson

type ContractValuedItemResponsibleReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractValuedItemResponsible
  type: URI
  identifier: Identifier
  display: String
}

union ContractValuedItemRecipient = Organization | Patient | Practitioner | PractitionerRole | RelatedPerson

type ContractValuedItemRecipientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractValuedItemRecipient
  type: URI
  identifier: Identifier
  display: String
}

type ContractValuedItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  entityCodeableConcept: CodeableConcept
  entityReference: ContractValuedItemEntityReferenceReference
  identifier: Identifier
  effectiveTime: DateTime
  quantity: Quantity
  unitPrice: Money
  factor: Float
  points: Float
  net: Money
  payment: String
  paymentDate: DateTime
  responsible: ContractValuedItemResponsibleReference
  recipient: ContractValuedItemRecipientReference
  linkId: [String]
  securityLabelNumber: [Int]
}

type CoverageClass {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  value: String
  name: String
}

type CoverageCostToBeneficiary {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueQuantity: Quantity
  valueMoney: Money
  exception: [CoverageException]
}

type CoverageEligibilityRequestDiagnosisDiagnosisReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Condition
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityRequestDiagnosis {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  diagnosisCodeableConcept: CodeableConcept
  diagnosisReference: CoverageEligibilityRequestDiagnosisDiagnosisReferenceReference
}

type CoverageEligibilityRequestInsuranceCoverageReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Coverage
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityRequestInsurance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  focal: Boolean
  coverage: CoverageEligibilityRequestInsuranceCoverageReference
  businessArrangement: String
}

union CoverageEligibilityRequestItemProvider = Practitioner | PractitionerRole

type CoverageEligibilityRequestItemProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CoverageEligibilityRequestItemProvider
  type: URI
  identifier: Identifier
  display: String
}

union CoverageEligibilityRequestItemFacility = Location | Organization

type CoverageEligibilityRequestItemFacilityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CoverageEligibilityRequestItemFacility
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityRequestItemDetailReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityRequestItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  supportingInfoSequence: [Int]
  category: CodeableConcept
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  provider: CoverageEligibilityRequestItemProviderReference
  quantity: Quantity
  unitPrice: Money
  facility: CoverageEligibilityRequestItemFacilityReference
  diagnosis: [CoverageEligibilityRequestDiagnosis]
  detail: [CoverageEligibilityRequestItemDetailReference]
}

type CoverageEligibilityRequestSupportingInfoInformationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityRequestSupportingInfo {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  information: CoverageEligibilityRequestSupportingInfoInformationReference
  appliesToAll: Boolean
}

type CoverageEligibilityResponseBenefit {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  allowedUnsignedInt: Int
  allowedString: String
  allowedMoney: Money
  usedUnsignedInt: Int
  usedString: String
  usedMoney: Money
}

type CoverageEligibilityResponseError {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
}

type CoverageEligibilityResponseInsuranceCoverageReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Coverage
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityResponseInsurance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  coverage: CoverageEligibilityResponseInsuranceCoverageReference
  inforce: Boolean
  benefitPeriod: Period
  item: [CoverageEligibilityResponseItem]
}

union CoverageEligibilityResponseItemProvider = Practitioner | PractitionerRole

type CoverageEligibilityResponseItemProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CoverageEligibilityResponseItemProvider
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityResponseItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  category: CodeableConcept
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  provider: CoverageEligibilityResponseItemProviderReference
  excluded: Boolean
  name: String
  description: String
  network: CodeableConcept
  unit: CodeableConcept
  term: CodeableConcept
  benefit: [CoverageEligibilityResponseBenefit]
  authorizationRequired: Boolean
  authorizationSupporting: [CodeableConcept]
  authorizationUrl: URI
}

type CoverageException {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  period: Period
}

type DetectedIssueEvidenceDetailReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type DetectedIssueEvidence {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: [CodeableConcept]
  detail: [DetectedIssueEvidenceDetailReference]
}

union DetectedIssueMitigationAuthor = Practitioner | PractitionerRole

type DetectedIssueMitigationAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DetectedIssueMitigationAuthor
  type: URI
  identifier: Identifier
  display: String
}

type DetectedIssueMitigation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  action: CodeableConcept
  date: DateTime
  author: DetectedIssueMitigationAuthorReference
}

type DeviceDefinitionCapability {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  description: [CodeableConcept]
}

type DeviceDefinitionDeviceName {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  type: Code
}

type DeviceDefinitionMaterial {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  substance: CodeableConcept
  alternate: Boolean
  allergenicIndicator: Boolean
}

type DeviceDefinitionProperty {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueQuantity: [Quantity]
  valueCode: [CodeableConcept]
}

type DeviceDefinitionSpecialization {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  systemType: String
  version: String
}

type DeviceDefinitionUdiDeviceIdentifier {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  deviceIdentifier: String
  issuer: URI
  jurisdiction: URI
}

type DeviceDeviceName {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  type: Code
}

type DeviceMetricCalibration {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  state: Code
  time: Instant
}

type DeviceProperty {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueQuantity: [Quantity]
  valueCode: [CodeableConcept]
}

type DeviceRequestParameter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  valueCodeableConcept: CodeableConcept
  valueQuantity: Quantity
  valueRange: Range
  valueBoolean: Boolean
}

type DeviceSpecialization {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  systemType: CodeableConcept
  version: String
}

type DeviceUdiCarrier {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  deviceIdentifier: String
  issuer: URI
  jurisdiction: URI
  carrierAIDC: Base64Binary
  carrierHRF: String
  entryType: Code
}

type DeviceVersion {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  component: Identifier
  value: String
}

type DiagnosticReportMediaLinkReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Media
  type: URI
  identifier: Identifier
  display: String
}

type DiagnosticReportMedia {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  comment: String
  link: DiagnosticReportMediaLinkReference
}

type DocumentManifestRelatedRefReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type DocumentManifestRelated {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  ref: DocumentManifestRelatedRefReference
}

type DocumentReferenceContent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  attachment: DocumentReferenceAttachment
  format: Coding
}

union DocumentReferenceContextEncounter = Encounter | EpisodeOfCare

type DocumentReferenceContextEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReferenceContextEncounter
  type: URI
  identifier: Identifier
  display: String
}

type DocumentReferenceContextSourcePatientInfoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type DocumentReferenceContextRelatedReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type DocumentReferenceContext {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  encounter: [DocumentReferenceContextEncounterReference]
  event: [CodeableConcept]
  period: Period
  facilityType: CodeableConcept
  practiceSetting: CodeableConcept
  sourcePatientInfo: DocumentReferenceContextSourcePatientInfoReference
  related: [DocumentReferenceContextRelatedReference]
}

type DocumentReferenceRelatesToTargetReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReference
  type: URI
  identifier: Identifier
  display: String
}

type DocumentReferenceRelatesTo {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  target: DocumentReferenceRelatesToTargetReference
}

type Dosage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  text: String
  additionalInstruction: [CodeableConcept]
  patientInstruction: String
  timing: Timing
  asNeededBoolean: Boolean
  asNeededCodeableConcept: CodeableConcept
  site: CodeableConcept
  route: CodeableConcept
  method: CodeableConcept
  doseAndRate: [DosageDoseAndRate]
  maxDosePerPeriod: Ratio
  maxDosePerAdministration: Quantity
  maxDosePerLifetime: Quantity
}

type DosageDoseAndRate {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  doseRange: Range
  doseQuantity: Quantity
  rateRatio: Ratio
  rateRange: Range
  rateQuantity: Quantity
}

type ElementDefinitionDefaultValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ElementDefinitionFixedReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ElementDefinitionPatternReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ElementDefinition {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  path: String
  representation: [Code]
  sliceName: String
  sliceIsConstraining: Boolean
  label: String
  code: [Coding]
  slicing: ElementDefinitionSlicing
  short: String
  definition: Markdown
  comment: Markdown
  requirements: Markdown
  alias: [String]
  min: Int
  max: String
  base: ElementDefinitionBase
  contentReference: URI
  type: [ElementDefinitionType]
  defaultValueBase64Binary: Base64Binary
  defaultValueBoolean: Boolean
  defaultValueCanonical: Canonical
  defaultValueCode: Code
  defaultValueDate: Date
  defaultValueDateTime: DateTime
  defaultValueDecimal: Float
  defaultValueId: ID
  defaultValueInstant: Instant
  defaultValueInteger: Int
  defaultValueMarkdown: Markdown
  defaultValueOid: OID
  defaultValuePositiveInt: Int
  defaultValueString: String
  defaultValueTime: Time
  defaultValueUnsignedInt: Int
  defaultValueUri: URI
  defaultValueUrl: URL
  defaultValueUuid: UUID
  defaultValueAddress: Address
  defaultValueAge: Quantity
  defaultValueAnnotation: Annotation
  defaultValueAttachment: Attachment
  defaultValueCodeableConcept: CodeableConcept
  defaultValueCodeableReference: CodeableReference
  defaultValueCoding: Coding
  defaultValueContactPoint: ContactPoint
  defaultValueCount: Quantity
  defaultValueDistance: Quantity
  defaultValueDuration: Quantity
  defaultValueHumanName: HumanName
  defaultValueIdentifier: Identifier
  defaultValueMoney: Money
  defaultValuePeriod: Period
  defaultValueQuantity: Quantity
  defaultValueRange: Range
  defaultValueRatio: Ratio
  defaultValueRatioRange: RatioRange
  defaultValueReference: ElementDefinitionDefaultValueReferenceReference
  defaultValueSampledData: SampledData
  defaultValueSignature: Signature
  defaultValueTiming: Timing
  defaultValueContactDetail: ContactDetail
  defaultValueContributor: Contributor
  defaultValueDataRequirement: DataRequirement
  defaultValueExpression: Expression
  defaultValueParameterDefinition: ParameterDefinition
  defaultValueRelatedArtifact: RelatedArtifact
  defaultValueTriggerDefinition: TriggerDefinition
  defaultValueUsageContext: UsageContext
  defaultValueDosage: Dosage
  meaningWhenMissing: Markdown
  orderMeaning: String
  fixedBase64Binary: Base64Binary
  fixedBoolean: Boolean
  fixedCanonical: Canonical
  fixedCode: Code
  fixedDate: Date
  fixedDateTime: DateTime
  fixedDecimal: Float
  fixedId: ID
  fixedInstant: Instant
  fixedInteger: Int
  fixedMarkdown: Markdown
  fixedOid: OID
  fixedPositiveInt: Int
  fixedString: String
  fixedTime: Time
  fixedUnsignedInt: Int
  fixedUri: URI
  fixedUrl: URL
  fixedUuid: UUID
  fixedAddress: Address
  fixedAge: Quantity
  fixedAnnotation: Annotation
  fixedAttachment: Attachment
  fixedCodeableConcept: CodeableConcept
  fixedCodeableReference: CodeableReference
  fixedCoding: Coding
  fixedContactPoint: ContactPoint
  fixedCount: Quantity
  fixedDistance: Quantity
  fixedDuration: Quantity
  fixedHumanName: HumanName
  fixedIdentifier: Identifier
  fixedMoney: Money
  fixedPeriod: Period
  fixedQuantity: Quantity
  fixedRange: Range
  fixedRatio: Ratio
  fixedRatioRange: RatioRange
  fixedReference: ElementDefinitionFixedReferenceReference
  fixedSampledData: SampledData
  fixedSignature: Signature
  fixedTiming: Timing
  fixedContactDetail: ContactDetail
  fixedContributor: Contributor
  fixedDataRequirement: DataRequirement
  fixedExpression: Expression
  fixedParameterDefinition: ParameterDefinition
  fixedRelatedArtifact: RelatedArtifact
  fixedTriggerDefinition: TriggerDefinition
  fixedUsageContext: UsageContext
  fixedDosage: Dosage
  patternBase64Binary: Base64Binary
  patternBoolean: Boolean
  patternCanonical: Canonical
  patternCode: Code
  patternDate: Date
  patternDateTime: DateTime
  patternDecimal: Float
  patternId: ID
  patternInstant: Instant
  patternInteger: Int
  patternMarkdown: Markdown
  patternOid: OID
  patternPositiveInt: Int
  patternString: String
  patternTime: Time
  patternUnsignedInt: Int
  patternUri: URI
  patternUrl: URL
  patternUuid: UUID
  patternAddress: Address
  patternAge: Quantity
  patternAnnotation: Annotation
  patternAttachment: Attachment
  patternCodeableConcept: CodeableConcept
  patternCodeableReference: CodeableReference
  patternCoding: Coding
  patternContactPoint: ContactPoint
  patternCount: Quantity
  patternDistance: Quantity
  patternDuration: Quantity
  patternHumanName: HumanName
  patternIdentifier: Identifier
  patternMoney: Money
  patternPeriod: Period
  patternQuantity: Quantity
  patternRange: Range
  patternRatio: Ratio
  patternRatioRange: RatioRange
  patternReference: ElementDefinitionPatternReferenceReference
  patternSampledData: SampledData
  patternSignature: Signature
  patternTiming: Timing
  patternContactDetail: ContactDetail
  patternContributor: Contributor
  patternDataRequirement: DataRequirement
  patternExpression: Expression
  patternParameterDefinition: ParameterDefinition
  patternRelatedArtifact: RelatedArtifact
  patternTriggerDefinition: TriggerDefinition
  patternUsageContext: UsageContext
  patternDosage: Dosage
  example: [ElementDefinitionExample]
  minValueDate: Date
  minValueDateTime: DateTime
  minValueInstant: Instant
  minValueTime: Time
  minValueDecimal: Float
  minValueInteger: Int
  minValuePositiveInt: Int
  minValueUnsignedInt: Int
  minValueQuantity: Quantity
  maxValueDate: Date
  maxValueDateTime: DateTime
  maxValueInstant: Instant
  maxValueTime: Time
  maxValueDecimal: Float
  maxValueInteger: Int
  maxValuePositiveInt: Int
  maxValueUnsignedInt: Int
  maxValueQuantity: Quantity
  maxLength: Int
  condition: [ID]
  constraint: [ElementDefinitionConstraint]
  mustSupport: Boolean
  isModifier: Boolean
  isModifierReason: String
  isSummary: Boolean
  binding: ElementDefinitionBinding
  mapping: [ElementDefinitionMapping]
}

type ElementDefinitionBase {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  path: String
  min: Int
  max: String
}

type ElementDefinitionBinding {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  strength: Code
  description: String
  valueSet: Canonical
}

type ElementDefinitionConstraint {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  key: ID
  requirements: String
  severity: Code
  human: String
  expression: String
  xpath: String
  source: Canonical
}

type ElementDefinitionDiscriminator {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  path: String
}

type ElementDefinitionExampleValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ElementDefinitionExample {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  label: String
  valueBase64Binary: Base64Binary
  valueBoolean: Boolean
  valueCanonical: Canonical
  valueCode: Code
  valueDate: Date
  valueDateTime: DateTime
  valueDecimal: Float
  valueId: ID
  valueInstant: Instant
  valueInteger: Int
  valueMarkdown: Markdown
  valueOid: OID
  valuePositiveInt: Int
  valueString: String
  valueTime: Time
  valueUnsignedInt: Int
  valueUri: URI
  valueUrl: URL
  valueUuid: UUID
  valueAddress: Address
  valueAge: Quantity
  valueAnnotation: Annotation
  valueAttachment: Attachment
  valueCodeableConcept: CodeableConcept
  valueCodeableReference: CodeableReference
  valueCoding: Coding
  valueContactPoint: ContactPoint
  valueCount: Quantity
  valueDistance: Quantity
  valueDuration: Quantity
  valueHumanName: HumanName
  valueIdentifier: Identifier
  valueMoney: Money
  valuePeriod: Period
  valueQuantity: Quantity
  valueRange: Range
  valueRatio: Ratio
  valueRatioRange: RatioRange
  valueReference: ElementDefinitionExampleValueReferenceReference
  valueSampledData: SampledData
  valueSignature: Signature
  valueTiming: Timing
  valueContactDetail: ContactDetail
  valueContributor: Contributor
  valueDataRequirement: DataRequirement
  valueExpression: Expression
  valueParameterDefinition: ParameterDefinition
  valueRelatedArtifact: RelatedArtifact
  valueTriggerDefinition: TriggerDefinition
  valueUsageContext: UsageContext
  valueDosage: Dosage
}

type ElementDefinitionMapping {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identity: ID
  language: Code
  map: String
  comment: String
}

type ElementDefinitionSlicing {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  discriminator: [ElementDefinitionDiscriminator]
  description: String
  ordered: Boolean
  rules: Code
}

type ElementDefinitionType {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: URI
  profile: [Canonical]
  targetProfile: [Canonical]
  aggregation: [Code]
  versioning: Code
}

type EncounterClassHistory {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  class: Coding
  period: Period
}

union EncounterDiagnosisCondition = Condition | Procedure

type EncounterDiagnosisConditionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EncounterDiagnosisCondition
  type: URI
  identifier: Identifier
  display: String
}

type EncounterDiagnosis {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  condition: EncounterDiagnosisConditionReference
  use: CodeableConcept
  rank: Int
}

union EncounterHospitalizationOrigin = Location | Organization

type EncounterHospitalizationOriginReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EncounterHospitalizationOrigin
  type: URI
  identifier: Identifier
  display: String
}

union EncounterHospitalizationDestination = Location | Organization

type EncounterHospitalizationDestinationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EncounterHospitalizationDestination
  type: URI
  identifier: Identifier
  display: String
}

type EncounterHospitalization {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  preAdmissionIdentifier: Identifier
  origin: EncounterHospitalizationOriginReference
  admitSource: CodeableConcept
  reAdmission: CodeableConcept
  dietPreference: [CodeableConcept]
  specialCourtesy: [CodeableConcept]
  specialArrangement: [CodeableConcept]
  destination: EncounterHospitalizationDestinationReference
  dischargeDisposition: CodeableConcept
}

type EncounterLocationLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type EncounterLocation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  location: EncounterLocationLocationReference
  status: Code
  physicalType: CodeableConcept
  period: Period
}

union EncounterParticipantIndividual = Practitioner | PractitionerRole | RelatedPerson

type EncounterParticipantIndividualReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EncounterParticipantIndividual
  type: URI
  identifier: Identifier
  display: String
}

type EncounterParticipant {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: [CodeableConcept]
  period: Period
  individual: EncounterParticipantIndividualReference
}

type EncounterStatusHistory {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  status: Code
  period: Period
}

type EpisodeOfCareDiagnosisConditionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Condition
  type: URI
  identifier: Identifier
  display: String
}

type EpisodeOfCareDiagnosis {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  condition: EpisodeOfCareDiagnosisConditionReference
  role: CodeableConcept
  rank: Int
}

type EpisodeOfCareStatusHistory {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  status: Code
  period: Period
}

type EvidenceAttributeEstimate {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  note: [Annotation]
  type: CodeableConcept
  quantity: Quantity
  level: Float
  range: Range
  attributeEstimate: [EvidenceAttributeEstimate]
}

type EvidenceCertainty {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  note: [Annotation]
  type: CodeableConcept
  rating: CodeableConcept
  rater: String
  subcomponent: [EvidenceCertainty]
}

type EvidenceModelCharacteristic {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  value: Quantity
  variable: [BackboneEvidenceVariable]
  attributeEstimate: [EvidenceAttributeEstimate]
}

type EvidenceReportCharacteristicValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type EvidenceReportCharacteristic {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  valueReference: EvidenceReportCharacteristicValueReferenceReference
  valueCodeableConcept: CodeableConcept
  valueBoolean: Boolean
  valueQuantity: Quantity
  valueRange: Range
  exclude: Boolean
  period: Period
}

type EvidenceReportRelatesToTargetReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EvidenceReport
  type: URI
  identifier: Identifier
  display: String
}

type EvidenceReportRelatesTo {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  targetIdentifier: Identifier
  targetReference: EvidenceReportRelatesToTargetReferenceReference
}

type EvidenceReportSectionFocusReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union EvidenceReportSectionAuthor = Person | Device | Group | Organization

type EvidenceReportSectionAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EvidenceReportSectionAuthor
  type: URI
  identifier: Identifier
  display: String
}

type EvidenceReportSectionEntryReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type EvidenceReportSection {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  title: String
  focus: CodeableConcept
  focusReference: EvidenceReportSectionFocusReferenceReference
  author: [EvidenceReportSectionAuthorReference]
  text: Narrative
  mode: Code
  orderedBy: CodeableConcept
  entryClassifier: [CodeableConcept]
  entryReference: [EvidenceReportSectionEntryReferenceReference]
  entryQuantity: [Quantity]
  emptyReason: CodeableConcept
  section: [EvidenceReportSection]
}

type EvidenceReportSubject {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  characteristic: [EvidenceReportCharacteristic]
  note: [Annotation]
}

type EvidenceSampleSize {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  note: [Annotation]
  numberOfStudies: Int
  numberOfParticipants: Int
  knownDataCount: Int
}

type EvidenceStatistic {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  note: [Annotation]
  statisticType: CodeableConcept
  category: CodeableConcept
  quantity: Quantity
  numberOfEvents: Int
  numberAffected: Int
  sampleSize: EvidenceSampleSize
  attributeEstimate: [EvidenceAttributeEstimate]
  modelCharacteristic: [EvidenceModelCharacteristic]
}

union EvidenceVariableVariableDefinition = Group | EvidenceVariable

type EvidenceVariableVariableDefinitionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EvidenceVariableVariableDefinition
  type: URI
  identifier: Identifier
  display: String
}

type BackboneEvidenceVariable {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  variableDefinition: EvidenceVariableVariableDefinitionReference
  handling: Code
  valueCategory: [CodeableConcept]
  valueQuantity: [Quantity]
  valueRange: [Range]
}

type EvidenceVariableCategory {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  valueCodeableConcept: CodeableConcept
  valueQuantity: Quantity
  valueRange: Range
}

union EvidenceVariableCharacteristicDefinitionReference = Group | EvidenceVariable

type EvidenceVariableCharacteristicDefinitionReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EvidenceVariableCharacteristicDefinitionReference
  type: URI
  identifier: Identifier
  display: String
}

union EvidenceVariableCharacteristicDevice = Device | DeviceMetric

type EvidenceVariableCharacteristicDeviceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EvidenceVariableCharacteristicDevice
  type: URI
  identifier: Identifier
  display: String
}

type EvidenceVariableCharacteristic {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  definitionReference: EvidenceVariableCharacteristicDefinitionReferenceReference
  definitionCanonical: Canonical
  definitionCodeableConcept: CodeableConcept
  definitionExpression: Expression
  method: CodeableConcept
  device: EvidenceVariableCharacteristicDeviceReference
  exclude: Boolean
  timeFromStart: EvidenceVariableTimeFromStart
  groupMeasure: Code
}

union EvidenceVariableDefinitionObserved = Group | EvidenceVariable

type EvidenceVariableDefinitionObservedReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EvidenceVariableDefinitionObserved
  type: URI
  identifier: Identifier
  display: String
}

union EvidenceVariableDefinitionIntended = Group | EvidenceVariable

type EvidenceVariableDefinitionIntendedReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EvidenceVariableDefinitionIntended
  type: URI
  identifier: Identifier
  display: String
}

type EvidenceVariableDefinition {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: Markdown
  note: [Annotation]
  variableRole: CodeableConcept
  observed: EvidenceVariableDefinitionObservedReference
  intended: EvidenceVariableDefinitionIntendedReference
  directnessMatch: CodeableConcept
}

type EvidenceVariableTimeFromStart {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  quantity: Quantity
  range: Range
  note: [Annotation]
}

type ExampleScenarioActor {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  actorId: String
  type: Code
  name: String
  description: Markdown
}

type ExampleScenarioAlternative {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  title: String
  description: Markdown
  step: [ExampleScenarioStep]
}

type ExampleScenarioContainedInstance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  resourceId: String
  versionId: String
}

type ExampleScenarioInstance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  resourceId: String
  resourceType: Code
  name: String
  description: Markdown
  version: [ExampleScenarioVersion]
  containedInstance: [ExampleScenarioContainedInstance]
}

type ExampleScenarioOperation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  number: String
  type: String
  name: String
  initiator: String
  receiver: String
  description: Markdown
  initiatorActive: Boolean
  receiverActive: Boolean
  request: ExampleScenarioContainedInstance
  response: ExampleScenarioContainedInstance
}

type ExampleScenarioProcess {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  title: String
  description: Markdown
  preConditions: Markdown
  postConditions: Markdown
  step: [ExampleScenarioStep]
}

type ExampleScenarioStep {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  process: [ExampleScenarioProcess]
  pause: Boolean
  operation: ExampleScenarioOperation
  alternative: [ExampleScenarioAlternative]
}

type ExampleScenarioVersion {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  versionId: String
  description: Markdown
}

type ExplanationOfBenefitAccidentLocationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitAccident {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  date: Date
  type: CodeableConcept
  locationAddress: Address
  locationReference: ExplanationOfBenefitAccidentLocationReferenceReference
}

union ExplanationOfBenefitAddItemProvider = Practitioner | PractitionerRole | Organization

type ExplanationOfBenefitAddItemProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ExplanationOfBenefitAddItemProvider
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitAddItemLocationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitAddItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  itemSequence: [Int]
  detailSequence: [Int]
  subDetailSequence: [Int]
  provider: [ExplanationOfBenefitAddItemProviderReference]
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  programCode: [CodeableConcept]
  servicedDate: Date
  servicedPeriod: Period
  locationCodeableConcept: CodeableConcept
  locationAddress: Address
  locationReference: ExplanationOfBenefitAddItemLocationReferenceReference
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  bodySite: CodeableConcept
  subSite: [CodeableConcept]
  noteNumber: [Int]
  adjudication: [ExplanationOfBenefitAdjudication]
  detail: [ExplanationOfBenefitDetail1]
}

type ExplanationOfBenefitAdjudication {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  category: CodeableConcept
  reason: CodeableConcept
  amount: Money
  value: Float
}

type ExplanationOfBenefitBenefitBalance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  category: CodeableConcept
  excluded: Boolean
  name: String
  description: String
  network: CodeableConcept
  unit: CodeableConcept
  term: CodeableConcept
  financial: [ExplanationOfBenefitFinancial]
}

union ExplanationOfBenefitCareTeamProvider = Practitioner | PractitionerRole | Organization

type ExplanationOfBenefitCareTeamProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ExplanationOfBenefitCareTeamProvider
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitCareTeam {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  provider: ExplanationOfBenefitCareTeamProviderReference
  responsible: Boolean
  role: CodeableConcept
  qualification: CodeableConcept
}

type ExplanationOfBenefitDetailUdiReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitDetail {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  revenue: CodeableConcept
  category: CodeableConcept
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  programCode: [CodeableConcept]
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  udi: [ExplanationOfBenefitDetailUdiReference]
  noteNumber: [Int]
  adjudication: [ExplanationOfBenefitAdjudication]
  subDetail: [ExplanationOfBenefitSubDetail]
}

type ExplanationOfBenefitDetail1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  noteNumber: [Int]
  adjudication: [ExplanationOfBenefitAdjudication]
  subDetail: [ExplanationOfBenefitSubDetail1]
}

type ExplanationOfBenefitDiagnosisDiagnosisReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Condition
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitDiagnosis {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  diagnosisCodeableConcept: CodeableConcept
  diagnosisReference: ExplanationOfBenefitDiagnosisDiagnosisReferenceReference
  type: [CodeableConcept]
  onAdmission: CodeableConcept
  packageCode: CodeableConcept
}

type ExplanationOfBenefitFinancial {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  allowedUnsignedInt: Int
  allowedString: String
  allowedMoney: Money
  usedUnsignedInt: Int
  usedMoney: Money
}

type ExplanationOfBenefitInsuranceCoverageReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Coverage
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitInsurance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  focal: Boolean
  coverage: ExplanationOfBenefitInsuranceCoverageReference
  preAuthRef: [String]
}

type ExplanationOfBenefitItemLocationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitItemUdiReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitItemEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  careTeamSequence: [Int]
  diagnosisSequence: [Int]
  procedureSequence: [Int]
  informationSequence: [Int]
  revenue: CodeableConcept
  category: CodeableConcept
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  programCode: [CodeableConcept]
  servicedDate: Date
  servicedPeriod: Period
  locationCodeableConcept: CodeableConcept
  locationAddress: Address
  locationReference: ExplanationOfBenefitItemLocationReferenceReference
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  udi: [ExplanationOfBenefitItemUdiReference]
  bodySite: CodeableConcept
  subSite: [CodeableConcept]
  encounter: [ExplanationOfBenefitItemEncounterReference]
  noteNumber: [Int]
  adjudication: [ExplanationOfBenefitAdjudication]
  detail: [ExplanationOfBenefitDetail]
}

union ExplanationOfBenefitPayeeParty = Practitioner | PractitionerRole | Organization | Patient | RelatedPerson

type ExplanationOfBenefitPayeePartyReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ExplanationOfBenefitPayeeParty
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitPayee {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  party: ExplanationOfBenefitPayeePartyReference
}

type ExplanationOfBenefitPayment {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  adjustment: Money
  adjustmentReason: CodeableConcept
  date: Date
  amount: Money
  identifier: Identifier
}

type ExplanationOfBenefitProcedureProcedureReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Procedure
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitProcedureUdiReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitProcedure {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  type: [CodeableConcept]
  date: DateTime
  procedureCodeableConcept: CodeableConcept
  procedureReference: ExplanationOfBenefitProcedureProcedureReferenceReference
  udi: [ExplanationOfBenefitProcedureUdiReference]
}

type ExplanationOfBenefitProcessNote {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  number: Int
  type: Code
  text: String
  language: CodeableConcept
}

type ExplanationOfBenefitRelatedClaimReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Claim
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitRelated {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  claim: ExplanationOfBenefitRelatedClaimReference
  relationship: CodeableConcept
  reference: Identifier
}

type ExplanationOfBenefitSubDetailUdiReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitSubDetail {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  revenue: CodeableConcept
  category: CodeableConcept
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  programCode: [CodeableConcept]
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  udi: [ExplanationOfBenefitSubDetailUdiReference]
  noteNumber: [Int]
  adjudication: [ExplanationOfBenefitAdjudication]
}

type ExplanationOfBenefitSubDetail1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  productOrService: CodeableConcept
  modifier: [CodeableConcept]
  quantity: Quantity
  unitPrice: Money
  factor: Float
  net: Money
  noteNumber: [Int]
  adjudication: [ExplanationOfBenefitAdjudication]
}

type ExplanationOfBenefitSupportingInfoValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitSupportingInfo {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  category: CodeableConcept
  code: CodeableConcept
  timingDate: Date
  timingPeriod: Period
  valueBoolean: Boolean
  valueString: String
  valueQuantity: Quantity
  valueAttachment: Attachment
  valueReference: ExplanationOfBenefitSupportingInfoValueReferenceReference
  reason: Coding
}

type ExplanationOfBenefitTotal {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  category: CodeableConcept
  amount: Money
}

type FamilyMemberHistoryCondition {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  outcome: CodeableConcept
  contributedToDeath: Boolean
  onsetAge: Quantity
  onsetRange: Range
  onsetPeriod: Period
  onsetString: String
  note: [Annotation]
}

type GoalTarget {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  measure: CodeableConcept
  detailQuantity: Quantity
  detailRange: Range
  detailCodeableConcept: CodeableConcept
  detailString: String
  detailBoolean: Boolean
  detailInteger: Int
  detailRatio: Ratio
  dueDate: Date
  dueDuration: Quantity
}

type GraphDefinitionCompartment {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  use: Code
  code: Code
  rule: Code
  expression: String
  description: String
}

type GraphDefinitionLink {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  path: String
  sliceName: String
  min: Int
  max: String
  description: String
  target: [GraphDefinitionTarget]
}

type GraphDefinitionTarget {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  params: String
  profile: Canonical
  compartment: [GraphDefinitionCompartment]
  link: [GraphDefinitionLink]
}

type GroupCharacteristicValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type GroupCharacteristic {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  valueCodeableConcept: CodeableConcept
  valueBoolean: Boolean
  valueQuantity: Quantity
  valueRange: Range
  valueReference: GroupCharacteristicValueReferenceReference
  exclude: Boolean
  period: Period
}

union GroupMemberEntity = Patient | RelatedPerson | Practitioner | PractitionerRole | Device | Medication | Substance | Group

type GroupMemberEntityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: GroupMemberEntity
  type: URI
  identifier: Identifier
  display: String
}

type GroupMember {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  entity: GroupMemberEntityReference
  period: Period
  inactive: Boolean
}

type HealthcareServiceAvailableTime {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  daysOfWeek: [Code]
  allDay: Boolean
  availableStartTime: Time
  availableEndTime: Time
}

type HealthcareServiceEligibility {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  comment: Markdown
}

type HealthcareServiceNotAvailable {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  during: Period
}

type ImagingStudyInstance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  uid: ID
  sopClass: Coding
  number: Int
  title: String
}

union ImagingStudyPerformerActor = Practitioner | PractitionerRole | Organization | CareTeam | Patient | Device | RelatedPerson

type ImagingStudyPerformerActorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ImagingStudyPerformerActor
  type: URI
  identifier: Identifier
  display: String
}

type ImagingStudyPerformer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  function: CodeableConcept
  actor: ImagingStudyPerformerActorReference
}

type ImagingStudySeriesEndpointReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Endpoint
  type: URI
  identifier: Identifier
  display: String
}

type ImagingStudySeriesSpecimenReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Specimen
  type: URI
  identifier: Identifier
  display: String
}

type ImagingStudySeries {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  uid: ID
  number: Int
  modality: Coding
  description: String
  numberOfInstances: Int
  endpoint: [ImagingStudySeriesEndpointReference]
  bodySite: Coding
  laterality: Coding
  specimen: [ImagingStudySeriesSpecimenReference]
  started: DateTime
  performer: [ImagingStudyPerformer]
  instance: [ImagingStudyInstance]
}

type ImmunizationEducation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  documentType: String
  reference: URI
  publicationDate: DateTime
  presentationDate: DateTime
}

union ImmunizationPerformerActor = Practitioner | PractitionerRole | Organization

type ImmunizationPerformerActorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ImmunizationPerformerActor
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationPerformer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  function: CodeableConcept
  actor: ImmunizationPerformerActorReference
}

type ImmunizationProtocolAppliedAuthorityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationProtocolApplied {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  series: String
  authority: ImmunizationProtocolAppliedAuthorityReference
  targetDisease: [CodeableConcept]
  doseNumberPositiveInt: Int
  doseNumberString: String
  seriesDosesPositiveInt: Int
  seriesDosesString: String
}

type ImmunizationReactionDetailReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Observation
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationReaction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  date: DateTime
  detail: ImmunizationReactionDetailReference
  reported: Boolean
}

type ImmunizationRecommendationDateCriterion {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  value: DateTime
}

union ImmunizationRecommendationRecommendationSupportingImmunization = Immunization | ImmunizationEvaluation

type ImmunizationRecommendationRecommendationSupportingImmunizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ImmunizationRecommendationRecommendationSupportingImmunization
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationRecommendationRecommendationSupportingPatientInformationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationRecommendationRecommendation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  vaccineCode: [CodeableConcept]
  targetDisease: CodeableConcept
  contraindicatedVaccineCode: [CodeableConcept]
  forecastStatus: CodeableConcept
  forecastReason: [CodeableConcept]
  dateCriterion: [ImmunizationRecommendationDateCriterion]
  description: String
  series: String
  doseNumberPositiveInt: Int
  doseNumberString: String
  seriesDosesPositiveInt: Int
  seriesDosesString: String
  supportingImmunization: [ImmunizationRecommendationRecommendationSupportingImmunizationReference]
  supportingPatientInformation: [ImmunizationRecommendationRecommendationSupportingPatientInformationReference]
}

type ImplementationGuideDefinition {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  grouping: [ImplementationGuideGrouping]
  resource: [ImplementationGuideResource]
  page: ImplementationGuidePage
  parameter: [ImplementationGuideParameter]
  template: [ImplementationGuideTemplate]
}

type ImplementationGuideDependsOn {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  uri: Canonical
  packageId: ID
  version: String
}

type ImplementationGuideGlobal {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  profile: Canonical
}

type ImplementationGuideGrouping {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  description: String
}

type ImplementationGuideManifest {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  rendering: URL
  resource: [ImplementationGuideResource1]
  page: [ImplementationGuidePage1]
  image: [String]
  other: [String]
}

type ImplementationGuidePageNameReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Binary
  type: URI
  identifier: Identifier
  display: String
}

type ImplementationGuidePage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  nameUrl: URL
  nameReference: ImplementationGuidePageNameReferenceReference
  title: String
  generation: Code
  page: [ImplementationGuidePage]
}

type ImplementationGuidePage1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  title: String
  anchor: [String]
}

type ImplementationGuideParameter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  value: String
}

type ImplementationGuideResourceReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ImplementationGuideResource {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  reference: ImplementationGuideResourceReferenceReference
  fhirVersion: [Code]
  name: String
  description: String
  exampleBoolean: Boolean
  exampleCanonical: Canonical
  groupingId: ID
}

type ImplementationGuideResource1ReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ImplementationGuideResource1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  reference: ImplementationGuideResource1ReferenceReference
  exampleBoolean: Boolean
  exampleCanonical: Canonical
  relativePath: URL
}

type ImplementationGuideTemplate {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  source: String
  scope: String
}

type IngredientManufacturerManufacturerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type IngredientManufacturer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  role: Code
  manufacturer: IngredientManufacturerManufacturerReference
}

type IngredientReferenceStrengthSubstanceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SubstanceDefinition
  type: URI
  identifier: Identifier
  display: String
}

type IngredientReferenceStrength {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  substance: IngredientReferenceStrengthSubstanceReference
  strengthRatio: Ratio
  strengthRatioRange: RatioRange
  measurementPoint: String
  country: [CodeableConcept]
}

type IngredientStrength {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  presentationRatio: Ratio
  presentationRatioRange: RatioRange
  textPresentation: String
  concentrationRatio: Ratio
  concentrationRatioRange: RatioRange
  textConcentration: String
  measurementPoint: String
  country: [CodeableConcept]
  referenceStrength: [IngredientReferenceStrength]
}

type IngredientSubstanceCodeReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SubstanceDefinition
  type: URI
  identifier: Identifier
  display: String
}

type IngredientSubstance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: IngredientSubstanceCodeReference
  strength: [IngredientStrength]
}

type InsurancePlanBenefit {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  requirement: String
  limit: [InsurancePlanLimit]
}

type InsurancePlanBenefit1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  cost: [InsurancePlanCost]
}

type InsurancePlanContact {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  purpose: CodeableConcept
  name: HumanName
  telecom: [ContactPoint]
  address: Address
}

type InsurancePlanCost {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  applicability: CodeableConcept
  qualifiers: [CodeableConcept]
  value: Quantity
}

type InsurancePlanCoverageNetworkReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type InsurancePlanCoverage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  network: [InsurancePlanCoverageNetworkReference]
  benefit: [InsurancePlanBenefit]
}

type InsurancePlanGeneralCost {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  groupSize: Int
  cost: Money
  comment: String
}

type InsurancePlanLimit {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  value: Quantity
  code: CodeableConcept
}

type InsurancePlanPlanCoverageAreaReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type InsurancePlanPlanNetworkReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type InsurancePlanPlan {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  type: CodeableConcept
  coverageArea: [InsurancePlanPlanCoverageAreaReference]
  network: [InsurancePlanPlanNetworkReference]
  generalCost: [InsurancePlanGeneralCost]
  specificCost: [InsurancePlanSpecificCost]
}

type InsurancePlanSpecificCost {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  category: CodeableConcept
  benefit: [InsurancePlanBenefit1]
}

type InvoiceLineItemChargeItemReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ChargeItem
  type: URI
  identifier: Identifier
  display: String
}

type InvoiceLineItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  sequence: Int
  chargeItemReference: InvoiceLineItemChargeItemReferenceReference
  chargeItemCodeableConcept: CodeableConcept
  priceComponent: [InvoicePriceComponent]
}

union InvoiceParticipantActor = Practitioner | Organization | Patient | PractitionerRole | Device | RelatedPerson

type InvoiceParticipantActorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: InvoiceParticipantActor
  type: URI
  identifier: Identifier
  display: String
}

type InvoiceParticipant {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  role: CodeableConcept
  actor: InvoiceParticipantActorReference
}

type InvoicePriceComponent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  code: CodeableConcept
  factor: Float
  amount: Money
}

type LinkageItemResourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type LinkageItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  resource: LinkageItemResourceReference
}

type ListEntryItemReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ListEntry {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  flag: CodeableConcept
  deleted: Boolean
  date: DateTime
  item: ListEntryItemReference
}

type LocationHoursOfOperation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  daysOfWeek: [Code]
  allDay: Boolean
  openingTime: Time
  closingTime: Time
}

type LocationPosition {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  longitude: Float
  latitude: Float
  altitude: Float
}

type ManufacturedItemDefinitionProperty {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueCodeableConcept: CodeableConcept
  valueQuantity: Quantity
  valueDate: Date
  valueBoolean: Boolean
  valueAttachment: Attachment
}

type MarketingStatus {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  country: CodeableConcept
  jurisdiction: CodeableConcept
  status: CodeableConcept
  dateRange: Period
  restoreDate: DateTime
}

type MeasureComponent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  description: String
  criteria: Expression
}

type MeasureGroup {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  description: String
  population: [MeasurePopulation]
  stratifier: [MeasureStratifier]
}

type MeasurePopulation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  description: String
  criteria: Expression
}

type MeasureReportComponent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  value: CodeableConcept
}

type MeasureReportGroup {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  population: [MeasureReportPopulation]
  measureScore: Quantity
  stratifier: [MeasureReportStratifier]
}

type MeasureReportPopulationSubjectResultsReference {
  id: String
  extension: [Extension]
  reference: String
  resource: List
  type: URI
  identifier: Identifier
  display: String
}

type MeasureReportPopulation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  count: Int
  subjectResults: MeasureReportPopulationSubjectResultsReference
}

type MeasureReportPopulation1SubjectResultsReference {
  id: String
  extension: [Extension]
  reference: String
  resource: List
  type: URI
  identifier: Identifier
  display: String
}

type MeasureReportPopulation1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  count: Int
  subjectResults: MeasureReportPopulation1SubjectResultsReference
}

type MeasureReportStratifier {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: [CodeableConcept]
  stratum: [MeasureReportStratum]
}

type MeasureReportStratum {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  value: CodeableConcept
  component: [MeasureReportComponent]
  population: [MeasureReportPopulation1]
  measureScore: Quantity
}

type MeasureStratifier {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  description: String
  criteria: Expression
  component: [MeasureComponent]
}

type MeasureSupplementalData {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  usage: [CodeableConcept]
  description: String
  criteria: Expression
}

type MedicationAdministrationDosage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  text: String
  site: CodeableConcept
  route: CodeableConcept
  method: CodeableConcept
  dose: Quantity
  rateRatio: Ratio
  rateQuantity: Quantity
}

union MedicationAdministrationPerformerActor = Practitioner | PractitionerRole | Patient | RelatedPerson | Device

type MedicationAdministrationPerformerActorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationAdministrationPerformerActor
  type: URI
  identifier: Identifier
  display: String
}

type MedicationAdministrationPerformer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  function: CodeableConcept
  actor: MedicationAdministrationPerformerActorReference
}

type MedicationBatch {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  lotNumber: String
  expirationDate: DateTime
}

union MedicationDispensePerformerActor = Practitioner | PractitionerRole | Organization | Patient | Device | RelatedPerson

type MedicationDispensePerformerActorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationDispensePerformerActor
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispensePerformer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  function: CodeableConcept
  actor: MedicationDispensePerformerActorReference
}

union MedicationDispenseSubstitutionResponsibleParty = Practitioner | PractitionerRole

type MedicationDispenseSubstitutionResponsiblePartyReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationDispenseSubstitutionResponsibleParty
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispenseSubstitution {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  wasSubstituted: Boolean
  type: CodeableConcept
  reason: [CodeableConcept]
  responsibleParty: [MedicationDispenseSubstitutionResponsiblePartyReference]
}

union MedicationIngredientItemReference = Substance | Medication

type MedicationIngredientItemReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationIngredientItemReference
  type: URI
  identifier: Identifier
  display: String
}

type MedicationIngredient {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  itemCodeableConcept: CodeableConcept
  itemReference: MedicationIngredientItemReferenceReference
  isActive: Boolean
  strength: Ratio
}

type MedicationKnowledgeAdministrationGuidelinesIndicationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type MedicationKnowledgeAdministrationGuidelines {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  dosage: [MedicationKnowledgeDosage]
  indicationCodeableConcept: CodeableConcept
  indicationReference: MedicationKnowledgeAdministrationGuidelinesIndicationReferenceReference
  patientCharacteristics: [MedicationKnowledgePatientCharacteristics]
}

type MedicationKnowledgeCost {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  source: String
  cost: Money
}

type MedicationKnowledgeDosage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  dosage: [Dosage]
}

type MedicationKnowledgeDrugCharacteristic {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueCodeableConcept: CodeableConcept
  valueString: String
  valueQuantity: Quantity
  valueBase64Binary: Base64Binary
}

type MedicationKnowledgeIngredientItemReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Substance
  type: URI
  identifier: Identifier
  display: String
}

type MedicationKnowledgeIngredient {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  itemCodeableConcept: CodeableConcept
  itemReference: MedicationKnowledgeIngredientItemReferenceReference
  isActive: Boolean
  strength: Ratio
}

type MedicationKnowledgeKinetics {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  areaUnderCurve: [Quantity]
  lethalDose50: [Quantity]
  halfLifePeriod: Quantity
}

type MedicationKnowledgeMaxDispense {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  quantity: Quantity
  period: Quantity
}

type MedicationKnowledgeMedicineClassification {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  classification: [CodeableConcept]
}

type MedicationKnowledgeMonitoringProgram {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  name: String
}

union MedicationKnowledgeMonographSource = DocumentReference | Media

type MedicationKnowledgeMonographSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationKnowledgeMonographSource
  type: URI
  identifier: Identifier
  display: String
}

type MedicationKnowledgeMonograph {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  source: MedicationKnowledgeMonographSourceReference
}

type MedicationKnowledgePackaging {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  quantity: Quantity
}

type MedicationKnowledgePatientCharacteristics {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  characteristicCodeableConcept: CodeableConcept
  characteristicQuantity: Quantity
  value: [String]
}

type MedicationKnowledgeRegulatoryRegulatoryAuthorityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type MedicationKnowledgeRegulatory {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  regulatoryAuthority: MedicationKnowledgeRegulatoryRegulatoryAuthorityReference
  substitution: [MedicationKnowledgeSubstitution]
  schedule: [MedicationKnowledgeSchedule]
  maxDispense: MedicationKnowledgeMaxDispense
}

type MedicationKnowledgeRelatedMedicationKnowledgeReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationKnowledge
  type: URI
  identifier: Identifier
  display: String
}

type MedicationKnowledgeRelatedMedicationKnowledge {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  reference: [MedicationKnowledgeRelatedMedicationKnowledgeReferenceReference]
}

type MedicationKnowledgeSchedule {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  schedule: CodeableConcept
}

type MedicationKnowledgeSubstitution {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  allowed: Boolean
}

type MedicationRequestDispenseRequestPerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type MedicationRequestDispenseRequest {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  initialFill: MedicationRequestInitialFill
  dispenseInterval: Quantity
  validityPeriod: Period
  numberOfRepeatsAllowed: Int
  quantity: Quantity
  expectedSupplyDuration: Quantity
  performer: MedicationRequestDispenseRequestPerformerReference
}

type MedicationRequestInitialFill {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  quantity: Quantity
  duration: Quantity
}

type MedicationRequestSubstitution {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  allowedBoolean: Boolean
  allowedCodeableConcept: CodeableConcept
  reason: CodeableConcept
}

type MedicinalProductDefinitionCharacteristic {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueCodeableConcept: CodeableConcept
  valueQuantity: Quantity
  valueDate: Date
  valueBoolean: Boolean
  valueAttachment: Attachment
}

union MedicinalProductDefinitionContactContact = Organization | PractitionerRole

type MedicinalProductDefinitionContactContactReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicinalProductDefinitionContactContact
  type: URI
  identifier: Identifier
  display: String
}

type MedicinalProductDefinitionContact {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  contact: MedicinalProductDefinitionContactContactReference
}

type MedicinalProductDefinitionCountryLanguage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  country: CodeableConcept
  jurisdiction: CodeableConcept
  language: CodeableConcept
}

type MedicinalProductDefinitionCrossReferenceProductReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicinalProductDefinition
  type: URI
  identifier: Identifier
  display: String
}

type MedicinalProductDefinitionCrossReference {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  product: MedicinalProductDefinitionCrossReferenceProductReference
  type: CodeableConcept
}

type MedicinalProductDefinitionName {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  productName: String
  type: CodeableConcept
  namePart: [MedicinalProductDefinitionNamePart]
  countryLanguage: [MedicinalProductDefinitionCountryLanguage]
}

type MedicinalProductDefinitionNamePart {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  part: String
  type: CodeableConcept
}

union MedicinalProductDefinitionOperationType = ActivityDefinition | PlanDefinition

type MedicinalProductDefinitionOperationTypeReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicinalProductDefinitionOperationType
  type: URI
  identifier: Identifier
  display: String
}

type MedicinalProductDefinitionOperationOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type MedicinalProductDefinitionOperation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: MedicinalProductDefinitionOperationTypeReference
  effectiveDate: Period
  organization: [MedicinalProductDefinitionOperationOrganizationReference]
  confidentialityIndicator: CodeableConcept
}

type MessageDefinitionAllowedResponse {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  message: Canonical
  situation: Markdown
}

type MessageDefinitionFocus {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  profile: Canonical
  min: Int
  max: String
}

type MessageHeaderDestinationTargetReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

union MessageHeaderDestinationReceiver = Practitioner | PractitionerRole | Organization

type MessageHeaderDestinationReceiverReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MessageHeaderDestinationReceiver
  type: URI
  identifier: Identifier
  display: String
}

type MessageHeaderDestination {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  target: MessageHeaderDestinationTargetReference
  endpoint: URL
  receiver: MessageHeaderDestinationReceiverReference
}

type MessageHeaderResponseDetailsReference {
  id: String
  extension: [Extension]
  reference: String
  resource: OperationOutcome
  type: URI
  identifier: Identifier
  display: String
}

type MessageHeaderResponse {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: ID
  code: Code
  details: MessageHeaderResponseDetailsReference
}

type MessageHeaderSource {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  software: String
  version: String
  contact: ContactPoint
  endpoint: URL
}

type MolecularSequenceInner {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  start: Int
  end: Int
}

type MolecularSequenceOuter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  start: Int
  end: Int
}

type MolecularSequenceQuality {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  standardSequence: CodeableConcept
  start: Int
  end: Int
  score: Quantity
  method: CodeableConcept
  truthTP: Float
  queryTP: Float
  truthFN: Float
  queryFP: Float
  gtFP: Float
  precision: Float
  recall: Float
  fScore: Float
  roc: MolecularSequenceRoc
}

type MolecularSequenceReferenceSeqReferenceSeqPointerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MolecularSequence
  type: URI
  identifier: Identifier
  display: String
}

type MolecularSequenceReferenceSeq {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  chromosome: CodeableConcept
  genomeBuild: String
  orientation: Code
  referenceSeqId: CodeableConcept
  referenceSeqPointer: MolecularSequenceReferenceSeqReferenceSeqPointerReference
  referenceSeqString: String
  strand: Code
  windowStart: Int
  windowEnd: Int
}

type MolecularSequenceRepository {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  url: URI
  name: String
  datasetId: String
  variantsetId: String
  readsetId: String
}

type MolecularSequenceRoc {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  score: [Int]
  numTP: [Int]
  numFP: [Int]
  numFN: [Int]
  precision: [Float]
  sensitivity: [Float]
  fMeasure: [Float]
}

type MolecularSequenceStructureVariant {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  variantType: CodeableConcept
  exact: Boolean
  length: Int
  outer: MolecularSequenceOuter
  inner: MolecularSequenceInner
}

type MolecularSequenceVariantVariantPointerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Observation
  type: URI
  identifier: Identifier
  display: String
}

type MolecularSequenceVariant {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  start: Int
  end: Int
  observedAllele: String
  referenceAllele: String
  cigar: String
  variantPointer: MolecularSequenceVariantVariantPointerReference
}

type NamingSystemUniqueId {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  value: String
  preferred: Boolean
  comment: String
  period: Period
}

type NutritionOrderAdministration {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  schedule: Timing
  quantity: Quantity
  rateQuantity: Quantity
  rateRatio: Ratio
}

type NutritionOrderEnteralFormula {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  baseFormulaType: CodeableConcept
  baseFormulaProductName: String
  additiveType: CodeableConcept
  additiveProductName: String
  caloricDensity: Quantity
  routeofAdministration: CodeableConcept
  administration: [NutritionOrderAdministration]
  maxVolumeToDeliver: Quantity
  administrationInstruction: String
}

type NutritionOrderNutrient {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  modifier: CodeableConcept
  amount: Quantity
}

type NutritionOrderOralDiet {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: [CodeableConcept]
  schedule: [Timing]
  nutrient: [NutritionOrderNutrient]
  texture: [NutritionOrderTexture]
  fluidConsistencyType: [CodeableConcept]
  instruction: String
}

type NutritionOrderSupplement {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  productName: String
  schedule: [Timing]
  quantity: Quantity
  instruction: String
}

type NutritionOrderTexture {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  modifier: CodeableConcept
  foodType: CodeableConcept
}

type NutritionProductIngredientItemReference {
  id: String
  extension: [Extension]
  reference: String
  resource: NutritionProduct
  type: URI
  identifier: Identifier
  display: String
}

type NutritionProductIngredient {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  item: NutritionProductIngredientItemReference
  amount: [Ratio]
}

type NutritionProductInstance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  quantity: Quantity
  identifier: [Identifier]
  lotNumber: String
  expiry: DateTime
  useBy: DateTime
}

type NutritionProductNutrientItemReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Substance
  type: URI
  identifier: Identifier
  display: String
}

type NutritionProductNutrient {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  item: NutritionProductNutrientItemReference
  amount: [Ratio]
}

type NutritionProductProductCharacteristic {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueCodeableConcept: CodeableConcept
  valueString: String
  valueQuantity: Quantity
  valueBase64Binary: Base64Binary
  valueAttachment: Attachment
  valueBoolean: Boolean
}

type ObservationComponent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  valueQuantity: Quantity
  valueCodeableConcept: CodeableConcept
  valueString: String
  valueBoolean: Boolean
  valueInteger: Int
  valueRange: Range
  valueRatio: Ratio
  valueSampledData: SampledData
  valueTime: Time
  valueDateTime: DateTime
  valuePeriod: Period
  dataAbsentReason: CodeableConcept
  interpretation: [CodeableConcept]
  referenceRange: [ObservationReferenceRange]
}

type ObservationDefinitionQualifiedInterval {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  category: Code
  range: Range
  context: CodeableConcept
  appliesTo: [CodeableConcept]
  gender: Code
  age: Range
  gestationalAge: Range
  condition: String
}

type ObservationDefinitionQuantitativeDetails {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  customaryUnit: CodeableConcept
  unit: CodeableConcept
  conversionFactor: Float
  decimalPrecision: Int
}

type ObservationReferenceRange {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  low: Quantity
  high: Quantity
  type: CodeableConcept
  appliesTo: [CodeableConcept]
  age: Range
  text: String
}

type OperationDefinitionBinding {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  strength: Code
  valueSet: Canonical
}

type OperationDefinitionOverload {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  parameterName: [String]
  comment: String
}

type OperationDefinitionParameter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: Code
  use: Code
  min: Int
  max: String
  documentation: String
  type: Code
  targetProfile: [Canonical]
  searchType: Code
  binding: OperationDefinitionBinding
  referencedFrom: [OperationDefinitionReferencedFrom]
  part: [OperationDefinitionParameter]
}

type OperationDefinitionReferencedFrom {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  source: String
  sourceId: String
}

type OperationOutcomeIssue {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  severity: Code
  code: Code
  details: CodeableConcept
  diagnostics: String
  location: [String]
  expression: [String]
}

type OrganizationContact {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  purpose: CodeableConcept
  name: HumanName
  telecom: [ContactPoint]
  address: Address
}

union PackagedProductDefinitionContainedItemItem = ManufacturedItemDefinition | DeviceDefinition | PackagedProductDefinition | BiologicallyDerivedProduct | NutritionProduct

type PackagedProductDefinitionContainedItemItemReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PackagedProductDefinitionContainedItemItem
  type: URI
  identifier: Identifier
  display: String
}

type PackagedProductDefinitionContainedItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  item: PackagedProductDefinitionContainedItemItemReference
  amount: Quantity
}

type PackagedProductDefinitionLegalStatusOfSupply {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  jurisdiction: CodeableConcept
}

type PackagedProductDefinitionPackageManufacturerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type PackagedProductDefinitionPackage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  type: CodeableConcept
  quantity: Int
  material: [CodeableConcept]
  alternateMaterial: [CodeableConcept]
  shelfLifeStorage: [PackagedProductDefinitionShelfLifeStorage]
  manufacturer: [PackagedProductDefinitionPackageManufacturerReference]
  property: [PackagedProductDefinitionProperty]
  containedItem: [PackagedProductDefinitionContainedItem]
  package: [PackagedProductDefinitionPackage]
}

type PackagedProductDefinitionProperty {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueCodeableConcept: CodeableConcept
  valueQuantity: Quantity
  valueDate: Date
  valueBoolean: Boolean
  valueAttachment: Attachment
}

type PackagedProductDefinitionShelfLifeStorage {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  periodDuration: Quantity
  periodString: String
  specialPrecautionsForStorage: [CodeableConcept]
}

type ParametersParameterValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ParametersParameter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  valueBase64Binary: Base64Binary
  valueBoolean: Boolean
  valueCanonical: Canonical
  valueCode: Code
  valueDate: Date
  valueDateTime: DateTime
  valueDecimal: Float
  valueId: ID
  valueInstant: Instant
  valueInteger: Int
  valueMarkdown: Markdown
  valueOid: OID
  valuePositiveInt: Int
  valueString: String
  valueTime: Time
  valueUnsignedInt: Int
  valueUri: URI
  valueUrl: URL
  valueUuid: UUID
  valueAddress: Address
  valueAge: Quantity
  valueAnnotation: Annotation
  valueAttachment: Attachment
  valueCodeableConcept: CodeableConcept
  valueCoding: Coding
  valueContactPoint: ContactPoint
  valueCount: Quantity
  valueDistance: Quantity
  valueDuration: Quantity
  valueHumanName: HumanName
  valueIdentifier: Identifier
  valueMoney: Money
  valuePeriod: Period
  valueQuantity: Quantity
  valueRange: Range
  valueRatio: Ratio
  valueReference: ParametersParameterValueReferenceReference
  valueSampledData: SampledData
  valueSignature: Signature
  valueTiming: Timing
  valueContactDetail: ContactDetail
  valueContributor: Contributor
  valueDataRequirement: DataRequirement
  valueExpression: Expression
  valueParameterDefinition: ParameterDefinition
  valueRelatedArtifact: RelatedArtifact
  valueTriggerDefinition: TriggerDefinition
  valueUsageContext: UsageContext
  valueDosage: Dosage
  valueMeta: Meta
  resource: Resource
  part: [ParametersParameter]
}

type PatientCommunication {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  language: CodeableConcept
  preferred: Boolean
}

type PatientContactOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type PatientContact {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  relationship: [CodeableConcept]
  name: HumanName
  telecom: [ContactPoint]
  address: Address
  gender: Code
  organization: PatientContactOrganizationReference
  period: Period
}

union PatientLinkOther = Patient | RelatedPerson

type PatientLinkOtherReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PatientLinkOther
  type: URI
  identifier: Identifier
  display: String
}

type PatientLink {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  other: PatientLinkOtherReference
  type: Code
}

type PaymentReconciliationDetailRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union PaymentReconciliationDetailSubmitter = Practitioner | PractitionerRole | Organization

type PaymentReconciliationDetailSubmitterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PaymentReconciliationDetailSubmitter
  type: URI
  identifier: Identifier
  display: String
}

type PaymentReconciliationDetailResponseReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type PaymentReconciliationDetailResponsibleReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PractitionerRole
  type: URI
  identifier: Identifier
  display: String
}

union PaymentReconciliationDetailPayee = Practitioner | PractitionerRole | Organization

type PaymentReconciliationDetailPayeeReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PaymentReconciliationDetailPayee
  type: URI
  identifier: Identifier
  display: String
}

type PaymentReconciliationDetail {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  predecessor: Identifier
  type: CodeableConcept
  request: PaymentReconciliationDetailRequestReference
  submitter: PaymentReconciliationDetailSubmitterReference
  response: PaymentReconciliationDetailResponseReference
  date: Date
  responsible: PaymentReconciliationDetailResponsibleReference
  payee: PaymentReconciliationDetailPayeeReference
  amount: Money
}

type PaymentReconciliationProcessNote {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  text: String
}

union PersonLinkTarget = Patient | Practitioner | RelatedPerson | Person

type PersonLinkTargetReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PersonLinkTarget
  type: URI
  identifier: Identifier
  display: String
}

type PersonLink {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  target: PersonLinkTargetReference
  assurance: Code
}

type PlanDefinitionActionSubjectReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type PlanDefinitionAction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  prefix: String
  title: String
  description: String
  textEquivalent: String
  priority: Code
  code: [CodeableConcept]
  reason: [CodeableConcept]
  documentation: [RelatedArtifact]
  goalId: [ID]
  subjectCodeableConcept: CodeableConcept
  subjectReference: PlanDefinitionActionSubjectReferenceReference
  subjectCanonical: Canonical
  trigger: [TriggerDefinition]
  condition: [PlanDefinitionCondition]
  input: [DataRequirement]
  output: [DataRequirement]
  relatedAction: [PlanDefinitionRelatedAction]
  timingDateTime: DateTime
  timingAge: Quantity
  timingPeriod: Period
  timingDuration: Quantity
  timingRange: Range
  timingTiming: Timing
  participant: [PlanDefinitionParticipant]
  type: CodeableConcept
  groupingBehavior: Code
  selectionBehavior: Code
  requiredBehavior: Code
  precheckBehavior: Code
  cardinalityBehavior: Code
  definitionCanonical: Canonical
  definitionUri: URI
  transform: Canonical
  dynamicValue: [PlanDefinitionDynamicValue]
  action: [PlanDefinitionAction]
}

type PlanDefinitionCondition {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  kind: Code
  expression: Expression
}

type PlanDefinitionDynamicValue {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  path: String
  expression: Expression
}

type PlanDefinitionGoal {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  category: CodeableConcept
  description: CodeableConcept
  priority: CodeableConcept
  start: CodeableConcept
  addresses: [CodeableConcept]
  documentation: [RelatedArtifact]
  target: [PlanDefinitionTarget]
}

type PlanDefinitionParticipant {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  role: CodeableConcept
}

type PlanDefinitionRelatedAction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  actionId: ID
  relationship: Code
  offsetDuration: Quantity
  offsetRange: Range
}

type PlanDefinitionTarget {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  measure: CodeableConcept
  detailQuantity: Quantity
  detailRange: Range
  detailCodeableConcept: CodeableConcept
  due: Quantity
}

type Population {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  ageRange: Range
  ageCodeableConcept: CodeableConcept
  gender: CodeableConcept
  race: CodeableConcept
  physiologicalCondition: CodeableConcept
}

type PractitionerQualificationIssuerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type PractitionerQualification {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  code: CodeableConcept
  period: Period
  issuer: PractitionerQualificationIssuerReference
}

type PractitionerRoleAvailableTime {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  daysOfWeek: [Code]
  allDay: Boolean
  availableStartTime: Time
  availableEndTime: Time
}

type PractitionerRoleNotAvailable {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  during: Period
}

type ProcedureFocalDeviceManipulatedReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type ProcedureFocalDevice {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  action: CodeableConcept
  manipulated: ProcedureFocalDeviceManipulatedReference
}

union ProcedurePerformerActor = Practitioner | PractitionerRole | Organization | Patient | RelatedPerson | Device

type ProcedurePerformerActorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProcedurePerformerActor
  type: URI
  identifier: Identifier
  display: String
}

type ProcedurePerformerOnBehalfOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type ProcedurePerformer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  function: CodeableConcept
  actor: ProcedurePerformerActorReference
  onBehalfOf: ProcedurePerformerOnBehalfOfReference
}

type ProdCharacteristic {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  height: Quantity
  width: Quantity
  depth: Quantity
  weight: Quantity
  nominalVolume: Quantity
  externalDiameter: Quantity
  shape: String
  color: [String]
  imprint: [String]
  image: [Attachment]
  scoring: CodeableConcept
}

type ProductShelfLife {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  type: CodeableConcept
  period: Quantity
  specialPrecautionsForStorage: [CodeableConcept]
}

union ProvenanceAgentWho = Practitioner | PractitionerRole | RelatedPerson | Patient | Device | Organization

type ProvenanceAgentWhoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProvenanceAgentWho
  type: URI
  identifier: Identifier
  display: String
}

union ProvenanceAgentOnBehalfOf = Practitioner | PractitionerRole | RelatedPerson | Patient | Device | Organization

type ProvenanceAgentOnBehalfOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProvenanceAgentOnBehalfOf
  type: URI
  identifier: Identifier
  display: String
}

type ProvenanceAgent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  role: [CodeableConcept]
  who: ProvenanceAgentWhoReference
  onBehalfOf: ProvenanceAgentOnBehalfOfReference
}

type ProvenanceEntityWhatReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ProvenanceEntity {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  role: Code
  what: ProvenanceEntityWhatReference
  agent: [ProvenanceAgent]
}

type QuestionnaireAnswerOptionValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type QuestionnaireAnswerOption {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  valueInteger: Int
  valueDate: Date
  valueTime: Time
  valueString: String
  valueCoding: Coding
  valueReference: QuestionnaireAnswerOptionValueReferenceReference
  initialSelected: Boolean
}

type QuestionnaireEnableWhenAnswerReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type QuestionnaireEnableWhen {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  question: String
  operator: Code
  answerBoolean: Boolean
  answerDecimal: Float
  answerInteger: Int
  answerDate: Date
  answerDateTime: DateTime
  answerTime: Time
  answerString: String
  answerCoding: Coding
  answerQuantity: Quantity
  answerReference: QuestionnaireEnableWhenAnswerReferenceReference
}

type QuestionnaireInitialValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type QuestionnaireInitial {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  valueBoolean: Boolean
  valueDecimal: Float
  valueInteger: Int
  valueDate: Date
  valueDateTime: DateTime
  valueTime: Time
  valueString: String
  valueUri: URI
  valueAttachment: Attachment
  valueCoding: Coding
  valueQuantity: Quantity
  valueReference: QuestionnaireInitialValueReferenceReference
}

type QuestionnaireItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  linkId: String
  definition: URI
  code: [Coding]
  prefix: String
  text: String
  type: Code
  enableWhen: [QuestionnaireEnableWhen]
  enableBehavior: Code
  required: Boolean
  repeats: Boolean
  readOnly: Boolean
  maxLength: Int
  answerValueSet: Canonical
  answerOption: [QuestionnaireAnswerOption]
  initial: [QuestionnaireInitial]
  item: [QuestionnaireItem]
}

type QuestionnaireResponseAnswerValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type QuestionnaireResponseAnswer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  valueBoolean: Boolean
  valueDecimal: Float
  valueInteger: Int
  valueDate: Date
  valueDateTime: DateTime
  valueTime: Time
  valueString: String
  valueUri: URI
  valueAttachment: Attachment
  valueCoding: Coding
  valueQuantity: Quantity
  valueReference: QuestionnaireResponseAnswerValueReferenceReference
  item: [QuestionnaireResponseItem]
}

type QuestionnaireResponseItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  linkId: String
  definition: URI
  text: String
  answer: [QuestionnaireResponseAnswer]
  item: [QuestionnaireResponseItem]
}

type RegulatedAuthorizationCase {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  type: CodeableConcept
  status: CodeableConcept
  datePeriod: Period
  dateDateTime: DateTime
  application: [RegulatedAuthorizationCase]
}

type RelatedPersonCommunication {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  language: CodeableConcept
  preferred: Boolean
}

union RequestGroupActionParticipant = Patient | Practitioner | PractitionerRole | RelatedPerson | Device

type RequestGroupActionParticipantReference {
  id: String
  extension: [Extension]
  reference: String
  resource: RequestGroupActionParticipant
  type: URI
  identifier: Identifier
  display: String
}

type RequestGroupActionResourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type RequestGroupAction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  prefix: String
  title: String
  description: String
  textEquivalent: String
  priority: Code
  code: [CodeableConcept]
  documentation: [RelatedArtifact]
  condition: [RequestGroupCondition]
  relatedAction: [RequestGroupRelatedAction]
  timingDateTime: DateTime
  timingAge: Quantity
  timingPeriod: Period
  timingDuration: Quantity
  timingRange: Range
  timingTiming: Timing
  participant: [RequestGroupActionParticipantReference]
  type: CodeableConcept
  groupingBehavior: Code
  selectionBehavior: Code
  requiredBehavior: Code
  precheckBehavior: Code
  cardinalityBehavior: Code
  resource: RequestGroupActionResourceReference
  action: [RequestGroupAction]
}

type RequestGroupCondition {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  kind: Code
  expression: Expression
}

type RequestGroupRelatedAction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  actionId: ID
  relationship: Code
  offsetDuration: Quantity
  offsetRange: Range
}

type ResearchElementDefinitionCharacteristic {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  definitionCodeableConcept: CodeableConcept
  definitionCanonical: Canonical
  definitionExpression: Expression
  definitionDataRequirement: DataRequirement
  usageContext: [UsageContext]
  exclude: Boolean
  unitOfMeasure: CodeableConcept
  studyEffectiveDescription: String
  studyEffectiveDateTime: DateTime
  studyEffectivePeriod: Period
  studyEffectiveDuration: Quantity
  studyEffectiveTiming: Timing
  studyEffectiveTimeFromStart: Quantity
  studyEffectiveGroupMeasure: Code
  participantEffectiveDescription: String
  participantEffectiveDateTime: DateTime
  participantEffectivePeriod: Period
  participantEffectiveDuration: Quantity
  participantEffectiveTiming: Timing
  participantEffectiveTimeFromStart: Quantity
  participantEffectiveGroupMeasure: Code
}

type ResearchStudyArm {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  type: CodeableConcept
  description: String
}

type ResearchStudyObjective {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  type: CodeableConcept
}

type RiskAssessmentPrediction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  outcome: CodeableConcept
  probabilityDecimal: Float
  probabilityRange: Range
  qualitativeRisk: CodeableConcept
  relativeRisk: Float
  whenPeriod: Period
  whenRange: Range
  rationale: String
}

type SearchParameterComponent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  definition: Canonical
  expression: String
}

union SpecimenCollectionCollector = Practitioner | PractitionerRole

type SpecimenCollectionCollectorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SpecimenCollectionCollector
  type: URI
  identifier: Identifier
  display: String
}

type SpecimenCollection {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  collector: SpecimenCollectionCollectorReference
  collectedDateTime: DateTime
  collectedPeriod: Period
  duration: Quantity
  quantity: Quantity
  method: CodeableConcept
  bodySite: CodeableConcept
  fastingStatusCodeableConcept: CodeableConcept
  fastingStatusDuration: Quantity
}

type SpecimenContainerAdditiveReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Substance
  type: URI
  identifier: Identifier
  display: String
}

type SpecimenContainer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  description: String
  type: CodeableConcept
  capacity: Quantity
  specimenQuantity: Quantity
  additiveCodeableConcept: CodeableConcept
  additiveReference: SpecimenContainerAdditiveReferenceReference
}

type SpecimenDefinitionAdditiveAdditiveReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Substance
  type: URI
  identifier: Identifier
  display: String
}

type SpecimenDefinitionAdditive {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  additiveCodeableConcept: CodeableConcept
  additiveReference: SpecimenDefinitionAdditiveAdditiveReferenceReference
}

type SpecimenDefinitionContainer {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  material: CodeableConcept
  type: CodeableConcept
  cap: CodeableConcept
  description: String
  capacity: Quantity
  minimumVolumeQuantity: Quantity
  minimumVolumeString: String
  additive: [SpecimenDefinitionAdditive]
  preparation: String
}

type SpecimenDefinitionHandling {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  temperatureQualifier: CodeableConcept
  temperatureRange: Range
  maxDuration: Quantity
  instruction: String
}

type SpecimenDefinitionTypeTested {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  isDerived: Boolean
  type: CodeableConcept
  preference: Code
  container: SpecimenDefinitionContainer
  requirement: String
  retentionTime: Quantity
  rejectionCriterion: [CodeableConcept]
  handling: [SpecimenDefinitionHandling]
}

type SpecimenProcessingAdditiveReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Substance
  type: URI
  identifier: Identifier
  display: String
}

type SpecimenProcessing {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  procedure: CodeableConcept
  additive: [SpecimenProcessingAdditiveReference]
  timeDateTime: DateTime
  timePeriod: Period
}

type StructureDefinitionContext {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  expression: String
}

type StructureDefinitionDifferential {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  element: [ElementDefinition]
}

type StructureDefinitionMapping {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identity: ID
  uri: URI
  name: String
  comment: String
}

type StructureDefinitionSnapshot {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  element: [ElementDefinition]
}

type StructureMapDependent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: ID
  variable: [String]
}

type StructureMapGroup {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: ID
  extends: ID
  typeMode: Code
  documentation: String
  input: [StructureMapInput]
  rule: [StructureMapRule]
}

type StructureMapInput {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: ID
  type: String
  mode: Code
  documentation: String
}

type StructureMapParameter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  valueId: ID
  valueString: String
  valueBoolean: Boolean
  valueInteger: Int
  valueDecimal: Float
}

type StructureMapRule {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: ID
  source: [StructureMapSource]
  target: [StructureMapTarget]
  rule: [StructureMapRule]
  dependent: [StructureMapDependent]
  documentation: String
}

type StructureMapSourceDefaultValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type StructureMapSource {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  context: ID
  min: Int
  max: String
  type: String
  defaultValueBase64Binary: Base64Binary
  defaultValueBoolean: Boolean
  defaultValueCanonical: Canonical
  defaultValueCode: Code
  defaultValueDate: Date
  defaultValueDateTime: DateTime
  defaultValueDecimal: Float
  defaultValueId: ID
  defaultValueInstant: Instant
  defaultValueInteger: Int
  defaultValueMarkdown: Markdown
  defaultValueOid: OID
  defaultValuePositiveInt: Int
  defaultValueString: String
  defaultValueTime: Time
  defaultValueUnsignedInt: Int
  defaultValueUri: URI
  defaultValueUrl: URL
  defaultValueUuid: UUID
  defaultValueAddress: Address
  defaultValueAge: Quantity
  defaultValueAnnotation: Annotation
  defaultValueAttachment: Attachment
  defaultValueCodeableConcept: CodeableConcept
  defaultValueCoding: Coding
  defaultValueContactPoint: ContactPoint
  defaultValueCount: Quantity
  defaultValueDistance: Quantity
  defaultValueDuration: Quantity
  defaultValueHumanName: HumanName
  defaultValueIdentifier: Identifier
  defaultValueMoney: Money
  defaultValuePeriod: Period
  defaultValueQuantity: Quantity
  defaultValueRange: Range
  defaultValueRatio: Ratio
  defaultValueReference: StructureMapSourceDefaultValueReferenceReference
  defaultValueSampledData: SampledData
  defaultValueSignature: Signature
  defaultValueTiming: Timing
  defaultValueContactDetail: ContactDetail
  defaultValueContributor: Contributor
  defaultValueDataRequirement: DataRequirement
  defaultValueExpression: Expression
  defaultValueParameterDefinition: ParameterDefinition
  defaultValueRelatedArtifact: RelatedArtifact
  defaultValueTriggerDefinition: TriggerDefinition
  defaultValueUsageContext: UsageContext
  defaultValueDosage: Dosage
  defaultValueMeta: Meta
  element: String
  listMode: Code
  variable: ID
  condition: String
  check: String
  logMessage: String
}

type StructureMapStructure {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  url: Canonical
  mode: Code
  alias: String
  documentation: String
}

type StructureMapTarget {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  context: ID
  contextType: Code
  element: String
  variable: ID
  listMode: [Code]
  listRuleId: ID
  transform: Code
  parameter: [StructureMapParameter]
}

type SubscriptionChannel {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  endpoint: URL
  payload: Code
  header: [String]
}

type SubscriptionStatusNotificationEventFocusReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type SubscriptionStatusNotificationEventAdditionalContextReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type SubscriptionStatusNotificationEvent {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  eventNumber: String
  timestamp: Instant
  focus: SubscriptionStatusNotificationEventFocusReference
  additionalContext: [SubscriptionStatusNotificationEventAdditionalContextReference]
}

type SubscriptionTopicCanFilterBy {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: Markdown
  resource: URI
  filterParameter: String
  filterDefinition: URI
  modifier: [Code]
}

type SubscriptionTopicEventTrigger {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: Markdown
  event: CodeableConcept
  resource: URI
}

type SubscriptionTopicNotificationShape {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  resource: URI
  include: [String]
  revInclude: [String]
}

type SubscriptionTopicQueryCriteria {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  previous: String
  resultForCreate: Code
  current: String
  resultForDelete: Code
  requireBoth: Boolean
}

type SubscriptionTopicResourceTrigger {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: Markdown
  resource: URI
  supportedInteraction: [Code]
  queryCriteria: SubscriptionTopicQueryCriteria
  fhirPathCriteria: String
}

type SubstanceDefinitionCodeSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReference
  type: URI
  identifier: Identifier
  display: String
}

type SubstanceDefinitionCode {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  status: CodeableConcept
  statusDate: DateTime
  note: [Annotation]
  source: [SubstanceDefinitionCodeSourceReference]
}

type SubstanceDefinitionMoiety {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  role: CodeableConcept
  identifier: Identifier
  name: String
  stereochemistry: CodeableConcept
  opticalActivity: CodeableConcept
  molecularFormula: String
  amountQuantity: Quantity
  amountString: String
  measurementType: CodeableConcept
}

type SubstanceDefinitionMolecularWeight {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  method: CodeableConcept
  type: CodeableConcept
  amount: Quantity
}

type SubstanceDefinitionNameSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReference
  type: URI
  identifier: Identifier
  display: String
}

type SubstanceDefinitionName {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  type: CodeableConcept
  status: CodeableConcept
  preferred: Boolean
  language: [CodeableConcept]
  domain: [CodeableConcept]
  jurisdiction: [CodeableConcept]
  synonym: [SubstanceDefinitionName]
  translation: [SubstanceDefinitionName]
  official: [SubstanceDefinitionOfficial]
  source: [SubstanceDefinitionNameSourceReference]
}

type SubstanceDefinitionOfficial {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  authority: CodeableConcept
  status: CodeableConcept
  date: DateTime
}

type SubstanceDefinitionProperty {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueCodeableConcept: CodeableConcept
  valueQuantity: Quantity
  valueDate: Date
  valueBoolean: Boolean
  valueAttachment: Attachment
}

type SubstanceDefinitionRelationshipSubstanceDefinitionReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SubstanceDefinition
  type: URI
  identifier: Identifier
  display: String
}

type SubstanceDefinitionRelationshipSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReference
  type: URI
  identifier: Identifier
  display: String
}

type SubstanceDefinitionRelationship {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  substanceDefinitionReference: SubstanceDefinitionRelationshipSubstanceDefinitionReferenceReference
  substanceDefinitionCodeableConcept: CodeableConcept
  type: CodeableConcept
  isDefining: Boolean
  amountQuantity: Quantity
  amountRatio: Ratio
  amountString: String
  ratioHighLimitAmount: Ratio
  comparator: CodeableConcept
  source: [SubstanceDefinitionRelationshipSourceReference]
}

type SubstanceDefinitionRepresentationDocumentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReference
  type: URI
  identifier: Identifier
  display: String
}

type SubstanceDefinitionRepresentation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  representation: String
  format: CodeableConcept
  document: SubstanceDefinitionRepresentationDocumentReference
}

type SubstanceDefinitionSourceMaterial {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  genus: CodeableConcept
  species: CodeableConcept
  part: CodeableConcept
  countryOfOrigin: [CodeableConcept]
}

type SubstanceDefinitionStructureSourceDocumentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReference
  type: URI
  identifier: Identifier
  display: String
}

type SubstanceDefinitionStructure {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  stereochemistry: CodeableConcept
  opticalActivity: CodeableConcept
  molecularFormula: String
  molecularFormulaByMoiety: String
  molecularWeight: SubstanceDefinitionMolecularWeight
  technique: [CodeableConcept]
  sourceDocument: [SubstanceDefinitionStructureSourceDocumentReference]
  representation: [SubstanceDefinitionRepresentation]
}

type SubstanceIngredientSubstanceReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Substance
  type: URI
  identifier: Identifier
  display: String
}

type SubstanceIngredient {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  quantity: Ratio
  substanceCodeableConcept: CodeableConcept
  substanceReference: SubstanceIngredientSubstanceReferenceReference
}

type SubstanceInstance {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  expiry: DateTime
  quantity: Quantity
}

union SupplyDeliverySuppliedItemItemReference = Medication | Substance | Device

type SupplyDeliverySuppliedItemItemReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyDeliverySuppliedItemItemReference
  type: URI
  identifier: Identifier
  display: String
}

type SupplyDeliverySuppliedItem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  quantity: Quantity
  itemCodeableConcept: CodeableConcept
  itemReference: SupplyDeliverySuppliedItemItemReferenceReference
}

type SupplyRequestParameter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  valueCodeableConcept: CodeableConcept
  valueQuantity: Quantity
  valueRange: Range
  valueBoolean: Boolean
}

type TaskInputValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type TaskInput {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueBase64Binary: Base64Binary
  valueBoolean: Boolean
  valueCanonical: Canonical
  valueCode: Code
  valueDate: Date
  valueDateTime: DateTime
  valueDecimal: Float
  valueId: ID
  valueInstant: Instant
  valueInteger: Int
  valueMarkdown: Markdown
  valueOid: OID
  valuePositiveInt: Int
  valueString: String
  valueTime: Time
  valueUnsignedInt: Int
  valueUri: URI
  valueUrl: URL
  valueUuid: UUID
  valueAddress: Address
  valueAge: Quantity
  valueAnnotation: Annotation
  valueAttachment: Attachment
  valueCodeableConcept: CodeableConcept
  valueCoding: Coding
  valueContactPoint: ContactPoint
  valueCount: Quantity
  valueDistance: Quantity
  valueDuration: Quantity
  valueHumanName: HumanName
  valueIdentifier: Identifier
  valueMoney: Money
  valuePeriod: Period
  valueQuantity: Quantity
  valueRange: Range
  valueRatio: Ratio
  valueReference: TaskInputValueReferenceReference
  valueSampledData: SampledData
  valueSignature: Signature
  valueTiming: Timing
  valueContactDetail: ContactDetail
  valueContributor: Contributor
  valueDataRequirement: DataRequirement
  valueExpression: Expression
  valueParameterDefinition: ParameterDefinition
  valueRelatedArtifact: RelatedArtifact
  valueTriggerDefinition: TriggerDefinition
  valueUsageContext: UsageContext
  valueDosage: Dosage
  valueMeta: Meta
}

type TaskOutputValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type TaskOutput {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: CodeableConcept
  valueBase64Binary: Base64Binary
  valueBoolean: Boolean
  valueCanonical: Canonical
  valueCode: Code
  valueDate: Date
  valueDateTime: DateTime
  valueDecimal: Float
  valueId: ID
  valueInstant: Instant
  valueInteger: Int
  valueMarkdown: Markdown
  valueOid: OID
  valuePositiveInt: Int
  valueString: String
  valueTime: Time
  valueUnsignedInt: Int
  valueUri: URI
  valueUrl: URL
  valueUuid: UUID
  valueAddress: Address
  valueAge: Quantity
  valueAnnotation: Annotation
  valueAttachment: Attachment
  valueCodeableConcept: CodeableConcept
  valueCoding: Coding
  valueContactPoint: ContactPoint
  valueCount: Quantity
  valueDistance: Quantity
  valueDuration: Quantity
  valueHumanName: HumanName
  valueIdentifier: Identifier
  valueMoney: Money
  valuePeriod: Period
  valueQuantity: Quantity
  valueRange: Range
  valueRatio: Ratio
  valueReference: TaskOutputValueReferenceReference
  valueSampledData: SampledData
  valueSignature: Signature
  valueTiming: Timing
  valueContactDetail: ContactDetail
  valueContributor: Contributor
  valueDataRequirement: DataRequirement
  valueExpression: Expression
  valueParameterDefinition: ParameterDefinition
  valueRelatedArtifact: RelatedArtifact
  valueTriggerDefinition: TriggerDefinition
  valueUsageContext: UsageContext
  valueDosage: Dosage
  valueMeta: Meta
}

union TaskRestrictionRecipient = Patient | Practitioner | PractitionerRole | RelatedPerson | Group | Organization

type TaskRestrictionRecipientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: TaskRestrictionRecipient
  type: URI
  identifier: Identifier
  display: String
}

type TaskRestriction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  repetitions: Int
  period: Period
  recipient: [TaskRestrictionRecipientReference]
}

type TerminologyCapabilitiesClosure {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  translation: Boolean
}

type TerminologyCapabilitiesCodeSystem {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  uri: Canonical
  version: [TerminologyCapabilitiesVersion]
  subsumption: Boolean
}

type TerminologyCapabilitiesExpansion {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  hierarchical: Boolean
  paging: Boolean
  incomplete: Boolean
  parameter: [TerminologyCapabilitiesParameter]
  textFilter: Markdown
}

type TerminologyCapabilitiesFilter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  op: [Code]
}

type TerminologyCapabilitiesImplementation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  description: String
  url: URL
}

type TerminologyCapabilitiesParameter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: Code
  documentation: String
}

type TerminologyCapabilitiesSoftware {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  version: String
}

type TerminologyCapabilitiesTranslation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  needsMap: Boolean
}

type TerminologyCapabilitiesValidateCode {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  translations: Boolean
}

type TerminologyCapabilitiesVersion {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: String
  isDefault: Boolean
  compositional: Boolean
  language: [Code]
  filter: [TerminologyCapabilitiesFilter]
  property: [Code]
}

type TestReportAction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  operation: TestReportOperation
  assert: TestReportAssert
}

type TestReportAction1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  operation: TestReportOperation
  assert: TestReportAssert
}

type TestReportAction2 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  operation: TestReportOperation
}

type TestReportAssert {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  result: Code
  message: Markdown
  detail: String
}

type TestReportOperation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  result: Code
  message: Markdown
  detail: URI
}

type TestReportParticipant {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Code
  uri: URI
  display: String
}

type TestReportSetup {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  action: [TestReportAction]
}

type TestReportTeardown {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  action: [TestReportAction2]
}

type TestReportTest {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  description: String
  action: [TestReportAction1]
}

type TestScriptAction {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  operation: TestScriptOperation
  assert: TestScriptAssert
}

type TestScriptAction1 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  operation: TestScriptOperation
  assert: TestScriptAssert
}

type TestScriptAction2 {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  operation: TestScriptOperation
}

type TestScriptAssert {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  label: String
  description: String
  direction: Code
  compareToSourceId: String
  compareToSourceExpression: String
  compareToSourcePath: String
  contentType: Code
  expression: String
  headerField: String
  minimumId: String
  navigationLinks: Boolean
  operator: Code
  path: String
  requestMethod: Code
  requestURL: String
  resource: Code
  response: Code
  responseCode: String
  sourceId: ID
  validateProfileId: ID
  value: String
  warningOnly: Boolean
}

type TestScriptCapability {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  required: Boolean
  validated: Boolean
  description: String
  origin: [Int]
  destination: Int
  link: [URI]
  capabilities: Canonical
}

type TestScriptDestination {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  index: Int
  profile: Coding
}

type TestScriptFixtureResourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type TestScriptFixture {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  autocreate: Boolean
  autodelete: Boolean
  resource: TestScriptFixtureResourceReference
}

type TestScriptLink {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  description: String
}

type TestScriptMetadata {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  link: [TestScriptLink]
  capability: [TestScriptCapability]
}

type TestScriptOperation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  type: Coding
  resource: Code
  label: String
  description: String
  accept: Code
  contentType: Code
  destination: Int
  encodeRequestUrl: Boolean
  method: Code
  origin: Int
  params: String
  requestHeader: [TestScriptRequestHeader]
  requestId: ID
  responseId: ID
  sourceId: ID
  targetId: ID
  url: String
}

type TestScriptOrigin {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  index: Int
  profile: Coding
}

type TestScriptRequestHeader {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  field: String
  value: String
}

type TestScriptSetup {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  action: [TestScriptAction]
}

type TestScriptTeardown {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  action: [TestScriptAction2]
}

type TestScriptTest {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  description: String
  action: [TestScriptAction1]
}

type TestScriptVariable {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  defaultValue: String
  description: String
  expression: String
  headerField: String
  hint: String
  path: String
  sourceId: ID
}

type Timing {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  event: [DateTime]
  repeat: TimingRepeat
  code: CodeableConcept
}

type TimingRepeat {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  boundsDuration: Quantity
  boundsRange: Range
  boundsPeriod: Period
  count: Int
  countMax: Int
  duration: Float
  durationMax: Float
  durationUnit: Code
  frequency: Int
  frequencyMax: Int
  period: Float
  periodMax: Float
  periodUnit: Code
  dayOfWeek: [Code]
  timeOfDay: [Time]
  when: [Code]
  offset: Int
}

type ValueSetCompose {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  lockedDate: Date
  inactive: Boolean
  include: [ValueSetInclude]
  exclude: [ValueSetInclude]
}

type ValueSetConcept {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  code: Code
  display: String
  designation: [ValueSetDesignation]
}

type ValueSetContains {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  system: URI
  abstract: Boolean
  inactive: Boolean
  version: String
  code: Code
  display: String
  designation: [ValueSetDesignation]
  contains: [ValueSetContains]
}

type ValueSetDesignation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  language: Code
  use: Coding
  value: String
}

type ValueSetExpansion {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: URI
  timestamp: DateTime
  total: Int
  offset: Int
  parameter: [ValueSetParameter]
  contains: [ValueSetContains]
}

type ValueSetFilter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  property: Code
  op: Code
  value: String
}

type ValueSetInclude {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  system: URI
  version: String
  concept: [ValueSetConcept]
  filter: [ValueSetFilter]
  valueSet: [Canonical]
}

type ValueSetParameter {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  valueString: String
  valueBoolean: Boolean
  valueInteger: Int
  valueDecimal: Float
  valueUri: URI
  valueCode: Code
  valueDateTime: DateTime
}

union VerificationResultAttestationWho = Practitioner | PractitionerRole | Organization

type VerificationResultAttestationWhoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: VerificationResultAttestationWho
  type: URI
  identifier: Identifier
  display: String
}

union VerificationResultAttestationOnBehalfOf = Organization | Practitioner | PractitionerRole

type VerificationResultAttestationOnBehalfOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: VerificationResultAttestationOnBehalfOf
  type: URI
  identifier: Identifier
  display: String
}

type VerificationResultAttestation {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  who: VerificationResultAttestationWhoReference
  onBehalfOf: VerificationResultAttestationOnBehalfOfReference
  communicationMethod: CodeableConcept
  date: Date
  sourceIdentityCertificate: String
  proxyIdentityCertificate: String
  proxySignature: Signature
  sourceSignature: Signature
}

union VerificationResultPrimarySourceWho = Organization | Practitioner | PractitionerRole

type VerificationResultPrimarySourceWhoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: VerificationResultPrimarySourceWho
  type: URI
  identifier: Identifier
  display: String
}

type VerificationResultPrimarySource {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  who: VerificationResultPrimarySourceWhoReference
  type: [CodeableConcept]
  communicationMethod: [CodeableConcept]
  validationStatus: CodeableConcept
  validationDate: DateTime
  canPushUpdates: CodeableConcept
  pushTypeAvailable: [CodeableConcept]
}

type VerificationResultValidatorOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type VerificationResultValidator {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  organization: VerificationResultValidatorOrganizationReference
  identityCertificate: String
  attestationSignature: Signature
}

type VisionPrescriptionLensSpecification {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  product: CodeableConcept
  eye: Code
  sphere: Float
  cylinder: Float
  axis: Int
  prism: [VisionPrescriptionPrism]
  add: Float
  power: Float
  backCurve: Float
  diameter: Float
  duration: Quantity
  color: String
  brand: String
  note: [Annotation]
}

type VisionPrescriptionPrism {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
  amount: Float
  base: Code
}

type Address {
  id: String
  extension: [Extension]
  use: Code
  type: Code
  text: String
  line: [String]
  city: String
  district: String
  state: String
  postalCode: String
  country: String
  period: Period
}

type Age {
  value: Float
  comparator: Code
  unit: String
  system: URI
  code: Code
}

union AnnotationAuthorReference = Practitioner | Patient | RelatedPerson | Organization

type AnnotationAuthorReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AnnotationAuthorReference
  type: URI
  identifier: Identifier
  display: String
}

type Annotation {
  id: String
  extension: [Extension]
  authorReference: AnnotationAuthorReferenceReference
  authorString: String
  time: DateTime
  text: Markdown
}

type Attachment {
  id: String
  extension: [Extension]
  contentType: Code
  language: Code
  data: Base64Binary
  url: URL
  size: Int
  hash: Base64Binary
  title: String
  creation: DateTime
}

type BackboneElement {
  id: String
  extension: [Extension]
  modifierExtension: [Extension]
}

type CodeableConcept {
  id: String
  extension: [Extension]
  coding: [Coding]
  text: String
}

type CodeableReferenceReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CodeableReference {
  id: String
  extension: [Extension]
  concept: CodeableConcept
  reference: CodeableReferenceReferenceReference
}

type Coding {
  id: String
  extension: [Extension]
  system: URI
  version: String
  code: Code
  display: String
  userSelected: Boolean
}

type ContactDetail {
  id: String
  extension: [Extension]
  name: String
  telecom: [ContactPoint]
}

type ContactPoint {
  id: String
  extension: [Extension]
  system: Code
  value: String
  use: Code
  rank: Int
  period: Period
}

type Contributor {
  id: String
  extension: [Extension]
  type: Code
  name: String
  contact: [ContactDetail]
}

type Count {
  value: Float
  comparator: Code
  unit: String
  system: URI
  code: Code
}

type DataRequirementSubjectReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type DataRequirement {
  id: String
  extension: [Extension]
  type: Code
  profile: [Canonical]
  subjectCodeableConcept: CodeableConcept
  subjectReference: DataRequirementSubjectReferenceReference
  mustSupport: [String]
  codeFilter: [DataRequirementCodeFilter]
  dateFilter: [DataRequirementDateFilter]
  limit: Int
  sort: [DataRequirementSort]
}

type DataRequirementCodeFilter {
  id: String
  extension: [Extension]
  path: String
  searchParam: String
  valueSet: Canonical
  code: [Coding]
}

type DataRequirementDateFilter {
  id: String
  extension: [Extension]
  path: String
  searchParam: String
  valueDateTime: DateTime
  valuePeriod: Period
  valueDuration: Quantity
}

type DataRequirementSort {
  id: String
  extension: [Extension]
  path: String
  direction: Code
}

type Distance {
  value: Float
  comparator: Code
  unit: String
  system: URI
  code: Code
}

type Duration {
  id: String
  extension: [Extension]
  value: Float
  comparator: Code
  unit: String
  system: URI
  code: Code
}

type Element {
  id: String
  extension: [Extension]
}

type Expression {
  id: String
  extension: [Extension]
  description: String
  name: ID
  language: Code
  expression: String
  reference: URI
}

type HumanName {
  id: String
  extension: [Extension]
  use: Code
  text: String
  family: String
  given: [String]
  prefix: [String]
  suffix: [String]
  period: Period
}

type IdentifierAssignerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type Identifier {
  id: String
  extension: [Extension]
  use: Code
  type: CodeableConcept
  system: URI
  value: String
  period: Period
  assigner: IdentifierAssignerReference
}

type Meta {
  id: String
  extension: [Extension]
  versionId: ID
  lastUpdated: Instant
  source: URI
  profile: [Canonical]
  security: [Coding]
  tag: [Coding]
}

type Money {
  id: String
  extension: [Extension]
  value: Float
  currency: Code
}

type Narrative {
  id: String
  extension: [Extension]
  status: Code
  div: XHTML
}

type ParameterDefinition {
  id: String
  extension: [Extension]
  name: Code
  use: Code
  min: Int
  max: String
  documentation: String
  type: Code
  profile: Canonical
}

type Period {
  id: String
  extension: [Extension]
  start: DateTime
  end: DateTime
}

type Quantity {
  id: String
  extension: [Extension]
  value: Float
  comparator: Code
  unit: String
  system: URI
  code: Code
}

type Range {
  id: String
  extension: [Extension]
  low: Quantity
  high: Quantity
}

type Ratio {
  id: String
  extension: [Extension]
  numerator: Quantity
  denominator: Quantity
}

type RatioRange {
  id: String
  extension: [Extension]
  lowNumerator: Quantity
  highNumerator: Quantity
  denominator: Quantity
}

type Reference {
  id: String
  extension: [Extension]
  reference: String
  type: URI
  identifier: Identifier
  display: String
}

type RelatedArtifact {
  id: String
  extension: [Extension]
  type: Code
  label: String
  display: String
  citation: Markdown
  url: URL
  document: Attachment
  resource: Canonical
}

type SampledData {
  id: String
  extension: [Extension]
  origin: Quantity
  period: Float
  factor: Float
  lowerLimit: Float
  upperLimit: Float
  dimensions: Int
  data: String
}

union SignatureWho = Practitioner | PractitionerRole | RelatedPerson | Patient | Device | Organization

type SignatureWhoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SignatureWho
  type: URI
  identifier: Identifier
  display: String
}

union SignatureOnBehalfOf = Practitioner | PractitionerRole | RelatedPerson | Patient | Device | Organization

type SignatureOnBehalfOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SignatureOnBehalfOf
  type: URI
  identifier: Identifier
  display: String
}

type Signature {
  id: String
  extension: [Extension]
  type: [Coding]
  when: Instant
  who: SignatureWhoReference
  onBehalfOf: SignatureOnBehalfOfReference
  targetFormat: Code
  sigFormat: Code
  data: Base64Binary
}

type TriggerDefinitionTimingReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Schedule
  type: URI
  identifier: Identifier
  display: String
}

type TriggerDefinition {
  id: String
  extension: [Extension]
  type: Code
  name: String
  timingTiming: Timing
  timingReference: TriggerDefinitionTimingReferenceReference
  timingDate: Date
  timingDateTime: DateTime
  data: [DataRequirement]
  condition: Expression
}

union UsageContextValueReference = PlanDefinition | ResearchStudy | InsurancePlan | HealthcareService | Group | Location | Organization

type UsageContextValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: UsageContextValueReference
  type: URI
  identifier: Identifier
  display: String
}

type UsageContext {
  id: String
  extension: [Extension]
  code: Coding
  valueCodeableConcept: CodeableConcept
  valueQuantity: Quantity
  valueRange: Range
  valueReference: UsageContextValueReferenceReference
}

"""
DocumentReferenceAttachment
    For referring to data content defined in other formats.
    If the element is present, it must have a value for at least one of the
    defined elements, an @id referenced from the Narrative, or extensions
"""
type DocumentReferenceAttachment {
  """None"""
  id: String

  """
  May be used to represent additional information that is not part of the basic
  definition of the element. To make the use of extensions safe and manageable,
  there is a strict set of governance  applied to the definition and use of
  extensions. Though any implementer can define an extension, there is a set of
  requirements that SHALL be met as part of the definition of the extension.
  """
  extension: [Extension]

  """
  Identifies the type of the data in the attachment and allows a method to be
  chosen to interpret or render the data. Includes mime type parameters such as
  charset where appropriate.
  """
  contentType: Code

  """
  The human language of the content. The value can be any valid value according
  to BCP 47.
  """
  language: Code

  """
  The actual data of the attachment - a sequence of bytes, base64 encoded.
  """
  data: Base64Binary

  """A location where the data can be accessed."""
  url: URL

  """For accessing binary resource saved in 'url' field."""
  resource: Binary

  """
  The number of bytes of data that make up this attachment (before base64
  encoding, if that is done).
  """
  size: Int

  """The calculated hash of the data using SHA-1. Represented using base64."""
  hash: Base64Binary

  """A label or set of text to display in place of the data."""
  title: String

  """The date that the attachment was first created."""
  creation: DateTime
}

type MedicationRequest implements DomainResource & Resource {
  dispense: [MedicationDispense]
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  statusReason: CodeableConcept
  intent: Code
  category: [CodeableConcept]
  priority: Code
  doNotPerform: Boolean
  reportedBoolean: Boolean
  reportedReference: MedicationRequestReportedReferenceReference
  medicationCodeableConcept: CodeableConcept
  medicationReference: MedicationRequestMedicationReferenceReference
  subject: MedicationRequestSubjectReference
  encounter: MedicationRequestEncounterReference
  supportingInformation: [MedicationRequestSupportingInformationReference]
  authoredOn: DateTime
  requester: MedicationRequestRequesterReference
  performer: MedicationRequestPerformerReference
  performerType: CodeableConcept
  recorder: MedicationRequestRecorderReference
  reasonCode: [CodeableConcept]
  reasonReference: [MedicationRequestReasonReferenceReference]
  instantiatesCanonical: [Canonical]
  instantiatesUri: [URI]
  basedOn: [MedicationRequestBasedOnReference]
  groupIdentifier: Identifier
  courseOfTherapyType: CodeableConcept
  insurance: [MedicationRequestInsuranceReference]
  note: [Annotation]
  dosageInstruction: [Dosage]
  dispenseRequest: MedicationRequestDispenseRequest
  substitution: MedicationRequestSubstitution
  priorPrescription: MedicationRequestPriorPrescriptionReference
  detectedIssue: [MedicationRequestDetectedIssueReference]
  eventHistory: [MedicationRequestEventHistoryReference]
}

type Patient implements DomainResource & Resource {
  accounts: [Account]
  adverseEvents: [AdverseEvent]
  allergyIntolerances: [AllergyIntolerance]
  appointments: [Appointment]
  appointmentResponses: [AppointmentResponse]
  basics: [Basic]
  bodyStructures: [BodyStructure]
  carePlans: [CarePlan]
  careTeams: [CareTeam]
  chargeItems: [ChargeItem]
  claims: [Claim]
  claimResponses: [ClaimResponse]
  clinicalImpressions: [ClinicalImpression]
  communications: [Communication]
  communicationRequests: [CommunicationRequest]
  compositions: [Composition]
  conditions: [Condition]
  consents: [Consent]
  contracts: [Contract]
  coverages: [Coverage]
  coverageEligibilityRequests: [CoverageEligibilityRequest]
  coverageEligibilityResponses: [CoverageEligibilityResponse]
  detectedIssues: [DetectedIssue]
  devices: [Device]
  deviceRequests: [DeviceRequest]
  deviceUseStatements: [DeviceUseStatement]
  diagnosticReports: [DiagnosticReport]
  documentManifests: [DocumentManifest]
  documentReferences: [DocumentReference]
  encounters: [Encounter]
  enrollmentRequests: [EnrollmentRequest]
  episodesOfCare: [EpisodeOfCare]
  explanationOfBenefits: [ExplanationOfBenefit]
  familyMemberHistories: [FamilyMemberHistory]
  flags: [Flag]
  goals: [Goal]
  groups: [Group]
  guidanceResponses: [GuidanceResponse]
  imagingStudies: [ImagingStudy]
  immunizations: [Immunization]
  immunizationEvaluations: [ImmunizationEvaluation]
  immunizationRecommendations: [ImmunizationRecommendation]
  invoices: [Invoice]
  linkages: [Linkage]
  lists: [List]
  measureReports: [MeasureReport]
  media: [Media]
  medicationAdministrations: [MedicationAdministration]
  medicationDispenses: [MedicationDispense]
  medicationRequests: [MedicationRequest]
  medicationStatements: [MedicationStatement]
  molecularSequences: [MolecularSequence]
  nutritionOrders: [NutritionOrder]
  observations: [Observation]
  paymentNotices: [PaymentNotice]
  persons: [Person]
  procedures: [Procedure]
  provenances: [Provenance]
  questionnaireResponses: [QuestionnaireResponse]
  relatedPersons: [RelatedPerson]
  requestGroups: [RequestGroup]
  researchSubjects: [ResearchSubject]
  riskAssessments: [RiskAssessment]
  schedules: [Schedule]
  serviceRequests: [ServiceRequest]
  specimens: [Specimen]
  subscriptions: [Subscription]
  subscriptionStatuses: [SubscriptionStatus]
  subscriptionTopics: [SubscriptionTopic]
  supplyDeliveries: [SupplyDelivery]
  supplyRequests: [SupplyRequest]
  tasks: [Task]
  visionPrescriptions: [VisionPrescription]
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  active: Boolean
  name: [HumanName]
  telecom: [ContactPoint]
  gender: Code
  birthDate: Date
  deceasedBoolean: Boolean
  deceasedDateTime: DateTime
  address: [Address]
  maritalStatus: CodeableConcept
  multipleBirthBoolean: Boolean
  multipleBirthInteger: Int
  photo: [Attachment]
  contact: [PatientContact]
  communication: [PatientCommunication]
  generalPractitioner: [PatientGeneralPractitionerReference]
  managingOrganization: PatientManagingOrganizationReference
  link: [PatientLink]
}

type Practitioner implements DomainResource & Resource {
  practitionerRole: [PractitionerRole]
  group: [Group]
  measureReport: [MeasureReport]
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  active: Boolean
  name: [HumanName]
  telecom: [ContactPoint]
  address: [Address]
  gender: Code
  birthDate: Date
  photo: [Attachment]
  qualification: [PractitionerQualification]
  communication: [CodeableConcept]
}

type Subscription implements DomainResource & Resource {
  subscriptionStatus: [SubscriptionStatus]
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  status: Code
  contact: [ContactPoint]
  end: Instant
  reason: String
  criteria: String
  error: String
  channel: SubscriptionChannel
}

type SubscriptionStatus implements DomainResource & Resource {
  subscriptionTopic: SubscriptionTopic
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  status: Code
  type: Code
  eventsSinceSubscriptionStart: String
  notificationEvent: [SubscriptionStatusNotificationEvent]
  subscription: SubscriptionStatusSubscriptionReference
  topic: Canonical
  error: [CodeableConcept]
}

type ExtensionValueReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type Extension {
  id: String
  extension: [Extension]
  url: URI
  valueBase64Binary: Base64Binary
  valueBoolean: Boolean
  valueCanonical: Canonical
  valueCode: Code
  valueDate: Date
  valueDateTime: DateTime
  valueDecimal: Float
  valueId: ID
  valueInstant: Instant
  valueInteger: Int
  valueMarkdown: Markdown
  valueOid: OID
  valuePositiveInt: Int
  valueString: String
  valueTime: Time
  valueUnsignedInt: Int
  valueUri: URI
  valueUrl: URL
  valueUuid: UUID
  valueAddress: Address
  valueAge: Quantity
  valueAnnotation: Annotation
  valueAttachment: Attachment
  valueCodeableConcept: CodeableConcept
  valueCodeableReference: CodeableReference
  valueCoding: Coding
  valueContactPoint: ContactPoint
  valueCount: Quantity
  valueDistance: Quantity
  valueDuration: Quantity
  valueHumanName: HumanName
  valueIdentifier: Identifier
  valueMoney: Money
  valuePeriod: Period
  valueQuantity: Quantity
  valueRange: Range
  valueRatio: Ratio
  valueRatioRange: RatioRange
  valueReference: ExtensionValueReferenceReference
  valueSampledData: SampledData
  valueSignature: Signature
  valueTiming: Timing
  valueContactDetail: ContactDetail
  valueContributor: Contributor
  valueDataRequirement: DataRequirement
  valueExpression: Expression
  valueParameterDefinition: ParameterDefinition
  valueRelatedArtifact: RelatedArtifact
  valueTriggerDefinition: TriggerDefinition
  valueUsageContext: UsageContext
  valueDosage: Dosage
}

input SearchDateValue {
  """
  the value for the parameter in the resource is equal to the provided value
  """
  equals: Date

  """
  the value for the parameter in the resource is not equal to the provided value
  """
  notEquals: Date

  """
  the value for the parameter in the resource is greater than the provided value
  """
  greaterThan: Date

  """
  the value for the parameter in the resource is greater or equal to the provided value
  """
  greaterThanOrEqualTo: Date

  """
  the value for the parameter in the resource is less than the provided value
  """
  lessThan: Date

  """
  the value for the parameter in the resource is less or equal to the provided value
  """
  lessThanOrEqualTo: Date

  """
  the value for the parameter in the resource starts after the provided value
  """
  startsAfter: Date

  """
  the value for the parameter in the resource ends before the provided value
  """
  endsBefore: Date

  """
  the value for the parameter in the resource is approximately the same to the provided value.
  Note that the recommended value for the approximation is 10% of the stated value (or for a date, 10% of the gap between now and the date), but systems may choose other values where appropriate
  """
  approximately: Date
}

input SearchDate {
  searchType: String = "date"
  value: SearchDateValue
  values: [SearchDateValue]
  missing: Boolean
}

input SearchExtensionValue {
  url: String
  valueString: String
  notEquals: NotSearchExtensionValue
}

input NotSearchExtensionValue {
  url: String
  valueString: String
  values: [SearchExtensionValue]
}

input SearchExtension {
  searchType: String = "token"
  value: SearchExtensionValue
  values: [SearchExtensionValue]
  missing: Boolean
  notEquals: NotSearchExtensionValue
}

input SearchNumberValue {
  """
  the value for the parameter in the resource is equal to the provided value
  """
  equals: Decimal

  """
  the value for the parameter in the resource is not equal to the provided value
  """
  notEquals: Decimal

  """
  the value for the parameter in the resource is greater than the provided value
  """
  greaterThan: Decimal

  """
  the value for the parameter in the resource is greater or equal to the provided value
  """
  greaterThanOrEqualTo: Decimal

  """
  the value for the parameter in the resource is less than the provided value
  """
  lessThan: Decimal

  """
  the value for the parameter in the resource is less or equal to the provided value
  """
  lessThanOrEqualTo: Decimal

  """
  the value for the parameter in the resource starts after the provided value
  """
  startsAfter: Decimal

  """
  the value for the parameter in the resource ends before the provided value
  """
  endsBefore: Decimal

  """
  the value for the parameter in the resource is approximately the same to the provided value.
  Note that the recommended value for the approximation is 10% of the stated value (or for a date, 10% of the gap between now and the date), but systems may choose other values where appropriate
  """
  approximately: Decimal
}

input SearchNumber {
  searchType: String = "number"
  value: SearchNumberValue
  values: [SearchNumberValue]
  missing: Boolean
}

input SearchQuantityValue {
  prefix: String
  value: Decimal
  system: String
  code: String
}

input SearchQuantity {
  searchType: String = "quantity"
  prefix: String
  value: Decimal
  system: String
  code: String
  missing: Boolean
  notEquals: SearchQuantityValue
}

input SearchReferenceValue {
  value: String
  target: String
}

input SearchReference {
  searchType: String = "reference"
  value: String
  target: String
  missing: Boolean
  notEquals: SearchReferenceValue
}

input SearchStringValue {
  value: String
  values: [String]
}

input SearchString {
  searchType: String = "string"
  value: String
  values: [String]
  missing: Boolean
  above: Boolean
  below: Boolean
  notEquals: SearchStringValue
  contains: String
  exact: String
}

input SearchTokenValue {
  code: String
  value: String
  system: String
  notEquals: NotSearchTokenValue
}

input NotSearchTokenValue {
  code: String
  value: String
  system: String
  values: [SearchTokenValue]
}

input SearchToken {
  searchType: String = "token"
  value: SearchTokenValue
  values: [SearchTokenValue]
  missing: Boolean
  notEquals: NotSearchTokenValue
  text: String
  ofType: SearchTokenValue
}

interface DomainResource implements Resource {
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
}

interface Resource {
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
}

union AccountSubject = Patient | Device | Practitioner | PractitionerRole | Location | HealthcareService | Organization

type AccountSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AccountSubject
  type: URI
  identifier: Identifier
  display: String
}

type AccountOwnerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type AccountPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Account
  type: URI
  identifier: Identifier
  display: String
}

type Account implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  type: CodeableConcept
  name: String
  subject: [AccountSubjectReference]
  servicePeriod: Period
  coverage: [AccountCoverage]
  owner: AccountOwnerReference
  description: String
  guarantor: [AccountGuarantor]
  partOf: AccountPartOfReference
}

type AccountBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Account
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type AccountBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [AccountBundleEntry]
}

type ActivityDefinitionSubjectReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type ActivityDefinitionLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

union ActivityDefinitionProductReference = Medication | Substance | Ingredient

type ActivityDefinitionProductReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ActivityDefinitionProductReference
  type: URI
  identifier: Identifier
  display: String
}

type ActivityDefinitionSpecimenRequirementReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SpecimenDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ActivityDefinitionObservationRequirementReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ActivityDefinitionObservationResultRequirementReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ActivityDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  subtitle: String
  status: Code
  experimental: Boolean
  subjectCodeableConcept: CodeableConcept
  subjectReference: ActivityDefinitionSubjectReferenceReference
  subjectCanonical: Canonical
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  usage: String
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  topic: [CodeableConcept]
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  relatedArtifact: [RelatedArtifact]
  library: [Canonical]
  kind: Code
  profile: Canonical
  code: CodeableConcept
  intent: Code
  priority: Code
  doNotPerform: Boolean
  timingTiming: Timing
  timingDateTime: DateTime
  timingAge: Quantity
  timingPeriod: Period
  timingRange: Range
  timingDuration: Quantity
  location: ActivityDefinitionLocationReference
  participant: [ActivityDefinitionParticipant]
  productReference: ActivityDefinitionProductReferenceReference
  productCodeableConcept: CodeableConcept
  quantity: Quantity
  dosage: [Dosage]
  bodySite: [CodeableConcept]
  specimenRequirement: [ActivityDefinitionSpecimenRequirementReference]
  observationRequirement: [ActivityDefinitionObservationRequirementReference]
  observationResultRequirement: [ActivityDefinitionObservationResultRequirementReference]
  transform: Canonical
  dynamicValue: [ActivityDefinitionDynamicValue]
}

type ActivityDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ActivityDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ActivityDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ActivityDefinitionBundleEntry]
}

type AdministrableProductDefinitionFormOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicinalProductDefinition
  type: URI
  identifier: Identifier
  display: String
}

type AdministrableProductDefinitionProducedFromReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ManufacturedItemDefinition
  type: URI
  identifier: Identifier
  display: String
}

type AdministrableProductDefinitionDeviceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceDefinition
  type: URI
  identifier: Identifier
  display: String
}

type AdministrableProductDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  formOf: [AdministrableProductDefinitionFormOfReference]
  administrableDoseForm: CodeableConcept
  unitOfPresentation: CodeableConcept
  producedFrom: [AdministrableProductDefinitionProducedFromReference]
  ingredient: [CodeableConcept]
  device: AdministrableProductDefinitionDeviceReference
  property: [AdministrableProductDefinitionProperty]
  routeOfAdministration: [AdministrableProductDefinitionRouteOfAdministration]
}

type AdministrableProductDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: AdministrableProductDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type AdministrableProductDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [AdministrableProductDefinitionBundleEntry]
}

union AdverseEventSubject = Patient | Group | Practitioner | RelatedPerson

type AdverseEventSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AdverseEventSubject
  type: URI
  identifier: Identifier
  display: String
}

type AdverseEventEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

type AdverseEventResultingConditionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Condition
  type: URI
  identifier: Identifier
  display: String
}

type AdverseEventLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

union AdverseEventRecorder = Patient | Practitioner | PractitionerRole | RelatedPerson

type AdverseEventRecorderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AdverseEventRecorder
  type: URI
  identifier: Identifier
  display: String
}

union AdverseEventContributor = Practitioner | PractitionerRole | Device

type AdverseEventContributorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AdverseEventContributor
  type: URI
  identifier: Identifier
  display: String
}

union AdverseEventSubjectMedicalHistory = Condition | Observation | AllergyIntolerance | FamilyMemberHistory | Immunization | Procedure | Media | DocumentReference

type AdverseEventSubjectMedicalHistoryReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AdverseEventSubjectMedicalHistory
  type: URI
  identifier: Identifier
  display: String
}

type AdverseEventReferenceDocumentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReference
  type: URI
  identifier: Identifier
  display: String
}

type AdverseEventStudyReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ResearchStudy
  type: URI
  identifier: Identifier
  display: String
}

type AdverseEvent implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  actuality: Code
  category: [CodeableConcept]
  event: CodeableConcept
  subject: AdverseEventSubjectReference
  encounter: AdverseEventEncounterReference
  date: DateTime
  detected: DateTime
  recordedDate: DateTime
  resultingCondition: [AdverseEventResultingConditionReference]
  location: AdverseEventLocationReference
  seriousness: CodeableConcept
  severity: CodeableConcept
  outcome: CodeableConcept
  recorder: AdverseEventRecorderReference
  contributor: [AdverseEventContributorReference]
  suspectEntity: [AdverseEventSuspectEntity]
  subjectMedicalHistory: [AdverseEventSubjectMedicalHistoryReference]
  referenceDocument: [AdverseEventReferenceDocumentReference]
  study: [AdverseEventStudyReference]
}

type AdverseEventBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: AdverseEvent
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type AdverseEventBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [AdverseEventBundleEntry]
}

type AllergyIntolerancePatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type AllergyIntoleranceEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union AllergyIntoleranceRecorder = Practitioner | PractitionerRole | Patient | RelatedPerson

type AllergyIntoleranceRecorderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AllergyIntoleranceRecorder
  type: URI
  identifier: Identifier
  display: String
}

union AllergyIntoleranceAsserter = Patient | RelatedPerson | Practitioner | PractitionerRole

type AllergyIntoleranceAsserterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AllergyIntoleranceAsserter
  type: URI
  identifier: Identifier
  display: String
}

type AllergyIntolerance implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  clinicalStatus: CodeableConcept
  verificationStatus: CodeableConcept
  type: Code
  category: [Code]
  criticality: Code
  code: CodeableConcept
  patient: AllergyIntolerancePatientReference
  encounter: AllergyIntoleranceEncounterReference
  onsetDateTime: DateTime
  onsetAge: Quantity
  onsetPeriod: Period
  onsetRange: Range
  onsetString: String
  recordedDate: DateTime
  recorder: AllergyIntoleranceRecorderReference
  asserter: AllergyIntoleranceAsserterReference
  lastOccurrence: DateTime
  note: [Annotation]
  reaction: [AllergyIntoleranceReaction]
}

type AllergyIntoleranceBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: AllergyIntolerance
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type AllergyIntoleranceBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [AllergyIntoleranceBundleEntry]
}

union AppointmentReasonReference = Condition | Procedure | Observation | ImmunizationRecommendation

type AppointmentReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AppointmentReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type AppointmentSupportingInformationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type AppointmentSlotReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Slot
  type: URI
  identifier: Identifier
  display: String
}

type AppointmentBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequest
  type: URI
  identifier: Identifier
  display: String
}

type Appointment implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  cancelationReason: CodeableConcept
  serviceCategory: [CodeableConcept]
  serviceType: [CodeableConcept]
  specialty: [CodeableConcept]
  appointmentType: CodeableConcept
  reasonCode: [CodeableConcept]
  reasonReference: [AppointmentReasonReferenceReference]
  priority: Int
  description: String
  supportingInformation: [AppointmentSupportingInformationReference]
  start: Instant
  end: Instant
  minutesDuration: Int
  slot: [AppointmentSlotReference]
  created: DateTime
  comment: String
  patientInstruction: String
  basedOn: [AppointmentBasedOnReference]
  participant: [AppointmentParticipant]
  requestedPeriod: [Period]
}

type AppointmentBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Appointment
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type AppointmentBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [AppointmentBundleEntry]
}

type AppointmentResponseAppointmentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Appointment
  type: URI
  identifier: Identifier
  display: String
}

union AppointmentResponseActor = Patient | Practitioner | PractitionerRole | RelatedPerson | Device | HealthcareService | Location

type AppointmentResponseActorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AppointmentResponseActor
  type: URI
  identifier: Identifier
  display: String
}

type AppointmentResponse implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  appointment: AppointmentResponseAppointmentReference
  start: Instant
  end: Instant
  participantType: [CodeableConcept]
  actor: AppointmentResponseActorReference
  participantStatus: Code
  comment: String
}

type AppointmentResponseBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: AppointmentResponse
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type AppointmentResponseBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [AppointmentResponseBundleEntry]
}

type AuditEvent implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  type: Coding
  subtype: [Coding]
  action: Code
  period: Period
  recorded: Instant
  outcome: Code
  outcomeDesc: String
  purposeOfEvent: [CodeableConcept]
  agent: [AuditEventAgent]
  source: AuditEventSource
  entity: [AuditEventEntity]
}

type AuditEventBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: AuditEvent
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type AuditEventBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [AuditEventBundleEntry]
}

type BasicSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union BasicAuthor = Practitioner | PractitionerRole | Patient | RelatedPerson | Organization

type BasicAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: BasicAuthor
  type: URI
  identifier: Identifier
  display: String
}

type Basic implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  code: CodeableConcept
  subject: BasicSubjectReference
  created: Date
  author: BasicAuthorReference
}

type BasicBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Basic
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type BasicBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [BasicBundleEntry]
}

type BinarySecurityContextReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type Binary implements Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  contentType: Code
  securityContext: BinarySecurityContextReference
  data: Base64Binary
}

type BinaryBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Binary
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type BinaryBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [BinaryBundleEntry]
}

type BiologicallyDerivedProductRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequest
  type: URI
  identifier: Identifier
  display: String
}

type BiologicallyDerivedProductParentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: BiologicallyDerivedProduct
  type: URI
  identifier: Identifier
  display: String
}

type BiologicallyDerivedProduct implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  productCategory: Code
  productCode: CodeableConcept
  status: Code
  request: [BiologicallyDerivedProductRequestReference]
  quantity: Int
  parent: [BiologicallyDerivedProductParentReference]
  collection: BiologicallyDerivedProductCollection
  processing: [BiologicallyDerivedProductProcessing]
  manipulation: BiologicallyDerivedProductManipulation
  storage: [BiologicallyDerivedProductStorage]
}

type BiologicallyDerivedProductBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: BiologicallyDerivedProduct
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type BiologicallyDerivedProductBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [BiologicallyDerivedProductBundleEntry]
}

type BodyStructurePatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type BodyStructure implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  active: Boolean
  morphology: CodeableConcept
  location: CodeableConcept
  locationQualifier: [CodeableConcept]
  description: String
  image: [Attachment]
  patient: BodyStructurePatientReference
}

type BodyStructureBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: BodyStructure
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type BodyStructureBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [BodyStructureBundleEntry]
}

type Bundle implements Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  identifier: Identifier
  type: Code
  timestamp: Instant
  total: Int
  link: [BundleLink]
  entry: [BundleEntry]
  signature: Signature
}

type BundleBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Bundle
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type BundleBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [BundleBundleEntry]
}

type CapabilityStatement implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  version: String
  name: String
  title: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  kind: Code
  instantiates: [Canonical]
  imports: [Canonical]
  software: CapabilityStatementSoftware
  implementation: CapabilityStatementImplementation
  fhirVersion: Code
  format: [Code]
  patchFormat: [Code]
  implementationGuide: [Canonical]
  rest: [CapabilityStatementRest]
  messaging: [CapabilityStatementMessaging]
  document: [CapabilityStatementDocument]
}

type CapabilityStatementBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: CapabilityStatement
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CapabilityStatementBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CapabilityStatementBundleEntry]
}

type CarePlanBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CarePlan
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanReplacesReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CarePlan
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CarePlan
  type: URI
  identifier: Identifier
  display: String
}

union CarePlanSubject = Patient | Group

type CarePlanSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CarePlanSubject
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union CarePlanAuthor = Patient | Practitioner | PractitionerRole | Device | RelatedPerson | Organization | CareTeam

type CarePlanAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CarePlanAuthor
  type: URI
  identifier: Identifier
  display: String
}

union CarePlanContributor = Patient | Practitioner | PractitionerRole | Device | RelatedPerson | Organization | CareTeam

type CarePlanContributorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CarePlanContributor
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanCareTeamReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CareTeam
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanAddressesReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Condition
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanSupportingInfoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CarePlanGoalReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Goal
  type: URI
  identifier: Identifier
  display: String
}

type CarePlan implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  instantiatesCanonical: [Canonical]
  instantiatesUri: [URI]
  basedOn: [CarePlanBasedOnReference]
  replaces: [CarePlanReplacesReference]
  partOf: [CarePlanPartOfReference]
  status: Code
  intent: Code
  category: [CodeableConcept]
  title: String
  description: String
  subject: CarePlanSubjectReference
  encounter: CarePlanEncounterReference
  period: Period
  created: DateTime
  author: CarePlanAuthorReference
  contributor: [CarePlanContributorReference]
  careTeam: [CarePlanCareTeamReference]
  addresses: [CarePlanAddressesReference]
  supportingInfo: [CarePlanSupportingInfoReference]
  goal: [CarePlanGoalReference]
  activity: [CarePlanActivity]
  note: [Annotation]
}

type CarePlanBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: CarePlan
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CarePlanBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CarePlanBundleEntry]
}

union CareTeamSubject = Patient | Group

type CareTeamSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CareTeamSubject
  type: URI
  identifier: Identifier
  display: String
}

type CareTeamEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

type CareTeamReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Condition
  type: URI
  identifier: Identifier
  display: String
}

type CareTeamManagingOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type CareTeam implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  category: [CodeableConcept]
  name: String
  subject: CareTeamSubjectReference
  encounter: CareTeamEncounterReference
  period: Period
  participant: [CareTeamParticipant]
  reasonCode: [CodeableConcept]
  reasonReference: [CareTeamReasonReferenceReference]
  managingOrganization: [CareTeamManagingOrganizationReference]
  telecom: [ContactPoint]
  note: [Annotation]
}

type CareTeamBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: CareTeam
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CareTeamBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CareTeamBundleEntry]
}

union CatalogEntryReferencedItem = Medication | Device | Organization | Practitioner | PractitionerRole | HealthcareService | ActivityDefinition | PlanDefinition | SpecimenDefinition | ObservationDefinition | Binary

type CatalogEntryReferencedItemReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CatalogEntryReferencedItem
  type: URI
  identifier: Identifier
  display: String
}

type CatalogEntry implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  type: CodeableConcept
  orderable: Boolean
  referencedItem: CatalogEntryReferencedItemReference
  additionalIdentifier: [Identifier]
  classification: [CodeableConcept]
  status: Code
  validityPeriod: Period
  validTo: DateTime
  lastUpdated: DateTime
  additionalCharacteristic: [CodeableConcept]
  additionalClassification: [CodeableConcept]
  relatedEntry: [CatalogEntryRelatedEntry]
}

type CatalogEntryBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: CatalogEntry
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CatalogEntryBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CatalogEntryBundleEntry]
}

type ChargeItemPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ChargeItem
  type: URI
  identifier: Identifier
  display: String
}

union ChargeItemSubject = Patient | Group

type ChargeItemSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ChargeItemSubject
  type: URI
  identifier: Identifier
  display: String
}

union ChargeItemContext = Encounter | EpisodeOfCare

type ChargeItemContextReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ChargeItemContext
  type: URI
  identifier: Identifier
  display: String
}

type ChargeItemPerformingOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type ChargeItemRequestingOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type ChargeItemCostCenterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

union ChargeItemEnterer = Practitioner | PractitionerRole | Organization | Patient | Device | RelatedPerson

type ChargeItemEntererReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ChargeItemEnterer
  type: URI
  identifier: Identifier
  display: String
}

union ChargeItemService = DiagnosticReport | ImagingStudy | Immunization | MedicationAdministration | MedicationDispense | Observation | Procedure | SupplyDelivery

type ChargeItemServiceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ChargeItemService
  type: URI
  identifier: Identifier
  display: String
}

union ChargeItemProductReference = Device | Medication | Substance

type ChargeItemProductReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ChargeItemProductReference
  type: URI
  identifier: Identifier
  display: String
}

type ChargeItemAccountReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Account
  type: URI
  identifier: Identifier
  display: String
}

type ChargeItemSupportingInformationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ChargeItem implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  definitionUri: [URI]
  definitionCanonical: [Canonical]
  status: Code
  partOf: [ChargeItemPartOfReference]
  code: CodeableConcept
  subject: ChargeItemSubjectReference
  context: ChargeItemContextReference
  occurrenceDateTime: DateTime
  occurrencePeriod: Period
  occurrenceTiming: Timing
  performer: [ChargeItemPerformer]
  performingOrganization: ChargeItemPerformingOrganizationReference
  requestingOrganization: ChargeItemRequestingOrganizationReference
  costCenter: ChargeItemCostCenterReference
  quantity: Quantity
  bodysite: [CodeableConcept]
  factorOverride: Float
  priceOverride: Money
  overrideReason: String
  enterer: ChargeItemEntererReference
  enteredDate: DateTime
  reason: [CodeableConcept]
  service: [ChargeItemServiceReference]
  productReference: ChargeItemProductReferenceReference
  productCodeableConcept: CodeableConcept
  account: [ChargeItemAccountReference]
  note: [Annotation]
  supportingInformation: [ChargeItemSupportingInformationReference]
}

type ChargeItemBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ChargeItem
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ChargeItemBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ChargeItemBundleEntry]
}

union ChargeItemDefinitionInstance = Medication | Substance | Device

type ChargeItemDefinitionInstanceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ChargeItemDefinitionInstance
  type: URI
  identifier: Identifier
  display: String
}

type ChargeItemDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  title: String
  derivedFromUri: [URI]
  partOf: [Canonical]
  replaces: [Canonical]
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  code: CodeableConcept
  instance: [ChargeItemDefinitionInstanceReference]
  applicability: [ChargeItemDefinitionApplicability]
  propertyGroup: [ChargeItemDefinitionPropertyGroup]
}

type ChargeItemDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ChargeItemDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ChargeItemDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ChargeItemDefinitionBundleEntry]
}

type Citation implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  summary: [CitationSummary]
  classification: [CitationClassification]
  note: [Annotation]
  currentState: [CodeableConcept]
  statusDate: [CitationStatusDate]
  relatesTo: [CitationRelatesTo]
  citedArtifact: CitationCitedArtifact
}

type CitationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Citation
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CitationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CitationBundleEntry]
}

type ClaimPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

union ClaimEnterer = Practitioner | PractitionerRole

type ClaimEntererReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimEnterer
  type: URI
  identifier: Identifier
  display: String
}

type ClaimInsurerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

union ClaimProvider = Practitioner | PractitionerRole | Organization

type ClaimProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimProvider
  type: URI
  identifier: Identifier
  display: String
}

union ClaimPrescription = DeviceRequest | MedicationRequest | VisionPrescription

type ClaimPrescriptionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimPrescription
  type: URI
  identifier: Identifier
  display: String
}

union ClaimOriginalPrescription = DeviceRequest | MedicationRequest | VisionPrescription

type ClaimOriginalPrescriptionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimOriginalPrescription
  type: URI
  identifier: Identifier
  display: String
}

type ClaimReferralReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequest
  type: URI
  identifier: Identifier
  display: String
}

type ClaimFacilityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type Claim implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  type: CodeableConcept
  subType: CodeableConcept
  use: Code
  patient: ClaimPatientReference
  billablePeriod: Period
  created: DateTime
  enterer: ClaimEntererReference
  insurer: ClaimInsurerReference
  provider: ClaimProviderReference
  priority: CodeableConcept
  fundsReserve: CodeableConcept
  related: [ClaimRelated]
  prescription: ClaimPrescriptionReference
  originalPrescription: ClaimOriginalPrescriptionReference
  payee: ClaimPayee
  referral: ClaimReferralReference
  facility: ClaimFacilityReference
  careTeam: [ClaimCareTeam]
  supportingInfo: [ClaimSupportingInfo]
  diagnosis: [ClaimDiagnosis]
  procedure: [ClaimProcedure]
  insurance: [ClaimInsurance]
  accident: ClaimAccident
  item: [ClaimItem]
  total: Money
}

type ClaimBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Claim
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ClaimBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ClaimBundleEntry]
}

type ClaimResponsePatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type ClaimResponseInsurerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

union ClaimResponseRequestor = Practitioner | PractitionerRole | Organization

type ClaimResponseRequestorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimResponseRequestor
  type: URI
  identifier: Identifier
  display: String
}

type ClaimResponseRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Claim
  type: URI
  identifier: Identifier
  display: String
}

type ClaimResponseCommunicationRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationRequest
  type: URI
  identifier: Identifier
  display: String
}

type ClaimResponse implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  type: CodeableConcept
  subType: CodeableConcept
  use: Code
  patient: ClaimResponsePatientReference
  created: DateTime
  insurer: ClaimResponseInsurerReference
  requestor: ClaimResponseRequestorReference
  request: ClaimResponseRequestReference
  outcome: Code
  disposition: String
  preAuthRef: String
  preAuthPeriod: Period
  payeeType: CodeableConcept
  item: [ClaimResponseItem]
  addItem: [ClaimResponseAddItem]
  adjudication: [ClaimResponseAdjudication]
  total: [ClaimResponseTotal]
  payment: ClaimResponsePayment
  fundsReserve: CodeableConcept
  formCode: CodeableConcept
  form: Attachment
  processNote: [ClaimResponseProcessNote]
  communicationRequest: [ClaimResponseCommunicationRequestReference]
  insurance: [ClaimResponseInsurance]
  error: [ClaimResponseError]
}

type ClaimResponseBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ClaimResponse
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ClaimResponseBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ClaimResponseBundleEntry]
}

union ClinicalImpressionSubject = Patient | Group

type ClinicalImpressionSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalImpressionSubject
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalImpressionEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union ClinicalImpressionAssessor = Practitioner | PractitionerRole

type ClinicalImpressionAssessorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalImpressionAssessor
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalImpressionPreviousReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalImpression
  type: URI
  identifier: Identifier
  display: String
}

union ClinicalImpressionProblem = Condition | AllergyIntolerance

type ClinicalImpressionProblemReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalImpressionProblem
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalImpressionPrognosisReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: RiskAssessment
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalImpressionSupportingInfoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalImpression implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  statusReason: CodeableConcept
  code: CodeableConcept
  description: String
  subject: ClinicalImpressionSubjectReference
  encounter: ClinicalImpressionEncounterReference
  effectiveDateTime: DateTime
  effectivePeriod: Period
  date: DateTime
  assessor: ClinicalImpressionAssessorReference
  previous: ClinicalImpressionPreviousReference
  problem: [ClinicalImpressionProblemReference]
  investigation: [ClinicalImpressionInvestigation]
  protocol: [URI]
  summary: String
  finding: [ClinicalImpressionFinding]
  prognosisCodeableConcept: [CodeableConcept]
  prognosisReference: [ClinicalImpressionPrognosisReferenceReference]
  supportingInfo: [ClinicalImpressionSupportingInfoReference]
  note: [Annotation]
}

type ClinicalImpressionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ClinicalImpression
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ClinicalImpressionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ClinicalImpressionBundleEntry]
}

union ClinicalUseDefinitionSubject = MedicinalProductDefinition | Medication | ActivityDefinition | PlanDefinition | Device | DeviceDefinition | Substance

type ClinicalUseDefinitionSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalUseDefinitionSubject
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinitionPopulationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type ClinicalUseDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  type: Code
  category: [CodeableConcept]
  subject: [ClinicalUseDefinitionSubjectReference]
  status: CodeableConcept
  contraindication: ClinicalUseDefinitionContraindication
  indication: ClinicalUseDefinitionIndication
  interaction: ClinicalUseDefinitionInteraction
  population: [ClinicalUseDefinitionPopulationReference]
  undesirableEffect: ClinicalUseDefinitionUndesirableEffect
  warning: ClinicalUseDefinitionWarning
}

type ClinicalUseDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ClinicalUseDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ClinicalUseDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ClinicalUseDefinitionBundleEntry]
}

type CodeSystem implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  caseSensitive: Boolean
  valueSet: Canonical
  hierarchyMeaning: Code
  compositional: Boolean
  versionNeeded: Boolean
  content: Code
  supplements: Canonical
  count: Int
  filter: [CodeSystemFilter]
  property: [CodeSystemProperty]
  concept: [CodeSystemConcept]
}

type CodeSystemBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: CodeSystem
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CodeSystemBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CodeSystemBundleEntry]
}

type CommunicationBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CommunicationPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CommunicationInResponseToReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Communication
  type: URI
  identifier: Identifier
  display: String
}

union CommunicationSubject = Patient | Group

type CommunicationSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationSubject
  type: URI
  identifier: Identifier
  display: String
}

type CommunicationAboutReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CommunicationEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union CommunicationRecipient = Device | Organization | Patient | Practitioner | PractitionerRole | RelatedPerson | Group | CareTeam | HealthcareService

type CommunicationRecipientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationRecipient
  type: URI
  identifier: Identifier
  display: String
}

union CommunicationSender = Device | Organization | Patient | Practitioner | PractitionerRole | RelatedPerson | HealthcareService

type CommunicationSenderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationSender
  type: URI
  identifier: Identifier
  display: String
}

union CommunicationReasonReference = Condition | Observation | DiagnosticReport | DocumentReference

type CommunicationReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type Communication implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  instantiatesCanonical: [Canonical]
  instantiatesUri: [URI]
  basedOn: [CommunicationBasedOnReference]
  partOf: [CommunicationPartOfReference]
  inResponseTo: [CommunicationInResponseToReference]
  status: Code
  statusReason: CodeableConcept
  category: [CodeableConcept]
  priority: Code
  medium: [CodeableConcept]
  subject: CommunicationSubjectReference
  topic: CodeableConcept
  about: [CommunicationAboutReference]
  encounter: CommunicationEncounterReference
  sent: DateTime
  received: DateTime
  recipient: [CommunicationRecipientReference]
  sender: CommunicationSenderReference
  reasonCode: [CodeableConcept]
  reasonReference: [CommunicationReasonReferenceReference]
  payload: [CommunicationPayload]
  note: [Annotation]
}

type CommunicationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Communication
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CommunicationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CommunicationBundleEntry]
}

type CommunicationRequestBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CommunicationRequestReplacesReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationRequest
  type: URI
  identifier: Identifier
  display: String
}

union CommunicationRequestSubject = Patient | Group

type CommunicationRequestSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationRequestSubject
  type: URI
  identifier: Identifier
  display: String
}

type CommunicationRequestAboutReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CommunicationRequestEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union CommunicationRequestRequester = Practitioner | PractitionerRole | Organization | Patient | RelatedPerson | Device

type CommunicationRequestRequesterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationRequestRequester
  type: URI
  identifier: Identifier
  display: String
}

union CommunicationRequestRecipient = Device | Organization | Patient | Practitioner | PractitionerRole | RelatedPerson | Group | CareTeam | HealthcareService

type CommunicationRequestRecipientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationRequestRecipient
  type: URI
  identifier: Identifier
  display: String
}

union CommunicationRequestSender = Device | Organization | Patient | Practitioner | PractitionerRole | RelatedPerson | HealthcareService

type CommunicationRequestSenderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationRequestSender
  type: URI
  identifier: Identifier
  display: String
}

union CommunicationRequestReasonReference = Condition | Observation | DiagnosticReport | DocumentReference

type CommunicationRequestReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CommunicationRequestReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type CommunicationRequest implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  basedOn: [CommunicationRequestBasedOnReference]
  replaces: [CommunicationRequestReplacesReference]
  groupIdentifier: Identifier
  status: Code
  statusReason: CodeableConcept
  category: [CodeableConcept]
  priority: Code
  doNotPerform: Boolean
  medium: [CodeableConcept]
  subject: CommunicationRequestSubjectReference
  about: [CommunicationRequestAboutReference]
  encounter: CommunicationRequestEncounterReference
  payload: [CommunicationRequestPayload]
  occurrenceDateTime: DateTime
  occurrencePeriod: Period
  authoredOn: DateTime
  requester: CommunicationRequestRequesterReference
  recipient: [CommunicationRequestRecipientReference]
  sender: CommunicationRequestSenderReference
  reasonCode: [CodeableConcept]
  reasonReference: [CommunicationRequestReasonReferenceReference]
  note: [Annotation]
}

type CommunicationRequestBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: CommunicationRequest
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CommunicationRequestBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CommunicationRequestBundleEntry]
}

type CompartmentDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  version: String
  name: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  purpose: Markdown
  code: Code
  search: Boolean
  resource: [CompartmentDefinitionResource]
}

type CompartmentDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: CompartmentDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CompartmentDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CompartmentDefinitionBundleEntry]
}

type CompositionSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type CompositionEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union CompositionAuthor = Practitioner | PractitionerRole | Device | Patient | RelatedPerson | Organization

type CompositionAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CompositionAuthor
  type: URI
  identifier: Identifier
  display: String
}

type CompositionCustodianReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type Composition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  status: Code
  type: CodeableConcept
  category: [CodeableConcept]
  subject: CompositionSubjectReference
  encounter: CompositionEncounterReference
  date: DateTime
  author: [CompositionAuthorReference]
  title: String
  confidentiality: Code
  attester: [CompositionAttester]
  custodian: CompositionCustodianReference
  relatesTo: [CompositionRelatesTo]
  event: [CompositionEvent]
  section: [CompositionSection]
}

type CompositionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Composition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CompositionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CompositionBundleEntry]
}

type ConceptMap implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: Identifier
  version: String
  name: String
  title: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  sourceUri: URI
  sourceCanonical: Canonical
  targetUri: URI
  targetCanonical: Canonical
  group: [ConceptMapGroup]
}

type ConceptMapBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ConceptMap
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ConceptMapBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ConceptMapBundleEntry]
}

union ConditionSubject = Patient | Group

type ConditionSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ConditionSubject
  type: URI
  identifier: Identifier
  display: String
}

type ConditionEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union ConditionRecorder = Practitioner | PractitionerRole | Patient | RelatedPerson

type ConditionRecorderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ConditionRecorder
  type: URI
  identifier: Identifier
  display: String
}

union ConditionAsserter = Practitioner | PractitionerRole | Patient | RelatedPerson

type ConditionAsserterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ConditionAsserter
  type: URI
  identifier: Identifier
  display: String
}

type Condition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  clinicalStatus: CodeableConcept
  verificationStatus: CodeableConcept
  category: [CodeableConcept]
  severity: CodeableConcept
  code: CodeableConcept
  bodySite: [CodeableConcept]
  subject: ConditionSubjectReference
  encounter: ConditionEncounterReference
  onsetDateTime: DateTime
  onsetAge: Quantity
  onsetPeriod: Period
  onsetRange: Range
  onsetString: String
  abatementDateTime: DateTime
  abatementAge: Quantity
  abatementPeriod: Period
  abatementRange: Range
  abatementString: String
  recordedDate: DateTime
  recorder: ConditionRecorderReference
  asserter: ConditionAsserterReference
  stage: [ConditionStage]
  evidence: [ConditionEvidence]
  note: [Annotation]
}

type ConditionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Condition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ConditionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ConditionBundleEntry]
}

type ConsentPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

union ConsentPerformer = Organization | Patient | Practitioner | RelatedPerson | PractitionerRole

type ConsentPerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ConsentPerformer
  type: URI
  identifier: Identifier
  display: String
}

type ConsentOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

union ConsentSourceReference = Consent | DocumentReference | Contract | QuestionnaireResponse

type ConsentSourceReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ConsentSourceReference
  type: URI
  identifier: Identifier
  display: String
}

type Consent implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  scope: CodeableConcept
  category: [CodeableConcept]
  patient: ConsentPatientReference
  dateTime: DateTime
  performer: [ConsentPerformerReference]
  organization: [ConsentOrganizationReference]
  sourceAttachment: Attachment
  sourceReference: ConsentSourceReferenceReference
  policy: [ConsentPolicy]
  policyRule: CodeableConcept
  verification: [ConsentVerification]
  provision: ConsentProvision
}

type ConsentBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Consent
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ConsentBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ConsentBundleEntry]
}

type ContractInstantiatesCanonicalReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Contract
  type: URI
  identifier: Identifier
  display: String
}

type ContractSubjectTypeReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ContractAuthorityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type ContractDomainReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type ContractSiteReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

union ContractAuthor = Patient | Practitioner | PractitionerRole | Organization

type ContractAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractAuthor
  type: URI
  identifier: Identifier
  display: String
}

type ContractTopicReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ContractSupportingInfoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ContractRelevantHistoryReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Provenance
  type: URI
  identifier: Identifier
  display: String
}

union ContractLegallyBindingReference = Composition | DocumentReference | QuestionnaireResponse | Contract

type ContractLegallyBindingReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ContractLegallyBindingReference
  type: URI
  identifier: Identifier
  display: String
}

type Contract implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  url: URI
  version: String
  status: Code
  legalState: CodeableConcept
  instantiatesCanonical: ContractInstantiatesCanonicalReference
  instantiatesUri: URI
  contentDerivative: CodeableConcept
  issued: DateTime
  applies: Period
  expirationType: CodeableConcept
  subject: [ContractSubjectTypeReference]
  authority: [ContractAuthorityReference]
  domain: [ContractDomainReference]
  site: [ContractSiteReference]
  name: String
  title: String
  subtitle: String
  alias: [String]
  author: ContractAuthorReference
  scope: CodeableConcept
  topicCodeableConcept: CodeableConcept
  topicReference: ContractTopicReferenceReference
  type: CodeableConcept
  subType: [CodeableConcept]
  contentDefinition: ContractContentDefinition
  term: [ContractTerm]
  supportingInfo: [ContractSupportingInfoReference]
  relevantHistory: [ContractRelevantHistoryReference]
  signer: [ContractSigner]
  friendly: [ContractFriendly]
  legal: [ContractLegal]
  rule: [ContractRule]
  legallyBindingAttachment: Attachment
  legallyBindingReference: ContractLegallyBindingReferenceReference
}

type ContractBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Contract
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ContractBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ContractBundleEntry]
}

union CoveragePolicyHolder = Patient | RelatedPerson | Organization

type CoveragePolicyHolderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CoveragePolicyHolder
  type: URI
  identifier: Identifier
  display: String
}

union CoverageSubscriber = Patient | RelatedPerson

type CoverageSubscriberReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CoverageSubscriber
  type: URI
  identifier: Identifier
  display: String
}

type CoverageBeneficiaryReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

union CoveragePayor = Organization | Patient | RelatedPerson

type CoveragePayorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CoveragePayor
  type: URI
  identifier: Identifier
  display: String
}

type CoverageContractReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Contract
  type: URI
  identifier: Identifier
  display: String
}

type Coverage implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  type: CodeableConcept
  policyHolder: CoveragePolicyHolderReference
  subscriber: CoverageSubscriberReference
  subscriberId: String
  beneficiary: CoverageBeneficiaryReference
  dependent: String
  relationship: CodeableConcept
  period: Period
  payor: [CoveragePayorReference]
  class: [CoverageClass]
  order: Int
  network: String
  costToBeneficiary: [CoverageCostToBeneficiary]
  subrogation: Boolean
  contract: [CoverageContractReference]
}

type CoverageBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Coverage
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CoverageBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CoverageBundleEntry]
}

type CoverageEligibilityRequestPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

union CoverageEligibilityRequestEnterer = Practitioner | PractitionerRole

type CoverageEligibilityRequestEntererReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CoverageEligibilityRequestEnterer
  type: URI
  identifier: Identifier
  display: String
}

union CoverageEligibilityRequestProvider = Practitioner | PractitionerRole | Organization

type CoverageEligibilityRequestProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CoverageEligibilityRequestProvider
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityRequestInsurerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityRequestFacilityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityRequest implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  priority: CodeableConcept
  purpose: [Code]
  patient: CoverageEligibilityRequestPatientReference
  servicedDate: Date
  servicedPeriod: Period
  created: DateTime
  enterer: CoverageEligibilityRequestEntererReference
  provider: CoverageEligibilityRequestProviderReference
  insurer: CoverageEligibilityRequestInsurerReference
  facility: CoverageEligibilityRequestFacilityReference
  supportingInfo: [CoverageEligibilityRequestSupportingInfo]
  insurance: [CoverageEligibilityRequestInsurance]
  item: [CoverageEligibilityRequestItem]
}

type CoverageEligibilityRequestBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: CoverageEligibilityRequest
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CoverageEligibilityRequestBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CoverageEligibilityRequestBundleEntry]
}

type CoverageEligibilityResponsePatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

union CoverageEligibilityResponseRequestor = Practitioner | PractitionerRole | Organization

type CoverageEligibilityResponseRequestorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CoverageEligibilityResponseRequestor
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityResponseRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CoverageEligibilityRequest
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityResponseInsurerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type CoverageEligibilityResponse implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  purpose: [Code]
  patient: CoverageEligibilityResponsePatientReference
  servicedDate: Date
  servicedPeriod: Period
  created: DateTime
  requestor: CoverageEligibilityResponseRequestorReference
  request: CoverageEligibilityResponseRequestReference
  outcome: Code
  disposition: String
  insurer: CoverageEligibilityResponseInsurerReference
  insurance: [CoverageEligibilityResponseInsurance]
  preAuthRef: String
  form: CodeableConcept
  error: [CoverageEligibilityResponseError]
}

type CoverageEligibilityResponseBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: CoverageEligibilityResponse
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type CoverageEligibilityResponseBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [CoverageEligibilityResponseBundleEntry]
}

type DetectedIssuePatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

union DetectedIssueAuthor = Practitioner | PractitionerRole | Device

type DetectedIssueAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DetectedIssueAuthor
  type: URI
  identifier: Identifier
  display: String
}

type DetectedIssueImplicatedReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type DetectedIssue implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  code: CodeableConcept
  severity: Code
  patient: DetectedIssuePatientReference
  identifiedDateTime: DateTime
  identifiedPeriod: Period
  author: DetectedIssueAuthorReference
  implicated: [DetectedIssueImplicatedReference]
  evidence: [DetectedIssueEvidence]
  detail: String
  reference: URI
  mitigation: [DetectedIssueMitigation]
}

type DetectedIssueBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: DetectedIssue
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type DetectedIssueBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [DetectedIssueBundleEntry]
}

type DeviceDefinitionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceDefinition
  type: URI
  identifier: Identifier
  display: String
}

type DevicePatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type DeviceOwnerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type DeviceLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type DeviceParentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type Device implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  definition: DeviceDefinitionReference
  udiCarrier: [DeviceUdiCarrier]
  status: Code
  statusReason: [CodeableConcept]
  distinctIdentifier: String
  manufacturer: String
  manufactureDate: DateTime
  expirationDate: DateTime
  lotNumber: String
  serialNumber: String
  deviceName: [DeviceDeviceName]
  modelNumber: String
  partNumber: String
  type: CodeableConcept
  specialization: [DeviceSpecialization]
  version: [DeviceVersion]
  property: [DeviceProperty]
  patient: DevicePatientReference
  owner: DeviceOwnerReference
  contact: [ContactPoint]
  location: DeviceLocationReference
  url: URI
  note: [Annotation]
  safety: [CodeableConcept]
  parent: DeviceParentReference
}

type DeviceBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Device
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type DeviceBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [DeviceBundleEntry]
}

type DeviceDefinitionManufacturerReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type DeviceDefinitionOwnerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type DeviceDefinitionParentDeviceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceDefinition
  type: URI
  identifier: Identifier
  display: String
}

type DeviceDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  udiDeviceIdentifier: [DeviceDefinitionUdiDeviceIdentifier]
  manufacturerString: String
  manufacturerReference: DeviceDefinitionManufacturerReferenceReference
  deviceName: [DeviceDefinitionDeviceName]
  modelNumber: String
  type: CodeableConcept
  specialization: [DeviceDefinitionSpecialization]
  version: [String]
  safety: [CodeableConcept]
  shelfLifeStorage: [ProductShelfLife]
  physicalCharacteristics: ProdCharacteristic
  languageCode: [CodeableConcept]
  capability: [DeviceDefinitionCapability]
  property: [DeviceDefinitionProperty]
  owner: DeviceDefinitionOwnerReference
  contact: [ContactPoint]
  url: URI
  onlineInformation: URI
  note: [Annotation]
  quantity: Quantity
  parentDevice: DeviceDefinitionParentDeviceReference
  material: [DeviceDefinitionMaterial]
}

type DeviceDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: DeviceDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type DeviceDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [DeviceDefinitionBundleEntry]
}

type DeviceMetricSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type DeviceMetricParentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type DeviceMetric implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  type: CodeableConcept
  unit: CodeableConcept
  source: DeviceMetricSourceReference
  parent: DeviceMetricParentReference
  operationalStatus: Code
  color: Code
  category: Code
  measurementPeriod: Timing
  calibration: [DeviceMetricCalibration]
}

type DeviceMetricBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: DeviceMetric
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type DeviceMetricBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [DeviceMetricBundleEntry]
}

type DeviceRequestBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type DeviceRequestPriorRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type DeviceRequestCodeReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

union DeviceRequestSubject = Patient | Group | Location | Device

type DeviceRequestSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceRequestSubject
  type: URI
  identifier: Identifier
  display: String
}

type DeviceRequestEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union DeviceRequestRequester = Device | Practitioner | PractitionerRole | Organization

type DeviceRequestRequesterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceRequestRequester
  type: URI
  identifier: Identifier
  display: String
}

union DeviceRequestPerformer = Practitioner | PractitionerRole | Organization | CareTeam | HealthcareService | Patient | Device | RelatedPerson

type DeviceRequestPerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceRequestPerformer
  type: URI
  identifier: Identifier
  display: String
}

union DeviceRequestReasonReference = Condition | Observation | DiagnosticReport | DocumentReference

type DeviceRequestReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceRequestReasonReference
  type: URI
  identifier: Identifier
  display: String
}

union DeviceRequestInsurance = Coverage | ClaimResponse

type DeviceRequestInsuranceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceRequestInsurance
  type: URI
  identifier: Identifier
  display: String
}

type DeviceRequestSupportingInfoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type DeviceRequestRelevantHistoryReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Provenance
  type: URI
  identifier: Identifier
  display: String
}

type DeviceRequest implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  instantiatesCanonical: [Canonical]
  instantiatesUri: [URI]
  basedOn: [DeviceRequestBasedOnReference]
  priorRequest: [DeviceRequestPriorRequestReference]
  groupIdentifier: Identifier
  status: Code
  intent: Code
  priority: Code
  codeReference: DeviceRequestCodeReferenceReference
  codeCodeableConcept: CodeableConcept
  parameter: [DeviceRequestParameter]
  subject: DeviceRequestSubjectReference
  encounter: DeviceRequestEncounterReference
  occurrenceDateTime: DateTime
  occurrencePeriod: Period
  occurrenceTiming: Timing
  authoredOn: DateTime
  requester: DeviceRequestRequesterReference
  performerType: CodeableConcept
  performer: DeviceRequestPerformerReference
  reasonCode: [CodeableConcept]
  reasonReference: [DeviceRequestReasonReferenceReference]
  insurance: [DeviceRequestInsuranceReference]
  supportingInfo: [DeviceRequestSupportingInfoReference]
  note: [Annotation]
  relevantHistory: [DeviceRequestRelevantHistoryReference]
}

type DeviceRequestBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: DeviceRequest
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type DeviceRequestBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [DeviceRequestBundleEntry]
}

type DeviceUseStatementBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequest
  type: URI
  identifier: Identifier
  display: String
}

union DeviceUseStatementSubject = Patient | Group

type DeviceUseStatementSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceUseStatementSubject
  type: URI
  identifier: Identifier
  display: String
}

union DeviceUseStatementDerivedFrom = ServiceRequest | Procedure | Claim | Observation | QuestionnaireResponse | DocumentReference

type DeviceUseStatementDerivedFromReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceUseStatementDerivedFrom
  type: URI
  identifier: Identifier
  display: String
}

union DeviceUseStatementSource = Patient | Practitioner | PractitionerRole | RelatedPerson

type DeviceUseStatementSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceUseStatementSource
  type: URI
  identifier: Identifier
  display: String
}

type DeviceUseStatementDeviceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

union DeviceUseStatementReasonReference = Condition | Observation | DiagnosticReport | DocumentReference | Media

type DeviceUseStatementReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DeviceUseStatementReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type DeviceUseStatement implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  basedOn: [DeviceUseStatementBasedOnReference]
  status: Code
  subject: DeviceUseStatementSubjectReference
  derivedFrom: [DeviceUseStatementDerivedFromReference]
  timingTiming: Timing
  timingPeriod: Period
  timingDateTime: DateTime
  recordedOn: DateTime
  source: DeviceUseStatementSourceReference
  device: DeviceUseStatementDeviceReference
  reasonCode: [CodeableConcept]
  reasonReference: [DeviceUseStatementReasonReferenceReference]
  bodySite: CodeableConcept
  note: [Annotation]
}

type DeviceUseStatementBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: DeviceUseStatement
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type DeviceUseStatementBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [DeviceUseStatementBundleEntry]
}

union DiagnosticReportBasedOn = CarePlan | ImmunizationRecommendation | MedicationRequest | NutritionOrder | ServiceRequest

type DiagnosticReportBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DiagnosticReportBasedOn
  type: URI
  identifier: Identifier
  display: String
}

union DiagnosticReportSubject = Patient | Group | Device | Location | Organization | Procedure | Practitioner | Medication | Substance

type DiagnosticReportSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DiagnosticReportSubject
  type: URI
  identifier: Identifier
  display: String
}

type DiagnosticReportEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union DiagnosticReportPerformer = Practitioner | PractitionerRole | Organization | CareTeam

type DiagnosticReportPerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DiagnosticReportPerformer
  type: URI
  identifier: Identifier
  display: String
}

union DiagnosticReportResultsInterpreter = Practitioner | PractitionerRole | Organization | CareTeam

type DiagnosticReportResultsInterpreterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DiagnosticReportResultsInterpreter
  type: URI
  identifier: Identifier
  display: String
}

type DiagnosticReportSpecimenReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Specimen
  type: URI
  identifier: Identifier
  display: String
}

type DiagnosticReportResultReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Observation
  type: URI
  identifier: Identifier
  display: String
}

type DiagnosticReportImagingStudyReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ImagingStudy
  type: URI
  identifier: Identifier
  display: String
}

type DiagnosticReport implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  basedOn: [DiagnosticReportBasedOnReference]
  status: Code
  category: [CodeableConcept]
  code: CodeableConcept
  subject: DiagnosticReportSubjectReference
  encounter: DiagnosticReportEncounterReference
  effectiveDateTime: DateTime
  effectivePeriod: Period
  issued: Instant
  performer: [DiagnosticReportPerformerReference]
  resultsInterpreter: [DiagnosticReportResultsInterpreterReference]
  specimen: [DiagnosticReportSpecimenReference]
  result: [DiagnosticReportResultReference]
  imagingStudy: [DiagnosticReportImagingStudyReference]
  media: [DiagnosticReportMedia]
  conclusion: String
  conclusionCode: [CodeableConcept]
  presentedForm: [Attachment]
}

type DiagnosticReportBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: DiagnosticReport
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type DiagnosticReportBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [DiagnosticReportBundleEntry]
}

union DocumentManifestSubject = Patient | Practitioner | Group | Device

type DocumentManifestSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentManifestSubject
  type: URI
  identifier: Identifier
  display: String
}

union DocumentManifestAuthor = Practitioner | PractitionerRole | Organization | Device | Patient | RelatedPerson

type DocumentManifestAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentManifestAuthor
  type: URI
  identifier: Identifier
  display: String
}

union DocumentManifestRecipient = Patient | Practitioner | PractitionerRole | RelatedPerson | Organization

type DocumentManifestRecipientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentManifestRecipient
  type: URI
  identifier: Identifier
  display: String
}

type DocumentManifestContentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type DocumentManifest implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  masterIdentifier: Identifier
  identifier: [Identifier]
  status: Code
  type: CodeableConcept
  subject: DocumentManifestSubjectReference
  created: DateTime
  author: [DocumentManifestAuthorReference]
  recipient: [DocumentManifestRecipientReference]
  source: URI
  description: String
  content: [DocumentManifestContentReference]
  related: [DocumentManifestRelated]
}

type DocumentManifestBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: DocumentManifest
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type DocumentManifestBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [DocumentManifestBundleEntry]
}

union DocumentReferenceSubject = Patient | Practitioner | Group | Device

type DocumentReferenceSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReferenceSubject
  type: URI
  identifier: Identifier
  display: String
}

union DocumentReferenceAuthor = Practitioner | PractitionerRole | Organization | Device | Patient | RelatedPerson

type DocumentReferenceAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReferenceAuthor
  type: URI
  identifier: Identifier
  display: String
}

union DocumentReferenceAuthenticator = Practitioner | PractitionerRole | Organization

type DocumentReferenceAuthenticatorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReferenceAuthenticator
  type: URI
  identifier: Identifier
  display: String
}

type DocumentReferenceCustodianReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type DocumentReference implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  masterIdentifier: Identifier
  identifier: [Identifier]
  status: Code
  docStatus: Code
  type: CodeableConcept
  category: [CodeableConcept]
  subject: DocumentReferenceSubjectReference
  date: Instant
  author: [DocumentReferenceAuthorReference]
  authenticator: DocumentReferenceAuthenticatorReference
  custodian: DocumentReferenceCustodianReference
  relatesTo: [DocumentReferenceRelatesTo]
  description: String
  securityLabel: [CodeableConcept]
  content: [DocumentReferenceContent]
  context: DocumentReferenceContext
}

type DocumentReferenceBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: DocumentReference
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type DocumentReferenceBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [DocumentReferenceBundleEntry]
}

union EncounterSubject = Patient | Group

type EncounterSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EncounterSubject
  type: URI
  identifier: Identifier
  display: String
}

type EncounterEpisodeOfCareReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EpisodeOfCare
  type: URI
  identifier: Identifier
  display: String
}

type EncounterBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequest
  type: URI
  identifier: Identifier
  display: String
}

type EncounterAppointmentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Appointment
  type: URI
  identifier: Identifier
  display: String
}

union EncounterReasonReference = Condition | Procedure | Observation | ImmunizationRecommendation

type EncounterReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EncounterReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type EncounterAccountReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Account
  type: URI
  identifier: Identifier
  display: String
}

type EncounterServiceProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type EncounterPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

type Encounter implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  statusHistory: [EncounterStatusHistory]
  class: Coding
  classHistory: [EncounterClassHistory]
  type: [CodeableConcept]
  serviceType: CodeableConcept
  priority: CodeableConcept
  subject: EncounterSubjectReference
  episodeOfCare: [EncounterEpisodeOfCareReference]
  basedOn: [EncounterBasedOnReference]
  participant: [EncounterParticipant]
  appointment: [EncounterAppointmentReference]
  period: Period
  length: Quantity
  reasonCode: [CodeableConcept]
  reasonReference: [EncounterReasonReferenceReference]
  diagnosis: [EncounterDiagnosis]
  account: [EncounterAccountReference]
  hospitalization: EncounterHospitalization
  location: [EncounterLocation]
  serviceProvider: EncounterServiceProviderReference
  partOf: EncounterPartOfReference
}

type EncounterBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Encounter
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type EncounterBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [EncounterBundleEntry]
}

type EndpointManagingOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type Endpoint implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  connectionType: Coding
  name: String
  managingOrganization: EndpointManagingOrganizationReference
  contact: [ContactPoint]
  period: Period
  payloadType: [CodeableConcept]
  payloadMimeType: [Code]
  address: URL
  header: [String]
}

type EndpointBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Endpoint
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type EndpointBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [EndpointBundleEntry]
}

type EnrollmentRequestInsurerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

union EnrollmentRequestProvider = Practitioner | PractitionerRole | Organization

type EnrollmentRequestProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EnrollmentRequestProvider
  type: URI
  identifier: Identifier
  display: String
}

type EnrollmentRequestCandidateReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type EnrollmentRequestCoverageReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Coverage
  type: URI
  identifier: Identifier
  display: String
}

type EnrollmentRequest implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  created: DateTime
  insurer: EnrollmentRequestInsurerReference
  provider: EnrollmentRequestProviderReference
  candidate: EnrollmentRequestCandidateReference
  coverage: EnrollmentRequestCoverageReference
}

type EnrollmentRequestBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: EnrollmentRequest
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type EnrollmentRequestBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [EnrollmentRequestBundleEntry]
}

type EnrollmentResponseRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EnrollmentRequest
  type: URI
  identifier: Identifier
  display: String
}

type EnrollmentResponseOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

union EnrollmentResponseRequestProvider = Practitioner | PractitionerRole | Organization

type EnrollmentResponseRequestProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EnrollmentResponseRequestProvider
  type: URI
  identifier: Identifier
  display: String
}

type EnrollmentResponse implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  request: EnrollmentResponseRequestReference
  outcome: Code
  disposition: String
  created: DateTime
  organization: EnrollmentResponseOrganizationReference
  requestProvider: EnrollmentResponseRequestProviderReference
}

type EnrollmentResponseBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: EnrollmentResponse
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type EnrollmentResponseBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [EnrollmentResponseBundleEntry]
}

type EpisodeOfCarePatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type EpisodeOfCareManagingOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type EpisodeOfCareReferralRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequest
  type: URI
  identifier: Identifier
  display: String
}

union EpisodeOfCareCareManager = Practitioner | PractitionerRole

type EpisodeOfCareCareManagerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: EpisodeOfCareCareManager
  type: URI
  identifier: Identifier
  display: String
}

type EpisodeOfCareTeamReference {
  id: String
  extension: [Extension]
  reference: String
  resource: CareTeam
  type: URI
  identifier: Identifier
  display: String
}

type EpisodeOfCareAccountReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Account
  type: URI
  identifier: Identifier
  display: String
}

type EpisodeOfCare implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  statusHistory: [EpisodeOfCareStatusHistory]
  type: [CodeableConcept]
  diagnosis: [EpisodeOfCareDiagnosis]
  patient: EpisodeOfCarePatientReference
  managingOrganization: EpisodeOfCareManagingOrganizationReference
  period: Period
  referralRequest: [EpisodeOfCareReferralRequestReference]
  careManager: EpisodeOfCareCareManagerReference
  team: [EpisodeOfCareTeamReference]
  account: [EpisodeOfCareAccountReference]
}

type EpisodeOfCareBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: EpisodeOfCare
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type EpisodeOfCareBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [EpisodeOfCareBundleEntry]
}

type EventDefinitionSubjectReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type EventDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  subtitle: String
  status: Code
  experimental: Boolean
  subjectCodeableConcept: CodeableConcept
  subjectReference: EventDefinitionSubjectReferenceReference
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  usage: String
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  topic: [CodeableConcept]
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  relatedArtifact: [RelatedArtifact]
  trigger: [TriggerDefinition]
}

type EventDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: EventDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type EventDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [EventDefinitionBundleEntry]
}

type EvidenceCiteAsReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Citation
  type: URI
  identifier: Identifier
  display: String
}

type Evidence implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  title: String
  citeAsReference: EvidenceCiteAsReferenceReference
  citeAsMarkdown: Markdown
  status: Code
  date: DateTime
  useContext: [UsageContext]
  approvalDate: Date
  lastReviewDate: Date
  publisher: String
  contact: [ContactDetail]
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  relatedArtifact: [RelatedArtifact]
  description: Markdown
  assertion: Markdown
  note: [Annotation]
  variableDefinition: [EvidenceVariableDefinition]
  synthesisType: CodeableConcept
  studyType: CodeableConcept
  statistic: [EvidenceStatistic]
  certainty: [EvidenceCertainty]
}

type EvidenceBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Evidence
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type EvidenceBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [EvidenceBundleEntry]
}

type EvidenceReportCiteAsReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Citation
  type: URI
  identifier: Identifier
  display: String
}

type EvidenceReport implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  status: Code
  useContext: [UsageContext]
  identifier: [Identifier]
  relatedIdentifier: [Identifier]
  citeAsReference: EvidenceReportCiteAsReferenceReference
  citeAsMarkdown: Markdown
  type: CodeableConcept
  note: [Annotation]
  relatedArtifact: [RelatedArtifact]
  subject: EvidenceReportSubject
  publisher: String
  contact: [ContactDetail]
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  relatesTo: [EvidenceReportRelatesTo]
  section: [EvidenceReportSection]
}

type EvidenceReportBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: EvidenceReport
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type EvidenceReportBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [EvidenceReportBundleEntry]
}

type EvidenceVariable implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  shortTitle: String
  subtitle: String
  status: Code
  date: DateTime
  description: Markdown
  note: [Annotation]
  useContext: [UsageContext]
  publisher: String
  contact: [ContactDetail]
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  relatedArtifact: [RelatedArtifact]
  actual: Boolean
  characteristicCombination: Code
  characteristic: [EvidenceVariableCharacteristic]
  handling: Code
  category: [EvidenceVariableCategory]
}

type EvidenceVariableBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: EvidenceVariable
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type EvidenceVariableBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [EvidenceVariableBundleEntry]
}

type ExampleScenario implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  copyright: Markdown
  purpose: Markdown
  actor: [ExampleScenarioActor]
  instance: [ExampleScenarioInstance]
  process: [ExampleScenarioProcess]
  workflow: [Canonical]
}

type ExampleScenarioBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ExampleScenario
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ExampleScenarioBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ExampleScenarioBundleEntry]
}

type ExplanationOfBenefitPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

union ExplanationOfBenefitEnterer = Practitioner | PractitionerRole

type ExplanationOfBenefitEntererReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ExplanationOfBenefitEnterer
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitInsurerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

union ExplanationOfBenefitProvider = Practitioner | PractitionerRole | Organization

type ExplanationOfBenefitProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ExplanationOfBenefitProvider
  type: URI
  identifier: Identifier
  display: String
}

union ExplanationOfBenefitPrescription = MedicationRequest | VisionPrescription

type ExplanationOfBenefitPrescriptionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ExplanationOfBenefitPrescription
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitOriginalPrescriptionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequest
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitReferralReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequest
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitFacilityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitClaimReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Claim
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefitClaimResponseReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClaimResponse
  type: URI
  identifier: Identifier
  display: String
}

type ExplanationOfBenefit implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  type: CodeableConcept
  subType: CodeableConcept
  use: Code
  patient: ExplanationOfBenefitPatientReference
  billablePeriod: Period
  created: DateTime
  enterer: ExplanationOfBenefitEntererReference
  insurer: ExplanationOfBenefitInsurerReference
  provider: ExplanationOfBenefitProviderReference
  priority: CodeableConcept
  fundsReserveRequested: CodeableConcept
  fundsReserve: CodeableConcept
  related: [ExplanationOfBenefitRelated]
  prescription: ExplanationOfBenefitPrescriptionReference
  originalPrescription: ExplanationOfBenefitOriginalPrescriptionReference
  payee: ExplanationOfBenefitPayee
  referral: ExplanationOfBenefitReferralReference
  facility: ExplanationOfBenefitFacilityReference
  claim: ExplanationOfBenefitClaimReference
  claimResponse: ExplanationOfBenefitClaimResponseReference
  outcome: Code
  disposition: String
  preAuthRef: [String]
  preAuthRefPeriod: [Period]
  careTeam: [ExplanationOfBenefitCareTeam]
  supportingInfo: [ExplanationOfBenefitSupportingInfo]
  diagnosis: [ExplanationOfBenefitDiagnosis]
  procedure: [ExplanationOfBenefitProcedure]
  precedence: Int
  insurance: [ExplanationOfBenefitInsurance]
  accident: ExplanationOfBenefitAccident
  item: [ExplanationOfBenefitItem]
  addItem: [ExplanationOfBenefitAddItem]
  adjudication: [ExplanationOfBenefitAdjudication]
  total: [ExplanationOfBenefitTotal]
  payment: ExplanationOfBenefitPayment
  formCode: CodeableConcept
  form: Attachment
  processNote: [ExplanationOfBenefitProcessNote]
  benefitPeriod: Period
  benefitBalance: [ExplanationOfBenefitBenefitBalance]
}

type ExplanationOfBenefitBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ExplanationOfBenefit
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ExplanationOfBenefitBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ExplanationOfBenefitBundleEntry]
}

type FamilyMemberHistoryPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

union FamilyMemberHistoryReasonReference = Condition | Observation | AllergyIntolerance | QuestionnaireResponse | DiagnosticReport | DocumentReference

type FamilyMemberHistoryReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: FamilyMemberHistoryReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type FamilyMemberHistory implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  instantiatesCanonical: [Canonical]
  instantiatesUri: [URI]
  status: Code
  dataAbsentReason: CodeableConcept
  patient: FamilyMemberHistoryPatientReference
  date: DateTime
  name: String
  relationship: CodeableConcept
  sex: CodeableConcept
  bornPeriod: Period
  bornDate: Date
  bornString: String
  ageAge: Quantity
  ageRange: Range
  ageString: String
  estimatedAge: Boolean
  deceasedBoolean: Boolean
  deceasedAge: Quantity
  deceasedRange: Range
  deceasedDate: Date
  deceasedString: String
  reasonCode: [CodeableConcept]
  reasonReference: [FamilyMemberHistoryReasonReferenceReference]
  note: [Annotation]
  condition: [FamilyMemberHistoryCondition]
}

type FamilyMemberHistoryBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: FamilyMemberHistory
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type FamilyMemberHistoryBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [FamilyMemberHistoryBundleEntry]
}

union FlagSubject = Patient | Location | Group | Organization | Practitioner | PlanDefinition | Medication | Procedure

type FlagSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: FlagSubject
  type: URI
  identifier: Identifier
  display: String
}

type FlagEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union FlagAuthor = Device | Organization | Patient | Practitioner | PractitionerRole

type FlagAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: FlagAuthor
  type: URI
  identifier: Identifier
  display: String
}

type Flag implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  category: [CodeableConcept]
  code: CodeableConcept
  subject: FlagSubjectReference
  period: Period
  encounter: FlagEncounterReference
  author: FlagAuthorReference
}

type FlagBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Flag
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type FlagBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [FlagBundleEntry]
}

union GoalSubject = Patient | Group | Organization

type GoalSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: GoalSubject
  type: URI
  identifier: Identifier
  display: String
}

union GoalExpressedBy = Patient | Practitioner | PractitionerRole | RelatedPerson

type GoalExpressedByReference {
  id: String
  extension: [Extension]
  reference: String
  resource: GoalExpressedBy
  type: URI
  identifier: Identifier
  display: String
}

union GoalAddresses = Condition | Observation | MedicationStatement | NutritionOrder | ServiceRequest | RiskAssessment

type GoalAddressesReference {
  id: String
  extension: [Extension]
  reference: String
  resource: GoalAddresses
  type: URI
  identifier: Identifier
  display: String
}

type GoalOutcomeReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Observation
  type: URI
  identifier: Identifier
  display: String
}

type Goal implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  lifecycleStatus: Code
  achievementStatus: CodeableConcept
  category: [CodeableConcept]
  priority: CodeableConcept
  description: CodeableConcept
  subject: GoalSubjectReference
  startDate: Date
  startCodeableConcept: CodeableConcept
  target: [GoalTarget]
  statusDate: Date
  statusReason: String
  expressedBy: GoalExpressedByReference
  addresses: [GoalAddressesReference]
  note: [Annotation]
  outcomeCode: [CodeableConcept]
  outcomeReference: [GoalOutcomeReferenceReference]
}

type GoalBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Goal
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type GoalBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [GoalBundleEntry]
}

type GraphDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  version: String
  name: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  start: Code
  profile: Canonical
  link: [GraphDefinitionLink]
}

type GraphDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: GraphDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type GraphDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [GraphDefinitionBundleEntry]
}

union GroupManagingEntity = Organization | RelatedPerson | Practitioner | PractitionerRole

type GroupManagingEntityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: GroupManagingEntity
  type: URI
  identifier: Identifier
  display: String
}

type Group implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  active: Boolean
  type: Code
  actual: Boolean
  code: CodeableConcept
  name: String
  quantity: Int
  managingEntity: GroupManagingEntityReference
  characteristic: [GroupCharacteristic]
  member: [GroupMember]
}

type GroupBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Group
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type GroupBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [GroupBundleEntry]
}

union GuidanceResponseSubject = Patient | Group

type GuidanceResponseSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: GuidanceResponseSubject
  type: URI
  identifier: Identifier
  display: String
}

type GuidanceResponseEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

type GuidanceResponsePerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

union GuidanceResponseReasonReference = Condition | Observation | DiagnosticReport | DocumentReference

type GuidanceResponseReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: GuidanceResponseReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type GuidanceResponseEvaluationMessageReference {
  id: String
  extension: [Extension]
  reference: String
  resource: OperationOutcome
  type: URI
  identifier: Identifier
  display: String
}

type GuidanceResponseOutputParametersReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Parameters
  type: URI
  identifier: Identifier
  display: String
}

union GuidanceResponseResult = CarePlan | RequestGroup

type GuidanceResponseResultReference {
  id: String
  extension: [Extension]
  reference: String
  resource: GuidanceResponseResult
  type: URI
  identifier: Identifier
  display: String
}

type GuidanceResponse implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  requestIdentifier: Identifier
  identifier: [Identifier]
  moduleUri: URI
  moduleCanonical: Canonical
  moduleCodeableConcept: CodeableConcept
  status: Code
  subject: GuidanceResponseSubjectReference
  encounter: GuidanceResponseEncounterReference
  occurrenceDateTime: DateTime
  performer: GuidanceResponsePerformerReference
  reasonCode: [CodeableConcept]
  reasonReference: [GuidanceResponseReasonReferenceReference]
  note: [Annotation]
  evaluationMessage: [GuidanceResponseEvaluationMessageReference]
  outputParameters: GuidanceResponseOutputParametersReference
  result: GuidanceResponseResultReference
  dataRequirement: [DataRequirement]
}

type GuidanceResponseBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: GuidanceResponse
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type GuidanceResponseBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [GuidanceResponseBundleEntry]
}

type HealthcareServiceProvidedByReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type HealthcareServiceLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type HealthcareServiceCoverageAreaReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type HealthcareServiceEndpointReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Endpoint
  type: URI
  identifier: Identifier
  display: String
}

type HealthcareService implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  active: Boolean
  providedBy: HealthcareServiceProvidedByReference
  category: [CodeableConcept]
  type: [CodeableConcept]
  specialty: [CodeableConcept]
  location: [HealthcareServiceLocationReference]
  name: String
  comment: String
  extraDetails: Markdown
  photo: Attachment
  telecom: [ContactPoint]
  coverageArea: [HealthcareServiceCoverageAreaReference]
  serviceProvisionCode: [CodeableConcept]
  eligibility: [HealthcareServiceEligibility]
  program: [CodeableConcept]
  characteristic: [CodeableConcept]
  communication: [CodeableConcept]
  referralMethod: [CodeableConcept]
  appointmentRequired: Boolean
  availableTime: [HealthcareServiceAvailableTime]
  notAvailable: [HealthcareServiceNotAvailable]
  availabilityExceptions: String
  endpoint: [HealthcareServiceEndpointReference]
}

type HealthcareServiceBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: HealthcareService
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type HealthcareServiceBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [HealthcareServiceBundleEntry]
}

union ImagingStudySubject = Patient | Device | Group

type ImagingStudySubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ImagingStudySubject
  type: URI
  identifier: Identifier
  display: String
}

type ImagingStudyEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union ImagingStudyBasedOn = CarePlan | ServiceRequest | Appointment | AppointmentResponse | Task

type ImagingStudyBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ImagingStudyBasedOn
  type: URI
  identifier: Identifier
  display: String
}

union ImagingStudyReferrer = Practitioner | PractitionerRole

type ImagingStudyReferrerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ImagingStudyReferrer
  type: URI
  identifier: Identifier
  display: String
}

union ImagingStudyInterpreter = Practitioner | PractitionerRole

type ImagingStudyInterpreterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ImagingStudyInterpreter
  type: URI
  identifier: Identifier
  display: String
}

type ImagingStudyEndpointReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Endpoint
  type: URI
  identifier: Identifier
  display: String
}

type ImagingStudyProcedureReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Procedure
  type: URI
  identifier: Identifier
  display: String
}

type ImagingStudyLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

union ImagingStudyReasonReference = Condition | Observation | Media | DiagnosticReport | DocumentReference

type ImagingStudyReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ImagingStudyReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type ImagingStudy implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  modality: [Coding]
  subject: ImagingStudySubjectReference
  encounter: ImagingStudyEncounterReference
  started: DateTime
  basedOn: [ImagingStudyBasedOnReference]
  referrer: ImagingStudyReferrerReference
  interpreter: [ImagingStudyInterpreterReference]
  endpoint: [ImagingStudyEndpointReference]
  numberOfSeries: Int
  numberOfInstances: Int
  procedureReference: ImagingStudyProcedureReferenceReference
  procedureCode: [CodeableConcept]
  location: ImagingStudyLocationReference
  reasonCode: [CodeableConcept]
  reasonReference: [ImagingStudyReasonReferenceReference]
  note: [Annotation]
  description: String
  series: [ImagingStudySeries]
}

type ImagingStudyBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ImagingStudy
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ImagingStudyBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ImagingStudyBundleEntry]
}

type ImmunizationPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationManufacturerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

union ImmunizationReasonReference = Condition | Observation | DiagnosticReport

type ImmunizationReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ImmunizationReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type Immunization implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  statusReason: CodeableConcept
  vaccineCode: CodeableConcept
  patient: ImmunizationPatientReference
  encounter: ImmunizationEncounterReference
  occurrenceDateTime: DateTime
  occurrenceString: String
  recorded: DateTime
  primarySource: Boolean
  reportOrigin: CodeableConcept
  location: ImmunizationLocationReference
  manufacturer: ImmunizationManufacturerReference
  lotNumber: String
  expirationDate: Date
  site: CodeableConcept
  route: CodeableConcept
  doseQuantity: Quantity
  performer: [ImmunizationPerformer]
  note: [Annotation]
  reasonCode: [CodeableConcept]
  reasonReference: [ImmunizationReasonReferenceReference]
  isSubpotent: Boolean
  subpotentReason: [CodeableConcept]
  education: [ImmunizationEducation]
  programEligibility: [CodeableConcept]
  fundingSource: CodeableConcept
  reaction: [ImmunizationReaction]
  protocolApplied: [ImmunizationProtocolApplied]
}

type ImmunizationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Immunization
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ImmunizationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ImmunizationBundleEntry]
}

type ImmunizationEvaluationPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationEvaluationAuthorityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationEvaluationImmunizationEventReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Immunization
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationEvaluation implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  patient: ImmunizationEvaluationPatientReference
  date: DateTime
  authority: ImmunizationEvaluationAuthorityReference
  targetDisease: CodeableConcept
  immunizationEvent: ImmunizationEvaluationImmunizationEventReference
  doseStatus: CodeableConcept
  doseStatusReason: [CodeableConcept]
  description: String
  series: String
  doseNumberPositiveInt: Int
  doseNumberString: String
  seriesDosesPositiveInt: Int
  seriesDosesString: String
}

type ImmunizationEvaluationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ImmunizationEvaluation
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ImmunizationEvaluationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ImmunizationEvaluationBundleEntry]
}

type ImmunizationRecommendationPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationRecommendationAuthorityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type ImmunizationRecommendation implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  patient: ImmunizationRecommendationPatientReference
  date: DateTime
  authority: ImmunizationRecommendationAuthorityReference
  recommendation: [ImmunizationRecommendationRecommendation]
}

type ImmunizationRecommendationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ImmunizationRecommendation
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ImmunizationRecommendationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ImmunizationRecommendationBundleEntry]
}

type ImplementationGuide implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  version: String
  name: String
  title: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  copyright: Markdown
  packageId: ID
  license: Code
  fhirVersion: [Code]
  dependsOn: [ImplementationGuideDependsOn]
  global: [ImplementationGuideGlobal]
  definition: ImplementationGuideDefinition
  manifest: ImplementationGuideManifest
}

type ImplementationGuideBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ImplementationGuide
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ImplementationGuideBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ImplementationGuideBundleEntry]
}

union IngredientFor = MedicinalProductDefinition | AdministrableProductDefinition | ManufacturedItemDefinition

type IngredientForReference {
  id: String
  extension: [Extension]
  reference: String
  resource: IngredientFor
  type: URI
  identifier: Identifier
  display: String
}

type Ingredient implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  status: Code
  for: [IngredientForReference]
  role: CodeableConcept
  function: [CodeableConcept]
  allergenicIndicator: Boolean
  manufacturer: [IngredientManufacturer]
  substance: IngredientSubstance
}

type IngredientBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Ingredient
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type IngredientBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [IngredientBundleEntry]
}

type InsurancePlanOwnedByReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type InsurancePlanAdministeredByReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type InsurancePlanCoverageAreaReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type InsurancePlanEndpointReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Endpoint
  type: URI
  identifier: Identifier
  display: String
}

type InsurancePlanNetworkReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type InsurancePlan implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  type: [CodeableConcept]
  name: String
  alias: [String]
  period: Period
  ownedBy: InsurancePlanOwnedByReference
  administeredBy: InsurancePlanAdministeredByReference
  coverageArea: [InsurancePlanCoverageAreaReference]
  contact: [InsurancePlanContact]
  endpoint: [InsurancePlanEndpointReference]
  network: [InsurancePlanNetworkReference]
  coverage: [InsurancePlanCoverage]
  plan: [InsurancePlanPlan]
}

type InsurancePlanBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: InsurancePlan
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type InsurancePlanBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [InsurancePlanBundleEntry]
}

union InvoiceSubject = Patient | Group

type InvoiceSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: InvoiceSubject
  type: URI
  identifier: Identifier
  display: String
}

union InvoiceRecipient = Organization | Patient | RelatedPerson

type InvoiceRecipientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: InvoiceRecipient
  type: URI
  identifier: Identifier
  display: String
}

type InvoiceIssuerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type InvoiceAccountReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Account
  type: URI
  identifier: Identifier
  display: String
}

type Invoice implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  cancelledReason: String
  type: CodeableConcept
  subject: InvoiceSubjectReference
  recipient: InvoiceRecipientReference
  date: DateTime
  participant: [InvoiceParticipant]
  issuer: InvoiceIssuerReference
  account: InvoiceAccountReference
  lineItem: [InvoiceLineItem]
  totalPriceComponent: [InvoicePriceComponent]
  totalNet: Money
  totalGross: Money
  paymentTerms: Markdown
  note: [Annotation]
}

type InvoiceBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Invoice
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type InvoiceBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [InvoiceBundleEntry]
}

type LibrarySubjectReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type Library implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  subtitle: String
  status: Code
  experimental: Boolean
  type: CodeableConcept
  subjectCodeableConcept: CodeableConcept
  subjectReference: LibrarySubjectReferenceReference
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  usage: String
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  topic: [CodeableConcept]
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  relatedArtifact: [RelatedArtifact]
  parameter: [ParameterDefinition]
  dataRequirement: [DataRequirement]
  content: [Attachment]
}

type LibraryBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Library
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type LibraryBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [LibraryBundleEntry]
}

union LinkageAuthor = Practitioner | PractitionerRole | Organization

type LinkageAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: LinkageAuthor
  type: URI
  identifier: Identifier
  display: String
}

type Linkage implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  active: Boolean
  author: LinkageAuthorReference
  item: [LinkageItem]
}

type LinkageBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Linkage
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type LinkageBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [LinkageBundleEntry]
}

union ListSubject = Patient | Group | Device | Location

type ListSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ListSubject
  type: URI
  identifier: Identifier
  display: String
}

type ListEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union ListSource = Practitioner | PractitionerRole | Patient | Device

type ListSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ListSource
  type: URI
  identifier: Identifier
  display: String
}

type List implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  mode: Code
  title: String
  code: CodeableConcept
  subject: ListSubjectReference
  encounter: ListEncounterReference
  date: DateTime
  source: ListSourceReference
  orderedBy: CodeableConcept
  note: [Annotation]
  entry: [ListEntry]
  emptyReason: CodeableConcept
}

type ListBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: List
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ListBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ListBundleEntry]
}

type LocationManagingOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type LocationPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type LocationEndpointReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Endpoint
  type: URI
  identifier: Identifier
  display: String
}

type Location implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  operationalStatus: Coding
  name: String
  alias: [String]
  description: String
  mode: Code
  type: [CodeableConcept]
  telecom: [ContactPoint]
  address: Address
  physicalType: CodeableConcept
  position: LocationPosition
  managingOrganization: LocationManagingOrganizationReference
  partOf: LocationPartOfReference
  hoursOfOperation: [LocationHoursOfOperation]
  availabilityExceptions: String
  endpoint: [LocationEndpointReference]
}

type LocationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Location
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type LocationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [LocationBundleEntry]
}

type ManufacturedItemDefinitionManufacturerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type ManufacturedItemDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  manufacturedDoseForm: CodeableConcept
  unitOfPresentation: CodeableConcept
  manufacturer: [ManufacturedItemDefinitionManufacturerReference]
  ingredient: [CodeableConcept]
  property: [ManufacturedItemDefinitionProperty]
}

type ManufacturedItemDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ManufacturedItemDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ManufacturedItemDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ManufacturedItemDefinitionBundleEntry]
}

type MeasureSubjectReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type Measure implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  subtitle: String
  status: Code
  experimental: Boolean
  subjectCodeableConcept: CodeableConcept
  subjectReference: MeasureSubjectReferenceReference
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  usage: String
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  topic: [CodeableConcept]
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  relatedArtifact: [RelatedArtifact]
  library: [Canonical]
  disclaimer: Markdown
  scoring: CodeableConcept
  compositeScoring: CodeableConcept
  type: [CodeableConcept]
  riskAdjustment: String
  rateAggregation: String
  rationale: Markdown
  clinicalRecommendationStatement: Markdown
  improvementNotation: CodeableConcept
  definition: [Markdown]
  guidance: Markdown
  group: [MeasureGroup]
  supplementalData: [MeasureSupplementalData]
}

type MeasureBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Measure
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MeasureBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MeasureBundleEntry]
}

union MeasureReportSubject = Patient | Practitioner | PractitionerRole | Location | Device | RelatedPerson | Group

type MeasureReportSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MeasureReportSubject
  type: URI
  identifier: Identifier
  display: String
}

union MeasureReportReporter = Practitioner | PractitionerRole | Location | Organization

type MeasureReportReporterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MeasureReportReporter
  type: URI
  identifier: Identifier
  display: String
}

type MeasureReportEvaluatedResourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type MeasureReport implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  type: Code
  measure: Canonical
  subject: MeasureReportSubjectReference
  date: DateTime
  reporter: MeasureReportReporterReference
  period: Period
  improvementNotation: CodeableConcept
  group: [MeasureReportGroup]
  evaluatedResource: [MeasureReportEvaluatedResourceReference]
}

type MeasureReportBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: MeasureReport
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MeasureReportBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MeasureReportBundleEntry]
}

union MediaBasedOn = ServiceRequest | CarePlan

type MediaBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MediaBasedOn
  type: URI
  identifier: Identifier
  display: String
}

type MediaPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union MediaSubject = Patient | Practitioner | PractitionerRole | Group | Device | Specimen | Location

type MediaSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MediaSubject
  type: URI
  identifier: Identifier
  display: String
}

type MediaEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union MediaOperator = Practitioner | PractitionerRole | Organization | CareTeam | Patient | Device | RelatedPerson

type MediaOperatorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MediaOperator
  type: URI
  identifier: Identifier
  display: String
}

union MediaDevice = Device | DeviceMetric

type MediaDeviceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MediaDevice
  type: URI
  identifier: Identifier
  display: String
}

type Media implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  basedOn: [MediaBasedOnReference]
  partOf: [MediaPartOfReference]
  status: Code
  type: CodeableConcept
  modality: CodeableConcept
  view: CodeableConcept
  subject: MediaSubjectReference
  encounter: MediaEncounterReference
  createdDateTime: DateTime
  createdPeriod: Period
  issued: Instant
  operator: MediaOperatorReference
  reasonCode: [CodeableConcept]
  bodySite: CodeableConcept
  deviceName: String
  device: MediaDeviceReference
  height: Int
  width: Int
  frames: Int
  duration: Float
  content: Attachment
  note: [Annotation]
}

type MediaBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Media
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MediaBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MediaBundleEntry]
}

type MedicationManufacturerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type Medication implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  code: CodeableConcept
  status: Code
  manufacturer: MedicationManufacturerReference
  form: CodeableConcept
  amount: Ratio
  ingredient: [MedicationIngredient]
  batch: MedicationBatch
}

type MedicationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Medication
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MedicationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MedicationBundleEntry]
}

union MedicationAdministrationPartOf = MedicationAdministration | Procedure

type MedicationAdministrationPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationAdministrationPartOf
  type: URI
  identifier: Identifier
  display: String
}

type MedicationAdministrationMedicationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Medication
  type: URI
  identifier: Identifier
  display: String
}

union MedicationAdministrationSubject = Patient | Group

type MedicationAdministrationSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationAdministrationSubject
  type: URI
  identifier: Identifier
  display: String
}

union MedicationAdministrationContext = Encounter | EpisodeOfCare

type MedicationAdministrationContextReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationAdministrationContext
  type: URI
  identifier: Identifier
  display: String
}

type MedicationAdministrationSupportingInformationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union MedicationAdministrationReasonReference = Condition | Observation | DiagnosticReport

type MedicationAdministrationReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationAdministrationReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type MedicationAdministrationRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequest
  type: URI
  identifier: Identifier
  display: String
}

type MedicationAdministrationDeviceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type MedicationAdministrationEventHistoryReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Provenance
  type: URI
  identifier: Identifier
  display: String
}

type MedicationAdministration implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  instantiates: [URI]
  partOf: [MedicationAdministrationPartOfReference]
  status: Code
  statusReason: [CodeableConcept]
  category: CodeableConcept
  medicationCodeableConcept: CodeableConcept
  medicationReference: MedicationAdministrationMedicationReferenceReference
  subject: MedicationAdministrationSubjectReference
  context: MedicationAdministrationContextReference
  supportingInformation: [MedicationAdministrationSupportingInformationReference]
  effectiveDateTime: DateTime
  effectivePeriod: Period
  performer: [MedicationAdministrationPerformer]
  reasonCode: [CodeableConcept]
  reasonReference: [MedicationAdministrationReasonReferenceReference]
  request: MedicationAdministrationRequestReference
  device: [MedicationAdministrationDeviceReference]
  note: [Annotation]
  dosage: MedicationAdministrationDosage
  eventHistory: [MedicationAdministrationEventHistoryReference]
}

type MedicationAdministrationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: MedicationAdministration
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MedicationAdministrationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MedicationAdministrationBundleEntry]
}

type MedicationDispensePartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Procedure
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispenseStatusReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DetectedIssue
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispenseMedicationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Medication
  type: URI
  identifier: Identifier
  display: String
}

union MedicationDispenseSubject = Patient | Group

type MedicationDispenseSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationDispenseSubject
  type: URI
  identifier: Identifier
  display: String
}

union MedicationDispenseContext = Encounter | EpisodeOfCare

type MedicationDispenseContextReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationDispenseContext
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispenseSupportingInformationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispenseLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispenseAuthorizingPrescriptionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequest
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispenseDestinationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

union MedicationDispenseReceiver = Patient | Practitioner

type MedicationDispenseReceiverReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationDispenseReceiver
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispenseDetectedIssueReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DetectedIssue
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispenseEventHistoryReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Provenance
  type: URI
  identifier: Identifier
  display: String
}

type MedicationDispense implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  partOf: [MedicationDispensePartOfReference]
  status: Code
  statusReasonCodeableConcept: CodeableConcept
  statusReasonReference: MedicationDispenseStatusReasonReferenceReference
  category: CodeableConcept
  medicationCodeableConcept: CodeableConcept
  medicationReference: MedicationDispenseMedicationReferenceReference
  subject: MedicationDispenseSubjectReference
  context: MedicationDispenseContextReference
  supportingInformation: [MedicationDispenseSupportingInformationReference]
  performer: [MedicationDispensePerformer]
  location: MedicationDispenseLocationReference
  authorizingPrescription: [MedicationDispenseAuthorizingPrescriptionReference]
  type: CodeableConcept
  quantity: Quantity
  daysSupply: Quantity
  whenPrepared: DateTime
  whenHandedOver: DateTime
  destination: MedicationDispenseDestinationReference
  receiver: [MedicationDispenseReceiverReference]
  note: [Annotation]
  dosageInstruction: [Dosage]
  substitution: MedicationDispenseSubstitution
  detectedIssue: [MedicationDispenseDetectedIssueReference]
  eventHistory: [MedicationDispenseEventHistoryReference]
}

type MedicationDispenseBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: MedicationDispense
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MedicationDispenseBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MedicationDispenseBundleEntry]
}

type MedicationKnowledgeManufacturerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type MedicationKnowledgeAssociatedMedicationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Medication
  type: URI
  identifier: Identifier
  display: String
}

type MedicationKnowledgeContraindicationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DetectedIssue
  type: URI
  identifier: Identifier
  display: String
}

type MedicationKnowledge implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  code: CodeableConcept
  status: Code
  manufacturer: MedicationKnowledgeManufacturerReference
  doseForm: CodeableConcept
  amount: Quantity
  synonym: [String]
  relatedMedicationKnowledge: [MedicationKnowledgeRelatedMedicationKnowledge]
  associatedMedication: [MedicationKnowledgeAssociatedMedicationReference]
  productType: [CodeableConcept]
  monograph: [MedicationKnowledgeMonograph]
  ingredient: [MedicationKnowledgeIngredient]
  preparationInstruction: Markdown
  intendedRoute: [CodeableConcept]
  cost: [MedicationKnowledgeCost]
  monitoringProgram: [MedicationKnowledgeMonitoringProgram]
  administrationGuidelines: [MedicationKnowledgeAdministrationGuidelines]
  medicineClassification: [MedicationKnowledgeMedicineClassification]
  packaging: MedicationKnowledgePackaging
  drugCharacteristic: [MedicationKnowledgeDrugCharacteristic]
  contraindication: [MedicationKnowledgeContraindicationReference]
  regulatory: [MedicationKnowledgeRegulatory]
  kinetics: [MedicationKnowledgeKinetics]
}

type MedicationKnowledgeBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: MedicationKnowledge
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MedicationKnowledgeBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MedicationKnowledgeBundleEntry]
}

union MedicationRequestReportedReference = Patient | Practitioner | PractitionerRole | RelatedPerson | Organization

type MedicationRequestReportedReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequestReportedReference
  type: URI
  identifier: Identifier
  display: String
}

type MedicationRequestMedicationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Medication
  type: URI
  identifier: Identifier
  display: String
}

union MedicationRequestSubject = Patient | Group

type MedicationRequestSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequestSubject
  type: URI
  identifier: Identifier
  display: String
}

type MedicationRequestEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

type MedicationRequestSupportingInformationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union MedicationRequestRequester = Practitioner | PractitionerRole | Organization | Patient | RelatedPerson | Device

type MedicationRequestRequesterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequestRequester
  type: URI
  identifier: Identifier
  display: String
}

union MedicationRequestPerformer = Practitioner | PractitionerRole | Organization | Patient | Device | RelatedPerson | CareTeam

type MedicationRequestPerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequestPerformer
  type: URI
  identifier: Identifier
  display: String
}

union MedicationRequestRecorder = Practitioner | PractitionerRole

type MedicationRequestRecorderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequestRecorder
  type: URI
  identifier: Identifier
  display: String
}

union MedicationRequestReasonReference = Condition | Observation

type MedicationRequestReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequestReasonReference
  type: URI
  identifier: Identifier
  display: String
}

union MedicationRequestBasedOn = CarePlan | MedicationRequest | ServiceRequest | ImmunizationRecommendation

type MedicationRequestBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequestBasedOn
  type: URI
  identifier: Identifier
  display: String
}

union MedicationRequestInsurance = Coverage | ClaimResponse

type MedicationRequestInsuranceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequestInsurance
  type: URI
  identifier: Identifier
  display: String
}

type MedicationRequestPriorPrescriptionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationRequest
  type: URI
  identifier: Identifier
  display: String
}

type MedicationRequestDetectedIssueReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DetectedIssue
  type: URI
  identifier: Identifier
  display: String
}

type MedicationRequestEventHistoryReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Provenance
  type: URI
  identifier: Identifier
  display: String
}

type MedicationRequestBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: MedicationRequest
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MedicationRequestBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MedicationRequestBundleEntry]
}

union MedicationStatementBasedOn = MedicationRequest | CarePlan | ServiceRequest

type MedicationStatementBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationStatementBasedOn
  type: URI
  identifier: Identifier
  display: String
}

union MedicationStatementPartOf = MedicationAdministration | MedicationDispense | MedicationStatement | Procedure | Observation

type MedicationStatementPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationStatementPartOf
  type: URI
  identifier: Identifier
  display: String
}

type MedicationStatementMedicationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Medication
  type: URI
  identifier: Identifier
  display: String
}

union MedicationStatementSubject = Patient | Group

type MedicationStatementSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationStatementSubject
  type: URI
  identifier: Identifier
  display: String
}

union MedicationStatementContext = Encounter | EpisodeOfCare

type MedicationStatementContextReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationStatementContext
  type: URI
  identifier: Identifier
  display: String
}

union MedicationStatementInformationSource = Patient | Practitioner | PractitionerRole | RelatedPerson | Organization

type MedicationStatementInformationSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationStatementInformationSource
  type: URI
  identifier: Identifier
  display: String
}

type MedicationStatementDerivedFromReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union MedicationStatementReasonReference = Condition | Observation | DiagnosticReport

type MedicationStatementReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicationStatementReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type MedicationStatement implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  basedOn: [MedicationStatementBasedOnReference]
  partOf: [MedicationStatementPartOfReference]
  status: Code
  statusReason: [CodeableConcept]
  category: CodeableConcept
  medicationCodeableConcept: CodeableConcept
  medicationReference: MedicationStatementMedicationReferenceReference
  subject: MedicationStatementSubjectReference
  context: MedicationStatementContextReference
  effectiveDateTime: DateTime
  effectivePeriod: Period
  dateAsserted: DateTime
  informationSource: MedicationStatementInformationSourceReference
  derivedFrom: [MedicationStatementDerivedFromReference]
  reasonCode: [CodeableConcept]
  reasonReference: [MedicationStatementReasonReferenceReference]
  note: [Annotation]
  dosage: [Dosage]
}

type MedicationStatementBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: MedicationStatement
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MedicationStatementBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MedicationStatementBundleEntry]
}

type MedicinalProductDefinitionImpurityReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SubstanceDefinition
  type: URI
  identifier: Identifier
  display: String
}

type MedicinalProductDefinitionAttachedDocumentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReference
  type: URI
  identifier: Identifier
  display: String
}

type MedicinalProductDefinitionMasterFileReference {
  id: String
  extension: [Extension]
  reference: String
  resource: DocumentReference
  type: URI
  identifier: Identifier
  display: String
}

type MedicinalProductDefinitionClinicalTrialReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ResearchStudy
  type: URI
  identifier: Identifier
  display: String
}

type MedicinalProductDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  type: CodeableConcept
  domain: CodeableConcept
  version: String
  status: CodeableConcept
  statusDate: DateTime
  description: Markdown
  combinedPharmaceuticalDoseForm: CodeableConcept
  route: [CodeableConcept]
  indication: Markdown
  legalStatusOfSupply: CodeableConcept
  additionalMonitoringIndicator: CodeableConcept
  specialMeasures: [CodeableConcept]
  pediatricUseIndicator: CodeableConcept
  classification: [CodeableConcept]
  marketingStatus: [MarketingStatus]
  packagedMedicinalProduct: [CodeableConcept]
  ingredient: [CodeableConcept]
  impurity: [MedicinalProductDefinitionImpurityReference]
  attachedDocument: [MedicinalProductDefinitionAttachedDocumentReference]
  masterFile: [MedicinalProductDefinitionMasterFileReference]
  contact: [MedicinalProductDefinitionContact]
  clinicalTrial: [MedicinalProductDefinitionClinicalTrialReference]
  code: [Coding]
  name: [MedicinalProductDefinitionName]
  crossReference: [MedicinalProductDefinitionCrossReference]
  operation: [MedicinalProductDefinitionOperation]
  characteristic: [MedicinalProductDefinitionCharacteristic]
}

type MedicinalProductDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: MedicinalProductDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MedicinalProductDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MedicinalProductDefinitionBundleEntry]
}

type MessageDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  replaces: [Canonical]
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  base: Canonical
  parent: [Canonical]
  eventCoding: Coding
  eventUri: URI
  category: Code
  focus: [MessageDefinitionFocus]
  responseRequired: Code
  allowedResponse: [MessageDefinitionAllowedResponse]
  graph: [Canonical]
}

type MessageDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: MessageDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MessageDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MessageDefinitionBundleEntry]
}

union MessageHeaderSender = Practitioner | PractitionerRole | Organization

type MessageHeaderSenderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MessageHeaderSender
  type: URI
  identifier: Identifier
  display: String
}

union MessageHeaderEnterer = Practitioner | PractitionerRole

type MessageHeaderEntererReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MessageHeaderEnterer
  type: URI
  identifier: Identifier
  display: String
}

union MessageHeaderAuthor = Practitioner | PractitionerRole

type MessageHeaderAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MessageHeaderAuthor
  type: URI
  identifier: Identifier
  display: String
}

union MessageHeaderResponsible = Practitioner | PractitionerRole | Organization

type MessageHeaderResponsibleReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MessageHeaderResponsible
  type: URI
  identifier: Identifier
  display: String
}

type MessageHeaderFocusReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type MessageHeader implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  eventCoding: Coding
  eventUri: URI
  destination: [MessageHeaderDestination]
  sender: MessageHeaderSenderReference
  enterer: MessageHeaderEntererReference
  author: MessageHeaderAuthorReference
  source: MessageHeaderSource
  responsible: MessageHeaderResponsibleReference
  reason: CodeableConcept
  response: MessageHeaderResponse
  focus: [MessageHeaderFocusReference]
  definition: Canonical
}

type MessageHeaderBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: MessageHeader
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MessageHeaderBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MessageHeaderBundleEntry]
}

type MolecularSequencePatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type MolecularSequenceSpecimenReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Specimen
  type: URI
  identifier: Identifier
  display: String
}

type MolecularSequenceDeviceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Device
  type: URI
  identifier: Identifier
  display: String
}

type MolecularSequencePerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type MolecularSequencePointerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MolecularSequence
  type: URI
  identifier: Identifier
  display: String
}

type MolecularSequence implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  type: Code
  coordinateSystem: Int
  patient: MolecularSequencePatientReference
  specimen: MolecularSequenceSpecimenReference
  device: MolecularSequenceDeviceReference
  performer: MolecularSequencePerformerReference
  quantity: Quantity
  referenceSeq: MolecularSequenceReferenceSeq
  variant: [MolecularSequenceVariant]
  observedSeq: String
  quality: [MolecularSequenceQuality]
  readCoverage: Int
  repository: [MolecularSequenceRepository]
  pointer: [MolecularSequencePointerReference]
  structureVariant: [MolecularSequenceStructureVariant]
}

type MolecularSequenceBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: MolecularSequence
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type MolecularSequenceBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [MolecularSequenceBundleEntry]
}

type NamingSystem implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  name: String
  status: Code
  kind: Code
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  responsible: String
  type: CodeableConcept
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  usage: String
  uniqueId: [NamingSystemUniqueId]
}

type NamingSystemBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: NamingSystem
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type NamingSystemBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [NamingSystemBundleEntry]
}

type NutritionOrderPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type NutritionOrderEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union NutritionOrderOrderer = Practitioner | PractitionerRole

type NutritionOrderOrdererReference {
  id: String
  extension: [Extension]
  reference: String
  resource: NutritionOrderOrderer
  type: URI
  identifier: Identifier
  display: String
}

type NutritionOrderAllergyIntoleranceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: AllergyIntolerance
  type: URI
  identifier: Identifier
  display: String
}

type NutritionOrder implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  instantiatesCanonical: [Canonical]
  instantiatesUri: [URI]
  instantiates: [URI]
  status: Code
  intent: Code
  patient: NutritionOrderPatientReference
  encounter: NutritionOrderEncounterReference
  dateTime: DateTime
  orderer: NutritionOrderOrdererReference
  allergyIntolerance: [NutritionOrderAllergyIntoleranceReference]
  foodPreferenceModifier: [CodeableConcept]
  excludeFoodModifier: [CodeableConcept]
  oralDiet: NutritionOrderOralDiet
  supplement: [NutritionOrderSupplement]
  enteralFormula: NutritionOrderEnteralFormula
  note: [Annotation]
}

type NutritionOrderBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: NutritionOrder
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type NutritionOrderBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [NutritionOrderBundleEntry]
}

type NutritionProductManufacturerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type NutritionProductKnownAllergenReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Substance
  type: URI
  identifier: Identifier
  display: String
}

type NutritionProduct implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  status: Code
  category: [CodeableConcept]
  code: CodeableConcept
  manufacturer: [NutritionProductManufacturerReference]
  nutrient: [NutritionProductNutrient]
  ingredient: [NutritionProductIngredient]
  knownAllergen: [NutritionProductKnownAllergenReference]
  productCharacteristic: [NutritionProductProductCharacteristic]
  instance: NutritionProductInstance
  note: [Annotation]
}

type NutritionProductBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: NutritionProduct
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type NutritionProductBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [NutritionProductBundleEntry]
}

union ObservationBasedOn = CarePlan | DeviceRequest | ImmunizationRecommendation | MedicationRequest | NutritionOrder | ServiceRequest

type ObservationBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationBasedOn
  type: URI
  identifier: Identifier
  display: String
}

union ObservationPartOf = MedicationAdministration | MedicationDispense | MedicationStatement | Procedure | Immunization | ImagingStudy

type ObservationPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationPartOf
  type: URI
  identifier: Identifier
  display: String
}

union ObservationSubject = Patient | Group | Device | Location | Organization | Procedure | Practitioner | Medication | Substance

type ObservationSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationSubject
  type: URI
  identifier: Identifier
  display: String
}

type ObservationFocusReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ObservationEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union ObservationPerformer = Practitioner | PractitionerRole | Organization | CareTeam | Patient | RelatedPerson

type ObservationPerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationPerformer
  type: URI
  identifier: Identifier
  display: String
}

type ObservationSpecimenReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Specimen
  type: URI
  identifier: Identifier
  display: String
}

union ObservationDevice = Device | DeviceMetric

type ObservationDeviceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDevice
  type: URI
  identifier: Identifier
  display: String
}

union ObservationHasMember = Observation | QuestionnaireResponse | MolecularSequence

type ObservationHasMemberReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationHasMember
  type: URI
  identifier: Identifier
  display: String
}

union ObservationDerivedFrom = DocumentReference | ImagingStudy | Media | QuestionnaireResponse | Observation | MolecularSequence

type ObservationDerivedFromReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ObservationDerivedFrom
  type: URI
  identifier: Identifier
  display: String
}

type Observation implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  basedOn: [ObservationBasedOnReference]
  partOf: [ObservationPartOfReference]
  status: Code
  category: [CodeableConcept]
  code: CodeableConcept
  subject: ObservationSubjectReference
  focus: [ObservationFocusReference]
  encounter: ObservationEncounterReference
  effectiveDateTime: DateTime
  effectivePeriod: Period
  effectiveTiming: Timing
  effectiveInstant: Instant
  issued: Instant
  performer: [ObservationPerformerReference]
  valueQuantity: Quantity
  valueCodeableConcept: CodeableConcept
  valueString: String
  valueBoolean: Boolean
  valueInteger: Int
  valueRange: Range
  valueRatio: Ratio
  valueSampledData: SampledData
  valueTime: Time
  valueDateTime: DateTime
  valuePeriod: Period
  dataAbsentReason: CodeableConcept
  interpretation: [CodeableConcept]
  note: [Annotation]
  bodySite: CodeableConcept
  method: CodeableConcept
  specimen: ObservationSpecimenReference
  device: ObservationDeviceReference
  referenceRange: [ObservationReferenceRange]
  hasMember: [ObservationHasMemberReference]
  derivedFrom: [ObservationDerivedFromReference]
  component: [ObservationComponent]
}

type ObservationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Observation
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ObservationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ObservationBundleEntry]
}

type ObservationDefinitionValidCodedValueSetReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ValueSet
  type: URI
  identifier: Identifier
  display: String
}

type ObservationDefinitionNormalCodedValueSetReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ValueSet
  type: URI
  identifier: Identifier
  display: String
}

type ObservationDefinitionAbnormalCodedValueSetReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ValueSet
  type: URI
  identifier: Identifier
  display: String
}

type ObservationDefinitionCriticalCodedValueSetReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ValueSet
  type: URI
  identifier: Identifier
  display: String
}

type ObservationDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  category: [CodeableConcept]
  code: CodeableConcept
  identifier: [Identifier]
  permittedDataType: [Code]
  multipleResultsAllowed: Boolean
  method: CodeableConcept
  preferredReportName: String
  quantitativeDetails: ObservationDefinitionQuantitativeDetails
  qualifiedInterval: [ObservationDefinitionQualifiedInterval]
  validCodedValueSet: ObservationDefinitionValidCodedValueSetReference
  normalCodedValueSet: ObservationDefinitionNormalCodedValueSetReference
  abnormalCodedValueSet: ObservationDefinitionAbnormalCodedValueSetReference
  criticalCodedValueSet: ObservationDefinitionCriticalCodedValueSetReference
}

type ObservationDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ObservationDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ObservationDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ObservationDefinitionBundleEntry]
}

type OperationDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  version: String
  name: String
  title: String
  status: Code
  kind: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  affectsState: Boolean
  code: Code
  comment: Markdown
  base: Canonical
  resource: [Code]
  system: Boolean
  type: Boolean
  instance: Boolean
  inputProfile: Canonical
  outputProfile: Canonical
  parameter: [OperationDefinitionParameter]
  overload: [OperationDefinitionOverload]
}

type OperationDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: OperationDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type OperationDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [OperationDefinitionBundleEntry]
}

type OperationOutcome implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  issue: [OperationOutcomeIssue]
}

type OperationOutcomeBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: OperationOutcome
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type OperationOutcomeBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [OperationOutcomeBundleEntry]
}

type OrganizationPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type OrganizationEndpointReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Endpoint
  type: URI
  identifier: Identifier
  display: String
}

type Organization implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  active: Boolean
  type: [CodeableConcept]
  name: String
  alias: [String]
  telecom: [ContactPoint]
  address: [Address]
  partOf: OrganizationPartOfReference
  contact: [OrganizationContact]
  endpoint: [OrganizationEndpointReference]
}

type OrganizationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Organization
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type OrganizationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [OrganizationBundleEntry]
}

type OrganizationAffiliationOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type OrganizationAffiliationParticipatingOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type OrganizationAffiliationNetworkReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type OrganizationAffiliationLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type OrganizationAffiliationHealthcareServiceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: HealthcareService
  type: URI
  identifier: Identifier
  display: String
}

type OrganizationAffiliationEndpointReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Endpoint
  type: URI
  identifier: Identifier
  display: String
}

type OrganizationAffiliation implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  active: Boolean
  period: Period
  organization: OrganizationAffiliationOrganizationReference
  participatingOrganization: OrganizationAffiliationParticipatingOrganizationReference
  network: [OrganizationAffiliationNetworkReference]
  code: [CodeableConcept]
  specialty: [CodeableConcept]
  location: [OrganizationAffiliationLocationReference]
  healthcareService: [OrganizationAffiliationHealthcareServiceReference]
  telecom: [ContactPoint]
  endpoint: [OrganizationAffiliationEndpointReference]
}

type OrganizationAffiliationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: OrganizationAffiliation
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type OrganizationAffiliationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [OrganizationAffiliationBundleEntry]
}

type PackagedProductDefinitionPackageForReference {
  id: String
  extension: [Extension]
  reference: String
  resource: MedicinalProductDefinition
  type: URI
  identifier: Identifier
  display: String
}

type PackagedProductDefinitionManufacturerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type PackagedProductDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  name: String
  type: CodeableConcept
  packageFor: [PackagedProductDefinitionPackageForReference]
  status: CodeableConcept
  statusDate: DateTime
  containedItemQuantity: [Quantity]
  description: Markdown
  legalStatusOfSupply: [PackagedProductDefinitionLegalStatusOfSupply]
  marketingStatus: [MarketingStatus]
  characteristic: [CodeableConcept]
  copackagedIndicator: Boolean
  manufacturer: [PackagedProductDefinitionManufacturerReference]
  package: PackagedProductDefinitionPackage
}

type PackagedProductDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: PackagedProductDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type PackagedProductDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [PackagedProductDefinitionBundleEntry]
}

type Parameters implements Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  parameter: [ParametersParameter]
}

type ParametersBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Parameters
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ParametersBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ParametersBundleEntry]
}

union PatientGeneralPractitioner = Organization | Practitioner | PractitionerRole

type PatientGeneralPractitionerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PatientGeneralPractitioner
  type: URI
  identifier: Identifier
  display: String
}

type PatientManagingOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type PatientBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Patient
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type PatientBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [PatientBundleEntry]
}

type PaymentNoticeRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type PaymentNoticeResponseReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union PaymentNoticeProvider = Practitioner | PractitionerRole | Organization

type PaymentNoticeProviderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PaymentNoticeProvider
  type: URI
  identifier: Identifier
  display: String
}

type PaymentNoticePaymentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PaymentReconciliation
  type: URI
  identifier: Identifier
  display: String
}

union PaymentNoticePayee = Practitioner | PractitionerRole | Organization

type PaymentNoticePayeeReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PaymentNoticePayee
  type: URI
  identifier: Identifier
  display: String
}

type PaymentNoticeRecipientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type PaymentNotice implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  request: PaymentNoticeRequestReference
  response: PaymentNoticeResponseReference
  created: DateTime
  provider: PaymentNoticeProviderReference
  payment: PaymentNoticePaymentReference
  paymentDate: Date
  payee: PaymentNoticePayeeReference
  recipient: PaymentNoticeRecipientReference
  amount: Money
  paymentStatus: CodeableConcept
}

type PaymentNoticeBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: PaymentNotice
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type PaymentNoticeBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [PaymentNoticeBundleEntry]
}

type PaymentReconciliationPaymentIssuerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type PaymentReconciliationRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Task
  type: URI
  identifier: Identifier
  display: String
}

union PaymentReconciliationRequestor = Practitioner | PractitionerRole | Organization

type PaymentReconciliationRequestorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PaymentReconciliationRequestor
  type: URI
  identifier: Identifier
  display: String
}

type PaymentReconciliation implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  period: Period
  created: DateTime
  paymentIssuer: PaymentReconciliationPaymentIssuerReference
  request: PaymentReconciliationRequestReference
  requestor: PaymentReconciliationRequestorReference
  outcome: Code
  disposition: String
  paymentDate: Date
  paymentAmount: Money
  paymentIdentifier: Identifier
  detail: [PaymentReconciliationDetail]
  formCode: CodeableConcept
  processNote: [PaymentReconciliationProcessNote]
}

type PaymentReconciliationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: PaymentReconciliation
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type PaymentReconciliationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [PaymentReconciliationBundleEntry]
}

type PersonManagingOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type Person implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  name: [HumanName]
  telecom: [ContactPoint]
  gender: Code
  birthDate: Date
  address: [Address]
  photo: Attachment
  managingOrganization: PersonManagingOrganizationReference
  active: Boolean
  link: [PersonLink]
}

type PersonBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Person
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type PersonBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [PersonBundleEntry]
}

type PlanDefinitionSubjectReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type PlanDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  subtitle: String
  type: CodeableConcept
  status: Code
  experimental: Boolean
  subjectCodeableConcept: CodeableConcept
  subjectReference: PlanDefinitionSubjectReferenceReference
  subjectCanonical: Canonical
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  usage: String
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  topic: [CodeableConcept]
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  relatedArtifact: [RelatedArtifact]
  library: [Canonical]
  goal: [PlanDefinitionGoal]
  action: [PlanDefinitionAction]
}

type PlanDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: PlanDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type PlanDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [PlanDefinitionBundleEntry]
}

type PractitionerBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Practitioner
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type PractitionerBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [PractitionerBundleEntry]
}

type PractitionerRolePractitionerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Practitioner
  type: URI
  identifier: Identifier
  display: String
}

type PractitionerRoleOrganizationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type PractitionerRoleLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type PractitionerRoleHealthcareServiceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: HealthcareService
  type: URI
  identifier: Identifier
  display: String
}

type PractitionerRoleEndpointReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Endpoint
  type: URI
  identifier: Identifier
  display: String
}

type PractitionerRole implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  active: Boolean
  period: Period
  practitioner: PractitionerRolePractitionerReference
  organization: PractitionerRoleOrganizationReference
  code: [CodeableConcept]
  specialty: [CodeableConcept]
  location: [PractitionerRoleLocationReference]
  healthcareService: [PractitionerRoleHealthcareServiceReference]
  telecom: [ContactPoint]
  availableTime: [PractitionerRoleAvailableTime]
  notAvailable: [PractitionerRoleNotAvailable]
  availabilityExceptions: String
  endpoint: [PractitionerRoleEndpointReference]
}

type PractitionerRoleBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: PractitionerRole
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type PractitionerRoleBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [PractitionerRoleBundleEntry]
}

union ProcedureBasedOn = CarePlan | ServiceRequest

type ProcedureBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProcedureBasedOn
  type: URI
  identifier: Identifier
  display: String
}

union ProcedurePartOf = Procedure | Observation | MedicationAdministration

type ProcedurePartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProcedurePartOf
  type: URI
  identifier: Identifier
  display: String
}

union ProcedureSubject = Patient | Group

type ProcedureSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProcedureSubject
  type: URI
  identifier: Identifier
  display: String
}

type ProcedureEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union ProcedureRecorder = Patient | RelatedPerson | Practitioner | PractitionerRole

type ProcedureRecorderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProcedureRecorder
  type: URI
  identifier: Identifier
  display: String
}

union ProcedureAsserter = Patient | RelatedPerson | Practitioner | PractitionerRole

type ProcedureAsserterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProcedureAsserter
  type: URI
  identifier: Identifier
  display: String
}

type ProcedureLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

union ProcedureReasonReference = Condition | Observation | Procedure | DiagnosticReport | DocumentReference

type ProcedureReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProcedureReasonReference
  type: URI
  identifier: Identifier
  display: String
}

union ProcedureReport = DiagnosticReport | DocumentReference | Composition

type ProcedureReportReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProcedureReport
  type: URI
  identifier: Identifier
  display: String
}

type ProcedureComplicationDetailReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Condition
  type: URI
  identifier: Identifier
  display: String
}

union ProcedureUsedReference = Device | Medication | Substance

type ProcedureUsedReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ProcedureUsedReference
  type: URI
  identifier: Identifier
  display: String
}

type Procedure implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  instantiatesCanonical: [Canonical]
  instantiatesUri: [URI]
  basedOn: [ProcedureBasedOnReference]
  partOf: [ProcedurePartOfReference]
  status: Code
  statusReason: CodeableConcept
  category: CodeableConcept
  code: CodeableConcept
  subject: ProcedureSubjectReference
  encounter: ProcedureEncounterReference
  performedDateTime: DateTime
  performedPeriod: Period
  performedString: String
  performedAge: Quantity
  performedRange: Range
  recorder: ProcedureRecorderReference
  asserter: ProcedureAsserterReference
  performer: [ProcedurePerformer]
  location: ProcedureLocationReference
  reasonCode: [CodeableConcept]
  reasonReference: [ProcedureReasonReferenceReference]
  bodySite: [CodeableConcept]
  outcome: CodeableConcept
  report: [ProcedureReportReference]
  complication: [CodeableConcept]
  complicationDetail: [ProcedureComplicationDetailReference]
  followUp: [CodeableConcept]
  note: [Annotation]
  focalDevice: [ProcedureFocalDevice]
  usedReference: [ProcedureUsedReferenceReference]
  usedCode: [CodeableConcept]
}

type ProcedureBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Procedure
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ProcedureBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ProcedureBundleEntry]
}

type ProvenanceTargetReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ProvenanceLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type Provenance implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  target: [ProvenanceTargetReference]
  occurredPeriod: Period
  occurredDateTime: DateTime
  recorded: Instant
  policy: [URI]
  location: ProvenanceLocationReference
  reason: [CodeableConcept]
  activity: CodeableConcept
  agent: [ProvenanceAgent]
  entity: [ProvenanceEntity]
  signature: [Signature]
}

type ProvenanceBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Provenance
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ProvenanceBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ProvenanceBundleEntry]
}

type Questionnaire implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  derivedFrom: [Canonical]
  status: Code
  experimental: Boolean
  subjectType: [Code]
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  code: [Coding]
  item: [QuestionnaireItem]
}

type QuestionnaireBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Questionnaire
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type QuestionnaireBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [QuestionnaireBundleEntry]
}

union QuestionnaireResponseBasedOn = CarePlan | ServiceRequest

type QuestionnaireResponseBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: QuestionnaireResponseBasedOn
  type: URI
  identifier: Identifier
  display: String
}

union QuestionnaireResponsePartOf = Observation | Procedure

type QuestionnaireResponsePartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: QuestionnaireResponsePartOf
  type: URI
  identifier: Identifier
  display: String
}

type QuestionnaireResponseSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type QuestionnaireResponseEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union QuestionnaireResponseAuthor = Device | Practitioner | PractitionerRole | Patient | RelatedPerson | Organization

type QuestionnaireResponseAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: QuestionnaireResponseAuthor
  type: URI
  identifier: Identifier
  display: String
}

union QuestionnaireResponseSource = Patient | Practitioner | PractitionerRole | RelatedPerson

type QuestionnaireResponseSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: QuestionnaireResponseSource
  type: URI
  identifier: Identifier
  display: String
}

type QuestionnaireResponse implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  basedOn: [QuestionnaireResponseBasedOnReference]
  partOf: [QuestionnaireResponsePartOfReference]
  questionnaire: Canonical
  status: Code
  subject: QuestionnaireResponseSubjectReference
  encounter: QuestionnaireResponseEncounterReference
  authored: DateTime
  author: QuestionnaireResponseAuthorReference
  source: QuestionnaireResponseSourceReference
  item: [QuestionnaireResponseItem]
}

type QuestionnaireResponseBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: QuestionnaireResponse
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type QuestionnaireResponseBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [QuestionnaireResponseBundleEntry]
}

union RegulatedAuthorizationSubject = MedicinalProductDefinition | BiologicallyDerivedProduct | NutritionProduct | PackagedProductDefinition | SubstanceDefinition | DeviceDefinition | ResearchStudy | ActivityDefinition | PlanDefinition | ObservationDefinition | Practitioner | Organization | Location

type RegulatedAuthorizationSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: RegulatedAuthorizationSubject
  type: URI
  identifier: Identifier
  display: String
}

type RegulatedAuthorizationIndicationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ClinicalUseDefinition
  type: URI
  identifier: Identifier
  display: String
}

type RegulatedAuthorizationHolderReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type RegulatedAuthorizationRegulatorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type RegulatedAuthorization implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  subject: [RegulatedAuthorizationSubjectReference]
  type: CodeableConcept
  description: Markdown
  region: [CodeableConcept]
  status: CodeableConcept
  statusDate: DateTime
  validityPeriod: Period
  indication: RegulatedAuthorizationIndicationReference
  intendedUse: CodeableConcept
  basis: [CodeableConcept]
  holder: RegulatedAuthorizationHolderReference
  regulator: RegulatedAuthorizationRegulatorReference
  case: RegulatedAuthorizationCase
}

type RegulatedAuthorizationBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: RegulatedAuthorization
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type RegulatedAuthorizationBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [RegulatedAuthorizationBundleEntry]
}

type RelatedPersonPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type RelatedPerson implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  active: Boolean
  patient: RelatedPersonPatientReference
  relationship: [CodeableConcept]
  name: [HumanName]
  telecom: [ContactPoint]
  gender: Code
  birthDate: Date
  address: [Address]
  photo: [Attachment]
  period: Period
  communication: [RelatedPersonCommunication]
}

type RelatedPersonBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: RelatedPerson
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type RelatedPersonBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [RelatedPersonBundleEntry]
}

type RequestGroupBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type RequestGroupReplacesReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union RequestGroupSubject = Patient | Group

type RequestGroupSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: RequestGroupSubject
  type: URI
  identifier: Identifier
  display: String
}

type RequestGroupEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union RequestGroupAuthor = Device | Practitioner | PractitionerRole

type RequestGroupAuthorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: RequestGroupAuthor
  type: URI
  identifier: Identifier
  display: String
}

union RequestGroupReasonReference = Condition | Observation | DiagnosticReport | DocumentReference

type RequestGroupReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: RequestGroupReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type RequestGroup implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  instantiatesCanonical: [Canonical]
  instantiatesUri: [URI]
  basedOn: [RequestGroupBasedOnReference]
  replaces: [RequestGroupReplacesReference]
  groupIdentifier: Identifier
  status: Code
  intent: Code
  priority: Code
  code: CodeableConcept
  subject: RequestGroupSubjectReference
  encounter: RequestGroupEncounterReference
  authoredOn: DateTime
  author: RequestGroupAuthorReference
  reasonCode: [CodeableConcept]
  reasonReference: [RequestGroupReasonReferenceReference]
  note: [Annotation]
  action: [RequestGroupAction]
}

type RequestGroupBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: RequestGroup
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type RequestGroupBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [RequestGroupBundleEntry]
}

type ResearchDefinitionSubjectReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type ResearchDefinitionPopulationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ResearchElementDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ResearchDefinitionExposureReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ResearchElementDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ResearchDefinitionExposureAlternativeReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ResearchElementDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ResearchDefinitionOutcomeReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ResearchElementDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ResearchDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  shortTitle: String
  subtitle: String
  status: Code
  experimental: Boolean
  subjectCodeableConcept: CodeableConcept
  subjectReference: ResearchDefinitionSubjectReferenceReference
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  comment: [String]
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  usage: String
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  topic: [CodeableConcept]
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  relatedArtifact: [RelatedArtifact]
  library: [Canonical]
  population: ResearchDefinitionPopulationReference
  exposure: ResearchDefinitionExposureReference
  exposureAlternative: ResearchDefinitionExposureAlternativeReference
  outcome: ResearchDefinitionOutcomeReference
}

type ResearchDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ResearchDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ResearchDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ResearchDefinitionBundleEntry]
}

type ResearchElementDefinitionSubjectReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type ResearchElementDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  shortTitle: String
  subtitle: String
  status: Code
  experimental: Boolean
  subjectCodeableConcept: CodeableConcept
  subjectReference: ResearchElementDefinitionSubjectReferenceReference
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  comment: [String]
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  usage: String
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  topic: [CodeableConcept]
  author: [ContactDetail]
  editor: [ContactDetail]
  reviewer: [ContactDetail]
  endorser: [ContactDetail]
  relatedArtifact: [RelatedArtifact]
  library: [Canonical]
  type: Code
  variableType: Code
  characteristic: [ResearchElementDefinitionCharacteristic]
}

type ResearchElementDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ResearchElementDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ResearchElementDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ResearchElementDefinitionBundleEntry]
}

type ResearchStudyProtocolReference {
  id: String
  extension: [Extension]
  reference: String
  resource: PlanDefinition
  type: URI
  identifier: Identifier
  display: String
}

type ResearchStudyPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ResearchStudy
  type: URI
  identifier: Identifier
  display: String
}

type ResearchStudyEnrollmentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Group
  type: URI
  identifier: Identifier
  display: String
}

type ResearchStudySponsorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

union ResearchStudyPrincipalInvestigator = Practitioner | PractitionerRole

type ResearchStudyPrincipalInvestigatorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ResearchStudyPrincipalInvestigator
  type: URI
  identifier: Identifier
  display: String
}

type ResearchStudySiteReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type ResearchStudy implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  title: String
  protocol: [ResearchStudyProtocolReference]
  partOf: [ResearchStudyPartOfReference]
  status: Code
  primaryPurposeType: CodeableConcept
  phase: CodeableConcept
  category: [CodeableConcept]
  focus: [CodeableConcept]
  condition: [CodeableConcept]
  contact: [ContactDetail]
  relatedArtifact: [RelatedArtifact]
  keyword: [CodeableConcept]
  location: [CodeableConcept]
  description: Markdown
  enrollment: [ResearchStudyEnrollmentReference]
  period: Period
  sponsor: ResearchStudySponsorReference
  principalInvestigator: ResearchStudyPrincipalInvestigatorReference
  site: [ResearchStudySiteReference]
  reasonStopped: CodeableConcept
  note: [Annotation]
  arm: [ResearchStudyArm]
  objective: [ResearchStudyObjective]
}

type ResearchStudyBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ResearchStudy
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ResearchStudyBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ResearchStudyBundleEntry]
}

type ResearchSubjectStudyReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ResearchStudy
  type: URI
  identifier: Identifier
  display: String
}

type ResearchSubjectIndividualReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type ResearchSubjectConsentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Consent
  type: URI
  identifier: Identifier
  display: String
}

type ResearchSubject implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  period: Period
  study: ResearchSubjectStudyReference
  individual: ResearchSubjectIndividualReference
  assignedArm: String
  actualArm: String
  consent: ResearchSubjectConsentReference
}

type ResearchSubjectBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ResearchSubject
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ResearchSubjectBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ResearchSubjectBundleEntry]
}

type RiskAssessmentBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type RiskAssessmentParentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union RiskAssessmentSubject = Patient | Group

type RiskAssessmentSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: RiskAssessmentSubject
  type: URI
  identifier: Identifier
  display: String
}

type RiskAssessmentEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

type RiskAssessmentConditionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Condition
  type: URI
  identifier: Identifier
  display: String
}

union RiskAssessmentPerformer = Practitioner | PractitionerRole | Device

type RiskAssessmentPerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: RiskAssessmentPerformer
  type: URI
  identifier: Identifier
  display: String
}

union RiskAssessmentReasonReference = Condition | Observation | DiagnosticReport | DocumentReference

type RiskAssessmentReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: RiskAssessmentReasonReference
  type: URI
  identifier: Identifier
  display: String
}

type RiskAssessmentBasisReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type RiskAssessment implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  basedOn: RiskAssessmentBasedOnReference
  parent: RiskAssessmentParentReference
  status: Code
  method: CodeableConcept
  code: CodeableConcept
  subject: RiskAssessmentSubjectReference
  encounter: RiskAssessmentEncounterReference
  occurrenceDateTime: DateTime
  occurrencePeriod: Period
  condition: RiskAssessmentConditionReference
  performer: RiskAssessmentPerformerReference
  reasonCode: [CodeableConcept]
  reasonReference: [RiskAssessmentReasonReferenceReference]
  basis: [RiskAssessmentBasisReference]
  prediction: [RiskAssessmentPrediction]
  mitigation: String
  note: [Annotation]
}

type RiskAssessmentBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: RiskAssessment
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type RiskAssessmentBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [RiskAssessmentBundleEntry]
}

union ScheduleActor = Patient | Practitioner | PractitionerRole | RelatedPerson | Device | HealthcareService | Location

type ScheduleActorReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ScheduleActor
  type: URI
  identifier: Identifier
  display: String
}

type Schedule implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  active: Boolean
  serviceCategory: [CodeableConcept]
  serviceType: [CodeableConcept]
  specialty: [CodeableConcept]
  actor: [ScheduleActorReference]
  planningHorizon: Period
  comment: String
}

type ScheduleBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Schedule
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ScheduleBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ScheduleBundleEntry]
}

type SearchParameter implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  version: String
  name: String
  derivedFrom: Canonical
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  code: Code
  base: [Code]
  type: Code
  expression: String
  xpath: String
  xpathUsage: Code
  target: [Code]
  multipleOr: Boolean
  multipleAnd: Boolean
  comparator: [Code]
  modifier: [Code]
  chain: [String]
  component: [SearchParameterComponent]
}

type SearchParameterBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: SearchParameter
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SearchParameterBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SearchParameterBundleEntry]
}

union ServiceRequestBasedOn = CarePlan | ServiceRequest | MedicationRequest

type ServiceRequestBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequestBasedOn
  type: URI
  identifier: Identifier
  display: String
}

type ServiceRequestReplacesReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequest
  type: URI
  identifier: Identifier
  display: String
}

union ServiceRequestSubject = Patient | Group | Location | Device

type ServiceRequestSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequestSubject
  type: URI
  identifier: Identifier
  display: String
}

type ServiceRequestEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union ServiceRequestRequester = Practitioner | PractitionerRole | Organization | Patient | RelatedPerson | Device

type ServiceRequestRequesterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequestRequester
  type: URI
  identifier: Identifier
  display: String
}

union ServiceRequestPerformer = Practitioner | PractitionerRole | Organization | CareTeam | HealthcareService | Patient | Device | RelatedPerson

type ServiceRequestPerformerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequestPerformer
  type: URI
  identifier: Identifier
  display: String
}

type ServiceRequestLocationReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

union ServiceRequestReasonReference = Condition | Observation | DiagnosticReport | DocumentReference

type ServiceRequestReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequestReasonReference
  type: URI
  identifier: Identifier
  display: String
}

union ServiceRequestInsurance = Coverage | ClaimResponse

type ServiceRequestInsuranceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequestInsurance
  type: URI
  identifier: Identifier
  display: String
}

type ServiceRequestSupportingInfoReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type ServiceRequestSpecimenReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Specimen
  type: URI
  identifier: Identifier
  display: String
}

type ServiceRequestRelevantHistoryReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Provenance
  type: URI
  identifier: Identifier
  display: String
}

type ServiceRequest implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  instantiatesCanonical: [Canonical]
  instantiatesUri: [URI]
  basedOn: [ServiceRequestBasedOnReference]
  replaces: [ServiceRequestReplacesReference]
  requisition: Identifier
  status: Code
  intent: Code
  category: [CodeableConcept]
  priority: Code
  doNotPerform: Boolean
  code: CodeableConcept
  orderDetail: [CodeableConcept]
  quantityQuantity: Quantity
  quantityRatio: Ratio
  quantityRange: Range
  subject: ServiceRequestSubjectReference
  encounter: ServiceRequestEncounterReference
  occurrenceDateTime: DateTime
  occurrencePeriod: Period
  occurrenceTiming: Timing
  asNeededBoolean: Boolean
  asNeededCodeableConcept: CodeableConcept
  authoredOn: DateTime
  requester: ServiceRequestRequesterReference
  performerType: CodeableConcept
  performer: [ServiceRequestPerformerReference]
  locationCode: [CodeableConcept]
  locationReference: [ServiceRequestLocationReferenceReference]
  reasonCode: [CodeableConcept]
  reasonReference: [ServiceRequestReasonReferenceReference]
  insurance: [ServiceRequestInsuranceReference]
  supportingInfo: [ServiceRequestSupportingInfoReference]
  specimen: [ServiceRequestSpecimenReference]
  bodySite: [CodeableConcept]
  note: [Annotation]
  patientInstruction: String
  relevantHistory: [ServiceRequestRelevantHistoryReference]
}

type ServiceRequestBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ServiceRequest
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ServiceRequestBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ServiceRequestBundleEntry]
}

type SlotScheduleReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Schedule
  type: URI
  identifier: Identifier
  display: String
}

type Slot implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  serviceCategory: [CodeableConcept]
  serviceType: [CodeableConcept]
  specialty: [CodeableConcept]
  appointmentType: CodeableConcept
  schedule: SlotScheduleReference
  status: Code
  start: Instant
  end: Instant
  overbooked: Boolean
  comment: String
}

type SlotBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Slot
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SlotBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SlotBundleEntry]
}

union SpecimenSubject = Patient | Group | Device | Substance | Location

type SpecimenSubjectReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SpecimenSubject
  type: URI
  identifier: Identifier
  display: String
}

type SpecimenParentReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Specimen
  type: URI
  identifier: Identifier
  display: String
}

type SpecimenRequestReference {
  id: String
  extension: [Extension]
  reference: String
  resource: ServiceRequest
  type: URI
  identifier: Identifier
  display: String
}

type Specimen implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  accessionIdentifier: Identifier
  status: Code
  type: CodeableConcept
  subject: SpecimenSubjectReference
  receivedTime: DateTime
  parent: [SpecimenParentReference]
  request: [SpecimenRequestReference]
  collection: SpecimenCollection
  processing: [SpecimenProcessing]
  container: [SpecimenContainer]
  condition: [CodeableConcept]
  note: [Annotation]
}

type SpecimenBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Specimen
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SpecimenBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SpecimenBundleEntry]
}

type SpecimenDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  typeCollected: CodeableConcept
  patientPreparation: [CodeableConcept]
  timeAspect: String
  collection: [CodeableConcept]
  typeTested: [SpecimenDefinitionTypeTested]
}

type SpecimenDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: SpecimenDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SpecimenDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SpecimenDefinitionBundleEntry]
}

type StructureDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  keyword: [Coding]
  fhirVersion: Code
  mapping: [StructureDefinitionMapping]
  kind: Code
  abstract: Boolean
  context: [StructureDefinitionContext]
  contextInvariant: [String]
  type: URI
  baseDefinition: Canonical
  derivation: Code
  snapshot: StructureDefinitionSnapshot
  differential: StructureDefinitionDifferential
}

type StructureDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: StructureDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type StructureDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [StructureDefinitionBundleEntry]
}

type StructureMap implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  structure: [StructureMapStructure]
  import: [Canonical]
  group: [StructureMapGroup]
}

type StructureMapBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: StructureMap
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type StructureMapBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [StructureMapBundleEntry]
}

type SubscriptionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Subscription
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SubscriptionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SubscriptionBundleEntry]
}

type SubscriptionStatusSubscriptionReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Subscription
  type: URI
  identifier: Identifier
  display: String
}

type SubscriptionStatusBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: SubscriptionStatus
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SubscriptionStatusBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SubscriptionStatusBundleEntry]
}

type SubscriptionTopic implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  title: String
  derivedFrom: [Canonical]
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  approvalDate: Date
  lastReviewDate: Date
  effectivePeriod: Period
  resourceTrigger: [SubscriptionTopicResourceTrigger]
  eventTrigger: [SubscriptionTopicEventTrigger]
  canFilterBy: [SubscriptionTopicCanFilterBy]
  notificationShape: [SubscriptionTopicNotificationShape]
}

type SubscriptionTopicBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: SubscriptionTopic
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SubscriptionTopicBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SubscriptionTopicBundleEntry]
}

type Substance implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  category: [CodeableConcept]
  code: CodeableConcept
  description: String
  instance: [SubstanceInstance]
  ingredient: [SubstanceIngredient]
}

type SubstanceBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Substance
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SubstanceBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SubstanceBundleEntry]
}

type SubstanceDefinitionInformationSourceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Citation
  type: URI
  identifier: Identifier
  display: String
}

type SubstanceDefinitionManufacturerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type SubstanceDefinitionSupplierReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Organization
  type: URI
  identifier: Identifier
  display: String
}

type SubstanceDefinition implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  version: String
  status: CodeableConcept
  classification: [CodeableConcept]
  domain: CodeableConcept
  grade: [CodeableConcept]
  description: Markdown
  informationSource: [SubstanceDefinitionInformationSourceReference]
  note: [Annotation]
  manufacturer: [SubstanceDefinitionManufacturerReference]
  supplier: [SubstanceDefinitionSupplierReference]
  moiety: [SubstanceDefinitionMoiety]
  property: [SubstanceDefinitionProperty]
  molecularWeight: [SubstanceDefinitionMolecularWeight]
  structure: SubstanceDefinitionStructure
  code: [SubstanceDefinitionCode]
  name: [SubstanceDefinitionName]
  relationship: [SubstanceDefinitionRelationship]
  sourceMaterial: SubstanceDefinitionSourceMaterial
}

type SubstanceDefinitionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: SubstanceDefinition
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SubstanceDefinitionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SubstanceDefinitionBundleEntry]
}

type SupplyDeliveryBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyRequest
  type: URI
  identifier: Identifier
  display: String
}

union SupplyDeliveryPartOf = SupplyDelivery | Contract

type SupplyDeliveryPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyDeliveryPartOf
  type: URI
  identifier: Identifier
  display: String
}

type SupplyDeliveryPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

union SupplyDeliverySupplier = Practitioner | PractitionerRole | Organization

type SupplyDeliverySupplierReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyDeliverySupplier
  type: URI
  identifier: Identifier
  display: String
}

type SupplyDeliveryDestinationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

union SupplyDeliveryReceiver = Practitioner | PractitionerRole

type SupplyDeliveryReceiverReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyDeliveryReceiver
  type: URI
  identifier: Identifier
  display: String
}

type SupplyDelivery implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  basedOn: [SupplyDeliveryBasedOnReference]
  partOf: [SupplyDeliveryPartOfReference]
  status: Code
  patient: SupplyDeliveryPatientReference
  type: CodeableConcept
  suppliedItem: SupplyDeliverySuppliedItem
  occurrenceDateTime: DateTime
  occurrencePeriod: Period
  occurrenceTiming: Timing
  supplier: SupplyDeliverySupplierReference
  destination: SupplyDeliveryDestinationReference
  receiver: [SupplyDeliveryReceiverReference]
}

type SupplyDeliveryBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: SupplyDelivery
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SupplyDeliveryBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SupplyDeliveryBundleEntry]
}

union SupplyRequestItemReference = Medication | Substance | Device

type SupplyRequestItemReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyRequestItemReference
  type: URI
  identifier: Identifier
  display: String
}

union SupplyRequestRequester = Practitioner | PractitionerRole | Organization | Patient | RelatedPerson | Device

type SupplyRequestRequesterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyRequestRequester
  type: URI
  identifier: Identifier
  display: String
}

union SupplyRequestSupplier = Organization | HealthcareService

type SupplyRequestSupplierReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyRequestSupplier
  type: URI
  identifier: Identifier
  display: String
}

union SupplyRequestReasonReference = Condition | Observation | DiagnosticReport | DocumentReference

type SupplyRequestReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyRequestReasonReference
  type: URI
  identifier: Identifier
  display: String
}

union SupplyRequestDeliverFrom = Organization | Location

type SupplyRequestDeliverFromReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyRequestDeliverFrom
  type: URI
  identifier: Identifier
  display: String
}

union SupplyRequestDeliverTo = Organization | Location | Patient

type SupplyRequestDeliverToReference {
  id: String
  extension: [Extension]
  reference: String
  resource: SupplyRequestDeliverTo
  type: URI
  identifier: Identifier
  display: String
}

type SupplyRequest implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  category: CodeableConcept
  priority: Code
  itemCodeableConcept: CodeableConcept
  itemReference: SupplyRequestItemReferenceReference
  quantity: Quantity
  parameter: [SupplyRequestParameter]
  occurrenceDateTime: DateTime
  occurrencePeriod: Period
  occurrenceTiming: Timing
  authoredOn: DateTime
  requester: SupplyRequestRequesterReference
  supplier: [SupplyRequestSupplierReference]
  reasonCode: [CodeableConcept]
  reasonReference: [SupplyRequestReasonReferenceReference]
  deliverFrom: SupplyRequestDeliverFromReference
  deliverTo: SupplyRequestDeliverToReference
}

type SupplyRequestBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: SupplyRequest
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type SupplyRequestBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [SupplyRequestBundleEntry]
}

type TaskBasedOnReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type TaskPartOfReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Task
  type: URI
  identifier: Identifier
  display: String
}

type TaskFocusReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type TaskForReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type TaskEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union TaskRequester = Device | Organization | Patient | Practitioner | PractitionerRole | RelatedPerson

type TaskRequesterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: TaskRequester
  type: URI
  identifier: Identifier
  display: String
}

union TaskOwner = Practitioner | PractitionerRole | Organization | CareTeam | HealthcareService | Patient | Device | RelatedPerson

type TaskOwnerReference {
  id: String
  extension: [Extension]
  reference: String
  resource: TaskOwner
  type: URI
  identifier: Identifier
  display: String
}

type TaskLocationReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Location
  type: URI
  identifier: Identifier
  display: String
}

type TaskReasonReferenceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

union TaskInsurance = Coverage | ClaimResponse

type TaskInsuranceReference {
  id: String
  extension: [Extension]
  reference: String
  resource: TaskInsurance
  type: URI
  identifier: Identifier
  display: String
}

type TaskRelevantHistoryReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Provenance
  type: URI
  identifier: Identifier
  display: String
}

type Task implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  instantiatesCanonical: Canonical
  instantiatesUri: URI
  basedOn: [TaskBasedOnReference]
  groupIdentifier: Identifier
  partOf: [TaskPartOfReference]
  status: Code
  statusReason: CodeableConcept
  businessStatus: CodeableConcept
  intent: Code
  priority: Code
  code: CodeableConcept
  description: String
  focus: TaskFocusReference
  for: TaskForReference
  encounter: TaskEncounterReference
  executionPeriod: Period
  authoredOn: DateTime
  lastModified: DateTime
  requester: TaskRequesterReference
  performerType: [CodeableConcept]
  owner: TaskOwnerReference
  location: TaskLocationReference
  reasonCode: CodeableConcept
  reasonReference: TaskReasonReferenceReference
  insurance: [TaskInsuranceReference]
  note: [Annotation]
  relevantHistory: [TaskRelevantHistoryReference]
  restriction: TaskRestriction
  input: [TaskInput]
  output: [TaskOutput]
}

type TaskBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: Task
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type TaskBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [TaskBundleEntry]
}

type TerminologyCapabilities implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  version: String
  name: String
  title: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  kind: Code
  software: TerminologyCapabilitiesSoftware
  implementation: TerminologyCapabilitiesImplementation
  lockedDate: Boolean
  codeSystem: [TerminologyCapabilitiesCodeSystem]
  expansion: TerminologyCapabilitiesExpansion
  codeSearch: Code
  validateCode: TerminologyCapabilitiesValidateCode
  translation: TerminologyCapabilitiesTranslation
  closure: TerminologyCapabilitiesClosure
}

type TerminologyCapabilitiesBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: TerminologyCapabilities
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type TerminologyCapabilitiesBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [TerminologyCapabilitiesBundleEntry]
}

type TestReportTestScriptReference {
  id: String
  extension: [Extension]
  reference: String
  resource: TestScript
  type: URI
  identifier: Identifier
  display: String
}

type TestReport implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: Identifier
  name: String
  status: Code
  testScript: TestReportTestScriptReference
  result: Code
  score: Float
  tester: String
  issued: DateTime
  participant: [TestReportParticipant]
  setup: TestReportSetup
  test: [TestReportTest]
  teardown: TestReportTeardown
}

type TestReportBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: TestReport
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type TestReportBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [TestReportBundleEntry]
}

type TestScriptProfileReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type TestScript implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: Identifier
  version: String
  name: String
  title: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  purpose: Markdown
  copyright: Markdown
  origin: [TestScriptOrigin]
  destination: [TestScriptDestination]
  metadata: TestScriptMetadata
  fixture: [TestScriptFixture]
  profile: [TestScriptProfileReference]
  variable: [TestScriptVariable]
  setup: TestScriptSetup
  test: [TestScriptTest]
  teardown: TestScriptTeardown
}

type TestScriptBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: TestScript
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type TestScriptBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [TestScriptBundleEntry]
}

type ValueSet implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  url: URI
  identifier: [Identifier]
  version: String
  name: String
  title: String
  status: Code
  experimental: Boolean
  date: DateTime
  publisher: String
  contact: [ContactDetail]
  description: Markdown
  useContext: [UsageContext]
  jurisdiction: [CodeableConcept]
  immutable: Boolean
  purpose: Markdown
  copyright: Markdown
  compose: ValueSetCompose
  expansion: ValueSetExpansion
}

type ValueSetBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: ValueSet
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type ValueSetBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [ValueSetBundleEntry]
}

type VerificationResultTargetReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Resource
  type: URI
  identifier: Identifier
  display: String
}

type VerificationResult implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  target: [VerificationResultTargetReference]
  targetLocation: [String]
  need: CodeableConcept
  status: Code
  statusDate: DateTime
  validationType: CodeableConcept
  validationProcess: [CodeableConcept]
  frequency: Timing
  lastPerformed: DateTime
  nextScheduled: Date
  failureAction: CodeableConcept
  primarySource: [VerificationResultPrimarySource]
  attestation: VerificationResultAttestation
  validator: [VerificationResultValidator]
}

type VerificationResultBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: VerificationResult
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type VerificationResultBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [VerificationResultBundleEntry]
}

type VisionPrescriptionPatientReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Patient
  type: URI
  identifier: Identifier
  display: String
}

type VisionPrescriptionEncounterReference {
  id: String
  extension: [Extension]
  reference: String
  resource: Encounter
  type: URI
  identifier: Identifier
  display: String
}

union VisionPrescriptionPrescriber = Practitioner | PractitionerRole

type VisionPrescriptionPrescriberReference {
  id: String
  extension: [Extension]
  reference: String
  resource: VisionPrescriptionPrescriber
  type: URI
  identifier: Identifier
  display: String
}

type VisionPrescription implements DomainResource & Resource {
  resourceType: String
  id: ID!
  meta: Meta
  implicitRules: URI
  language: Code
  text: Narrative
  contained: [Resource]
  extension: [Extension]
  modifierExtension: [Extension]
  identifier: [Identifier]
  status: Code
  created: DateTime
  patient: VisionPrescriptionPatientReference
  encounter: VisionPrescriptionEncounterReference
  dateWritten: DateTime
  prescriber: VisionPrescriptionPrescriberReference
  lensSpecification: [VisionPrescriptionLensSpecification]
}

type VisionPrescriptionBundleEntry {
  id: String
  link: [BundleLink]
  fullUrl: URI
  resource: VisionPrescription
  search: BundleSearch
  request: BundleRequest
  response: BundleResponse
}

type VisionPrescriptionBundle {
  id: String
  meta: Meta
  identifier: [Identifier]
  type: Code
  timestamp: Instant
  total: Int
  entry: [VisionPrescriptionBundleEntry]
}

scalar Base64Binary

scalar Canonical

scalar Code

"""
Custom scalar type for date search parameter. Format can be one of YYYY, YYYY-MM, YYYY-MM-DD, YYYY-MM-DDThh:mm:ss+zz:zz or YYYY-MM-DDThh:mm:ssZ
"""
scalar Date

scalar DateTime

"""Decimal custom scalar type"""
scalar Decimal

scalar Instant

scalar Markdown

scalar OID

scalar Time

scalar URI

scalar URL

scalar UUID

scalar XHTML

scalar _FieldSet

scalar _Any

type _Service {
  sdl: String
}

union _Entity = Account | ActivityDefinition | AdministrableProductDefinition | AdverseEvent | AllergyIntolerance | Appointment | AppointmentResponse | AuditEvent | Basic | Binary | BiologicallyDerivedProduct | BodyStructure | Bundle | CapabilityStatement | CarePlan | CareTeam | CatalogEntry | ChargeItem | ChargeItemDefinition | Citation | Claim | ClaimResponse | ClinicalImpression | ClinicalUseDefinition | CodeSystem | Communication | CommunicationRequest | CompartmentDefinition | Composition | ConceptMap | Condition | Consent | Contract | Coverage | CoverageEligibilityRequest | CoverageEligibilityResponse | DetectedIssue | Device | DeviceDefinition | DeviceMetric | DeviceRequest | DeviceUseStatement | DiagnosticReport | DocumentManifest | DocumentReference | Encounter | Endpoint | EnrollmentRequest | EnrollmentResponse | EpisodeOfCare | EventDefinition | Evidence | EvidenceReport | EvidenceVariable | ExampleScenario | ExplanationOfBenefit | FamilyMemberHistory | Flag | Goal | GraphDefinition | Group | GuidanceResponse | HealthcareService | ImagingStudy | Immunization | ImmunizationEvaluation | ImmunizationRecommendation | ImplementationGuide | Ingredient | InsurancePlan | Invoice | Library | Linkage | List | Location | ManufacturedItemDefinition | Measure | MeasureReport | Media | Medication | MedicationAdministration | MedicationDispense | MedicationKnowledge | MedicationRequest | MedicationStatement | MedicinalProductDefinition | MessageDefinition | MessageHeader | MolecularSequence | NamingSystem | NutritionOrder | NutritionProduct | Observation | ObservationDefinition | OperationDefinition | OperationOutcome | Organization | OrganizationAffiliation | PackagedProductDefinition | Parameters | Patient | PaymentNotice | PaymentReconciliation | Person | PlanDefinition | Practitioner | PractitionerRole | Procedure | Provenance | Questionnaire | QuestionnaireResponse | RegulatedAuthorization | RelatedPerson | RequestGroup | ResearchDefinition | ResearchElementDefinition | ResearchStudy | ResearchSubject | RiskAssessment | Schedule | SearchParameter | ServiceRequest | Slot | Specimen | SpecimenDefinition | StructureDefinition | StructureMap | Subscription | SubscriptionStatus | SubscriptionTopic | Substance | SubstanceDefinition | SupplyDelivery | SupplyRequest | Task | TerminologyCapabilities | TestReport | TestScript | ValueSet | VerificationResult | VisionPrescription

'''

        return graphql_schema, "FHIR server graphql schema"

    def _run(self) -> Tuple[str, str]:
        """
        Synchronous version of the tool (falls back to async implementation).

        Raises:
            NotImplementedError: Always raises to enforce async usage
        """
        raise NotImplementedError("Use async version of this tool")
