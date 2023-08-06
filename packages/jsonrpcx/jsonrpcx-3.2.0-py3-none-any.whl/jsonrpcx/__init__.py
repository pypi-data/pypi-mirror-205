from os import times
from typing import *
import json
import httpx
import warnings
import uuid
import sys
import io
import logging
import inspect
from pytz import utc as tz_utc
from tzlocal import get_localzone as tz_getlocal
from functools import reduce

PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603

def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        def anyToAware(dt):
            if dt.tzinfo is None:
                return dt.replace(tzinfo=tz_getlocal())
            else:
                return dt

        obj = anyToAware(obj).astimezone(tz_utc)
        return obj.isoformat()
    return obj


class Error(Exception):
    def __init__(self, theCode = None, theMessage = "", theData = None):
        self.code = theCode
        self.data = theData
        self.message = theMessage


    # This setter is importat to do the magic (re/-initing the super class) with the new message either assigned via Error.message = "bla" or via the parser() method
    # If in the future there should be any errors with this class esspecially during initing look here first
    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        super(Exception, self).__init__(self._message)


    def parse(self, jsonString):
        failed = 0
        try:
            jsonData = json.JSONDecoder().decode(jsonString)
            self.code = jsonData["code"]
            self.message = jsonData["message"]
            
            # check if the key "data" exists and only try to access it if it does exist
            for key in jsonData:
                if key == "data":
                    self.data = jsonData[key]
            
        except:
            failed = 1
        
        if failed == 1:
            raise(Exception)
        
    def serializeToDict(self) -> Dict:
        return {
            "code"        : self.code,
            "message"    : self.message,
            "data"        : self.data
        }
    
    def stringify(self) -> str:
        stringified = json.JSONEncoder(default=json_date_handler).encode(self.serializeToDict())
        return stringified

class Request():
    def __init__(self, method = None, params = []):
        self._method = method
        self._params = params # TODO: take Array OR Dict


    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        assert type(value) == str, "The Method must be of type String"
        self._method = value


    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        assert type(value) == dict or type(value) == list, "The Method must be either of type Dict or List"
        self._params = value


    def parse(self, jsonString):
        failed = 0
        try:
            jsonData = json.JSONDecoder().decode(jsonString)
            self.method = jsonData["method"]
            self.params = jsonData["params"]

        except:
            failed = 1

        if failed == 1:
            raise(Exception)


    def stringify(self):    
        rpcObject = {
            "method"    : self.method,
            "params"    : self.params,
        }

        stringified = json.JSONEncoder(default=json_date_handler).encode(rpcObject)
        return stringified


class Response():
    def __init__(self):
        self._error = None # expecting the error object returned by RPC2Error
        self.result = None
        
    @classmethod
    def fromError(cls, error: Error):
        response = Response()
        response.error = error
        return response

    @classmethod
    def fromResultPrimitive(cls, result):
        response = Response()
        response.result = result
        return response

    # This Property is only in for typechecking
    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        assert isinstance(value, Error), "Parameter error must be an instance of Error."
        self._error = value


    def parse(self, jsonString):
        failed = 0
        try:
            jsonData = json.JSONDecoder().decode(jsonString)

            # check which message we have here and dependigly set either the error or the result
            for key in jsonData:
                if key == "error":
                    self.error = jsonData[key]
                    break
                elif key == "result":
                    self.result = jsonData[key]
                    break

        except:
            failed = 1

        if failed == 1:
            raise(Exception)


    def stringify(self):
        rpcObject = {} # we have to create either a result or an error object
        if self.indicatesSuccess():
            rpcObject = {
                "result"    : self.result
            }
        else:
            rpcObject = {
                "error"        : self.error.stringify()
            }


        stringified = json.JSONEncoder(default=json_date_handler).encode(rpcObject)
        return stringified    


    def indicatesSuccess(self):
        if (self.error is None):
            return True
        return False


