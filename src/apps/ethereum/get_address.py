from apps.common.layout import address_n_to_str, show_address, show_qr
from apps.ethereum import networks


async def get_address(ctx, msg):
    from trezor.messages.EthereumAddress import EthereumAddress
    from trezor.crypto.curve import secp256k1
    from trezor.crypto.hashlib import sha3_256
    from apps.common import seed

    node = await seed.derive_node(ctx, msg.address_n)

    seckey = node.private_key()
    public_key = secp256k1.publickey(seckey, False)  # uncompressed
    address = sha3_256(public_key[1:], keccak=True).digest()[12:]

    if msg.show_display:
        if len(msg.address_n) > 1:  # path has slip44 network identifier
            network = networks.by_slip44(msg.address_n[1] & 0x7FFFFFFF)
        else:
            network = None
        hex_addr = _ethereum_address_hex(address, network)
        desc = address_n_to_str(msg.address_n)
        while True:
            if await show_address(ctx, hex_addr, desc=desc):
                break
            if await show_qr(ctx, hex_addr, desc=desc):
                break

    return EthereumAddress(address=address)


def _ethereum_address_hex(address, network=None):
    from ubinascii import hexlify
    from trezor.crypto.hashlib import sha3_256

    rskip60 = network is not None and network.rskip60

    hx = hexlify(address).decode()

    prefix = str(network.chain_id) + "0x" if rskip60 else ""
    hs = sha3_256(prefix + hx, keccak=True).digest()
    h = ""

    for i in range(20):
        l = hx[i * 2]
        if hs[i] & 0x80 and l >= "a" and l <= "f":
            l = l.upper()
        h += l
        l = hx[i * 2 + 1]
        if hs[i] & 0x08 and l >= "a" and l <= "f":
            l = l.upper()
        h += l

    return "0x" + h
