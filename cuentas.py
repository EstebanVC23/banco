from productos import CuentaAhorro, CuentaCorriente, CDT

import json

class Cliente:
    def __init__(self, name, id):
        self.name = name
        self.id = str(id)

    def _cedulaValida(self):
        if not self.id.isdigit():
            return False

        if not (6 <= len(self.id) <= 10):
            return False

        if self.id[0] == "0":
            return False

        if len(set(self.id)) == 1:
            return False

        return True

    def validarCliente(self):
        if not self._cedulaValida():
            return False

        with open("Clientes.json", "r") as f:
            clientes = json.load(f)

        if self.id not in clientes:
            return False

        return clientes[self.id]["nombre"] == self.name

    def crearCuenta(self):
        if not self._cedulaValida():
            raise Exception("Cédula no válida")

        with open("Cuentas.json", "r") as f:
            data = json.load(f)

        if self.id in data:
            raise Exception("El cliente ya tiene cuenta")

        data[self.id] = {
            "ahorro": {},
            "corriente": {},
            "cdt": {}
        }

        with open("Cuentas.json", "w") as f:
            json.dump(data, f, indent=4)

    def getid(self):
        return self.id

    def getname(self):
        return self.name

    def setid(self, id):
        self.id = str(id)

    def setname(self, name):
        self.name = name


class Cuenta:
    def __init__(self, idCliente):
        self.idCliente = idCliente
        self.cuentaAhorro = CuentaAhorro(idCliente)
        self.cuentaCorriente = CuentaCorriente(idCliente)
        self.cdt = None

    def crearCDT(self, monto, plazoMeses):
        self.cdt = CDT(self.idCliente, plazoMeses)
        self.cdt.ingreso(monto)

    def ingresoAhorro(self, monto):
        self.cuentaAhorro.ingreso(monto)

    def ingresoCorriente(self, monto):
        self.cuentaCorriente.ingreso(monto)

    def retiroCorriente(self, monto):
        self.cuentaCorriente.retiro(monto)
        
    def retiroAhorro(self, monto):
        self.cuentaAhorro.retiro(monto)

    def ingresoCDT(self, monto, plazoMeses):
        self.crearCDT(monto, plazoMeses)
