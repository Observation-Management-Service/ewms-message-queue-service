<!--- Top of README Badges (automated) --->
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Observation-Management-Service/ewms-message-queue-service?include_prereleases)](https://github.com/Observation-Management-Service/ewms-message-queue-service/) [![GitHub issues](https://img.shields.io/github/issues/Observation-Management-Service/ewms-message-queue-service)](https://github.com/Observation-Management-Service/ewms-message-queue-service/issues?q=is%3Aissue+sort%3Aupdated-desc+is%3Aopen) [![GitHub pull requests](https://img.shields.io/github/issues-pr/Observation-Management-Service/ewms-message-queue-service)](https://github.com/Observation-Management-Service/ewms-message-queue-service/pulls?q=is%3Apr+sort%3Aupdated-desc+is%3Aopen)
<!--- End of README Badges (automated) --->

# ewms-message-queue-service v1

EWMS's Message Queue Service (MQS): The Interface to the DDS's Message Queue Broker

## API Documentation

See [Docs/](./Docs)

## Queue Creation

Queue creation (joined as a group of 1+ queues) has two distinct steps: reservation and activation. Queue groups must be
reserved before activation.