class Message():
    def __init__(self):
        self._request = None
        self._response = None
        self.jsonrpc = "2.0"
        self.id = None
        self.auth = None # usualy we expect a token:string here but it could also be anything else
    
    @classmethod
    def fromError(cls, error: Error, *, messageId):
        message = Message()
        message.id = messageId
        message.response = Response.fromError(error)
        return message

    @classmethod
    def fromResponse(cls, response: Response, *, messageId):
        message = Message()
        message.id = messageId
        message.response = response
        return message
        
    @property
    def request(self):
        return self._request
        
    @request.setter
    def request(self, value):
        assert isinstance(value, Request), "Parameter request must be instance of Request."
        self._request = value
    
    
    @property
    def response(self):
        return self._response
        
    @response.setter
    def response(self, value):
        assert isinstance(value, Response), "Parameter response must be instance of Response."
        self._response = value


    def parse(self, jsonString):
        failed = 0
        try:
            jsonData = json.JSONDecoder().decode(jsonString)

            try:
                self.id = jsonData["id"]
            except:
                logging.debug("Id was not supplied")

            # find out which message type we got
            for key in jsonData:

                if key == "method": # we assume this is a request
                    # reassemble the request object
                    reassembledRequest = Request()
                    reassembledRequest.method = jsonData["method"]
                    try:
                        reassembledRequest.params = jsonData["params"]
                    except KeyError:
                        # in the JSON-RPC 2.0 Spec the params field is not required
                        pass

                    self.request = reassembledRequest
                    break # in the spec there is only one messagetype to be expectet here

                elif key == "result" or key == "error": # we assume this is a response
                    # reassemble the response object
                    reassembledResponse = Response()

                    # determine the response type
                    if key == "result":
                        reassembledResponse.result = jsonData["result"]
                    else: # key == "error"
                        reassembledError = Error()
                        reassembledError.code = jsonData["error"]["code"]
                        reassembledError.message = jsonData["error"]["message"]

                        # as data is optional we have to make sure its in before atteming to access it
                        for key in jsonData:
                            if key == "data":
                                reassembledError.data = jsonData["error"]["data"]
                                break

                        reassembledResponse.error = reassembledError

                    self.response = reassembledResponse
                    break

        except:
            raise
            failed = 1

        if failed == 1:
            raise(Exception)


    def stringify(self):
        rpcObject = {
            "jsonrpc": self.jsonrpc,
            "id":        self.id,
        }
        
        if self.isRequest():
            rpcObject["method"] = self.request.method
            rpcObject["params"] = self.request.params
            
        elif self.isResponse():
            if self.response.indicatesSuccess():
                rpcObject["result"] = self.response.result
            else:
                rpcObject["error"] = self.response.error.serializeToDict()
                
        stringified = json.JSONEncoder(default=json_date_handler).encode(rpcObject)
        return stringified


    def isRequest(self):
        assert self.request == None or self.response == None, "The Message Object must and can not be a request and a response at the same time!"
        if (self.request != None and self.response == None):
            return True
        else:
            return False


    def isResponse(self):
        return not self.isRequest()


class ServiceProxy(object):
    def __init__(self, url: str, func: str=None, session=None):
        # Because there is a huge amount of old closed source code using this it's not yet removed
        # TODO: reenable warning
        # warnings.warn("The ServiceProxy class is deprecated use the call() function or it's async pendant instead")
        self.url = url
        self.func = func
        self.session = session
        if not session:
            self.session = httpx.Client()

    def __getattr__(self, name):
        if self.func != None:
            name = "%s.%s" % (self.func, name)
        return ServiceProxy(self.url, name, self.session)

    def __call__(self, *args):
        arglist = []
        if type(args) == tuple:
            for i in range(len(args)):
                arglist.append( args[i] )
        # TODO: fix bug in session management (Client cant be called)
        return call(self.url, self.func, arglist) #, session=self.session)

def _prepareCallRequest(method: str, params: Union[Dict, List]) -> Message:
    requestMessage = Message()
    request = Request(method = method, params=params)
    requestMessage.request = request
    requestMessage.id = str(uuid.uuid4())
    return requestMessage

def _processCallResponse(payload: str):
    responseMessage = Message()
    responseMessage.parse(payload.text)
    if responseMessage.response.indicatesSuccess():
        return responseMessage.response.result
    else:
        raise(responseMessage.response.error)

def call(url, method, params=[], *, session=None):
    assert type(params) in [dict, list], "PRC params must be dict or list"
    requestMessage = _prepareCallRequest(method, params)
    requestFunc = session if session else httpx.post
    resp = requestFunc(url, 
                        data=requestMessage.stringify(),
                        headers={'content-type': 'application/json'},
                        timeout=30,
                        )
    return _processCallResponse(resp)

