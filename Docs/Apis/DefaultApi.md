# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**mqbrokerIssuerWellKnownJwksJsonGet**](DefaultApi.md#mqbrokerIssuerWellKnownJwksJsonGet) | **GET** /mqbroker-issuer/.well-known/jwks.json |  |
| [**v1MqsGet**](DefaultApi.md#v1MqsGet) | **GET** /v1/mqs |  |
| [**v1MqsMqProfilesMqidGet**](DefaultApi.md#v1MqsMqProfilesMqidGet) | **GET** /v1/mqs/mq-profiles/{mqid} |  |
| [**v1MqsSchemaOpenapiGet**](DefaultApi.md#v1MqsSchemaOpenapiGet) | **GET** /v1/mqs/schema/openapi |  |
| [**v1MqsWorkflowsWorkflowIdMqGroupActivationPost**](DefaultApi.md#v1MqsWorkflowsWorkflowIdMqGroupActivationPost) | **POST** /v1/mqs/workflows/{workflow_id}/mq-group/activation |  |
| [**v1MqsWorkflowsWorkflowIdMqGroupGet**](DefaultApi.md#v1MqsWorkflowsWorkflowIdMqGroupGet) | **GET** /v1/mqs/workflows/{workflow_id}/mq-group |  |
| [**v1MqsWorkflowsWorkflowIdMqGroupReservationPost**](DefaultApi.md#v1MqsWorkflowsWorkflowIdMqGroupReservationPost) | **POST** /v1/mqs/workflows/{workflow_id}/mq-group/reservation |  |
| [**v1MqsWorkflowsWorkflowIdMqProfilesPublicGet**](DefaultApi.md#v1MqsWorkflowsWorkflowIdMqProfilesPublicGet) | **GET** /v1/mqs/workflows/{workflow_id}/mq-profiles/public |  |


<a name="mqbrokerIssuerWellKnownJwksJsonGet"></a>
# **mqbrokerIssuerWellKnownJwksJsonGet**
> _mqbroker_issuer__well_known_jwks_json_get_200_response mqbrokerIssuerWellKnownJwksJsonGet()



### Parameters
This endpoint does not need any parameter.

### Return type

[**_mqbroker_issuer__well_known_jwks_json_get_200_response**](../Models/_mqbroker_issuer__well_known_jwks_json_get_200_response.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="v1MqsGet"></a>
# **v1MqsGet**
> v1MqsGet()



### Parameters
This endpoint does not need any parameter.

### Return type

null (empty response body)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="v1MqsMqProfilesMqidGet"></a>
# **v1MqsMqProfilesMqidGet**
> MQProfileObject v1MqsMqProfilesMqidGet(mqid)



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

<a name="v1MqsSchemaOpenapiGet"></a>
# **v1MqsSchemaOpenapiGet**
> Map v1MqsSchemaOpenapiGet()



### Parameters
This endpoint does not need any parameter.

### Return type

[**Map**](../Models/AnyType.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="v1MqsWorkflowsWorkflowIdMqGroupActivationPost"></a>
# **v1MqsWorkflowsWorkflowIdMqGroupActivationPost**
> MQGroupObjectAndProfiles v1MqsWorkflowsWorkflowIdMqGroupActivationPost(workflow\_id, body)



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

<a name="v1MqsWorkflowsWorkflowIdMqGroupGet"></a>
# **v1MqsWorkflowsWorkflowIdMqGroupGet**
> MQGroupObject v1MqsWorkflowsWorkflowIdMqGroupGet(workflow\_id)



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

<a name="v1MqsWorkflowsWorkflowIdMqGroupReservationPost"></a>
# **v1MqsWorkflowsWorkflowIdMqGroupReservationPost**
> MQGroupObjectAndProfiles v1MqsWorkflowsWorkflowIdMqGroupReservationPost(workflow\_id, body)



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

<a name="v1MqsWorkflowsWorkflowIdMqProfilesPublicGet"></a>
# **v1MqsWorkflowsWorkflowIdMqProfilesPublicGet**
> oas_any_type_not_mapped v1MqsWorkflowsWorkflowIdMqProfilesPublicGet(workflow\_id)



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

