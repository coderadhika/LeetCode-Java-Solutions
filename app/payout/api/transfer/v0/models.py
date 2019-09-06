from datetime import datetime
from typing import Optional

from app.commons.api.models import PaymentResponse, PaymentRequest

# Dummy v0 api models copied directly from db domain models. Just to make sure v0 API signature is stable
# even if underlying db model changes, so we don't need to worry about DSJ v0 integration


class StripeTransfer(PaymentResponse):
    id: int
    created_at: datetime
    transfer_id: int
    stripe_status: str
    stripe_id: Optional[str]
    stripe_request_id: Optional[str]
    stripe_failure_code: Optional[str]
    stripe_account_id: Optional[str]
    stripe_account_type: Optional[str]
    country_shortname: Optional[str]
    bank_last_four: Optional[str]
    bank_name: Optional[str]
    submission_error_code: Optional[str]
    submission_error_type: Optional[str]
    submission_status: Optional[str]
    submitted_at: Optional[datetime]


class StripeTransferCreate(PaymentRequest):
    transfer_id: int
    stripe_status: str
    stripe_id: Optional[str]
    stripe_request_id: Optional[str]
    stripe_failure_code: Optional[str]
    stripe_account_id: Optional[str]
    stripe_account_type: Optional[str]
    country_shortname: Optional[str]
    bank_last_four: Optional[str]
    bank_name: Optional[str]
    submission_error_code: Optional[str]
    submission_error_type: Optional[str]
    submission_status: Optional[str]
    submitted_at: Optional[datetime]


class StripeTransferUpdate(PaymentRequest):
    stripe_id: Optional[str]
    stripe_request_id: Optional[str]
    stripe_failure_code: Optional[str]
    stripe_account_id: Optional[str]
    stripe_account_type: Optional[str]
    country_shortname: Optional[str]
    bank_last_four: Optional[str]
    bank_name: Optional[str]
    submission_error_code: Optional[str]
    submission_error_type: Optional[str]
    submission_status: Optional[str]
    submitted_at: Optional[datetime]
    stripe_status: Optional[str]
    transfer_id: Optional[int]
