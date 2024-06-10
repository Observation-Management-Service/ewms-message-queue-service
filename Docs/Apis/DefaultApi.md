# DefaultApi

All URIs are relative to *http://localhost*

| Method                                                                                                       | HTTP request                                              | Description |
|--------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|-------------|
| [**v0Get**](DefaultApi.md#v0Get)                                                                             | **GET** /v0/                                              |             |
| [**v0MqProfileMqidGet**](DefaultApi.md#v0MqProfileMqidGet)                                                   | **GET** /v0/mq-profiles/{mqid}                            |             |
| [**v0SchemaOpenapiGet**](DefaultApi.md#v0SchemaOpenapiGet)                                                   | **GET** /v0/schema/openapi                                |             |
| [**v0WorkflowsWorkflowIdMqGroupActivationPost**](DefaultApi.md#v0WorkflowsWorkflowIdMqGroupActivationPost)   | **POST** /v0/workflows/{workflow_id}/mq-group/activation  |             |
| [**v0WorkflowsWorkflowIdMqGroupGet**](DefaultApi.md#v0WorkflowsWorkflowIdMqGroupGet)                         | **GET** /v0/workflows/{workflow_id}/mq-group              |             |
| [**v0WorkflowsWorkflowIdMqGroupReservationPost**](DefaultApi.md#v0WorkflowsWorkflowIdMqGroupReservationPost) | **POST** /v0/workflows/{workflow_id}/mq-group/reservation |             |

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

<a name="v0MqProfileMqidGet"></a>

# **v0MqProfileMqidGet**

> MQProfileObject v0MqProfileMqidGet(mqid)

### Parameters

| Name     | Type       | Description                                       | Notes             |
|----------|------------|---------------------------------------------------|-------------------|
| **mqid** | **String** | the id of the message queue (found in mq profile) | [default to null] |

### Return type

[**MQProfileObject**](../Models/MQProfileObject.md)

### Authorization

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="v0SchemaOpenapiGet"></a>

# **v0SchemaOpenapiGet**

> Map v0SchemaOpenapiGet()

### Parameters

This endpoint does not need any parameter.

### Return type

[**Map**](../Models/AnyType.md)

### Authorization

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="v0WorkflowsWorkflowIdMqGroupActivationPost"></a>

# **v0WorkflowsWorkflowIdMqGroupActivationPost**

> MQGroupObjectAndProfiles v0WorkflowsWorkflowIdMqGroupActivationPost(workflow\_id, body)

### Parameters

| Name             | Type                        | Description                                          | Notes             |
|------------------|-----------------------------|------------------------------------------------------|-------------------|
| **workflow\_id** | **String**                  | the id of the ewms workflow that maps to an mq group | [default to null] |
| **body**         | **oas_any_type_not_mapped** |                                                      | [optional]        |

### Return type

[**MQGroupObjectAndProfiles**](../Models/MQGroupObjectAndProfiles.md)

### Authorization

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="v0WorkflowsWorkflowIdMqGroupGet"></a>

# **v0WorkflowsWorkflowIdMqGroupGet**

> MQGroupObject v0WorkflowsWorkflowIdMqGroupGet(workflow\_id)

### Parameters

| Name             | Type       | Description                                          | Notes             |
|------------------|------------|------------------------------------------------------|-------------------|
| **workflow\_id** | **String** | the id of the ewms workflow that maps to an mq group | [default to null] |

### Return type

[**MQGroupObject**](../Models/MQGroupObject.md)

### Authorization

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="v0WorkflowsWorkflowIdMqGroupReservationPost"></a>

# **v0WorkflowsWorkflowIdMqGroupReservationPost**

> MQGroupObjectAndProfiles v0WorkflowsWorkflowIdMqGroupReservationPost(workflow\_id, body)

### Parameters

| Name             | Type                        | Description                                          | Notes             |
|------------------|-----------------------------|------------------------------------------------------|-------------------|
| **workflow\_id** | **String**                  | the id of the ewms workflow that maps to an mq group | [default to null] |
| **body**         | **oas_any_type_not_mapped** |                                                      | [optional]        |

### Return type

[**MQGroupObjectAndProfiles**](../Models/MQGroupObjectAndProfiles.md)

### Authorization

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json
