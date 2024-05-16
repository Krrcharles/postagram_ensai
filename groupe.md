<u>**Groupe de 2 :**</u>
Guillaume TARPIN-BERNARD
Charles CARRERE

## Setup

Dans répertoire ```Terraform/```

```bash
pipenv sync
pipenv shell
```

selectionner l'interpréteur commençant par ```Terraform....```

```bash
cdktf deploy -a python3 main_serverless.py
```

Copier les sorties Terraform correspondantes à l'id du Bucket et celui de la table DynamoDB

Coller ces valeurs dans les emplacements prévus à cet effet dans le fichier ```main_server.py```

```bash
cdktf deploy -a python3 main_server.py
```

Copier la valeur de l'adresse DNS du loadbalancer donnée dans la sortie Terraform

Coller cette valeur dans le fichier ```webapp/src/index.js``` dans la variable ```axios.defaults.baseURL``` pour indiquer l'adresse de l'API à la Webapp

Dans ```webapp/```
```bash
npm start
```