async def acall(url, method, params=[]):
    """
    This funciton currenlty intentionaly does not support sessions because they represent mutable state combined with async this is mostly a bad idea
    """
    assert type(params) in [dict, list], "PRC params must be dict or list"
    requestMessage = _prepareCallRequest(method, params)
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, 
                            data=requestMessage.stringify(),
                            headers={'content-type': 'application/json'},
                            timeout=30,
                            )
    return _processCallResponse(resp)


class DiscoverMixin:
    async def rpcDiscover(self) -> Dict:
        """
        Returns OpenRPC JSON (https://spec.open-rpc.org/) description of the API.
        """
        return self.rpcDiscover()

    def rpcDiscover(self) -> Dict:
        """
        Returns OpenRPC JSON (https://spec.open-rpc.org/) description of the API.
        """
        # TODO: Add better support for List[], Optional[] and Union[] all of those work to some extend but could have better support.

        def isParameterRequired(param: inspect.Parameter) -> bool:
            # Has a default value
            hasDefaultValue = False if param.default is param.empty else True
            # Has the type annotation Optional[]
            hasOptioanAnnotation = param.annotation is Optional
            # Has the type annotation Union[] and allows for None
            hasUnionWithOneOptionalAnnotation = param.annotation is Union and type(
                None) in param.annotation.__args__
            if hasDefaultValue:
                return False
            elif hasOptioanAnnotation:
                return False
            elif hasUnionWithOneOptionalAnnotation:
                return False
            return True

        def buildSchema(annotation, name: Optional[str] = None) -> Optional[Dict]:
            dataTypeMapping = {
                "int": "integer",
                "flot": "number",
                "str": "string",
                "bool": "boolean",
                "List": "array",
                "Dict": "object",
            }
            if annotation is not inspect.Parameter.empty:
                _type = None
                if hasattr(annotation, "__name__") \
                        and annotation.__name__ in dataTypeMapping.keys():
                    _type = dataTypeMapping[annotation.__name__]
                elif annotation is None:
                    _type = "null"
                if not _type:
                    return None
                schema = {
                    "type": _type,
                }
                result: Dict = {"schema": schema}
                if name:
                    result["name"] = name
                return result
            return None

        def buildParamList(signature: inspect.Signature):
            params = []
            for name in signature.parameters.keys():
                param = signature.parameters[name]
                data = {
                    "name": name,
                    "required": isParameterRequired(param),
                }
                schema = buildSchema(param.annotation)
                if schema:
                    data.update(schema)
                params.append(data)
            return params

        def reduceMethodNamesWith(acc, method):
            methodName = "rpc.discover" if method[0] == "rpcDiscover" else method[0]
            methodObject = method[1]
            if methodName[0] == "_" or methodName == "parseRequest":
                # Don't add magic methods or private methods.
                return acc
            docstring = inspect.getdoc(methodObject)
            methodInfo = {
                "name": methodName,
                "description": docstring if docstring else "",
                "paramStructure": "by-name",
                "params": buildParamList(inspect.signature(methodObject)),
            }
            schemaName = "Invokation Result"
            schema = buildSchema(inspect.signature(
                methodObject).return_annotation, schemaName)
            # Currently the fallback is used if the return type is Optional or Union
            fallbackSchema = {"schema": {"type": "null"}, "name": schemaName,
                              "description": "**ERROR: Auto discovery was unable to detect the correct return type for this funciton. `null` is shown as a fallback. It is NOT the correct return type.**"}
            methodInfo["result"] = schema or fallbackSchema
            return acc + [methodInfo]
        applicationLevelMethods = inspect.getmembers(
            self, lambda input: inspect.ismethod(input))
        rpcMethods = applicationLevelMethods
        return {
            "openrpc": "1.0.0-rc1",
            "info": self.delegate.experimentalOpenRPCInfo(),
            "servers": self.delegate.experimentalOpenRPCServers(),
            "methods": reduce(reduceMethodNamesWith, rpcMethods, [])
        }


