#este se le tira a python shell_plus
from ventas.comunes import *
import datetime
ini=datetime.datetime(2015, 7, 03, 00, 05, 00, 287280)
fin=datetime.datetime(2015, 7, 03, 17, 05, 00, 287280)
mv=get_ventas(ini,fin)
mv
for i in  connection.queries:
    print i["sql"]
