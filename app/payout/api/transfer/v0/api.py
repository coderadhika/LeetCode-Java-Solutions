from typing import List, Optional

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.payout.repository.maindb.model import stripe_transfer
from app.payout.service import TransferRepository, TransferRepositoryInterface
from app.commons.api.models import PaymentException, PaymentErrorResponseBody
from app.payout.api.response import Acknowledgement
from app.payout.api.transfer.v0.models import (
    StripeTransfer,
    StripeTransferCreate,
    StripeTransferUpdate,
)
from app.payout.repository.maindb.model.transfer import (
    Transfer,
    TransferCreate,
    TransferUpdate,
)

api_tags = ["TransfersV0"]
router = APIRouter()


@router.post(
    "/",
    status_code=HTTP_201_CREATED,
    response_model=Transfer,
    operation_id="CreateTransfer",
    tags=api_tags,
)
async def create_transfer(
    data: TransferCreate,
    repository: TransferRepositoryInterface = Depends(TransferRepository),
):
    return await repository.create_transfer(data=data)


@router.get(
    "/{transfer_id}",
    response_model=Transfer,
    status_code=HTTP_200_OK,
    responses={HTTP_404_NOT_FOUND: {"model": PaymentErrorResponseBody}},
    operation_id="GetTransferById",
    tags=api_tags,
)
async def get_transfer_by_id(
    transfer_id: int,
    repository: TransferRepositoryInterface = Depends(TransferRepository),
):
    transfer = await repository.get_transfer_by_id(transfer_id=transfer_id)
    if not transfer:
        raise _transfer_not_found()

    return transfer


@router.patch(
    "/{transfer_id}",
    response_model=Transfer,
    status_code=HTTP_200_OK,
    responses={HTTP_404_NOT_FOUND: {"model": PaymentErrorResponseBody}},
    operation_id="UpdateTransferById",
    tags=api_tags,
)
async def update_transfer_by_id(
    transfer_id: int,
    data: TransferUpdate,
    repository: TransferRepositoryInterface = Depends(TransferRepository),
):
    updated_transfer = await repository.update_transfer_by_id(
        transfer_id=transfer_id, data=data
    )

    if not updated_transfer:
        raise _transfer_not_found()

    return updated_transfer


@router.post(
    "/stripe/",
    status_code=HTTP_201_CREATED,
    response_model=StripeTransfer,
    operation_id="CreateStripeTransfer",
    tags=api_tags,
)
async def create_stripe_transfer(
    data: StripeTransferCreate,
    repository: TransferRepositoryInterface = Depends(TransferRepository),
):
    internal_request = stripe_transfer.StripeTransferCreate(
        **data.dict(skip_defaults=True)
    )
    internal_stripe_transfer = await repository.create_stripe_transfer(
        data=internal_request
    )
    return StripeTransfer(**internal_stripe_transfer.dict())


@router.get(
    "/stripe/_get-by-stripe-id",
    status_code=HTTP_200_OK,
    response_model=Optional[StripeTransfer],
    operation_id="GetStripeTransferByStripeId",
    tags=api_tags,
)
async def get_stripe_transfer_by_stripe_id(
    stripe_id: str,
    repository: TransferRepositoryInterface = Depends(TransferRepository),
):
    internal_stripe_transfer = await repository.get_stripe_transfer_by_stripe_id(
        stripe_id=stripe_id
    )
    return (
        StripeTransfer(**internal_stripe_transfer.dict())
        if internal_stripe_transfer
        else None
    )


@router.get(
    "/stripe/_get-by-transfer-id",
    status_code=HTTP_200_OK,
    response_model=List[StripeTransfer],
    operation_id="GetStripeTransfersByTransferId",
    tags=api_tags,
)
async def get_stripe_transfer_by_transfer_id(
    transfer_id: int,
    repository: TransferRepositoryInterface = Depends(TransferRepository),
):
    internal_stripe_transfers = await repository.get_stripe_transfers_by_transfer_id(
        transfer_id=transfer_id
    )
    return [
        StripeTransfer(**internal_stripe_transfer.dict())
        for internal_stripe_transfer in internal_stripe_transfers
    ]


@router.get(
    "/stripe/{stripe_transfer_id}",
    response_model=StripeTransfer,
    status_code=HTTP_200_OK,
    responses={HTTP_404_NOT_FOUND: {"model": PaymentErrorResponseBody}},
    operation_id="GetStripeTransferById",
    tags=api_tags,
)
async def get_stripe_transfer_by_id(
    stripe_transfer_id: int,
    repository: TransferRepositoryInterface = Depends(TransferRepository),
):
    internal_stripe_transfer = await repository.get_stripe_transfer_by_id(
        stripe_transfer_id=stripe_transfer_id
    )

    if not internal_stripe_transfer:
        raise _stripe_transfer_not_found()

    return StripeTransfer(**internal_stripe_transfer.dict())


@router.patch(
    "/stripe/{stripe_transfer_id}",
    response_model=StripeTransfer,
    status_code=HTTP_200_OK,
    responses={HTTP_404_NOT_FOUND: {"model": PaymentErrorResponseBody}},
    operation_id="UpdateStripeTransferById",
    tags=api_tags,
)
async def update_stripe_transfer_by_id(
    stripe_transfer_id: int,
    body: StripeTransferUpdate,
    repository: TransferRepositoryInterface = Depends(TransferRepository),
) -> Optional[StripeTransfer]:

    internal_request = stripe_transfer.StripeTransferUpdate(
        **body.dict(skip_defaults=True)
    )

    internal_stripe_transfer = await repository.update_stripe_transfer_by_id(
        stripe_transfer_id=stripe_transfer_id, data=internal_request
    )

    if not internal_stripe_transfer:
        raise _stripe_transfer_not_found()

    return StripeTransfer(**internal_stripe_transfer.dict())


@router.delete(
    "/stripe/_delete-by-stripe-id",
    status_code=HTTP_200_OK,
    response_model=Acknowledgement,
    operation_id="DeleteStripeTransferByStripeId",
    tags=api_tags,
)
async def delete_stripe_transfer_by_stripe_id(
    stripe_id: str,
    repository: TransferRepositoryInterface = Depends(TransferRepository),
):
    await repository.delete_stripe_transfer_by_stripe_id(stripe_id=stripe_id)
    return Acknowledgement()


def _transfer_not_found() -> PaymentException:
    return PaymentException(
        http_status_code=HTTP_404_NOT_FOUND,
        error_code="transfer_not_found",  # not formalize error code yet
        error_message="transfer not found",
        retryable=False,
    )


def _stripe_transfer_not_found() -> PaymentException:
    return PaymentException(
        http_status_code=HTTP_404_NOT_FOUND,
        error_code="stripe_transfer_not_found",  # not formalize error code yet
        error_message="stripe transfer not found",
        retryable=False,
    )