class CommonServer(DiscoverMixin):
    def __init__(self, delegate=None):
        self.delegate = delegate
    
    def _error(self, messageId, jsonRpcErrorCode: int) -> Error:
        self.log.debug({
            PARSE_ERROR: "parse error",
            INVALID_REQUEST: "invalid request",
            METHOD_NOT_FOUND: "method not found",
            INVALID_PARAMS: "invalid params",
            INTERNAL_ERROR: "internal error",
        }.get(jsonRpcErrorCode) or f"unknown error with code {jsonRpcErrorCode}")
        error = Error(
                theCode=INVALID_REQUEST,
                theMessage="Invalid Request",
                theData="No Request"
                )
        return Message.fromError(error, messageId=messageId)

    def _processRequest(self, rawRequest: str) -> Message:
        error, callInfo = self._processRequestCore(rawRequest)
        if error:
            return error
        method = callInfo["method"]
        params = callInfo["params"]
        assert type(params) in [list, dict], "params must be list or dict"
        result = method(**params) if type(params) == dict else method(*params)
        return Message.fromResponse(Response.fromResultPrimitive(result), messageId=callInfo["messageId"])

    async def _async_processRequest(self, rawRequest: str) -> Message:
        error, callInfo = self._processRequestCore(rawRequest)
        if error:
            return error
        method = callInfo["method"]
        params = callInfo["params"]
        assert type(params) in [list, dict], "params must be list or dict"
        def mkResult(result):
            return Message.fromResponse(Response.fromResultPrimitive(result), messageId=callInfo["messageId"])
        
        if type(params) == dict:
            return mkResult(await method(**params))
        return mkResult(await method(*params))

    def _processRequestCore(self, rawRequest: str):
        # Instead of directly calling the rpc method we could just return information about
        # how it should be called. The advantage is that it can be used from a sync and async function call
        # allowing the new async feature of Python while maintaining backward compatibility
        if not rawRequest:
            return self._error(None, INVALID_REQUEST), None

        try:
            self.log.debug("processing request")
            requestingRPCMessage = Message()
            requestingRPCMessage.parse(rawRequest)
            logging.debug("RPC Request")
            logging.debug(requestingRPCMessage.stringify())
            methoToCall = "rpcDiscover" if requestingRPCMessage.request.method == "rpc.discover" else requestingRPCMessage.request.method
            paramsToCall = requestingRPCMessage.request.params

            # makes it easy to call RPC methods on a delegate if thats required at some point in the future
            rpcMethodTargetClass = self

            methodExists = hasattr(rpcMethodTargetClass.__class__, methoToCall) \
                and callable(getattr(rpcMethodTargetClass.__class__, methoToCall))
                
            if not methodExists:
                return self._error(requestingRPCMessage.id, METHOD_NOT_FOUND), None

            logging.debug("Method does exist")
            callableMethod = getattr(rpcMethodTargetClass,methoToCall)
            callableMethodArgSpec = inspect.getfullargspec(callableMethod)

            accountForMethodSelfVariable = 1
            if type(paramsToCall) == dict:
                return None, {
                    "method": callableMethod,
                    "params": paramsToCall,
                    "messageId": requestingRPCMessage.id
                }
            elif type(paramsToCall) == list:
                functionCountArguments = len(callableMethodArgSpec.args) - accountForMethodSelfVariable
                doesRpcCallNotExceedFunctionArgLength = len(paramsToCall) <= functionCountArguments
                doesRpcCallNotHaveLessArgumentsThenMandatory = True
                if doesRpcCallNotExceedFunctionArgLength and doesRpcCallNotHaveLessArgumentsThenMandatory:
                    return None, {
                        "method": callableMethod,
                        "params": paramsToCall,
                        "messageId": requestingRPCMessage.id
                    }
                else:
                    return self._error(requestingRPCMessage.id, INVALID_PARAMS), None
            else:
                raise Exception("JSON-RPC 2.0 CommonServer Parameters passed must bee DICT or LIST.")
        except Exception as ex:
            logging.exception(ex)
            return self._error(requestingRPCMessage.id, INTERNAL_ERROR), None


class CommonDelegate:
    def experimentalOpenRPCInfo(self):
        """
        Note: This function is currently experimental and the expected return type might change
        Return the `info` Dict of the OpenRPC spec
        """
        return {
            "version": "1.0.0",
            "title": "Example Title",
            "termsOfService": "https://example.eu/tos",
            "contact": {
                "name": "Support Contact Name",
                "email": "support@example.eu",
                "url": "https://example.eu"
            },
            "description": "This API uses JSON-RPC 2.0. For simplicity it does not support batch method calls."
            }
    
    def experimentalOpenRPCServers(self) -> Optional[List[Dict]]:
        """
        Note: This function is currently experimental and the expected return type might change

        Return a list containing a dict with `name` and `url` keys.
        Example:
        `[{ "name": "Example endpoint", "url": "https://localhost:8000" }]`
        """
        return [{
                "name": "Example endpoint",
                "url": "http://localhost:8000"
            }]


