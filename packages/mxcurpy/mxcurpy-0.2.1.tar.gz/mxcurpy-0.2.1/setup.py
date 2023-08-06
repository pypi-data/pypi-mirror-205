# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mxcurpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mxcurpy',
    'version': '0.2.1',
    'description': 'Compute CURP and RFC for Mexican Citizens',
    'long_description': '# MXCurpy\n\nGeneración de Clave Única de Registro de Población y el Registro Federal de Contibuyentes de México en Python.\n\nDocumentos en los que está basado este paquete:\n\n**CURP**: [INSTRUCTIVO NORMATIVO PARA LA ASIGNACIÓN DE LA CLAVE ÚNICA DE REGISTRO DE\nPOBLACIÓN](https://github.com/hectorip/mxcurpy/blob/master/docs/dof18102021.pdf)\n\n**RFC**: [Instructivo RFC-2006](https://github.com/hectorip/mxcurpy/blob/master/docs/RFC-2006.pdf). Este es un instructivo antiguo, del 2006, ya que no he encontrado documentos más recientes públicos, pero estoy investigando si hay algún documento normativo que se pueda conseguir. Digamos que el método oficial para conseguir el RFC es siempre preguntándole al Sistema de Administración Tributaria (SAT), también según los documentos oficiales. Si tienes algún documento oficial más reciente, por favor, házmelo saber.\n\n## Estado actual del proyecto\n\nSe puede generar tanto CURP como RFC, pero no se ha probado mucho, por lo que no se puede garantizar que funcione en todos los casos.\n\n## Uso\n\nGeneración de CURP:\n\n```python\nfrom mxcurpy.curp import curp\n\nmy_curp = curp(names="Juan José", lastname="Martínez", second_lastname="Pérez", birth_date="12-08-1989", birth_state="Durango", sex="h")\n\n# MAPJ890812HDGRRN00\n\n```\n\nGeneración de RFC:\n\n```python\nfrom mxcurpy.rfc import rfc\n\nmy_rfc = rfc(\n                "Emma",\n                "Gómez",\n                "Díaz",\n                "31-12-1956"\n            )\n# GODE561231GR8\n```\n\n## Casos excepcionales\n\nSi la persona es nacida en el extranjero, mandar la cadena `"NACIDO EN EL EXTRANJERO"` como estado de nacimiento.\n\n## Limitaciones\n\nAquí describimos algunas limitaciones que tenemos y que probablemente no se arreglen en un futuro cercano (ni lejano).\n\n### CURP\n\nLos dos últimos carácteres al final de la CURP oficial son generados por la entidad de gobierno encargada de asignación de las curps al momento de generarla, con el objetivo de\nevitar duplicados, por lo que no podemos generarlos con seguridad, por eso estos dos carácteres siempre serán `00`.\n\n## Lista de estados válidos\n\nEstados:\n\n* "AGUASCALIENTES"\n* "BAJA CALIFORNIA"\n* "BAJA CALIFORNIA SUR"\n* "CAMPECHE"\n* "COAHUILA"\n* "COLIMA"\n* "CHIAPAS"\n* "CHIHUAHUA"\n* "DISTRITO FEDERAL"\n* "CDMX"\n* "CIUDAD DE MEXICO"\n* "DURANGO"\n* "GUANAJUATO"\n* "GUERRERO"\n* "HIDALGO"\n* "JALISCO"\n* "MEXICO"\n* "MICHOACAN"\n* "MORELOS"\n* "NAYARIT"\n* "NUEVO LEON"\n* "OAXACA"\n* "PUEBLA"\n* "QUERETARO"\n* "QUINTANA ROO"\n* "SAN LUIS POTOSI"\n* "SINALOA"\n* "SONORA"\n* "TABASCO"\n* "TAMAULIPAS"\n* "TLAXCALA"\n* "VERACRUZ"\n* "YUCATAN"\n* "ZACATECAS"\n* "NACIDO EN EL EXTRANJERO"\n* "NE"\n\n## LICENCIA\n\nMIT',
    'author': 'Héctor Iván Patricio Moreno',
    'author_email': 'hectorivanpatriciomoreno@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hectorip/mxcurpy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
