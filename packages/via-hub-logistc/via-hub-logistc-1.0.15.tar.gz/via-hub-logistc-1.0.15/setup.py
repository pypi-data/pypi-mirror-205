# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['via_hub_logistc',
 'via_hub_logistc.core',
 'via_hub_logistc.keyword',
 'via_hub_logistc.model']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'via-hub-logistc',
    'version': '1.0.15',
    'description': 'This project is intended to be a facilitator for new developments for test automation',
    'long_description': '# Biblioteca customizada para testes automatizados com robotframework\n\nA finalidade deste documento é a de passar informações das funções e keywords que estão sendo entregues.\n\n## 🔧 Instalação\n\t$ pip install via-hub-logistic\n\n## 🚀 Keywords:\n**Microsoft Azure**\n  ```robotframework\n    *** Settings ***\n    $  Library    via_hub_logistc.keywords.kws_microsoft.ViaAzure\n  ```\n  - *Azure Connect Blob Server*<br>\n    *Create connect with microsoft blob server*\n    \n    >&nbsp;*Parameters:*<br>\n    >&ensp;**host: str**<br>\n    >&emsp;A url used for connect blob server<br>\n    >&ensp;**account_name: str**<br>\n    >&emsp;A username for connect account server<br>\n    >&ensp;**account_key: str** <br>\n    >&emsp;A access token the account<br>\n      \n    >&nbsp;*Returns:*<br>\n    >&ensp;*blob connect server or none for a search with no result*<br>\n \n  - *Azure List All Directories In Container*<br>\n    *A list all directories in container*\n    \n    >&nbsp;*Parameters:*<br>\n    >&ensp;**connection: blob connect server**<br>\n    >&emsp;A connect blob server<br>\n    >&ensp;**container_name: str**<br>\n    >&emsp;A name the of container in blob server<br>\n    >&ensp;**folder: str** <br>\n    >&emsp;A name the of folder for list as container<br>\n    >&ensp;**format: bolean, optional** <br>\n    >&emsp;Default false for return o path name the folder, true for return o full path name with folder <br>      \n\n    >&nbsp;*Returns:*<br>\n    >&ensp;*List json with all directories in a container or none for a search with no result*<br>\n\n  - Azure Is Exist Directory In Container\n    *Is check if directory exist in container*\n    \n    >&nbsp;*Parameters:*<br>\n    >&ensp;**connection: blob connect server**<br>\n    >&emsp;A connect blob server<br>\n    >&ensp;**container_name: str**<br>\n    >&emsp;A name the of container in blob server<br>\n    >&ensp;**folder: str** <br>\n    >&emsp;A name the of folder for list as container<br>\n    >&ensp;**directory: str** <br>\n    >&emsp;Default false for return o path name the folder, true for return o full path name with folder <br>      \n\n    >&nbsp;*Returns:*<br>\n    >&ensp;*True if the folder exists in the container or False if the folder not exist in container*<br>\n\n**Ibm Db2**\n\n  ```robotframework\n    *** Settings***\n    $  Library    via_hub_logistc.keywords.kws_db2.ViaDb2\n  ```\n  - Db2 Connect To Dataase\n    *Create connect with BD2*\n    \n    >&nbsp;*Parameters:*<br>\n    >&ensp;**host: str**<br>\n    >&emsp;A url used for connect db2 database<br>\n    >&ensp;**db_name: str**<br>\n    >&emsp;A name the of database<br>\n    >&ensp;**user_id: str** <br>\n    >&emsp;A name the of connect db2<br>\n    >&ensp;**password: str** <br>\n    >&emsp;A password the of connect db2<br>      \n\n    >&nbsp;*Returns:*<br>\n    >&ensp;*Db2 connect server or none for a search with no result*<br>\n\n\n  - Db2 Execute Qury\n    *Execute query in BD2*\n    \n    >&nbsp;*Parameters:*<br>\n    >&ensp;**connection: Db2 connect server**<br>\n    >&emsp;A connect db2 server<br>\n    >&ensp;**query: str**<br>\n    >&emsp;Query which will be used in the search<br>\n\n    >&nbsp;*Returns:*<br>\n    >&ensp;*List json or  none for a search with no result*<br>\n\n**Mongodb**\n\n  ```robotframework\n    *** Settings***\n    $  Library    via_hub_logistc.keywords.kws_mongodb.ViaMongo\n  ```\n  - Mongo Connect To Database\n\t  > Return conncection with mongoDB<br>\n    > Params:<br>\n    > - **strConnction**:  string connection :: *str*<br>\n\n  - Mongo Disconnect To Database\n\t  > Execute a disconnection with the server <br>\n    > Params:<br>\n    > - **client**: connection :: *Connection*<br>\n\n  - Mongo Find All\n\t  > Returns one json or list the json result <br>\n    > Params:<br>\n    > - **client**: connection :: *Connection*<br>\n    > - **baseName**: name the database :: *str*<br>\n    > - **collectionName**: name the collection:: *str*<br>\n\n  - Mongo Find By Parameter\n\t  > Returns one json or list the json result by parameter <br>\n    > Params:<br>\n    > - **client**: connection :: *Connection*<br>\n    > - **baseName**: name the database :: *str*<br>\n    > - **collectionName**: name the collection:: *str*<br>\n    > - **query**: Query which will be used in the search:: *dict*<br>\n\n**Mongodb**\n\n  ```robotframework\n    *** Settings***\n    $  Library    via_hub_logistc.keywords.kws_text.ViaText\n  ```\n  - Split Text\n\t  > Return text divide<br>\n    > Params:<br>\n    > - **text**:  text :: *str*<br>\n    > - **lengh**:  size limit caracteres :: *int*<br>',
    'author': 'Jaderson Macedo',
    'author_email': 'jaderson.macedo@viavarejo.com.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
