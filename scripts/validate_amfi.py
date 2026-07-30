# Compare AMFI codes
missing_codes = fund_codes - nav_codes

print("=" * 60)
print("AMFI CODE VALIDATION")
print("=" * 60)

print(f"Total AMFI Codes in Fund Master : {len(fund_codes)}")
print(f"Total AMFI Codes in NAV History : {len(nav_codes)}")

if len(missing_codes) == 0:
    print("\n✅ Validation Successful")
    print("All 40 AMFI codes in Fund Master are present in NAV History.")
else:
    print("\n❌ Missing AMFI Codes:")
    print(missing_codes)
