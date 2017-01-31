import weddingCountdown

days, hours, minutes, seconds, now = weddingCountdown.get_time_to_wedding()
link = weddingCountdown.pull_pinterest()
message = weddingCountdown.get_message(days, hours, minutes, seconds, link)
error_log = weddingCountdown.send_email(message, now)
weddingCountdown.log(link, error_log)