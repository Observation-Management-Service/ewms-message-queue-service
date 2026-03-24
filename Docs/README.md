# Documentation for EWMS Message Queue Service

<a name="documentation-for-api-endpoints"></a>
## Documentation for API Endpoints


| Class | Method | HTTP request | Description |
|------------ | ------------- | ------------- | -------------|
| *DefaultApi* | [_details_](Apis/DefaultApi.md#get-mqbroker-issuer.well-knownjwks.json) | **GET** /mqbroker-issuer/.well-known/jwks.json |  |
*DefaultApi* | [_details_](Apis/DefaultApi.md#get-v1mqs) | **GET** /v1/mqs |  |
*DefaultApi* | [_details_](Apis/DefaultApi.md#get-v1mqsmq-profilesmqid) | **GET** /v1/mqs/mq-profiles/{mqid} |  |
*DefaultApi* | [_details_](Apis/DefaultApi.md#get-v1mqsschemaopenapi) | **GET** /v1/mqs/schema/openapi |  |
*DefaultApi* | [_details_](Apis/DefaultApi.md#post-v1mqsworkflowsworkflow_idmq-groupactivation) | **POST** /v1/mqs/workflows/{workflow_id}/mq-group/activation |  |
*DefaultApi* | [_details_](Apis/DefaultApi.md#get-v1mqsworkflowsworkflow_idmq-group) | **GET** /v1/mqs/workflows/{workflow_id}/mq-group |  |
*DefaultApi* | [_details_](Apis/DefaultApi.md#post-v1mqsworkflowsworkflow_idmq-groupreservation) | **POST** /v1/mqs/workflows/{workflow_id}/mq-group/reservation |  |
*DefaultApi* | [_details_](Apis/DefaultApi.md#get-v1mqsworkflowsworkflow_idmq-profilespublic) | **GET** /v1/mqs/workflows/{workflow_id}/mq-profiles/public |  |


<a name="documentation-for-models"></a>
## Documentation for Models

 - [ErrorResponse](./Models/ErrorResponse.md)
 - [JWKSetResponse](./Models/JWKSetResponse.md)
 - [MQGroupActivationRequest](./Models/MQGroupActivationRequest.md)
 - [MQGroupObject](./Models/MQGroupObject.md)
 - [MQGroupObjectAndProfiles](./Models/MQGroupObjectAndProfiles.md)
 - [MQGroupObject_criteria](./Models/MQGroupObject_criteria.md)
 - [MQGroupReservationRequest](./Models/MQGroupReservationRequest.md)
 - [MQProfileObject](./Models/MQProfileObject.md)
 - [PublicMQProfilesResponse](./Models/PublicMQProfilesResponse.md)
 - [criteria](./Models/criteria.md)


<a name="documentation-for-authorization"></a>
## Documentation for Authorization

