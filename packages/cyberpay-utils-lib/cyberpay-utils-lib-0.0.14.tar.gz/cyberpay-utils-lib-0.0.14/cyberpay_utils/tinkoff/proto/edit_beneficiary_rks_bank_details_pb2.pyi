from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EditBeneficiaryRksBankDetailsRequest(_message.Message):
    __slots__ = ["account_number", "bank_details_id", "bank_name", "beneficiary_id", "bik", "corr_account_number", "inn", "is_default", "kpp", "name", "type"]
    ACCOUNT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    BANK_DETAILS_ID_FIELD_NUMBER: _ClassVar[int]
    BANK_NAME_FIELD_NUMBER: _ClassVar[int]
    BENEFICIARY_ID_FIELD_NUMBER: _ClassVar[int]
    BIK_FIELD_NUMBER: _ClassVar[int]
    CORR_ACCOUNT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    INN_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    KPP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    account_number: str
    bank_details_id: str
    bank_name: str
    beneficiary_id: str
    bik: str
    corr_account_number: str
    inn: str
    is_default: bool
    kpp: str
    name: str
    type: str
    def __init__(self, beneficiary_id: _Optional[str] = ..., bank_details_id: _Optional[str] = ..., type: _Optional[str] = ..., is_default: bool = ..., bik: _Optional[str] = ..., kpp: _Optional[str] = ..., inn: _Optional[str] = ..., name: _Optional[str] = ..., bank_name: _Optional[str] = ..., account_number: _Optional[str] = ..., corr_account_number: _Optional[str] = ...) -> None: ...

class EditBeneficiaryRksBankDetailsResponse(_message.Message):
    __slots__ = ["account_number", "bank_details_id", "bank_name", "beneficiary_id", "bik", "corr_account_number", "inn", "is_default", "kpp", "name", "type"]
    ACCOUNT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    BANK_DETAILS_ID_FIELD_NUMBER: _ClassVar[int]
    BANK_NAME_FIELD_NUMBER: _ClassVar[int]
    BENEFICIARY_ID_FIELD_NUMBER: _ClassVar[int]
    BIK_FIELD_NUMBER: _ClassVar[int]
    CORR_ACCOUNT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    INN_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    KPP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    account_number: str
    bank_details_id: str
    bank_name: str
    beneficiary_id: str
    bik: str
    corr_account_number: str
    inn: str
    is_default: bool
    kpp: str
    name: str
    type: str
    def __init__(self, beneficiary_id: _Optional[str] = ..., bank_details_id: _Optional[str] = ..., type: _Optional[str] = ..., is_default: bool = ..., bik: _Optional[str] = ..., kpp: _Optional[str] = ..., inn: _Optional[str] = ..., name: _Optional[str] = ..., bank_name: _Optional[str] = ..., account_number: _Optional[str] = ..., corr_account_number: _Optional[str] = ...) -> None: ...
