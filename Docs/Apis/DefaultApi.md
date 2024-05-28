# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**v0Get**](DefaultApi.md#v0Get) | **GET** /v0/ |  |
| [**v0MqGroupMqgroupIdGet**](DefaultApi.md#v0MqGroupMqgroupIdGet) | **GET** /v0/mq-group/{mqgroup_id} |  |
| [**v0MqGroupPost**](DefaultApi.md#v0MqGroupPost) | **POST** /v0/mq-group |  |
| [**v0MqMqidGet**](DefaultApi.md#v0MqMqidGet) | **GET** /v0/mq/{mqid} |  |
| [**v0SchemaOpenapiGet**](DefaultApi.md#v0SchemaOpenapiGet) | **GET** /v0/schema/openapi |  |


<a name="v0Get"></a>
# **v0Get**
> v0Get()



### Parameters
This endpoint does not need any parameter.

### Return type

null (empty response body)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="v0MqGroupMqgroupIdGet"></a>
# **v0MqGroupMqgroupIdGet**
> MQGroupObject v0MqGroupMqgroupIdGet(mqgroup\_id)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **mqgroup\_id** | **String**| the id of the mq group | [default to null] |

### Return type

[**MQGroupObject**](../Models/MQGroupObject.md)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="v0MqGroupPost"></a>
# **v0MqGroupPost**
> _v0_mq_group_post_200_response v0MqGroupPost(body)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **body** | **oas_any_type_not_mapped**|  | [optional] |

### Return type

[**_v0_mq_group_post_200_response**](../Models/_v0_mq_group_post_200_response.md)

### Authorization


### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="v0MqMqidGet"></a>
# **v0MqMqidGet**
> MQProfileObject v0MqMqidGet(mqid)



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

<a name="v0SchemaOpenapiGet"></a>
# **v0SchemaOpenapiGet**
> Object v0SchemaOpenapiGet()



### Parameters
This endpoint does not need any parameter.

### Return type

**Object**

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

