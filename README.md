<!--- Top of README Badges (automated) --->
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Observation-Management-Service/ewms-message-queue-service?include_prereleases)](https://github.com/Observation-Management-Service/ewms-message-queue-service) [![GitHub issues](https://img.shields.io/github/issues/Observation-Management-Service/ewms-message-queue-service)](https://github.com/Observation-Management-Service/ewms-message-queue-service/issues?q=is%3Aissue+sort%3Aupdated-desc+is%3Aopen) [![GitHub pull requests](https://img.shields.io/github/issues-pr/Observation-Management-Service/ewms-message-queue-service)](https://github.com/Observation-Management-Service/ewms-message-queue-service/pulls?q=is%3Apr+sort%3Aupdated-desc+is%3Aopen)
<!--- End of README Badges (automated) --->

# Message Queue Service

EWMS's Message Queue Service (MQS): The Interface to the DDS's Message Queue Broker
<!--- Top of README Metadata Section (automated) --->

<!--- note: this information is pulled from the pyproject.toml --->

<dl>
    <dt><sub>Keywords</sub></dt>
    <dd><sub>EWMS&nbsp;&nbsp;·&nbsp;&nbsp;task&nbsp;&nbsp;·&nbsp;&nbsp;Workflow Management Service&nbsp;&nbsp;·&nbsp;&nbsp;WIPAC&nbsp;&nbsp;·&nbsp;&nbsp;IceCube&nbsp;&nbsp;·&nbsp;&nbsp;Observation Management Service&nbsp;&nbsp;·&nbsp;&nbsp;Event Workflow Management System</sub></dd>
    <dt><sub>URLs</sub></dt>
    <dd><sub><a href='https://github.com/Observation-Management-Service/ewms-message-queue-service'>Homepage</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href='https://github.com/Observation-Management-Service/ewms-message-queue-service/issues'>Tracker</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href='https://github.com/Observation-Management-Service/ewms-message-queue-service'>Source</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href='https://observation-management-service.github.io/ewms-docs/services/mqs.html'>Documentation</a></sub></dd>
</dl>

<br>
<!--- End of README Metadata Section (automated) --->

## API Documentation

See [Docs/](./Docs)

## Queue Creation

Queue creation (joined as a group of 1+ queues) has two distinct steps: reservation and activation. Queue groups must be
reserved before activation.
