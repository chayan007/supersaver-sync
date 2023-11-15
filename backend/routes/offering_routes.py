import json

from fastapi import APIRouter, HTTPException
from starlette import status

from dependencies.constants import SuperSaverSyncConstants
from dependencies.logger import logger

offering_router = APIRouter()


@offering_router.get("/coupons/actual")
def get_coupons(mobile: str):
    try:
        coupon_file = open(f"data/mocked_data/coupon.json", mode='rb')
        coupon_list = json.load(coupon_file)

        vendors_file = open(f"data/ml_data/{mobile}/vendor.json")
        vendor_data = json.load(vendors_file)

        actual_vendor_set = set()
        for vendor_datum in vendor_data:
            actual_vendor_set.add(vendor_datum['vendor'])

        logger.info(f"Retrieved Vendors: {actual_vendor_set}")
        compiled_coupon_set = set()
        for coupon in coupon_list:
            if coupon['target_vendor'] in actual_vendor_set:
                compiled_coupon_set.add(coupon)

        return list(compiled_coupon_set)

    except Exception:
        logger.exception("Find traceback below")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SuperSaverSyncConstants.INTERNAL_ERROR_JSON,
        )


@offering_router.get("/coupons/alternate")
def get_coupons(mobile: str):
    try:
        coupon_file = open(f"data/mocked_data/coupon.json", mode='rb')
        coupon_list = json.load(coupon_file)

        vendors_file = open(f"data/ml_data/{mobile}/vendor.json")
        vendor_data = json.load(vendors_file)

        alternate_vendor_set = set()
        for vendor_datum in vendor_data:
            alternate_vendor_set.add(vendor_datum['vendor'])

        logger.info(f"Retrieved Vendors: {alternate_vendor_set}")
        compiled_coupon_set = set()
        for coupon in coupon_list:
            if any(vendor in coupon['alternate_vendors'] for vendor in alternate_vendor_set):
                compiled_coupon_set.add(coupon)

        return list(compiled_coupon_set)

    except Exception:
        logger.exception("Find traceback below")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SuperSaverSyncConstants.INTERNAL_ERROR_JSON,
        )


@offering_router.get("/credit_cards")
def get_credit_cards(mobile: str):
    try:
        cc_file = open(f"data/mocked_data/credit_card.json", mode='rb')
        cc_list = json.load(cc_file)

        vendors_file = open(f"data/ml_data/{mobile}/vendor.json")
        vendor_data = json.load(vendors_file)

        vendor_set = set()
        for vendor_datum in vendor_data:
            vendor_set.add(vendor_datum['vendor'])

        logger.info(f"Retrieved Vendors: {vendor_set}")
        compiled_cc_set = set()
        for cc in cc_list:
            if (
                    any(vendor in cc['alternate_vendors'] for vendor in vendor_set) or
                    cc['target_vendor'] in vendor_set
            ):
                compiled_cc_set.add(cc)

        return list(compiled_cc_set)

    except Exception:
        logger.exception("Find traceback below")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SuperSaverSyncConstants.INTERNAL_ERROR_JSON,
        )
