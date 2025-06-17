output sns_topic_arn {
  value       = aws_sns_topic.security_alerts.id
  description = "ARN of the SecurityAlerts SNS Topic"
}
