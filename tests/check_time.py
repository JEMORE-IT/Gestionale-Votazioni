from datetime import datetime, timezone

print(f"Naive now: {datetime.now()}")
print(f"Aware UTC now: {datetime.now(timezone.utc)}")
print(f"Naive type: {type(datetime.now())}")
print(f"Aware type: {type(datetime.now(timezone.utc))}")
