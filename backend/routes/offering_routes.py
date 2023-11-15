import json

from fastapi import APIRouter, HTTPException
from starlette import status

from dependencies.constants import SuperSaverSyncConstants
from dependencies.logger import logger

offering_router = APIRouter()


@offering_router.get("/coupons")
def get_coupons(mobile: str):
    try:
        coupon_file = open(f"data/mocked_data/coupon.json", mode='rb')
        coupon_list = json.load(coupon_file)
        return coupon_list

    except Exception:
        logger.exception("Find traceback below")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SuperSaverSyncConstants.INTERNAL_ERROR_JSON,
        )


@offering_router.get("/credit_cards")
def get_credit_cards(mobile: str):
    try:
        cc_file = open(f"data/mocked_data/coupon.json", mode='rb')
        cc_list = json.load(cc_file)
        return cc_list

    except Exception:
        logger.exception("Find traceback below")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SuperSaverSyncConstants.INTERNAL_ERROR_JSON,
        )