class CGIServerDelegate(CommonDelegate):
    def HTTPHeader(self):
        return "Content-Type: application/json"


class CommonCGIServer(CommonServer):
    def _cgiserver_writeHeaders(self):
        self.log.debug("writing header")
        header = self.delegate.HTTPHeader()
        print(header)
        print()


class CGIServer(CommonCGIServer):
    def __init__(self, delegate=None):
        super().__init__(delegate)
        self.log = logging.getLogger("CGIServer")
        self.log.debug("startet")
        if delegate == None:
            self.delegate = CGIServerDelegate()
        else:
            self.delegate = delegate
        self._cgiserver_writeHeaders()
        self._cgiserver_parseRequest()

    def _cgiserver_parseRequest(self):
        self.log.debug("parsing request")
        try:
            raw = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8').read()
        except Exception as ex:
            self.log.exception(ex)
        try:
            print(self._processRequest(raw).stringify())
        except Exception as ex:
            self.log.exception(ex)
            raise ex
        exit(0)


class AsyncCGIServer(CommonCGIServer):
    def __init__(self, delegate=None):
        super().__init__(delegate)
        self.log = logging.getLogger("CGIServer")
        self.log.debug("startet")
        if delegate == None:
            self.delegate = CGIServerDelegate()
        else:
            self.delegate = delegate
        self._cgiserver_writeHeaders()
    
    async def processRequests(self):
        self.log.debug("parsing request")
        try:
            raw = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8').read()
        except Exception as ex:
            self.log.exception(ex)
        try:
            response = await self._async_processRequest(raw)
        except Exception as ex:
            self.log.exception(ex)
            raise ex
        logging.debug("Response")
        logging.debug(response.stringify())
        print(response.stringify())
        exit(0)


class WSGIServerDelegate(CommonDelegate):
    def HTMLHeaders(self) -> List[str]:
        return [("Content-Type", "application/json")]


class WSGIServer(CommonServer):
    def __init__(self, *, delegate: WSGIServerDelegate=None):
        super().__init__(delegate)
        self.log = logging.getLogger("WSGIServer")
        self.log.debug("started")
        if delegate is None:
            self.delegate = WSGIServerDelegate()
        else:
            self.delegate = delegate

    def parseRequest(self, wsgiEnvironment, wsgiStartResponse):
        wsgiStartResponse("200 OK", self.delegate.HTMLHeaders())
        self.log.debug("parsing request")
        # the environment variable CONTENT_LENGTH may be empty or missing
        try:
            request_body_size = int(wsgiEnvironment.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        raw = None
        try:
            raw =  wsgiEnvironment['wsgi.input'].read(request_body_size).decode("utf-8")
        except Exception as ex:
            self.log.exception(ex)
        data = bytes(self._processRequest(raw).stringify(), encoding="utf-8")
        return iter([data])


class ASGIServerDelegate(CommonDelegate):
    pass


class ASGIServer(CommonServer):
    def __init__(self, *, delegate: ASGIServerDelegate=None):
        super().__init__(delegate)
        self.log = logging.getLogger("WSGIServer")
        self.log.debug("started")
        if delegate is None:
            self.delegate = ASGIServerDelegate()
        else:
            self.delegate = delegate


    async def parseRequest(self, scope, receive, send):
        async def read_body(receive):
            """
            Read and return the entire body from an incoming ASGI message.
            """
            body = b''
            more_body = True

            while more_body:
                message = await receive()
                body += message.get('body', b'')
                more_body = message.get('more_body', False)

            return body
        assert scope['type'] == 'http'
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'application/json'],
            ],
        })
        body = await read_body(receive)
        rpcRequest = body.decode("utf-8")
        print(rpcRequest)
        
        rpcResult = await self._async_processRequest(rpcRequest)
        await send({
            'type': 'http.response.body',
            'body': rpcResult.stringify().encode("utf-8")
        })

