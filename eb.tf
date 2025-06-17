resource "aws_cloudwatch_event_rule" "daily_check" {
    name                = "DailySecurityCheck"
    schedule_expression = "cron(0 7 * * ? *)" # 5PM AEST (UTC+10)
}
resource "aws_cloudwatch_event_target" "lambda_target" {
    rule      = aws_cloudwatch_event_rule.daily_check.name
    target_id = "CheckLambda"
    arn       = aws_lambda_function.security_checker.arn
}
resource "aws_lambda_permission" "allow_eventbridge" {
    statement_id  = "AllowExecutionFromEventbridge"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.security_checker.function_name
    principal     = "events.amazonaws.com"
    source_arn    = aws_cloudwatch_event_rule.daily_check.arn
}