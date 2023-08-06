# Biblioteca customizada para testes automatizados com robotframework

A finalidade deste documento é a de passar informações das funções e keywords que estão sendo entregues.

## 🔧 Instalação
	$ pip install via-hub-logistic

## 🚀 Keywords:
**Microsoft Azure**
  ```robotframework
    *** Settings ***
    $  Library    via_hub_logistc.keywords.kws_microsoft.ViaAzure
  ```
  - *Azure Connect Blob Server*<br>
    *&nbsp;Create connect with microsoft blob server*
    
    >&nbsp;*Parameters:*<br>
    >&ensp;**host: str**<br>
    >&emsp;A url used for connect blob server<br>
    >&ensp;**account_name: str**<br>
    >&emsp;A username for connect account server<br>
    >&ensp;**account_key: str** <br>
    >&emsp;A access token the account<br>
      
    >&nbsp;*Returns:*<br>
    >&ensp;*blob connect server or none for a search with no result*<br>
 
  - *Azure List All Directories In Container*<br>
    *&nbsp;A list all directories in container*
    
    >&nbsp;*Parameters:*<br>
    >&ensp;**connection: blob connect server**<br>
    >&emsp;A connect blob server<br>
    >&ensp;**container_name: str**<br>
    >&emsp;A name the of container in blob server<br>
    >&ensp;**folder: str** <br>
    >&emsp;A name the of folder for list as container<br>
    >&ensp;**format: bolean, optional** <br>
    >&emsp;Default false for return o path name the folder, true for return o full path name with folder <br>      

    >&nbsp;*Returns:*<br>
    >&ensp;*List json with all directories in a container or none for a search with no result*<br>

  - *Azure Is Exist Directory In Container*<br>
    *&nbsp;Is check if directory exist in container*
    
    >&nbsp;*Parameters:*<br>
    >&ensp;**connection: blob connect server**<br>
    >&emsp;A connect blob server<br>
    >&ensp;**container_name: str**<br>
    >&emsp;A name the of container in blob server<br>
    >&ensp;**folder: str** <br>
    >&emsp;A name the of folder for list as container<br>
    >&ensp;**directory: str** <br>
    >&emsp;Default false for return o path name the folder, true for return o full path name with folder <br>      

    >&nbsp;*Returns:*<br>
    >&ensp;*True if the folder exists in the container or False if the folder not exist in container*<br>

**Ibm Db2**

  ```robotframework
    *** Settings***
    $  Library    via_hub_logistc.keywords.kws_db2.ViaDb2
  ```
  - *Db2 Connect To Dataase*<br>
    *&nbsp;Create connect with BD2*
    
    >&nbsp;*Parameters:*<br>
    >&ensp;**host: str**<br>
    >&emsp;A url used for connect db2 database<br>
    >&ensp;**db_name: str**<br>
    >&emsp;A name the of database<br>
    >&ensp;**user_id: str** <br>
    >&emsp;A name the of connect db2<br>
    >&ensp;**password: str** <br>
    >&emsp;A password the of connect db2<br>      

    >&nbsp;*Returns:*<br>
    >&ensp;*Db2 connect server or none for a search with no result*<br>


  - *Db2 Execute Query*<br>
    *&nbsp;Execute query in BD2*
    
    >&nbsp;*Parameters:*<br>
    >&ensp;**connection: Db2 connect server**<br>
    >&emsp;A connect db2 server<br>
    >&ensp;**query: str**<br>
    >&emsp;Query which will be used in the search<br>

    >&nbsp;*Returns:*<br>
    >&ensp;*List json or  none for a search with no result*<br>

**Mongodb**

  ```robotframework
    *** Settings***
    $  Library    via_hub_logistc.keywords.kws_mongodb.ViaMongo
  ```
  - *Mongo Connect To Database*<br>
    *&nbsp;Create connect with mongobd*
    
    >&nbsp;*Parameters:*<br>
    >&ensp;**strConnction: str**<br>
    >&emsp;A url used for connect db2 database<br>

    >&nbsp;*Returns:*<br>
    >&ensp;*Mongo connect server or none for a search with no result*<br>

  - *Mongo Disconnect To Database*<br>
    *&nbsp;Disconnect connect mongobd*
    
    >&nbsp;*Parameters:*<br>
    >&ensp;**client: Mongo connect server**<br>
    >&emsp;A url used for connect db2 database<br>

    >&nbsp;*Returns:*<br>
    >&ensp;*NONE no result*<br>

  - *Mongo Find All*<br>
    *&nbsp;Execute search all elements in collection in mongodb*
    
    >&nbsp;*Parameters:*<br>
    >&ensp;**client: Mongo connect server**<br>
    >&emsp;A url used for connect db2 database<br>
    >&ensp;**baseName: str**<br>
    >&emsp;A name the of database<br>
    >&ensp;**collectionName: str** <br>
    >&emsp;A name the collection<br>

    >&nbsp;*Returns:*<br>
    >&ensp;*List json or list empty for a search with no result*<br>

  - *Mongo Execute Query*<br>
    *&nbsp;Execute search elements in collection by query in mongodb*
    
    >&nbsp;*Parameters:*<br>
    >&ensp;**client: Mongo connect server**<br>
    >&emsp;A url used for connect db2 database<br>
    >&ensp;**baseName: str**<br>
    >&emsp;A name the of database<br>
    >&ensp;**collectionName: str** <br>
    >&emsp;A name the collection<br>
    >&ensp;**query: dict** <br>
    >&emsp;A name the collection<br>

    >&nbsp;*Returns:*<br>
    >&ensp;*List json or none for a search with no result*<br>

**Text**

  ```robotframework
    *** Settings***
    $  Library    via_hub_logistc.keywords.kws_text.ViaText
  ```
  - *Cut Text*<br>
    *&nbsp;cut in string*
    
    >&nbsp;*Parameters:*<br>
    >&ensp;**text:str**<br>
    >&emsp;A text current<br>
    >&ensp;**lengh: int**<br>
    >&emsp;size limit caracteres for split<br>

    >&nbsp;*Returns:*<br>
    >&ensp;*String cut according to the size entered*<br>
