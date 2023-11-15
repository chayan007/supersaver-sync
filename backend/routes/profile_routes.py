import json

from fastapi import APIRouter, HTTPException
from starlette import status

from dependencies.constants import SuperSaverSyncConstants
from dependencies.logger import logger

profile_router = APIRouter()


@profile_router.get("/linked-banks")
def get_linked_banks(mobile: str):
    try:
        aa_file = open(f"data/aa_data/{mobile}.json", mode='rb')
        aa_report = json.load(aa_file)

        bank_identifiers = aa_report.keys()
        linked_banks = []

        for bank_identifier in bank_identifiers:
            linked_banks.append({
                "bank_name": SuperSaverSyncConstants.BANK_IDENTIFIER_MAPPING[bank_identifier][0],
                "bank_account": aa_report[bank_identifier][0].get('masked_account'),
                "bank_identifier": bank_identifier,
                "bank_logo": SuperSaverSyncConstants.BANK_IDENTIFIER_MAPPING[bank_identifier][1]
            })

        return linked_banks

    except Exception:
        logger.exception("Find traceback below")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SuperSaverSyncConstants.INTERNAL_ERROR_JSON,
        )


@profile_router.get("/transactions")
def get_transactions(mobile: str, bank_identifier: str, page: int):
    try:
        aa_file = open(f"data/aa_data/{mobile}.json", mode='rb')
        aa_report = json.load(aa_file)

        bank_data = aa_report[bank_identifier][0]
        transaction_list = bank_data['decrypted_data']['Account']['Transactions']['Transaction']

        offset = (page - 1) * SuperSaverSyncConstants.DEFAULT_PAGE_SIZE
        limit = offset + SuperSaverSyncConstants.DEFAULT_PAGE_SIZE
        return transaction_list[offset:limit]

    except Exception:
        logger.exception("Find traceback below")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SuperSaverSyncConstants.INTERNAL_ERROR_JSON,
        )


@profile_router.get("/history")
def get_transactions(mobile: str, bank_identifier: str, page: int):
    try:
        aa_file = open(f"data/aa_data/{mobile}.json", mode='rb')
        aa_report = json.load(aa_file)

        bank_data = aa_report[bank_identifier][0]
        transaction_list = bank_data['decrypted_data']['Account']['Transactions']['Transaction']

        offset = (page - 1) * SuperSaverSyncConstants.DEFAULT_PAGE_SIZE
        limit = offset + SuperSaverSyncConstants.DEFAULT_PAGE_SIZE
        return transaction_list[offset:limit]

    except Exception:
        logger.exception("Find traceback below")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SuperSaverSyncConstants.INTERNAL_ERROR_JSON,
        )
