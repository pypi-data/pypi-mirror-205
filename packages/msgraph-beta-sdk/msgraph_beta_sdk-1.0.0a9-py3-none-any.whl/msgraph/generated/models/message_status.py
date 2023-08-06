from enum import Enum

class MessageStatus(Enum):
    GettingStatus = "gettingStatus",
    Pending = "pending",
    Failed = "failed",
    Delivered = "delivered",
    Expanded = "expanded",
    Quarantined = "quarantined",
    FilteredAsSpam = "filteredAsSpam",
    UnknownFutureValue = "unknownFutureValue",

