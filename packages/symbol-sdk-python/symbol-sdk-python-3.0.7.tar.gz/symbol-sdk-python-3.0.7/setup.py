# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['symbolchain',
 'symbolchain.external',
 'symbolchain.facade',
 'symbolchain.impl',
 'symbolchain.nc',
 'symbolchain.nem',
 'symbolchain.sc',
 'symbolchain.symbol']

package_data = \
{'': ['*']}

install_requires = \
['Pillow==9.5.0',
 'PyNaCl==1.5.0',
 'PyYAML==6.0',
 'cryptography==40.0.2',
 'mnemonic==0.20',
 'pyzbar==0.1.9',
 'qrcode==7.4.2',
 'ripemd-hash==1.0.0',
 'safe-pysha3==1.0.3']

setup_kwargs = {
    'name': 'symbol-sdk-python',
    'version': '3.0.7',
    'description': 'Symbol SDK',
    'long_description': "# Symbol-SDK\n\n[![lint][sdk-python-lint]][sdk-python-job] [![test][sdk-python-test]][sdk-python-job] [![vectors][sdk-python-vectors]][sdk-python-job] [![][sdk-python-cov]][sdk-python-cov-link] [![][sdk-python-package]][sdk-python-package-link]\n\n[sdk-python-job]: https://jenkins.symboldev.com/blue/organizations/jenkins/Symbol%2Fgenerated%2Fsymbol%2Fpython/activity?branch=dev\n[sdk-python-lint]: https://jenkins.symboldev.com/buildStatus/icon?job=Symbol%2Fgenerated%2Fsymbol%2Fpython%2Fdev%2F&config=sdk-python-lint\n[sdk-python-build]: https://jenkins.symboldev.com/buildStatus/icon?job=Symbol%2Fgenerated%2Fsymbol%2Fpython%2Fdev%2F&config=sdk-python-build\n[sdk-python-test]: https://jenkins.symboldev.com/buildStatus/icon?job=Symbol%2Fgenerated%2Fsymbol%2Fpython%2Fdev%2F&config=sdk-python-test\n[sdk-python-examples]: https://jenkins.symboldev.com/buildStatus/icon?job=Symbol%2Fgenerated%2Fsymbol%2Fpython%2Fdev%2F&config=sdk-python-examples\n[sdk-python-vectors]: https://jenkins.symboldev.com/buildStatus/icon?job=Symbol%2Fgenerated%2Fsymbol%2Fpython%2Fdev%2F&config=sdk-python-vectors\n[sdk-python-cov]: https://codecov.io/gh/symbol/symbol/branch/dev/graph/badge.svg?token=SSYYBMK0M7&flag=sdk-python\n[sdk-python-cov-link]: https://codecov.io/gh/symbol/symbol/tree/dev/sdk/python\n[sdk-python-package]: https://img.shields.io/pypi/v/symbol-sdk-python\n[sdk-python-package-link]: https://pypi.org/project/symbol-sdk-python\n\nPython SDK for interacting with the Symbol and NEM blockchains.\n\nMost common functionality is grouped under facades so that the same programming paradigm can be used for interacting with both Symbol and NEM.\n\n## Sending a Transaction\n\nTo send a transaction, first create a facade for the desired network:\n\n_Symbol_\n```python\nfrom symbolchain.CryptoTypes import PrivateKey\nfrom symbolchain.facade.SymbolFacade import SymbolFacade\n\n\nfacade = SymbolFacade('testnet')\n```\n\n_NEM_\n```python\nfrom symbolchain.CryptoTypes import PrivateKey\nfrom symbolchain.facade.SymbolFacade import SymbolFacade\n\nfacade = SymbolFacade('testnet')\n````\n\nSecond, describe the transaction using a Python dictionary. For example, a transfer transaction can be described as follows:\n\n_Symbol_\n```python\ntransaction = facade.transaction_factory.create({\n\t'type': 'transfer_transaction_v1',\n\t'signer_public_key': '87DA603E7BE5656C45692D5FC7F6D0EF8F24BB7A5C10ED5FDA8C5CFBC49FCBC8',\n\t'fee': 1000000,\n\t'deadline': 41998024783,\n\t'recipient_address': 'TCHBDENCLKEBILBPWP3JPB2XNY64OE7PYHHE32I',\n\t'mosaics': [\n\t\t{'mosaic_id': 0x7CDF3B117A3C40CC, 'amount': 1000000}\n\t]\n})\n```\n\n_NEM_\n```python\ntransaction = facade.transaction_factory.create({\n\t'type': 'transfer_transaction_v1',\n\t'signer_public_key': 'A59277D56E9F4FA46854F5EFAAA253B09F8AE69A473565E01FD9E6A738E4AB74',\n\t'fee': 0x186A0,\n\t'timestamp': 191205516,\n\t'deadline': 191291916,\n\t'recipient_address': 'TALICE5VF6J5FYMTCB7A3QG6OIRDRUXDWJGFVXNW',\n\t'amount': 5100000\n})\n````\n\nThird, sign the transaction and attach the signature:\n\n\n```python\nprivate_key = PrivateKey('EDB671EB741BD676969D8A035271D1EE5E75DF33278083D877F23615EB839FEC')\nsignature = facade.sign_transaction(facade.KeyPair(private_key), transaction)\n\njson_payload = facade.transactionFactory.attachSignature(transaction, signature)\n```\n\nFinally, send the payload to the desired network using the specified node endpoint:\n\n_Symbol_: PUT `/transactions`\n<br>\n_NEM_: POST `/transaction/announce`\n\n\n## NEM Cheat Sheet\n\nIn order to simplify the learning curve for NEM and Symbol usage, the SDK uses Symbol terminology for shared Symbol and NEM concepts.\nWhere appropriate, NEM terminology is replaced with Symbol terminology, including the names of many of the NEM transactions.\nThe mapping of NEM transactions to SDK descriptors can be found in the following table:\n\n| NEM name (used in docs) | SDK descriptor name|\n|--- |--- |\n| ImportanceTransfer transaction | `account_key_link_transaction_v1` |\n| MosaicDefinitionCreation transaction | `mosaic_definition_transaction_v1` |\n| MosaicSupplyChange transaction | `mosaic_supply_change_transaction_v1` |\n| MultisigAggregateModification transaction | `multisig_account_modification_transaction_v1`<br>`multisig_account_modification_transaction_v2` |\n| MultisigSignature transaction or Cosignature transaction | `cosignature_v1` |\n| Multisig transaction | `multisig_transaction_v1` |\n| ProvisionNamespace transaction | `namespace_registration_transaction_v1` |\n| Transfer transaction | `transfer_transaction_v1`<br>`transfer_transaction_v2` |\n",
    'author': 'Symbol Contributors',
    'author_email': 'contributors@symbol.dev',
    'maintainer': 'Symbol Contributors',
    'maintainer_email': 'contributors@symbol.dev',
    'url': 'https://github.com/symbol/symbol/tree/main/sdk/python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
