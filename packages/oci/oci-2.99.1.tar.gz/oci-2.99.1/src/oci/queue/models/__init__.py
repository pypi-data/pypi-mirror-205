# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from __future__ import absolute_import

from .change_queue_compartment_details import ChangeQueueCompartmentDetails
from .create_queue_details import CreateQueueDetails
from .delete_messages_details import DeleteMessagesDetails
from .delete_messages_details_entry import DeleteMessagesDetailsEntry
from .delete_messages_result import DeleteMessagesResult
from .delete_messages_result_entry import DeleteMessagesResultEntry
from .get_message import GetMessage
from .get_messages import GetMessages
from .purge_queue_details import PurgeQueueDetails
from .put_message import PutMessage
from .put_messages import PutMessages
from .put_messages_details import PutMessagesDetails
from .put_messages_details_entry import PutMessagesDetailsEntry
from .queue import Queue
from .queue_collection import QueueCollection
from .queue_stats import QueueStats
from .queue_summary import QueueSummary
from .stats import Stats
from .update_message_details import UpdateMessageDetails
from .update_messages_details import UpdateMessagesDetails
from .update_messages_details_entry import UpdateMessagesDetailsEntry
from .update_messages_result import UpdateMessagesResult
from .update_messages_result_entry import UpdateMessagesResultEntry
from .update_queue_details import UpdateQueueDetails
from .updated_message import UpdatedMessage
from .work_request import WorkRequest
from .work_request_error import WorkRequestError
from .work_request_error_collection import WorkRequestErrorCollection
from .work_request_log_entry import WorkRequestLogEntry
from .work_request_log_entry_collection import WorkRequestLogEntryCollection
from .work_request_resource import WorkRequestResource
from .work_request_summary import WorkRequestSummary
from .work_request_summary_collection import WorkRequestSummaryCollection

# Maps type names to classes for queue services.
queue_type_mapping = {
    "ChangeQueueCompartmentDetails": ChangeQueueCompartmentDetails,
    "CreateQueueDetails": CreateQueueDetails,
    "DeleteMessagesDetails": DeleteMessagesDetails,
    "DeleteMessagesDetailsEntry": DeleteMessagesDetailsEntry,
    "DeleteMessagesResult": DeleteMessagesResult,
    "DeleteMessagesResultEntry": DeleteMessagesResultEntry,
    "GetMessage": GetMessage,
    "GetMessages": GetMessages,
    "PurgeQueueDetails": PurgeQueueDetails,
    "PutMessage": PutMessage,
    "PutMessages": PutMessages,
    "PutMessagesDetails": PutMessagesDetails,
    "PutMessagesDetailsEntry": PutMessagesDetailsEntry,
    "Queue": Queue,
    "QueueCollection": QueueCollection,
    "QueueStats": QueueStats,
    "QueueSummary": QueueSummary,
    "Stats": Stats,
    "UpdateMessageDetails": UpdateMessageDetails,
    "UpdateMessagesDetails": UpdateMessagesDetails,
    "UpdateMessagesDetailsEntry": UpdateMessagesDetailsEntry,
    "UpdateMessagesResult": UpdateMessagesResult,
    "UpdateMessagesResultEntry": UpdateMessagesResultEntry,
    "UpdateQueueDetails": UpdateQueueDetails,
    "UpdatedMessage": UpdatedMessage,
    "WorkRequest": WorkRequest,
    "WorkRequestError": WorkRequestError,
    "WorkRequestErrorCollection": WorkRequestErrorCollection,
    "WorkRequestLogEntry": WorkRequestLogEntry,
    "WorkRequestLogEntryCollection": WorkRequestLogEntryCollection,
    "WorkRequestResource": WorkRequestResource,
    "WorkRequestSummary": WorkRequestSummary,
    "WorkRequestSummaryCollection": WorkRequestSummaryCollection
}
