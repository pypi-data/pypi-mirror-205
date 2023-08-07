from pydantic import BaseModel, Extra
import datetime as dt
from typing import Union
from enum import Enum
import io
import base58
from sharingiscaring.GRPCClient import GRPCClient
from sharingiscaring.enums import NET
from rich import print


class TagAttribute(BaseModel):
    type: str
    name: str
    value: str


class TagDisplay(BaseModel):
    url: str
    hash: str


class ProvenanceTagModel(BaseModel):
    name: str
    unique: bool
    description: str
    attributes: list[TagAttribute]
    display: TagDisplay


class StandardIdentifiers(Enum):
    CIS_0 = "CIS-0"
    CIS_1 = "CIS-1"
    CIS_2 = "CIS-2"


class CIS:
    def __init__(
        self,
        grpcclient: GRPCClient,
        instance_index,
        instance_subindex,
        entrypoint,
        net: NET.MAINNET,
    ):
        self.grpcclient = grpcclient
        self.instance_index = instance_index
        self.instance_subindex = instance_subindex
        self.entrypoint = entrypoint
        self.net = net

    def standard_identifier(self, identifier: StandardIdentifiers) -> bytes:
        si = io.BytesIO()
        # write the length of ASCII characters for the identifier
        number = len(identifier.value)
        byte_array = number.to_bytes(1, "little")
        si.write(byte_array)
        # write the identifier
        si.write(bytes(identifier.value, encoding="ASCII"))
        # convert to bytes
        return si.getvalue()

    def supports_parameter(self, standard_identifier: StandardIdentifiers) -> bytes:
        sp = io.BytesIO()
        # write the number of standardIdentifiers present
        number = 1
        byte_array = number.to_bytes(2, "little")
        sp.write(byte_array)
        # write the standardIdentifier
        sp.write(self.standard_identifier(standard_identifier))
        # convert to bytes
        return sp.getvalue()

    def support_result(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(2), byteorder="little")
        if t == 0:
            return t, "Standard is not supported"
        elif t == 1:
            return t, "Standard is supported by this contract"
        elif t == 2:
            contracts = []
            n = int.from_bytes(bs.read(1), byteorder="little")
            for _ in range(n):
                contracts.append(self.contract_address(bs))
                return (
                    t,
                    "Standard is supported by using one of these contract addresses: "
                    + [x for x in contracts],
                )

    def supports_response(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        if bs.getbuffer().nbytes > 0:
            n = int.from_bytes(bs.read(2), byteorder="big")
            responses = []
            for _ in range(n):
                responses.append(self.support_result(bs))
            return responses[0]
        else:
            return False, "Lookup Failure"

    def supports_standard(self, standard_identifier: StandardIdentifiers) -> bool:
        parameter_bytes = self.supports_parameter(standard_identifier)

        ii = self.grpcclient.invoke_instance(
            "last_final",
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        support_result, support_result_text = self.supports_response(res)

        return support_result == 1

    # def supports_parameter(self, standard_identifier: StandardIdentifiers) -> bytes:
    #     sp = io.BytesIO()
    #     # write the number of standardIdentifiers present
    #     number = 2
    #     byte_array = number.to_bytes(1, "little")
    #     sp.write(byte_array)

    #     # write the standardIdentifier
    #     si = io.BytesIO()
    #     # write the length of ASCII characters for the identifier
    #     identifier = StandardIdentifiers.CIS_1
    #     number = len(identifier.value)
    #     byte_array = number.to_bytes(1, "little")
    #     si.write(byte_array)
    #     # write the identifier
    #     si.write(bytes(identifier.value, encoding="ASCII"))
    #     sp.write(si)
    #     si = io.BytesIO()
    #     identifier = StandardIdentifiers.CIS_1
    #     # write the length of ASCII characters for the identifier
    #     number = len(identifier.value)
    #     byte_array = number.to_bytes(1, "little")
    #     si.write(byte_array)
    #     # write the identifier
    #     si.write(bytes(identifier.value, encoding="ASCII"))
    #     sp.write(si)
    #     # convert to bytes
    #     return sp.getvalue()

    # def supportsParameter(self) -> bytes:
    #     sp = io.BytesIO()
    #     # write the number of standardIdentifiers present
    #     number = len(StandardIdentifiers)
    #     byte_array = number.to_bytes(2, "little")
    #     sp.write(byte_array)

    #     for standard in StandardIdentifiers:
    #         # write the standardIdentifier
    #         sp.write(self.standardIdentifier(standard.value))
    #     # convert to bytes
    #     return sp.getvalue()

    def account_address(self, bs: io.BytesIO):
        addr = bs.read(32)
        return base58.b58encode_check(b"\x01" + addr).decode()

    def contract_address(self, bs: io.BytesIO):
        return int.from_bytes(bs.read(8), byteorder="little"), int.from_bytes(
            bs.read(8), byteorder="little"
        )

    def address(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return self.account_address(bs)
        elif t == 1:
            return self.contract_address(bs)
        else:
            raise Exception("invalid type")

    def receiver(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return self.account_address(bs)
        elif t == 1:
            return self.contract_address(bs), self.receiveHookName(bs)
        else:
            raise Exception("invalid type")

    def url(self, n: int, bs: io.BytesIO):
        data = bs.read(n)
        return data

    def metadataChecksum(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return None
        elif t == 1:
            return bs.read(32)
        else:
            raise Exception("invalid type")

    def metadataUrl(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        url = bs.read(n).decode()
        checksum = self.metadataChecksum(bs)
        return [url, checksum]

    def tokenAmount(self, bs: io.BytesIO):
        return int.from_bytes(bs.read(8), byteorder="little")

    def receiveHookName(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        name = bs.read(n)
        return bytes.decode(name, "UTF-8")

    def additionalData(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        data = bs.read(n)
        return data

    def tokenID(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def balanceOfQuery(self, bs: io.BytesIO):
        tokenID = self.tokenID(bs)
        address = self.address(bs)
        return [tokenID, address]

    def balanceOfParameter(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        queries = []
        for _ in range(0, n):
            queries.append(self.balanceOfQuery(bs))

        return queries

    def balanceOfResponse(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        results = []
        for _ in range(0, n):
            results.append(self.tokenAmount(bs))

        return results

    def bytes_from_hex_tokenID(self, hex):
        the_list = list(bytes.fromhex(hex[2:]))
        the_list.insert(0, 32)
        return the_list

    def generate_tokenID(self, tokenID: str):
        sp = io.BytesIO()

        tokenID_in_bytes = bytes.fromhex(tokenID)

        sp.write(int(len(tokenID_in_bytes)).to_bytes(1, "little"))
        # write the standardIdentifier
        sp.write(tokenID_in_bytes)
        return sp.getvalue()

    def invoke_token_metadataUrl(self, tokenID: str) -> bool:
        parameter_bytes = self.tokenMetadataParameter(tokenID)

        ii = self.grpcclient.invoke_instance(
            "last_final",
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        return self.tokenMetadataResultParameter(res)

    def tokenMetadataParameter(self, tokenID: str):
        sp = io.BytesIO()

        sp.write(int(1).to_bytes(2, "little"))
        # write the standardIdentifier
        # sp.write(bytearray(self.bytes_from_hex_tokenID(tokenID)))
        sp.write(self.generate_tokenID(tokenID))
        # convert to bytes
        return sp.getvalue()

    def metadata_result(self, bs: bytes):
        n = int(bs[:2].decode("ASCII"))
        bs = io.BytesIO(bs)
        bs.read(2)
        url = self.url(n, bs)
        return url

    def metadata_response(self, bs: bytes):
        # bs: io.BytesIO = io.BytesIO(bs)
        if len(bs) > 0:
            n = int(bs[:2].decode("ASCII"))
            # n = int.from_bytes(bs.read(2), byteorder="big")
            responses = []
            for _ in range(n):
                responses.append(self.metadata_result(bs))
            return responses[0]
        else:
            return False, "Lookup Failure"

    def tokenMetadataResultParameter(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(2), byteorder="little")
        results = []
        for _ in range(0, n):
            results.append(self.metadataUrl(bs))

        return results

    # def receiveHookName(self, bs: io.BytesIO):
    #     n = int.from_bytes(bs.read(1), byteorder="little")
    #     return bytes.hex(bs.read(n))
