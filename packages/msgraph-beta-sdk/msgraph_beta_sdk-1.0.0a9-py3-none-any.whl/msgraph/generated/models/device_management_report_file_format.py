from enum import Enum

class DeviceManagementReportFileFormat(Enum):
    # CSV Format
    Csv = "csv",
    # PDF Format (Deprecate later)
    Pdf = "pdf",
    # JSON Format
    Json = "json",
    # Evolvable enumeration sentinel value. Do not use.
    UnknownFutureValue = "unknownFutureValue",

