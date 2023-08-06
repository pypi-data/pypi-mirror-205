# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flexlogger/automation/proto/LoggingSpecificationDocument.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flexlogger.automation.proto import Identifiers_pb2 as flexlogger_dot_automation_dot_proto_dot_Identifiers__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n>flexlogger/automation/proto/LoggingSpecificationDocument.proto\x12\x35national_instruments.flex_logger.automation.protocols\x1a-flexlogger/automation/proto/Identifiers.proto\x1a\x1bgoogle/protobuf/empty.proto\"\x82\x01\n\x19GetLogFileBasePathRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\"8\n\x1aGetLogFileBasePathResponse\x12\x1a\n\x12log_file_base_path\x18\x01 \x01(\t\"\x9e\x01\n\x19SetLogFileBasePathRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\x12\x1a\n\x12log_file_base_path\x18\x02 \x01(\t\"\x1c\n\x1aSetLogFileBasePathResponse\"~\n\x15GetLogFileNameRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\"/\n\x16GetLogFileNameResponse\x12\x15\n\rlog_file_name\x18\x01 \x01(\t\"\x95\x01\n\x15SetLogFileNameRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\x12\x15\n\rlog_file_name\x18\x02 \x01(\t\"\x18\n\x16SetLogFileNameResponse\"\x85\x01\n\x1cGetLogFileDescriptionRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\"=\n\x1dGetLogFileDescriptionResponse\x12\x1c\n\x14log_file_description\x18\x01 \x01(\t\"\xa3\x01\n\x1cSetLogFileDescriptionRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\x12\x1c\n\x14log_file_description\x18\x02 \x01(\t\"V\n\x0cTestProperty\x12\x15\n\rproperty_name\x18\x01 \x01(\t\x12\x16\n\x0eproperty_value\x18\x02 \x01(\t\x12\x17\n\x0fprompt_on_start\x18\x03 \x01(\x08\"\x81\x01\n\x18GetTestPropertiesRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\"y\n\x19GetTestPropertiesResponse\x12\\\n\x0ftest_properties\x18\x01 \x03(\x0b\x32\x43.national_instruments.flex_logger.automation.protocols.TestProperty\"\xdf\x01\n\x18SetTestPropertiesRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\x12\\\n\x0ftest_properties\x18\x02 \x03(\x0b\x32\x43.national_instruments.flex_logger.automation.protocols.TestProperty\"\x96\x01\n\x16GetTestPropertyRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\x12\x15\n\rproperty_name\x18\x02 \x01(\t\"u\n\x17GetTestPropertyResponse\x12Z\n\rtest_property\x18\x01 \x01(\x0b\x32\x43.national_instruments.flex_logger.automation.protocols.TestProperty\"\xdb\x01\n\x16SetTestPropertyRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\x12Z\n\rtest_property\x18\x02 \x01(\x0b\x32\x43.national_instruments.flex_logger.automation.protocols.TestProperty\"\x19\n\x17SetTestPropertyResponse\"\x99\x01\n\x19RemoveTestPropertyRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\x12\x15\n\rproperty_name\x18\x02 \x01(\t\"\x1c\n\x1aRemoveTestPropertyResponse\"\x8a\x01\n!GetResolvedLogFileBasePathRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\"I\n\"GetResolvedLogFileBasePathResponse\x12#\n\x1bresolved_log_file_base_path\x18\x01 \x01(\t\"\x86\x01\n\x1dGetResolvedLogFileNameRequest\x12\x65\n\x13\x64ocument_identifier\x18\x01 \x01(\x0b\x32H.national_instruments.diagram_sdk.automation.protocols.ElementIdentifier\"@\n\x1eGetResolvedLogFileNameResponse\x12\x1e\n\x16resolved_log_file_name\x18\x01 \x01(\t2\xd1\x12\n\x1cLoggingSpecificationDocument\x12\xbb\x01\n\x12GetLogFileBasePath\x12P.national_instruments.flex_logger.automation.protocols.GetLogFileBasePathRequest\x1aQ.national_instruments.flex_logger.automation.protocols.GetLogFileBasePathResponse\"\x00\x12\xbb\x01\n\x12SetLogFileBasePath\x12P.national_instruments.flex_logger.automation.protocols.SetLogFileBasePathRequest\x1aQ.national_instruments.flex_logger.automation.protocols.SetLogFileBasePathResponse\"\x00\x12\xaf\x01\n\x0eGetLogFileName\x12L.national_instruments.flex_logger.automation.protocols.GetLogFileNameRequest\x1aM.national_instruments.flex_logger.automation.protocols.GetLogFileNameResponse\"\x00\x12\xaf\x01\n\x0eSetLogFileName\x12L.national_instruments.flex_logger.automation.protocols.SetLogFileNameRequest\x1aM.national_instruments.flex_logger.automation.protocols.SetLogFileNameResponse\"\x00\x12\xc4\x01\n\x15GetLogFileDescription\x12S.national_instruments.flex_logger.automation.protocols.GetLogFileDescriptionRequest\x1aT.national_instruments.flex_logger.automation.protocols.GetLogFileDescriptionResponse\"\x00\x12\x86\x01\n\x15SetLogFileDescription\x12S.national_instruments.flex_logger.automation.protocols.SetLogFileDescriptionRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\xb8\x01\n\x11GetTestProperties\x12O.national_instruments.flex_logger.automation.protocols.GetTestPropertiesRequest\x1aP.national_instruments.flex_logger.automation.protocols.GetTestPropertiesResponse\"\x00\x12~\n\x11SetTestProperties\x12O.national_instruments.flex_logger.automation.protocols.SetTestPropertiesRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\xb2\x01\n\x0fGetTestProperty\x12M.national_instruments.flex_logger.automation.protocols.GetTestPropertyRequest\x1aN.national_instruments.flex_logger.automation.protocols.GetTestPropertyResponse\"\x00\x12\xb2\x01\n\x0fSetTestProperty\x12M.national_instruments.flex_logger.automation.protocols.SetTestPropertyRequest\x1aN.national_instruments.flex_logger.automation.protocols.SetTestPropertyResponse\"\x00\x12\xbb\x01\n\x12RemoveTestProperty\x12P.national_instruments.flex_logger.automation.protocols.RemoveTestPropertyRequest\x1aQ.national_instruments.flex_logger.automation.protocols.RemoveTestPropertyResponse\"\x00\x12\xd3\x01\n\x1aGetResolvedLogFileBasePath\x12X.national_instruments.flex_logger.automation.protocols.GetResolvedLogFileBasePathRequest\x1aY.national_instruments.flex_logger.automation.protocols.GetResolvedLogFileBasePathResponse\"\x00\x12\xc7\x01\n\x16GetResolvedLogFileName\x12T.national_instruments.flex_logger.automation.protocols.GetResolvedLogFileNameRequest\x1aU.national_instruments.flex_logger.automation.protocols.GetResolvedLogFileNameResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flexlogger.automation.proto.LoggingSpecificationDocument_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETLOGFILEBASEPATHREQUEST._serialized_start=198
  _GETLOGFILEBASEPATHREQUEST._serialized_end=328
  _GETLOGFILEBASEPATHRESPONSE._serialized_start=330
  _GETLOGFILEBASEPATHRESPONSE._serialized_end=386
  _SETLOGFILEBASEPATHREQUEST._serialized_start=389
  _SETLOGFILEBASEPATHREQUEST._serialized_end=547
  _SETLOGFILEBASEPATHRESPONSE._serialized_start=549
  _SETLOGFILEBASEPATHRESPONSE._serialized_end=577
  _GETLOGFILENAMEREQUEST._serialized_start=579
  _GETLOGFILENAMEREQUEST._serialized_end=705
  _GETLOGFILENAMERESPONSE._serialized_start=707
  _GETLOGFILENAMERESPONSE._serialized_end=754
  _SETLOGFILENAMEREQUEST._serialized_start=757
  _SETLOGFILENAMEREQUEST._serialized_end=906
  _SETLOGFILENAMERESPONSE._serialized_start=908
  _SETLOGFILENAMERESPONSE._serialized_end=932
  _GETLOGFILEDESCRIPTIONREQUEST._serialized_start=935
  _GETLOGFILEDESCRIPTIONREQUEST._serialized_end=1068
  _GETLOGFILEDESCRIPTIONRESPONSE._serialized_start=1070
  _GETLOGFILEDESCRIPTIONRESPONSE._serialized_end=1131
  _SETLOGFILEDESCRIPTIONREQUEST._serialized_start=1134
  _SETLOGFILEDESCRIPTIONREQUEST._serialized_end=1297
  _TESTPROPERTY._serialized_start=1299
  _TESTPROPERTY._serialized_end=1385
  _GETTESTPROPERTIESREQUEST._serialized_start=1388
  _GETTESTPROPERTIESREQUEST._serialized_end=1517
  _GETTESTPROPERTIESRESPONSE._serialized_start=1519
  _GETTESTPROPERTIESRESPONSE._serialized_end=1640
  _SETTESTPROPERTIESREQUEST._serialized_start=1643
  _SETTESTPROPERTIESREQUEST._serialized_end=1866
  _GETTESTPROPERTYREQUEST._serialized_start=1869
  _GETTESTPROPERTYREQUEST._serialized_end=2019
  _GETTESTPROPERTYRESPONSE._serialized_start=2021
  _GETTESTPROPERTYRESPONSE._serialized_end=2138
  _SETTESTPROPERTYREQUEST._serialized_start=2141
  _SETTESTPROPERTYREQUEST._serialized_end=2360
  _SETTESTPROPERTYRESPONSE._serialized_start=2362
  _SETTESTPROPERTYRESPONSE._serialized_end=2387
  _REMOVETESTPROPERTYREQUEST._serialized_start=2390
  _REMOVETESTPROPERTYREQUEST._serialized_end=2543
  _REMOVETESTPROPERTYRESPONSE._serialized_start=2545
  _REMOVETESTPROPERTYRESPONSE._serialized_end=2573
  _GETRESOLVEDLOGFILEBASEPATHREQUEST._serialized_start=2576
  _GETRESOLVEDLOGFILEBASEPATHREQUEST._serialized_end=2714
  _GETRESOLVEDLOGFILEBASEPATHRESPONSE._serialized_start=2716
  _GETRESOLVEDLOGFILEBASEPATHRESPONSE._serialized_end=2789
  _GETRESOLVEDLOGFILENAMEREQUEST._serialized_start=2792
  _GETRESOLVEDLOGFILENAMEREQUEST._serialized_end=2926
  _GETRESOLVEDLOGFILENAMERESPONSE._serialized_start=2928
  _GETRESOLVEDLOGFILENAMERESPONSE._serialized_end=2992
  _LOGGINGSPECIFICATIONDOCUMENT._serialized_start=2995
  _LOGGINGSPECIFICATIONDOCUMENT._serialized_end=5380
# @@protoc_insertion_point(module_scope)
