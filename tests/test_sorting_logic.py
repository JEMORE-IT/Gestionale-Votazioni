from datetime import datetime, timedelta

def test_sorting():
    # Simulate the structure returned by list_files
    files = [
        {'name': 'old.xlsx', 'timeLastModified': datetime(2023, 1, 1)},
        {'name': 'new.xlsx', 'timeLastModified': datetime(2023, 12, 31)},
        {'name': 'middle.xlsx', 'timeLastModified': datetime(2023, 6, 15)}
    ]

    print("Original order:")
    for f in files:
        print(f"{f['name']}: {f['timeLastModified']}")

    # Apply the sorting logic
    files.sort(key=lambda x: x['timeLastModified'], reverse=True)

    print("\nSorted order (Newest first):")
    for f in files:
        print(f"{f['name']}: {f['timeLastModified']}")

    # Verification
    assert files[0]['name'] == 'new.xlsx'
    assert files[1]['name'] == 'middle.xlsx'
    assert files[2]['name'] == 'old.xlsx'
    print("\n✅ Sorting verification passed!")

if __name__ == "__main__":
    test_sorting()
