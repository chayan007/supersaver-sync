import json

from fastapi import APIRouter, HTTPException
from starlette import status

from dependencies.constants import SuperSaverSyncConstants
from dependencies.logger import logger

dashboard_router = APIRouter()


@dashboard_router.get("/assets")
def get_assets(mobile: str):
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


@dashboard_router.get("/liabilities")
def get_liabilities(mobile: str):
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
