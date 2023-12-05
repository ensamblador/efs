
# Elastic File System

Este proyecto crea los siguientes recursos dentro de una región de AWS:

* 1 Elastic File System
* 1 EFS access Point
* nuevos Parametros de parameter store:
    * access-point-id
    * file-sytem-id

La idea de este proyecto es contar con un almacenamiento persistente para contenedores en proyectos. 
Se utiliza access-point-id y file-sytem-id para crear un volumen y montarlo en ecs task container.


![Elastic File System](/efs.jpg)

El codigo de la infra está en [`elastic_file_system_stack.py`](./elastic_file_system/elastic_file_system_stack.py)


## Instrucciones para despliegue


Clonar y crear un ambiente virtual python para el proyecto

```zsh
git clone https://github.com/ensamblador/efs.git
cd efs
python3 -m venv .venv
```

En linux o macos el ambiente se activa así:

```zsh
source .venv/bin/activate
```

en windows

```cmd
% .venv\Scripts\activate.bat
```

Una vez activado instalamos las dependencias
```zsh
pip install -r requirements.txt
```

en este punto ya se puede desplegar:

```zsh
cdk deploy
```

y para eliminar:

```zsh
cdk destroy
```


## Otros comandos útiles

 * `cdk synth`       crea un template de cloudformation con los recursos de este proyecto
 * `cdk diff`        compara el stack desplegado con el nuevo estado local

Enjoy!
