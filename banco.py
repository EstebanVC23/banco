import tkinter as tk
from tkinter import messagebox
from cuentas import Cliente, Cuenta

class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Bancario")
        self.root.geometry("400x450")

        self.cliente = None
        self.cuenta = None

        self._loginUI()

    def _loginUI(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Nombre").pack()
        self.nombreEntry = tk.Entry(self.frame)
        self.nombreEntry.pack()

        tk.Label(self.frame, text="Cédula").pack()
        self.idEntry = tk.Entry(self.frame)
        self.idEntry.pack()

        tk.Button(self.frame, text="Ingresar", command=self.validarCliente).pack(pady=10)

    def validarCliente(self):
        nombre = self.nombreEntry.get()
        cedula = self.idEntry.get()

        cliente = Cliente(nombre, cedula)

        if not cliente.validarCliente():
            messagebox.showerror("Error", "Cliente no válido")
            return

        self.cliente = cliente
        self.cuenta = Cuenta(cliente.getid())

        self.frame.destroy()
        self._menuUI()

    def _menuUI(self):
        self.menu = tk.Frame(self.root)
        self.menu.pack(pady=20)

        tk.Label(self.menu, text=f"Bienvenido {self.cliente.getname()}").pack(pady=10)

        tk.Button(self.menu, text="Ingreso Ahorro", command=self.ingresoAhorroUI).pack(fill="x")
        tk.Button(self.menu, text="Ingreso Corriente", command=self.ingresoCorrienteUI).pack(fill="x")
        tk.Button(self.menu, text="Retiro Corriente", command=self.retiroCorrienteUI).pack(fill="x")
        tk.Button(self.menu, text="Retiro Ahorro", command=self.retiroAhorroUI).pack(fill="x")
        tk.Button(self.menu, text="Crear CDT", command=self.cdtUI).pack(fill="x")

    def ingresoAhorroUI(self):
        self._montoVentana("Ingreso Ahorro", self.cuenta.ingresoAhorro)

    def ingresoCorrienteUI(self):
        self._montoVentana("Ingreso Corriente", self.cuenta.ingresoCorriente)

    def retiroCorrienteUI(self):
        self._montoVentana("Retiro Corriente", self.cuenta.retiroCorriente)
    
    def retiroAhorroUI(self):
        self._montoVentana("Retiro Ahorro", self.cuenta.retiroAhorro)

    def cdtUI(self):
        win = tk.Toplevel(self.root)
        win.title("Crear CDT")

        tk.Label(win, text="Monto").pack()
        montoEntry = tk.Entry(win)
        montoEntry.pack()

        tk.Label(win, text="Plazo (meses)").pack()
        plazoEntry = tk.Entry(win)
        plazoEntry.pack()

        def crear():
            try:
                monto = float(montoEntry.get())
                plazo = int(plazoEntry.get())
                self.cuenta.ingresoCDT(monto, plazo)
                messagebox.showinfo("Éxito", "CDT creado correctamente")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Crear", command=crear).pack(pady=10)

    def _montoVentana(self, titulo, accion):
        win = tk.Toplevel(self.root)
        win.title(titulo)

        tk.Label(win, text="Monto").pack()
        entry = tk.Entry(win)
        entry.pack()

        def ejecutar():
            try:
                monto = float(entry.get())
                accion(monto)
                messagebox.showinfo("Éxito", "Operación realizada")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Aceptar", command=ejecutar).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()
