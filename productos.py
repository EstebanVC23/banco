import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
import random

class ProductoBancario(ABC):
    archivo = "Cuentas.json"

    def __init__(self, idCliente):
        self.idCliente = str(idCliente)

        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump({}, f, indent=4)

    @abstractmethod
    def ingreso(self, monto):
        pass

    def _leer_json(self):
        with open(self.archivo, "r") as f:
            return json.load(f)

    def _guardar_json(self, data):
        with open(self.archivo, "w") as f:
            json.dump(data, f, indent=4)


class CuentaAhorro(ProductoBancario):
    tipo = "ahorro"
    tasaMensual = 0.006

    def ingreso(self, monto):
        data = self._leer_json()

        if self.idCliente not in data:
            data[self.idCliente] = {}

        if self.tipo not in data[self.idCliente]:
            ahora = datetime.now()
            data[self.idCliente][self.tipo] = {
                "saldo": monto,
                "fechaCreacion": ahora.isoformat(),
                "ultimoInteres": ahora.isoformat()
            }
        else:
            self.aplicar_interes(data)
            data[self.idCliente][self.tipo]["saldo"] += monto

        self._guardar_json(data)
        
    def retiro(self, monto):
        data = self._leer_json()

        if self.idCliente not in data or self.tipo not in data[self.idCliente]:
            raise Exception("La cuenta ahorro no existe")

        if monto > data[self.idCliente][self.tipo]["saldo"]:
            raise Exception("Fondos insuficientes")

        data[self.idCliente][self.tipo]["saldo"] -= monto
        self._guardar_json(data)
        

    def aplicar_interes(self, data):
        cuenta = data[self.idCliente][self.tipo]

        fechaUltimo = datetime.fromisoformat(cuenta["ultimoInteres"])
        ahora = datetime.now()

        meses = (ahora.year - fechaUltimo.year) * 12 + (ahora.month - fechaUltimo.month)

        if meses > 0:
            cuenta["saldo"] *= (1 + self.tasaMensual) ** meses
            cuenta["ultimoInteres"] = ahora.isoformat()



class CuentaCorriente(ProductoBancario):
    tipo = "corriente"

    def ingreso(self, monto):
        data = self._leer_json()

        if self.idCliente not in data:
            data[self.idCliente] = {}

        if self.tipo not in data[self.idCliente]:
            data[self.idCliente][self.tipo] = {
                "saldo": 0,
                "fechaCreacion": datetime.now().isoformat()
            }

        data[self.idCliente][self.tipo]["saldo"] += monto
        self._guardar_json(data)

    def retiro(self, monto):
        data = self._leer_json()

        if self.idCliente not in data or self.tipo not in data[self.idCliente]:
            raise Exception("La cuenta corriente no existe")

        if monto > data[self.idCliente][self.tipo]["saldo"]:
            raise Exception("Fondos insuficientes")

        data[self.idCliente][self.tipo]["saldo"] -= monto
        self._guardar_json(data)


class CDT(ProductoBancario):
    tipo = "cdt"

    def __init__(self, idCliente, plazoMeses):
        super().__init__(idCliente)
        self.plazoMeses = plazoMeses

    def ingreso(self, monto):
        data = self._leer_json()

        if self.idCliente not in data:
            data[self.idCliente] = {}

        ahora = datetime.now()

        if self.tipo in data[self.idCliente]:
            cdt = data[self.idCliente][self.tipo]
            fechaCreacion = datetime.fromisoformat(cdt["fechaCreacion"])

            mesesTranscurridos = (
                (ahora.year - fechaCreacion.year) * 12 +
                (ahora.month - fechaCreacion.month)
            )

            if mesesTranscurridos < cdt["plazoMeses"]:
                raise Exception("El CDT aún no ha vencido")

            self._liquidar_cdt(data)

        tasa = random.uniform(0.05, 0.20)

        data[self.idCliente][self.tipo] = {
            "saldo": monto,
            "fechaCreacion": ahora.isoformat(),
            "plazoMeses": self.plazoMeses,
            "tasaInteres": tasa
        }

        self._guardar_json(data)

    def liquidar_cdt(self, data):
        cdt = data[self.idCliente][self.tipo]

        saldoFinal = cdt["saldo"] * (1 + cdt["tasaInteres"])

        if "corriente" not in data[self.idCliente]:
            data[self.idCliente]["corriente"] = {
                "saldo": 0,
                "fechaCreacion": datetime.now().isoformat()
            }

        data[self.idCliente]["corriente"]["saldo"] += saldoFinal

        del data[self.idCliente][self.tipo]
