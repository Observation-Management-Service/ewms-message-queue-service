# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**v0MqsGet**](DefaultApi.md#v0MqsGet) | **GET** /v0/mqs |  |
| [**v0MqsMqProfilesMqidGet**](DefaultApi.md#v0MqsMqProfilesMqidGet) | **GET** /v0/mqs/mq-profiles/{mqid} |  |
| [**v0MqsSchemaOpenapiGet**](DefaultApi.md#v0MqsSchemaOpenapiGet) | **GET** /v0/mqs/schema/openapi |  |
| [**v0MqsWorkflowsWorkflowIdMqGroupActivationPost**](DefaultApi.md#v0MqsWorkflowsWorkflowIdMqGroupActivationPost) | **POST** /v0/mqs/workflows/{workflow_id}/mq-group/activation |  |
| [**v0MqsWorkflowsWorkflowIdMqGroupGet**](DefaultApi.md#v0MqsWorkflowsWorkflowIdMqGroupGet) | **GET** /v0/mqs/workflows/{workflow_id}/mq-group |  |
| [**v0MqsWorkflowsWorkflowIdMqGroupReservationPost**](DefaultApi.md#v0MqsWorkflowsWorkflowIdMqGroupReservationPost) | **POST** /v0/mqs/workflows/{workflow_id}/mq-group/reservation |  |
| [**v0MqsWorkflowsWorkflowIdMqProfilesPublicGet**](DefaultApi.md#v0MqsWorkflowsWorkflowIdMqProfilesPublicGet) | **GET** /v0/mqs/workflows/{workflow_id}/mq-profiles/public |  |
| [**wellKnownJwksJsonGet**](DefaultApi.md#wellKnownJwksJsonGet) | **GET** /.well-known/jwks.json |  |


<a name="v0MqsGet"></a>
# **v0MqsGet**
> v0MqsGet()



### Parameters
This endpoint does not need any parameter.

### Return type

null (empty response body)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="v0MqsMqProfilesMqidGet"></a>
# **v0MqsMqProfilesMqidGet**
> MQProfileObject v0MqsMqProfilesMqidGet(mqid)



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

<a name="v0MqsSchemaOpenapiGet"></a>
# **v0MqsSchemaOpenapiGet**
> Map v0MqsSchemaOpenapiGet()



### Parameters
This endpoint does not need any parameter.

### Return type

[**Map**](../Models/AnyType.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="v0MqsWorkflowsWorkflowIdMqGroupActivationPost"></a>
# **v0MqsWorkflowsWorkflowIdMqGroupActivationPost**
> MQGroupObjectAndProfiles v0MqsWorkflowsWorkflowIdMqGroupActivationPost(workflow\_id, body)



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

<a name="v0MqsWorkflowsWorkflowIdMqGroupGet"></a>
# **v0MqsWorkflowsWorkflowIdMqGroupGet**
> MQGroupObject v0MqsWorkflowsWorkflowIdMqGroupGet(workflow\_id)



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

<a name="v0MqsWorkflowsWorkflowIdMqGroupReservationPost"></a>
# **v0MqsWorkflowsWorkflowIdMqGroupReservationPost**
> MQGroupObjectAndProfiles v0MqsWorkflowsWorkflowIdMqGroupReservationPost(workflow\_id, body)



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

<a name="v0MqsWorkflowsWorkflowIdMqProfilesPublicGet"></a>
# **v0MqsWorkflowsWorkflowIdMqProfilesPublicGet**
> oas_any_type_not_mapped v0MqsWorkflowsWorkflowIdMqProfilesPublicGet(workflow\_id)



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

<a name="wellKnownJwksJsonGet"></a>
# **wellKnownJwksJsonGet**
> _well_known_jwks_json_get_200_response wellKnownJwksJsonGet()



### Parameters
This endpoint does not need any parameter.

### Return type

[**_well_known_jwks_json_get_200_response**](../Models/_well_known_jwks_json_get_200_response.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

