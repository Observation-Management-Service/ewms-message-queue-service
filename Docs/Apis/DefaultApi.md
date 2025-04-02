# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [_details_](DefaultApi.md#get-mqbroker-issuer.well-knownjwks.json) | **GET** /mqbroker-issuer/.well-known/jwks.json |  |
| [_details_](DefaultApi.md#get-v1mqs) | **GET** /v1/mqs |  |
| [_details_](DefaultApi.md#get-v1mqsmq-profilesmqid) | **GET** /v1/mqs/mq-profiles/{mqid} |  |
| [_details_](DefaultApi.md#get-v1mqsschemaopenapi) | **GET** /v1/mqs/schema/openapi |  |
| [_details_](DefaultApi.md#post-v1mqsworkflowsworkflow_idmq-groupactivation) | **POST** /v1/mqs/workflows/{workflow_id}/mq-group/activation |  |
| [_details_](DefaultApi.md#get-v1mqsworkflowsworkflow_idmq-group) | **GET** /v1/mqs/workflows/{workflow_id}/mq-group |  |
| [_details_](DefaultApi.md#post-v1mqsworkflowsworkflow_idmq-groupreservation) | **POST** /v1/mqs/workflows/{workflow_id}/mq-group/reservation |  |
| [_details_](DefaultApi.md#get-v1mqsworkflowsworkflow_idmq-profilespublic) | **GET** /v1/mqs/workflows/{workflow_id}/mq-profiles/public |  |


<a name="GET /mqbroker-issuer/.well-known/jwks.json"></a>
# **GET /mqbroker-issuer/.well-known/jwks.json**
> _mqbroker_issuer__well_known_jwks_json_get_200_response GET /mqbroker-issuer/.well-known/jwks.json()



### Parameters
This endpoint does not need any parameter.

### Return type

[**_mqbroker_issuer__well_known_jwks_json_get_200_response**](../Models/_mqbroker_issuer__well_known_jwks_json_get_200_response.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="GET /v1/mqs"></a>
# **GET /v1/mqs**
> GET /v1/mqs()



### Parameters
This endpoint does not need any parameter.

### Return type

null (empty response body)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="GET /v1/mqs/mq-profiles/{mqid}"></a>
# **GET /v1/mqs/mq-profiles/{mqid}**
> MQProfileObject GET /v1/mqs/mq-profiles/{mqid}(mqid)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **mqid** | **String**| the id of the message queue (found in mq profile) | [default to null] |

### Return type

[**MQProfileObject**](../Models/MQProfileObject.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="GET /v1/mqs/schema/openapi"></a>
# **GET /v1/mqs/schema/openapi**
> Map GET /v1/mqs/schema/openapi()



### Parameters
This endpoint does not need any parameter.

### Return type

[**Map**](../Models/AnyType.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="POST /v1/mqs/workflows/{workflow_id}/mq-group/activation"></a>
# **POST /v1/mqs/workflows/{workflow_id}/mq-group/activation**
> MQGroupObjectAndProfiles POST /v1/mqs/workflows/{workflow_id}/mq-group/activation(workflow\_id, body)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **workflow\_id** | **String**| the id of the ewms workflow that maps to an mq group | [default to null] |
| **body** | **oas_any_type_not_mapped**|  | [optional] |

### Return type

[**MQGroupObjectAndProfiles**](../Models/MQGroupObjectAndProfiles.md)

### Authorization


### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="GET /v1/mqs/workflows/{workflow_id}/mq-group"></a>
# **GET /v1/mqs/workflows/{workflow_id}/mq-group**
> MQGroupObject GET /v1/mqs/workflows/{workflow_id}/mq-group(workflow\_id)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **workflow\_id** | **String**| the id of the ewms workflow that maps to an mq group | [default to null] |

### Return type

[**MQGroupObject**](../Models/MQGroupObject.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="POST /v1/mqs/workflows/{workflow_id}/mq-group/reservation"></a>
# **POST /v1/mqs/workflows/{workflow_id}/mq-group/reservation**
> MQGroupObjectAndProfiles POST /v1/mqs/workflows/{workflow_id}/mq-group/reservation(workflow\_id, body)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **workflow\_id** | **String**| the id of the ewms workflow that maps to an mq group | [default to null] |
| **body** | **oas_any_type_not_mapped**|  | [optional] |

### Return type

[**MQGroupObjectAndProfiles**](../Models/MQGroupObjectAndProfiles.md)

### Authorization


### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="GET /v1/mqs/workflows/{workflow_id}/mq-profiles/public"></a>
# **GET /v1/mqs/workflows/{workflow_id}/mq-profiles/public**
> oas_any_type_not_mapped GET /v1/mqs/workflows/{workflow_id}/mq-profiles/public(workflow\_id)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **workflow\_id** | **String**| the id of the ewms workflow that maps to an mq group | [default to null] |

### Return type

[**oas_any_type_not_mapped**](../Models/AnyType.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

