# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**mqGroupMqgroupIdGet**](DefaultApi.md#mqGroupMqgroupIdGet) | **GET** /mq-group/{mqgroup_id} |  |
| [**mqGroupPost**](DefaultApi.md#mqGroupPost) | **POST** /mq-group |  |
| [**mqMqidGet**](DefaultApi.md#mqMqidGet) | **GET** /mq/{mqid} |  |
| [**rootGet**](DefaultApi.md#rootGet) | **GET** / |  |
| [**schemaOpenapiGet**](DefaultApi.md#schemaOpenapiGet) | **GET** /schema/openapi |  |


<a name="mqGroupMqgroupIdGet"></a>
# **mqGroupMqgroupIdGet**
> MQGroupObject mqGroupMqgroupIdGet(mqgroup\_id)



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

<a name="mqGroupPost"></a>
# **mqGroupPost**
> _mq_group_post_200_response mqGroupPost(body)



### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **body** | **MQGroupObject_criteria**|  | [optional] |

### Return type

[**_mq_group_post_200_response**](../Models/_mq_group_post_200_response.md)

### Authorization


### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="mqMqidGet"></a>
# **mqMqidGet**
> MQProfileObject mqMqidGet(mqid)



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

<a name="rootGet"></a>
# **rootGet**
> rootGet()



### Parameters
This endpoint does not need any parameter.

### Return type

null (empty response body)

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="schemaOpenapiGet"></a>
# **schemaOpenapiGet**
> Object schemaOpenapiGet()



### Parameters
This endpoint does not need any parameter.

### Return type

**Object**

### Authorization


### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

