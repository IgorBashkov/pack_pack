import tkinter as tk
from tkinter import ttk
from test_port import ComPort


class MainWindow:
    def __init__(self, root):
        root.title('Orders')
        self.root = root
        self.opts = Options(root)
        self.opts.grid(row=0, column=0, padx=10, pady=10)
        self.info = InfoWindow(root, self.opts)
        self.info.grid(row=1, column=0, padx=10, pady=10)


class Options(ttk.Frame):
    def __init__(self, root):
        super().__init__(master=root, width=300, height=150)
        self.com_port = None
        self.ports = ComPort.available_ports()
        self.chosen_port = tk.StringVar()
        self.chosen_spd_port = tk.IntVar()
        self.port_lbl = ttk.Label(self, text='Chose port:')
        self.ports_cmb = ttk.Combobox(self,
                                      values=self.ports,
                                      textvariable=self.chosen_port
                                      )
        self.port_lbl.grid(row=0, column=0, padx=10, pady=10)
        self.ports_cmb.grid(row=1, column=0, padx=10, pady=10)
        self.ports_cmb.bind('<<ComboboxSelected>>', lambda x: print(self.chosen_port.get()))

        self.port_spd_lbl = ttk.Label(self, text='Chose port speed:')
        self.port_speed_cmb = ttk.Combobox(self,
                                           values=ComPort.speeds,
                                           textvariable=self.chosen_spd_port
                                           )
        self.port_spd_lbl.grid(row=0, column=1, padx=10, pady=10)
        self.port_speed_cmb.grid(row=1, column=1, padx=10, pady=10)
        self.port_speed_cmb.bind('<<ComboboxSelected>>',
                                 lambda x: print(self.chosen_spd_port.get()))

        self.connect_btn = ttk.Button(self, text='Connect', command=self.connect)
        self.connect_btn.grid(column=2, row=0)

        self.disconnect_btn = ttk.Button(self, text='Disconnect', command=self.disconnect)
        self.disconnect_btn.grid(column=2, row=1)

    def connect(self):
        self.com_port = ComPort(port=self.chosen_port.get(),
                                speed=self.chosen_spd_port.get(),
                                timeout=200,
                                )

    def disconnect(self):
        self.com_port.close()


class InfoWindow(ttk.Frame):

    def __init__(self, root, opts):
        super().__init__(master=root, width=300, height=150)
        self.root = root
        self.opts = opts
        self.get_code_btn = ttk.Button(self, text='Get QR', command=self.get_code)
        self.get_code_btn.grid(column=0, row=0)
        self.data = []

        self.packer_lbl = ttk.Label(self, text='Packer')
        self.packer_lbl.grid(column=0, row=1)

        self.number_packer = tk.StringVar()
        self.packer_lbl = ttk.Label(self, text='Packer')
        self.packer_lbl.grid(column=0, row=1)
        self.number_packer_lbl = ttk.Label(self, textvariable=self.number_packer)
        self.number_packer_lbl.grid(column=0, row=2)

        self.number_order = tk.StringVar()
        self.order_lbl = ttk.Label(self, text='Order')
        self.order_lbl.grid(column=1, row=1)
        self.number_order_lbl = ttk.Label(self, textvariable=self.number_order)
        self.number_order_lbl.grid(column=1, row=2)
        header = ['Number', 'Content', 'Date', 'Choose']
        data = [
            ['1', 'matrices', '20/10/2020'],
            ['2', 'clamps', '20/10/2020'],
            ['3', 'forceps', '20/10/2020'],
            ['4', 'ring', '20/10/2020'],
        ]
        self.data_table = ShowTable(root, header=header, data=data)
        self.data_table.grid(columnspan=1, row=3)

    def get_code(self):
        self.data = self.opts.com_port.get_content()
        self.number_packer.set(self.data[0])
        self.number_order.set(self.data[1])
        print(self.data)


class ShowTable(ttk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(master=root, width=300, height=40)
        self.header = kwargs['header']
        self.data = kwargs['data']
        self.choice = tk.StringVar()
        for line, pos in enumerate(self.header):
            ttk.Label(self, text=pos, width=10).grid(row=0, column=line)
        for i, line in enumerate(self.data):

            for j, val in enumerate(line):
                ttk.Label(self, text=val).grid(row=i + 1, column=j)
            ttk.Radiobutton(self, variable=self.choice, value=line[0]).grid(row=i + 1, column=len(line))
