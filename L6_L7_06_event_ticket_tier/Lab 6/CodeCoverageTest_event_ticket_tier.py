import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


def make(tier="general", orders=None, confirmed=True, lounge=False):
    return {
        "is_confirmed": confirmed,
        "tier": tier,
        "exclusive_lounge": lounge,
        "orders": orders if orders is not None else [],
    }


# ---------- Starter test ----------
def test_single_general_order():
    manifests = [make("general", [{"qty": 2, "promo": ""}])]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["total_revenue"] == 99.0
    assert result["status"] == "COMPLETED"


# ---------- Validation (line 3) ----------
def test_invalid_manifests_not_list():
    with pytest.raises(ValueError):
        process_ticket_manifest("not a list", 0.1)


def test_invalid_negative_tax():
    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)


# ---------- Manifest-level lines ----------
def test_unconfirmed_manifest_skipped():
    result = process_ticket_manifest([make(orders=[{"qty": 2}], confirmed=False)], 0.1)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_default_tier_is_general():
    # manifest with no "tier" key -> defaults to general (45.0)
    manifests = [{"is_confirmed": True, "orders": [{"qty": 1}]}]
    result = process_ticket_manifest(manifests, 0.0)
    assert result["total_revenue"] == 45.0


def test_premium_tier():
    result = process_ticket_manifest([make("premium", [{"qty": 2}])], 0.0)
    assert result["total_revenue"] == 180.0
    assert result["status"] == "COMPLETED"


def test_vip_tier():
    result = process_ticket_manifest([make("vip", [{"qty": 1}])], 0.0)
    assert result["total_revenue"] == 150.0


def test_unknown_tier_rejected():
    result = process_ticket_manifest([make("platinum", [{"qty": 2}])], 0.1)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# ---------- Order-level lines ----------
def test_zero_qty_rejected():
    result = process_ticket_manifest([make("general", [{"qty": 0}])], 0.0)
    assert result["status"] == "ZERO_SALES"


def test_earlybird_discount():
    result = process_ticket_manifest([make("general", [{"qty": 2, "promo": "EARLYBIRD"}])], 0.0)
    assert result["total_revenue"] == 72.0  # 2*45*0.8


def test_bulk_discount_five_or_more():
    result = process_ticket_manifest([make("general", [{"qty": 5}])], 0.0)
    assert result["total_revenue"] == 205.0  # 5*45 - 20


def test_vip_fraud_risk_wipes_manifest():
    orders = [{"qty": 1, "promo": ""}, {"qty": 2, "promo": "FRAUD_RISK"}]
    result = process_ticket_manifest([make("vip", orders)], 0.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_exclusive_lounge_fee():
    result = process_ticket_manifest([make("general", [{"qty": 1}], lounge=True)], 0.0)
    assert result["total_revenue"] == 120.0  # 45 + 75


# ---------- Final status ----------
def test_audit_rejected_more_than_four_rejections():
    orders = [{"qty": 0}] * 5 + [{"qty": 1}]
    result = process_ticket_manifest([make("general", orders)], 0.0)
    assert result["status"] == "AUDIT_REJECTED"
    assert result["total_revenue"] == 45.0


# ---------- monitor_gate_flow ----------
def test_gate_no_data():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_gate_overflow():
    assert monitor_gate_flow([[10, 60, 70]]) == "OVERFLOW"


def test_gate_flow_normal():
    assert monitor_gate_flow([[10, 60, 20, 60, 20]]) == "FLOW_NORMAL"
