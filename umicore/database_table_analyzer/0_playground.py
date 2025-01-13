from datetime import datetime, timedelta

# Original SQL Server timestamp
ticks = 635242783025000000

# Convert to seconds and adjust for epoch difference
seconds_since_epoch = (ticks - 621355968000000000) / 10_000_000

# Convert to a datetime
timestamp = datetime(1970, 1, 1) + timedelta(seconds=seconds_since_epoch)

print("Converted timestamp:", timestamp)
