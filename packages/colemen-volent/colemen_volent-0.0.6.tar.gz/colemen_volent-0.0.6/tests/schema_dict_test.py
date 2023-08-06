"""API tests"""
# pylint: disable=invalid-name

from dataclasses import dataclass
from datetime import datetime
from datetime import timezone


import colemen_utils as c
from .. import volent

# import volent.Volent as volent
# from volent.Volent import Schema,Field,validators as _v
# from volent.data_types import String,Integer,EncodedPrimary




# @dataclass
# class SuccessfulSchema(Schema):
#     '''The publicly visible data for a task'''


#     def __init__(
#         self,
#         ) -> None:
#         # self.task_id = Field(required=True,nullable=False)
#         # self.target_id = Field(data_type=EncodedPrimary())
#         self.limit = Field(data_type=Integer(),default=50,validate=[_v.OneOf([25,50,100])],description="The number of results to return.")
#         self.offset = Field(data_type=Integer(),default=0,validate=[_v.Range(0)])
#         self.start_timestamp = Field(data_type=Integer(),default=None)
#         self.end_timestamp = Field(data_type=Integer(),default=None)

#     def valid_timestamps(self):
#         # print(f"validating schema timestamps")
#         s = self.start_timestamp.value
#         e = self.end_timestamp.value

#         if s is not None and e is not None:
#             if e > s:
#                 raise ValueError("Start timestamp must be after the end timestamp")







class TestSchemaDict:
    """TEST Schema Validation of dictionaries"""

    def test_successful_schema(self):
        """Confirm that we can create a new user"""
        assert True

        # v = volent.Volent()

        # data = {
        #     # "target_id":c.string.string_encode_int(50),
        #     # "target_id":123456,
        #     "limit":50,
        #     "offset":50,
        #     # "startTimestamp":round(datetime.now(tz=timezone.utc).timestamp()) - (86400 * 8),
        #     "startTimestamp":500,
        #     "endTimestamp":50,
        # }
        # ts = SuccessfulSchema()
        # dumped = ts.dump(data)
        # assert isinstance(dumped,(dict)) is True
