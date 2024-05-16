<u>**Groupe de 2 :**</u>
Guillaume TARPIN-BERNARD
Charles CARRÈRE

## Setup

Nécessité d'un compte étudiant pour avoir le role 'LabRole' et l'instance profile 'LabInstanceProfile'.

Mettre à jour les informations de connection à AWS dans ```home/.aws/credentials``` (ctrl+H pour afficher les répertoires cachés), ou via la commande
```bash
aws configure
```

Dans répertoire ```/terraform```

```bash
pipenv sync
pipenv shell
```

Sélectionner l'interpréteur commençant par ```terraform-...```

```bash
cdktf deploy
```

Copier les sorties Terraform correspondantes à l'id du Bucket et celui de la table DynamoDB.

Coller ces valeurs dans les emplacements prévus à cet effet dans le fichier ```main_server.py```.

Dans ```cdktf.json```, changer à la troisième ligne (```"app"```) : ```main_serverless.py``` en ```main_server.py```.

```bash
cdktf deploy
```

Copier la valeur de l'adresse DNS du Load Balancer donnée dans la sortie Terraform.

Coller cette valeur dans le fichier ```webapp/src/index.js``` dans la variable ```axios.defaults.baseURL``` pour indiquer l'adresse de l'API à la Webapp.

Attention il faut bien mettre le ```http://``` au début sinon l'url sera mal interprétée.

Dans ```webapp/```
```bash
npm start
```

Enfin ouvrir le navigateur à l'adresse donnée ([localhost](http://localhost:3000)).