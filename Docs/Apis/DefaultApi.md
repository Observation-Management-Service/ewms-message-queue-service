# DefaultApi


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
> JWKSetResponse GET /mqbroker-issuer/.well-known/jwks.json()



### Parameters
This endpoint does not need any parameter.

### Return type

[**JWKSetResponse**](../Models/JWKSetResponse.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="GET /v1/mqs"></a>
# **GET /v1/mqs**
> Object GET /v1/mqs()



### Parameters
This endpoint does not need any parameter.

### Return type

**Object**

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
| **mqid** | **String**| The ID of the message queue, as found in the MQ profile. | [default to null] |

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
> MQGroupObjectAndProfiles POST /v1/mqs/workflows/{workflow_id}/mq-group/activation(workflow\_id, MQGroupActivationRequest)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **workflow\_id** | **String**| The ID of the EWMS workflow that maps to an MQ group. | [default to null] |
| **MQGroupActivationRequest** | [**MQGroupActivationRequest**](../Models/MQGroupActivationRequest.md)|  | |

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
| **workflow\_id** | **String**| The ID of the EWMS workflow that maps to an MQ group. | [default to null] |

### Return type

[**MQGroupObject**](../Models/MQGroupObject.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="POST /v1/mqs/workflows/{workflow_id}/mq-group/reservation"></a>
# **POST /v1/mqs/workflows/{workflow_id}/mq-group/reservation**
> MQGroupObjectAndProfiles POST /v1/mqs/workflows/{workflow_id}/mq-group/reservation(workflow\_id, MQGroupReservationRequest)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **workflow\_id** | **String**| The ID of the EWMS workflow that maps to an MQ group. | [default to null] |
| **MQGroupReservationRequest** | [**MQGroupReservationRequest**](../Models/MQGroupReservationRequest.md)|  | |

### Return type

[**MQGroupObjectAndProfiles**](../Models/MQGroupObjectAndProfiles.md)

### Authorization


### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="GET /v1/mqs/workflows/{workflow_id}/mq-profiles/public"></a>
# **GET /v1/mqs/workflows/{workflow_id}/mq-profiles/public**
> PublicMQProfilesResponse GET /v1/mqs/workflows/{workflow_id}/mq-profiles/public(workflow\_id)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **workflow\_id** | **String**| The ID of the EWMS workflow that maps to an MQ group. | [default to null] |

### Return type

[**PublicMQProfilesResponse**](../Models/PublicMQProfilesResponse.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

