def decode_promo_voucher(voucher_code):
    # Validate type
    if not isinstance(voucher_code, str):
        return "Invalid voucher: input must be a string"

    code = voucher_code.strip()
    parts = code.split('-')

    # Must be exactly PREFIX-NUMBER
    if len(parts) != 2:
        return "Invalid voucher: expected format PREFIX-PERCENT (e.g. EARLY-20)"

    prefix, pct_str = parts[0].strip(), parts[1].strip()
    if not prefix:
        return "Invalid voucher: missing prefix"

    try:
        percentage = int(pct_str)
    except ValueError:
        return "Invalid voucher: percentage must be a whole number"

    if not 0 <= percentage <= 100:
        return "Invalid voucher: percentage must be between 0 and 100"

    return f"Valid {prefix.upper()}: {percentage}% OFF"


def calculate_seat_tier_price(tier_spec):
    if not isinstance(tier_spec, str):
        return "Invalid tier spec: input must be a string"

    parts = tier_spec.split('@')
    if len(parts) != 2:
        return "Invalid tier spec: expected format TIER@ROW (e.g. VIP@4)"

    tier = parts[0].strip().upper()
    tier_rates = {
        "VIP": 150.0,
        "PREMIUM": 90.0,
        "GENERAL": 45.0
    }
    if tier not in tier_rates:
        return "Invalid tier spec: unknown tier"

    try:
        row = int(parts[1])
    except ValueError:
        return "Invalid tier spec: row must be a whole number"

    if not 1 <= row <= 1000:
        return "Invalid tier spec: row must be between 1 and 1000"

    return tier_rates[tier] + (row * 2.0)


def parse_attendee_badge(badge_csv):
    if not isinstance(badge_csv, str):
        return "Invalid badge: input must be a string"

    tokens = badge_csv.split(',')
    if len(tokens) != 3:
        return "Invalid badge: expected format Name,Age,Seat"

    name = tokens[0].strip()
    seat = tokens[2].strip()
    if not name or not seat:
        return "Invalid badge: name and seat cannot be empty"

    try:
        age = int(tokens[1])
    except ValueError:
        return "Invalid badge: age must be a whole number"

    if not 0 <= age <= 120:
        return "Invalid badge: age must be between 0 and 120"

    category = "Child" if age < 18 else "Adult"
    return f"{name} [{category}] - Seat {seat}"


def main():
    print("==== Running decode_promo_voucher ====")
    v_input = input("Enter voucher (e.g. EARLY-20): ")
    print("Voucher:", decode_promo_voucher(v_input))

    print("\n==== Running calculate_seat_tier_price ====")
    t_input = input("Enter tier spec (e.g. VIP@4): ")
    print("Seat Price: $", calculate_seat_tier_price(t_input))

    print("\n==== Running parse_attendee_badge ====")
    b_input = input("Enter badge CSV (Name,Age,Seat): ")
    print("Badge:", parse_attendee_badge(b_input))


if __name__ == "__main__":
    main()