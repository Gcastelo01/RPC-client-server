# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: peerserver.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10peerserver.proto\x12\x04peer\"0\n\rInsertRequest\x12\r\n\x05\x63have\x18\x01 \x01(\x05\x12\x10\n\x08\x63onteudo\x18\x02 \x01(\t\"#\n\x0eInsertResponse\x12\x11\n\tresultado\x18\x01 \x01(\x05\" \n\x0f\x43onsultaRequest\x12\r\n\x05\x63have\x18\x01 \x01(\x05\"$\n\x10\x43onsultaResponse\x12\x10\n\x08\x63onteudo\x18\x01 \x01(\t\"\"\n\x0f\x41tivacaoRequest\x12\x0f\n\x07servico\x18\x01 \x01(\t\"$\n\x10\x41tivacaoResponse\x12\x10\n\x08mensagem\x18\x01 \x01(\x05\"\x10\n\x0eTerminoRequest\"#\n\x0fTerminoResponse\x12\x10\n\x08mensagem\x18\x01 \x01(\x05\x32\xf1\x01\n\nPeerServer\x12\x35\n\x08Insercao\x12\x13.peer.InsertRequest\x1a\x14.peer.InsertResponse\x12\x39\n\x08\x43onsulta\x12\x15.peer.ConsultaRequest\x1a\x16.peer.ConsultaResponse\x12\x39\n\x08\x41tivacao\x12\x15.peer.AtivacaoRequest\x1a\x16.peer.AtivacaoResponse\x12\x36\n\x07Termino\x12\x14.peer.TerminoRequest\x1a\x15.peer.TerminoResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'peerserver_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_INSERTREQUEST']._serialized_start=26
  _globals['_INSERTREQUEST']._serialized_end=74
  _globals['_INSERTRESPONSE']._serialized_start=76
  _globals['_INSERTRESPONSE']._serialized_end=111
  _globals['_CONSULTAREQUEST']._serialized_start=113
  _globals['_CONSULTAREQUEST']._serialized_end=145
  _globals['_CONSULTARESPONSE']._serialized_start=147
  _globals['_CONSULTARESPONSE']._serialized_end=183
  _globals['_ATIVACAOREQUEST']._serialized_start=185
  _globals['_ATIVACAOREQUEST']._serialized_end=219
  _globals['_ATIVACAORESPONSE']._serialized_start=221
  _globals['_ATIVACAORESPONSE']._serialized_end=257
  _globals['_TERMINOREQUEST']._serialized_start=259
  _globals['_TERMINOREQUEST']._serialized_end=275
  _globals['_TERMINORESPONSE']._serialized_start=277
  _globals['_TERMINORESPONSE']._serialized_end=312
  _globals['_PEERSERVER']._serialized_start=315
  _globals['_PEERSERVER']._serialized_end=556
# @@protoc_insertion_point(module_scope)
