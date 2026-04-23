#!/usr/bin/env python3
"""EasyPost CLI — EasyPost — shipping labels, rate comparison, package tracking, address verification, and insurance.

Zero dependencies beyond Python stdlib.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

API_BASE = "https://api.easypost.com/v2"


def get_env(name):
    val = os.environ.get(name, "")
    if not val:
        env_path = os.path.join(os.environ.get("WORKSPACE", os.path.expanduser("~/.openclaw/workspace")), ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(name + "="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
    return val


def req(method, url, data=None, headers=None, timeout=30):
    body = json.dumps(data).encode() if data else None
    r = urllib.request.Request(url, data=body, method=method)
    r.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            r.add_header(k, v)
    try:
        resp = urllib.request.urlopen(r, timeout=timeout)
        raw = resp.read().decode()
        return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(json.dumps({"error": True, "code": e.code, "message": err}), file=sys.stderr)
        sys.exit(1)


def api(method, path, data=None, params=None):
    """Make authenticated API request."""
    base = API_BASE
    token = get_env("EASYPOST_API_KEY")
    if not token:
        print("Error: EASYPOST_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{base}{path}"
    if params:
        qs = urllib.parse.urlencode({k: v for k, v in params.items() if v}, doseq=True)
        url = f"{url}{'&' if '?' in url else '?'}{qs}"
    return req(method, url, data=data, headers=headers)


def out(data):
    print(json.dumps(data, indent=2, default=str))


def cmd_create_shipment(args):
    """Create shipment & get rates"""
    path = "/shipments"
    data = {}
    if getattr(args, 'from'):
        data["from"] = getattr(args, 'from')
    if args.to:
        data["to"] = args.to
    if args.parcel:
        data["parcel"] = args.parcel
    result = api("POST", path, data=data)
    out(result)

def cmd_get_shipment(args):
    """Get shipment details"""
    path = "/shipments/{id}"
    path = path.replace("{id}", str(args.id))
    result = api("GET", path)
    out(result)

def cmd_list_shipments(args):
    """List shipments"""
    path = "/shipments"
    params = {}
    if args.page_size:
        params["page-size"] = args.page_size
    result = api("GET", path, params=params)
    out(result)

def cmd_buy_shipment(args):
    """Buy label for shipment"""
    path = "/shipments/{id}/buy"
    path = path.replace("{id}", str(args.id))
    data = {}
    if args.rate_id:
        data["rate-id"] = args.rate_id
    result = api("POST", path, data=data)
    out(result)

def cmd_create_tracker(args):
    """Create a tracker"""
    path = "/trackers"
    data = {}
    if args.tracking_code:
        data["tracking-code"] = args.tracking_code
    if args.carrier:
        data["carrier"] = args.carrier
    result = api("POST", path, data=data)
    out(result)

def cmd_get_tracker(args):
    """Get tracker details"""
    path = "/trackers/{id}"
    path = path.replace("{id}", str(args.id))
    result = api("GET", path)
    out(result)

def cmd_list_trackers(args):
    """List trackers"""
    path = "/trackers"
    params = {}
    if args.page_size:
        params["page-size"] = args.page_size
    result = api("GET", path, params=params)
    out(result)

def cmd_verify_address(args):
    """Verify/create address"""
    path = "/addresses"
    data = {}
    if args.street1:
        data["street1"] = args.street1
    if args.city:
        data["city"] = args.city
    if args.state:
        data["state"] = args.state
    if args.zip:
        data["zip"] = args.zip
    if args.country:
        data["country"] = args.country
    result = api("POST", path, data=data)
    out(result)

def cmd_create_insurance(args):
    """Insure a shipment"""
    path = "/insurances"
    data = {}
    if args.shipment_id:
        data["shipment-id"] = args.shipment_id
    if args.amount:
        data["amount"] = args.amount
    result = api("POST", path, data=data)
    out(result)

def cmd_create_refund(args):
    """Refund a label"""
    path = "/refunds"
    data = {}
    if args.carrier:
        data["carrier"] = args.carrier
    if args.tracking_codes:
        data["tracking-codes"] = args.tracking_codes
    result = api("POST", path, data=data)
    out(result)

def cmd_list_rates(args):
    """List rates for shipment"""
    path = "/shipments/{id}/rates"
    path = path.replace("{id}", str(args.id))
    result = api("GET", path)
    out(result)

def cmd_create_return(args):
    """Create return shipment"""
    path = "/shipments"
    data = {}
    if getattr(args, 'from'):
        data["from"] = getattr(args, 'from')
    if args.to:
        data["to"] = args.to
    if args.parcel:
        data["parcel"] = args.parcel
    if args.is_return:
        data["is-return"] = args.is_return
    result = api("POST", path, data=data)
    out(result)


def main():
    parser = argparse.ArgumentParser(description="EasyPost CLI")
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    p_create_shipment = sub.add_parser("create-shipment", help="Create shipment & get rates")
    p_create_shipment.add_argument("--from", dest="from_addr", default="JSON address")
    p_create_shipment.add_argument("--to", default="JSON address")
    p_create_shipment.add_argument("--parcel", default="JSON")
    p_create_shipment.set_defaults(func=cmd_create_shipment)

    p_get_shipment = sub.add_parser("get-shipment", help="Get shipment details")
    p_get_shipment.add_argument("id")
    p_get_shipment.set_defaults(func=cmd_get_shipment)

    p_list_shipments = sub.add_parser("list-shipments", help="List shipments")
    p_list_shipments.add_argument("--page-size", default="20")
    p_list_shipments.set_defaults(func=cmd_list_shipments)

    p_buy_shipment = sub.add_parser("buy-shipment", help="Buy label for shipment")
    p_buy_shipment.add_argument("id")
    p_buy_shipment.add_argument("--rate-id", required=True)
    p_buy_shipment.set_defaults(func=cmd_buy_shipment)

    p_create_tracker = sub.add_parser("create-tracker", help="Create a tracker")
    p_create_tracker.add_argument("--tracking-code", required=True)
    p_create_tracker.add_argument("--carrier", required=True)
    p_create_tracker.set_defaults(func=cmd_create_tracker)

    p_get_tracker = sub.add_parser("get-tracker", help="Get tracker details")
    p_get_tracker.add_argument("id")
    p_get_tracker.set_defaults(func=cmd_get_tracker)

    p_list_trackers = sub.add_parser("list-trackers", help="List trackers")
    p_list_trackers.add_argument("--page-size", default="20")
    p_list_trackers.set_defaults(func=cmd_list_trackers)

    p_verify_address = sub.add_parser("verify-address", help="Verify/create address")
    p_verify_address.add_argument("--street1", required=True)
    p_verify_address.add_argument("--city", required=True)
    p_verify_address.add_argument("--state", required=True)
    p_verify_address.add_argument("--zip", required=True)
    p_verify_address.add_argument("--country", default="US")
    p_verify_address.set_defaults(func=cmd_verify_address)

    p_create_insurance = sub.add_parser("create-insurance", help="Insure a shipment")
    p_create_insurance.add_argument("--shipment-id", required=True)
    p_create_insurance.add_argument("--amount", required=True)
    p_create_insurance.set_defaults(func=cmd_create_insurance)

    p_create_refund = sub.add_parser("create-refund", help="Refund a label")
    p_create_refund.add_argument("--carrier", required=True)
    p_create_refund.add_argument("--tracking-codes", default="comma-separated")
    p_create_refund.set_defaults(func=cmd_create_refund)

    p_list_rates = sub.add_parser("list-rates", help="List rates for shipment")
    p_list_rates.add_argument("id")
    p_list_rates.set_defaults(func=cmd_list_rates)

    p_create_return = sub.add_parser("create-return", help="Create return shipment")
    p_create_return.add_argument("--from", dest="from_addr", default="JSON")
    p_create_return.add_argument("--to", default="JSON")
    p_create_return.add_argument("--parcel", default="JSON")
    p_create_return.add_argument("--is-return", default="true")
    p_create_return.set_defaults(func=cmd_create_return)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
