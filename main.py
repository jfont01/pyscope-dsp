"""
ESTE PROYECTO FUE DESARROLLADO PARA TRABAJAR CON LA BOARD STM32F407 PARA LA MATERIA DSP - FCEFYN - UNC.


Para instalarlo, crear un entorno virtual con Python 3.10 64bits y ejecutar el siguiente comando:
        pip install -r requirements.txt

        
Este proyecto crea una interfaz gráfica de usuario (GUI) utilizando PyQt5 para incrustar un osciloscopio virtual en un widget. 
El osciloscopio es controlado mediante una biblioteca externa (Osc_DLL) y se embebe dentro de un contenedor de la GUI diseñado previamente con Qt Designer. 
Si el puerto virtual recibe la palabra reservada 0xFF, coloca los siguientes self.fft_size muestras en la ventana de matplotlib, las cuales corresponden a la FFT según la lógica definida en el programa del uC.
Librería DLL: https://www.oscilloscope-lib.com/


CONTENIDO DEL PROYECTO:
- Interfaz gráfica (PyQt5) con diseño modular e interactivo
- Integración de osciloscopio virtual en una widget mediante DLL externa
- Calculo en tiempo real de FFT mediante NumPy y visualizacion en un label
- Visualización de FFT enviada por el microcontrolador mediante Matplotlib en un widget
- Detección de picos de frecuencia en la FFT enviada por el microcontrolador y visualizacion en un label
- Envio de comandos al microcontrolador mediante Virtual Com Port
- Sistema multi-hilo para operaciones concurrentes

ESTRUCTURA DEL CODIGO
- Clase MainApp: Gestiona ventana principal y coordinación general
- Clase MplCanvas: Gestiona la ventana de matplotlib para la visualización de la FFT
- Métodos de inicialización: Configuran GUI y componentes
- Handlers de eventos: Gestionan interacción del usuario
- Hilos de ejecución: Lectura serial; serial_thread(). Cálculo de frecuencia de sampling; sampling_thread(). Cálculo de FFT para frecuencia pico; fft_thread()
- Métodos de bajo nivel: Operaciones con ctypes para interacción con el DLL del osciloscopio (extraídos de la biblioteca externa)

Para actualizar los cambios generados en gui.py, ejecutar en el bash del workspace (con el entorno virtual activo) el siguiente comando:
        pyuic5 -x gui.ui -o gui.py


IMPORTANTE: Al actualizar los cambios generados en QtDesigner, es necesario agregar los siguientes atributos dentro del metodo setupUi(self, MainWindow):

        self.checkBox_send.stateChanged.connect(self.send_button_clicked)
        self.checkBox_compute_fir.stateChanged.connect(self.compute_fir_button_clicked)
        self.checkBox_compute_fft.stateChanged.connect(self.compute_fft_button_clicked)
        self.disconnect_port_button.clicked.connect(self.disconnect_port_button_clicked)
        self.connect_port_button.clicked.connect(self.connect_port_button_clicked)
        self.fft_time_update_button.clicked.connect(self.fft_time_update_button_clicked)
        self.update_port_button.clicked.connect(self.update_port_button_clicked)
        self.enlarge_fft_button.clicked.connect(self.enlarge_fft)
        self.checkBox_emulateECG.stateChanged.connect(self.emulateECG_button_clicked)

        
CAMBIOS A REALIZAR:
- REALIZADO en v1.2.0        Añadir una señal de prueba para mostrarla en el osciloscopio.  
- REALIZADO en v1.3.0        Añadir el dato de cantidad de muestras (bytes) recibidas por segundo.
- REALIZADO en v1.4.0        Añadir funcionalidad para seleccionar el puerto COM a utilizar.                               
- REALIZADO en v1.4.0        Añadir funcionalidad para buscar automaticamente los COM disponibles al iniciar el programa.
- REALIZADO en v1.4.1        Corregir que al cerrar la ventana se finalice la ejecucion del programa.
- REALIZADO en v1.5.0        Añadir una conversion a tiempo de la escala horizontal. (usar Multithread)
- REALIZADO en v1.5.0        Añadir un boton para conectar y desconectar el osciloscopio.
- REALIZADO en v2.0.0        Añadir una ventana (con matplotlib, por ejemplo) donde se pueda visualizar la transformada de fourier en el dominio de la frecuencia.
- REALIZADO EN v1.6.0        Agregar funcionalidad de cambiar la frecuencia de muestreo del microcontrolador al enviar un comando por puerto serie.
- REALIZADO EN v1.7.0        Agregar funcionalidad de cambiar el tamaño del buffer del microcontrolador al enviar un comando por puerto serie.
- REALIZADO EN v1.8.0        Corregir problema que a veces se congelan los label de frecuencia de muestreo y escala horizontal al desconectar el puerto. Posible solucion reiniciarlos al desconectar el puerto.
- REALIZADO EN v2.0.0        Comienzo de visualizacion de fft.
- Crear un ejecutable .exe del proyecto.
- Crear un instalador del proyecto(si es necesario).
- Corregir para que al poner el osciloscopio en pantalla completa, el widget ScopeWidget se ajuste al tamaño de la ventana.
- Corregir problema que a veces se congelan los label de frecuencia de muestreo y escala horizontal al desconectar el puerto. Posible solucion reiniciarlos al desconectar el puerto.
- Agregar funcionalidad de actualizar busqueda de puertos (con un boton)
- Agregar documentacion del código con Doxygen, Sphinx o similar. Comentarlo mejor.



Historial de cambios:
Versión 1.0.0:      Versión inicial del programa.
Versión 1.1.0:      Experimental. Se añadió la funcionalidad de actualizar los datos del osciloscopio periódicamente. Método update_oscilloscope
                    Se configura un temporizador para actualizar los datos periódicamente. Revisar viabilidad de multihilos. Revisar fidelidad con señal original.
Versión 1.2.0:      Se agregó el purto COM para leer los datos del puerto serie. Se leen los datos en bytes y se castean a double con ctypes. Se actualiza el osciloscopio con los datos leidos.
                    Se utiliza multithread para leer los datos del puerto serie. Se quitó el temporizador para actualizar los datos del osciloscopio (QTimer). Método read_port().
Version 1.3.0:      Se añadió la funcionalidad de calcular la frecuencia de muestreo en bytes por segundo. Se muestra la frecuencia de muestreo en la consola.
                    Se utiliza Qtimer. Cambiar a multithread con libreria time.
Version 1.3.1:      Se cambio calculate_sampling_frequency(). Ahora se calcula la frecuencia con threading. Se añadió un hilo para calcular la frecuencia de muestreo que se dispara en __init__() junto con el hilo de leer el puerto.
                    Pendiente mostrar esto en la GUI, usando una QLabel.
Version 1.4.0:      Se agrega la funcionalidad de seleccionar el puerto COM a utilizar. Se añade el combobox para seleccionar el puerto COM. Objeto "connect_port_button". Metodos get_available_ports() y connect_port_button_clicked().
                    Queda pendiente agregar boton para desconectar el com.
                    Se agrega el label para mostrar el valor de la frecuencia de muestreo. Obejto "label_sampling_frequency"
                    Queda pendiente hacerlo mas bonito.
Version 1.4.1:      Se corrige el error que no se finalizaba la ejecucion al cerrar la ventana. Se agrega el flag "running" en los threads. En close_event() se detienen los hilos y se cierran los puertos.
Version 1.5.0:      Se agrega la funcionalidad de desconectar el puerto COM utilizado. Se detiene tambien el hilo correspondiente. Metodos "disconnect_port_button_clicked()" y modificaciones a "connect_port_button_clicked()"
                    Se agrega un label de eventos en la esquina inferior derecha. Objeto "label_status"
                    Se agrega la funcionalidad de elegir el baudrate del puerto COM. Objeto "baud_rate"
                    Se agrega el calculo del tiempo de la escala horizontal y se muestra en la GUI. Metodos "calculate_frequency()" y "calculate_scale()"
                    Pendiente crear una funcion "update_gui()" para actualizar la GUI en un solo lugar. Esto hará mas prolijo el código.
Versión 1.5.1:      Se agrega requirements.txt al proyecto.
Versión 1.5.2:      Se agregan comentarios al programa.
Versión 1.5.3:      Se agrega la opcion de baudrate: 2000000.
Versión 1.5.4:      Se cambia la font de los labels de fsampling y escala horizontal. Se emprolijan los imports.
Versión 1.6.0:      Se agregan RadioBoxes para cambiar la frecuencia de sampling enviando comandos al stm32f407. Frecuenas a elegir: 8k, 16k, 22k, 44k, 48k, 96k y 196k.
Versión 1.7.0       Se agregan RadioBoxes para cambiar el tamaño del buffer enviando comandos al stm32f407. Tamaños a elegir: 64, 128, 256, 512, 1024, 2048, 4096. 64 no funciona por algun motivo.
Versión 1.8.0       Se agrega el botón "Actualizar", ligado al metodo "update_port_button_clicked", el cual actualiza la lista de puertos. Se corrige la actualización de los label de frecuencia de muestreo y escala horizontal al desconectar el puerto.
Versión 2.0.0:      Se comienza a trabajar para visualizar la transformada de fourier en el dominio de la frecuencia. Para esto se crea la clase "MplCanvas(FigureCanvas)".
Versión 2.1.0:      Se corrige el tamaño de la ventana graficada en matplotlib. La misma debe ser fft_size/2, ya que la fft es simetrica con parte real e imaginaria. Modificaciones en "plot_fft()"
                    En la ventana que grafica la fft se coloca la escala horizontal en el dominio de la frecuencia. En la misma cada bin es frecuencia_sampling/fft_size.
Versión 2.1.1:      Se agregan comentarios y se emprolija el codigo.
Versión 2.2.0:      Se agregan cambio de frecuencia de actualización de ventana de fft mediante los radioBoxes. Velocidades a elegir = 20ms, 100ms, 250ms, 500ms.
Versión 2.3.0:      Se agrega "enlarge_fft_button" enlazado al metodo "enlarge_fft()", el cual aumenta el tamaño de la ventana de fft, o la vuelve a la normalidad.
Versión 2.4.0:      Se agrega el label "label_freqcueny" para mostrar el valor en frecuencia de la mayor componente de la fft. Se implementa el calculo en "plot_fft()"
Versión 2.5.0:      Se agrega el checkBox "checkBox_compute_fft" para enviar un comando al STM32 para que inicie o detenga el calculo y transmision de la fft.
Versión 2.5.1:      Se agrega la opcion de seleccionar fsampling de 1000Hz. Esto es util para observar los 50Hz al tener el ADC abierto.
Versión 2.5.2:      Se intenta manejar mejor la excepcion en "read_port". No me convence la solucion planteada.
Version 3.0.0:      Se agrega el hilo "fft_worker". El mismo calcula la fft de la señal que el microcontrolador envia a la PC cada 100ms. Se muestra la frecuencia pico a traves del label
                    "label_freqcueny_python".
Version 3.1.0:      Se agrega el checkBox "checkBox_compute_fir" para enviar un comando al STM32 para que inicie o detenga el filtrador FIR.
Version 3.1.1:      Se agrega la seleccion inicial luego del reset de fs = 8kHz y N = 512.
Version 3.1.2:      Se agrega el metodo "threading.Lock()" para ejecutar los hilos. Esto para mayor robustez
Version 3.2.0:      Se agrega el metodo checkBox "checkBox_send" para enviar un comando al STM32 para que inicie o detenga envio de la señal muestreada.
Version 4.0.0:      Se agrega el metodo checkBox "checkBox_emulateECG" para comenzar la simulación de electrocardiograma.





Font Julián - julian.font@mi.unc.edu.ar - 2025
"""

__version__ = "4.0.0"
__author__ = "Font Julián"


import sys, ctypes, serial, threading, time, Osc_DLL, ctypes.wintypes, serial.tools.list_ports,  numpy as np
from PyQt5.QtGui import QWindow  # Clase para manejar ventanas nativas en PyQt5
from PyQt5.QtWidgets import QWidget, QVBoxLayout  # Clases para widgets y diseños en PyQt5
from gui import Ui_MainWindow  # Clase generada automáticamente por Qt Designer que define la interfaz gráfica
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets

class MplCanvas(FigureCanvas):
    """Canvas de Matplotlib personalizado para gráficos FFT"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)




class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Clase principal de la aplicación que gestiona toda la interfaz y lógica    (clase generada automáticamente por Qt Designer).
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Configura la interfaz gráfica generada por Qt Designer

        # Inicialización de variables
        self.osc = Osc_DLL.OscDLL()  # Instancia de la biblioteca del osciloscopio
        self.scope_handle = None  # Identificador del osciloscopio
        self.osc_hwnd = None  # Identificador de ventana del osciloscopio (HWND)

        # Llama al método para inicializar el osciloscopio
        self.init_oscilloscope()

        # Configuración inicial
        self.port = None
        self.running = False
        self.port_connected = None
        self.byte_count = 0
        self.sampling_frequency = 0
        self.horizontal_scale = 0
        self.scale = 0
        self.unit = "mseg/div"
        self.auxiliar = False 
        self.fft_size = 512
        self.fft_array = []
        self.i = 0
        self.cmd = "FS:8000"
        self.fft_collecting = False
        self.sampling_rate = 8000
        self.fft_window_flag = True
        self.data_buffer = []
        self.indexBuffer = 0
        self.data_buffer = [0] * self.fft_size

        # Crear e incrustar el canvas de Matplotlib en fft_widget
        self.fft_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        fft_layout = QtWidgets.QVBoxLayout(self.fft_widget)
        fft_layout.addWidget(self.fft_canvas)
        self.fft_widget.setLayout(fft_layout)

        # Inicializar la gráfica
        self.fft_canvas.axes.set_title("FFT")
        self.fft_canvas.axes.set_xlabel("Frecuencia (Hz)")
        self.fft_canvas.axes.set_ylabel("Magnitud")
        self.fft_canvas.draw()


        self.FS_RadioButton_44k.toggled.connect(self.fs_radio_changed)
        self.FS_RadioButton_22k.toggled.connect(self.fs_radio_changed)
        self.FS_RadioButton_8k.toggled.connect(self.fs_radio_changed)
        self.FS_RadioButton_48k.toggled.connect(self.fs_radio_changed)
        self.FS_RadioButton_16k.toggled.connect(self.fs_radio_changed)
        self.FS_RadioButton_96k.toggled.connect(self.fs_radio_changed)
        self.FS_RadioButton_1k.toggled.connect(self.fs_radio_changed)
        self.FS_RadioButton_196k.toggled.connect(self.fs_radio_changed)

        self.BS_RadioButton_4096.toggled.connect(self.bs_radio_changed)
        self.BS_RadioButton_2048.toggled.connect(self.bs_radio_changed)
        self.BS_RadioButton_1024.toggled.connect(self.bs_radio_changed)
        self.BS_RadioButton_512.toggled.connect(self.bs_radio_changed)
        self.BS_RadioButton_256.toggled.connect(self.bs_radio_changed)
        self.BS_RadioButton_128.toggled.connect(self.bs_radio_changed)
        self.BS_RadioButton_64.toggled.connect(self.bs_radio_changed)

        self.FIR_RadioButton_LP.toggled.connect(self.FIR_radio_changed)
        self.FIR_RadioButton_HP.toggled.connect(self.FIR_radio_changed)
        self.FIR_RadioButton_BP.toggled.connect(self.FIR_radio_changed)
        self.FIR_RadioButton_N.toggled.connect(self.FIR_radio_changed)


        self.byte_count = 0
        self.data = [0,0,0]

        self.get_available_ports()

        self.buffer_lock = threading.Lock()

        
    def fft_worker(self):
        """ Hilo que cada 100 ms procesa la FFT de las últimas fft_size muestras y emite la frecuencia pico """
        while self.running:
            time.sleep(0.1)  # 100 ms de espera
            # Si no hay suficientes muestras, saltar esta iteración

            if len(self.data_buffer) < self.fft_size:
                continue
            
            data_block = np.array(self.data_buffer[-self.fft_size:])
            data_block = data_block - np.mean(data_block)
            fft_result = np.fft.fft(data_block)

            magnitude = np.abs(fft_result)[:self.fft_size // 2]
            peak_index = np.argmax(magnitude)
            peak_frequency = int(peak_index * self.sampling_rate / self.fft_size)
            # Emitir la señal para actualizar el label en el hilo principal
            self.label_freqcueny_python.setText(f"{peak_frequency} Hz")



    def init_oscilloscope(self):
        """
        Inicializa el osciloscopio y lo incrusta en el widget `ScopeWidget` de la GUI.
        """
        try:
            # Crea una instancia del osciloscopio utilizando un archivo de configuración ('scope_1.ini'). Extraido de Osc_DLL_DOC.txt
            self.scope_handle = self.osc.ScopeCreate('scope_1.ini', '1')
            self.osc.ScopeShow(self.scope_handle)  # Muestra el osciloscopio en una ventana externa


            # Encuentra el identificador de ventana (HWND) del osciloscopio
            self.osc_hwnd = self.find_oscilloscope_window("Oscilloscope")
            if not self.osc_hwnd:
                # Si no se encuentra el HWND, lanza un error
                raise RuntimeError("No se pudo obtener el HWND del osciloscopio.")

            # Crea un contenedor para incrustar el osciloscopio en el widget ScopeWidget
            container = QWindow.fromWinId(self.osc_hwnd)  # Convierte el HWND en un objeto QWindow
            embedded_widget = QWidget.createWindowContainer(container, self.ScopeWidget)  # Crea un widget que contiene el QWindow
            layout = QVBoxLayout(self.ScopeWidget)  # Crea un diseño vertical para el widget ScopeWidget
            layout.addWidget(embedded_widget)  # Agrega el widget incrustado al diseño
            self.label_status.setText(f"DLL cargada correctamente")


        except Exception as e:
            # Captura y muestra cualquier error durante la inicialización del osciloscopio
            self.label_status.setText(f"Error al inicializar el osciloscopio: {e}")
            

    def find_oscilloscope_window(self, window_name):
        """
        Encuentra el identificador de la ventana (HWND) de una ventana por su nombre.
        """
        hwnds = []  # Lista para almacenar los HWND encontrados

        # Función de callback que será llamada para cada ventana abierta
        def callback(hwnd, lparam):
            # Obtiene el título de la ventana
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)  # Longitud del título
            buff = ctypes.create_unicode_buffer(length + 1)  # Buffer para almacenar el título
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)  # Obtiene el título
            if window_name in buff.value:  # Si el título contiene el nombre de la ventana buscada
                hwnds.append(hwnd)  # Agrega el HWND a la lista
            return True

        # Enumera todas las ventanas abiertas
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        EnumWindows(EnumWindowsProc(callback), 0)  # Llama a la función `callback` para cada ventana

        # Devuelve el primer HWND encontrado o None si no se encontró
        return hwnds[0] if hwnds else None
    
    def read_port(self):
        while self.running:
            try:
                if self.port and self.port.in_waiting:
                    data = self.port.read(self.port.in_waiting)
                    self.byte_count += len(data)

                    for byte in data:
                        dato = int(byte)

                        # Si se detecta el marcador 255
                        if dato == 0xFF and not self.fft_collecting:
                            # Inicio de bloque FFT: activar recolección y vaciar array
                            self.fft_collecting = True
                            self.fft_array = []
                        elif dato == 0xFF and self.fft_collecting:
                            # Fin de bloque FFT: forzar fin del bloque
                            self.fft_collecting = False
                            self.plot_fft(self.fft_array)
                        elif self.fft_collecting:
                            self.fft_array.append(dato)
                            # Si ya se recolectó el número de muestras esperado, se puede forzar el fin del bloque
                            if len(self.fft_array) >= self.fft_size:
                                self.fft_collecting = False
                                self.plot_fft(self.fft_array)
                        elif not self.fft_collecting:
                            # Procesamiento normal de la señal muestreada (por ejemplo, actualizar osciloscopio)
                            self.data = (ctypes.c_double * 3)(*[0, 0, dato])
                            with self.buffer_lock:
                                self.data_buffer[self.indexBuffer] = self.data[2]
                            self.indexBuffer = (self.indexBuffer + 1) % self.fft_size
                            self.update_oscilloscope()
            except Exception as e:
                self.label_status.setText(f"Error en read_port(): {e}")




    def connect_port_button_clicked(self):
        com = self.ports_list.currentText()
        self.selected_com = com.split(" - ")[0]
        self.byte_count = 0
        self.running = True
        try:
            self.port  = serial.Serial(f"{self.selected_com}", timeout=None, write_timeout=None)
            try:
                self.serial_thread = threading.Thread(target=self.read_port)
                self.serial_thread.start()
                self.sampling_thread = threading.Thread(target=self.calculate_frequency)
                self.sampling_thread.start()
                self.fft_thread = threading.Thread(target=self.fft_worker)
                self.fft_thread.start()
                self.port_connected = self.selected_com
                self.label_status.setText(f"Puerto {self.selected_com} conectado correctamente")
            except Exception as e:
                self.label_status.setText(f"Error al inciar el threading de lectura del puerto {self.selected_com}: {e}")

        except Exception as e:
            self.label_status.setText(f"Error al abrir el puerto {self.selected_com}: {e}")

    def update_port_button_clicked(self):
        self.ports_list.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.ports_list.addItem(f"{port.device} - {port.description}")
        self.label_status.setText("GUI actualizada.")

    def disconnect_port_button_clicked(self):
        self.running = False
        self.byte_count = 0
        if self.port and self.port.is_open:
            try:
                if self.running and self.serial_thread and self.serial_thread.is_alive() and self.sampling_thread and self.sampling_thread.is_alive():
                    self.serial_thread.join()  # Esperar a que el hilo de lectura termine
                    self.sampling_thread.join()  # Esperar a que el hilo de muestreo termine

                self.port.close()
                self.label_status.setText(f"Puerto {self.port_connected} cerrado correctamente.")
            except Exception as e:
                self.label_status.setText(f"Error al cerrar el puerto {self.port_connected}: {e}")
        else:
            self.label_status.setText("No hay puerto COM abierto.")

    def fft_time_update_button_clicked(self):
        fft_time_update = self.fft_time_update_list.currentText()[:-3]
        self.cmd = "FFT:" + fft_time_update
        self.send_command(self.cmd)

    def calculate_frequency(self):
        """
        Calcula la frecuencia de muestreo (bytes recibidos por segundo) y la escala horizontal.
        """
        self.running = True
        while self.running:
            start_time = time.time()
            time.sleep(1)
            elapsed_time = time.time() - start_time  # Tiempo transcurrido en segundos

            if elapsed_time > 0:
                # Calcular frecuencia de muestreo
                self.sampling_frequency = int(self.byte_count / elapsed_time)
                self.byte_count = 0

                # Obtener escala horizontal desde la DLL
                try:
                    self.osc._hllDll.ScopeGetCellSampleSize.argtypes = [ctypes.c_int]
                    self.osc._hllDll.ScopeGetCellSampleSize.restype = ctypes.c_double
                    horizontal_scale = self.osc._hllDll.ScopeGetCellSampleSize(self.scope_handle)
                except Exception as e:
                    print(f"Error al obtener escala horizontal: {e}")
                    horizontal_scale = 0.0

                # Calcular escala y unidad
                self.scale, self.unit = self.calculate_scale(horizontal_scale, self.sampling_frequency)

                # Actualizar la GUI
                if(self.sampling_frequency == 0):
                    self.label_sampling_frequency.setText(f"N/A")
                else:
                    self.label_sampling_frequency.setText(f"{self.sampling_frequency} samples/seg")

                if(self.sampling_frequency == 0):
                    self.label_horizontal_scale.setText(f"N/A")
                else:
                    self.label_horizontal_scale.setText(f"{self.scale} {self.unit}")


    def calculate_scale(self, horizontal_scale, sampling_frequency):
        """
        Calcula la escala horizontal y selecciona la unidad apropiada.
        """
        if sampling_frequency > 0:
            scale_in_s = horizontal_scale / sampling_frequency
            if scale_in_s < 0.001:
                return round(scale_in_s * 1_000_000), "useg/div"
            elif scale_in_s < 1:
                return round(scale_in_s * 1_000), "mseg/div"
            else:
                return round(scale_in_s), "seg/div"
        else:
            return 0, "N/A"



       
    
    def get_available_ports(self):
        """
        Busca todos los puertos COM disponibles y los añade como opciones en el QComboBox (ports_list).
        """
        self.ports_list.clear()  # Limpiar el QComboBox antes de añadir nuevos elementos

        # Obtener todos los puertos disponibles con su descripción
        ports = serial.tools.list_ports.comports()
        for port in ports:
            # Añadir al QComboBox el nombre del puerto y su descripción
            self.ports_list.addItem(f"{port.device} - {port.description}")
        
        if not ports:
            self.ports_list.addItem("No se encontraron puertos disponibles")



    def update_oscilloscope(self):
        """
        Actualiza los datos mostrados en el osciloscopio.
        """
        try:

            # Enviar los datos al osciloscopio
            if self.scope_handle:
                self.osc.ShowNext(self.scope_handle, self.data)
        except Exception as e:
            self.label_status.setText(f"Error al actualizar el osciloscopio: {e}")

            
    def closeEvent(self, event):
        """
        Sobrecarga el evento de cerrar la ventana para liberar recursos del osciloscopio
        y detener los hilos antes de cerrar el programa.
        """
        try:
            # Detener los hilos
            self.running = False  # Señal para detener los hilos
            if self.sampling_thread.is_alive():
                self.sampling_thread.join()  # Esperar a que el hilo termine
            if self.serial_thread and self.serial_thread.is_alive():
                self.serial_thread.join()  # Esperar a que el hilo de lectura termine

            # Cerrar el puerto serie si está abierto
            if self.port and self.port.is_open:
                self.port.close()
                self.label_status.setText(f"Puerto COM cerrado correctamente.")


            # Liberar recursos del osciloscopio
            if self.scope_handle:
                self.osc.ScopeHide(self.scope_handle)
                self.osc.ScopeDestroy(self.scope_handle)
                self.label_status.setText(f"DLL cerrada correctamente")

        except Exception as e:
            self.label_status.setText(f"Error al cerrar recursos: {e}")
        finally:
            # Asegurarse de cerrar completamente la ventana
            event.accept()

    def fs_radio_changed(self, checked):
        """
        Slot que se llama cuando se cambia el estado de algún radio button de frecuencia.
        Solo actuará cuando se active (checked == True).
        """
        if not checked:
            return  # Solo procesamos cuando el radio button se activa.
        
        if self.FS_RadioButton_44k.isChecked():
            self.cmd = "FS:44000"
            self.sampling_rate = 44000
        elif self.FS_RadioButton_22k.isChecked():
            self.cmd = "FS:22000"
            self.sampling_rate = 22000
        elif self.FS_RadioButton_8k.isChecked():
            self.cmd = "FS:8000"
            self.sampling_rate = 8000
        elif self.FS_RadioButton_48k.isChecked():
            self.cmd = "FS:48000"
            self.sampling_rate = 48000
        elif self.FS_RadioButton_1k.isChecked():
            self.cmd = "FS:1000"
            self.sampling_rate = 1000
        elif self.FS_RadioButton_16k.isChecked():
            self.cmd = "FS:16000"
            self.sampling_rate = 16000
        elif self.FS_RadioButton_96k.isChecked():
            self.cmd = "FS:96000"
            self.sampling_rate = 96000
        elif self.FS_RadioButton_196k.isChecked():
            self.cmd = "FS:196000"
            self.sampling_rate = 196000
        else:
            return
        
        self.send_command(self.cmd)

    def FIR_radio_changed(self, checked):
        """
        Slot que se llama cuando se cambia el estado de algún radio button de filtro FIR.
        Solo actuará cuando se active (checked == True).
        """
        if not checked:
            return  # Solo procesamos cuando el radio button se activa.
        
        if self.FIR_RadioButton_LP.isChecked():
            self.cmd = "f_fir:0"
        elif self.FIR_RadioButton_HP.isChecked():
            self.cmd = "f_fir:1"
        elif self.FIR_RadioButton_BP.isChecked():
            self.cmd = "f_fir:2"
        elif self.FIR_RadioButton_N.isChecked():
            self.cmd = "f_fir:3"
        else:
            return
        
        self.send_command(self.cmd)

    def bs_radio_changed(self, checked):
        """
        Slot que se llama cuando se cambia el estado de algún radio button de Buffer Size.
        Solo actuará cuando se active (checked == True).
        """
        if not checked:
            return  # Solo procesamos cuando el radio button se activa.
        

        if self.BS_RadioButton_4096.isChecked():
            self.cmd = "BS:4096"
        elif self.BS_RadioButton_2048.isChecked():
            self.cmd = "BS:2048"
        elif self.BS_RadioButton_1024.isChecked():
            self.cmd = "BS:1024"
        elif self.BS_RadioButton_512.isChecked():
            self.cmd = "BS:512"
        elif self.BS_RadioButton_256.isChecked():
            self.cmd = "BS:256"
        elif self.BS_RadioButton_128.isChecked():
            self.cmd = "BS:128"
        elif self.BS_RadioButton_64.isChecked():
            self.cmd = "BS:64"
        else:
            return
        
        self.fft_size = int(self.cmd.split(":")[1])
        with self.buffer_lock:
            self.data_buffer = [0] * self.fft_size
        self.indexBuffer = 0

        self.send_command(self.cmd)

    def emulateECG_button_clicked(self):
        """Envía comando al STM32 para activar/desactivar la simulacion de ECG"""
        if self.checkBox_emulateECG.isChecked():  #Verifica estado actual
            self.cmd = "ECG:1"
        else:
            self.cmd = "ECG:0"
        
        self.send_command(self.cmd)

    def compute_fft_button_clicked(self):
        """Envía comando al STM32 para activar/desactivar el cálculo de FFT"""
        if self.checkBox_compute_fft.isChecked():  #Verifica estado actual
            self.cmd = "FFT:1"
        else:
            self.cmd = "FFT:0"
        
        self.send_command(self.cmd)

    def compute_fir_button_clicked(self):
        """Envía comando al STM32 para activar/desactivar el filtro FIR"""
        if self.checkBox_compute_fir.isChecked():  # Verifica estado actual
            self.cmd = "FIR:1"
        else:
            self.cmd = "FIR:0"
        
        self.send_command(self.cmd)

    def send_button_clicked(self):
        """Envía comando al STM32 para activar/desactivar el envio de la señal muestreada"""
        if self.checkBox_send.isChecked():  # <-- Verifica estado actual
            self.cmd = "SEND:1"
        else:
            self.cmd = "SEND:0"
        
        self.send_command(self.cmd)


    def enlarge_fft(self):
        # Ocultar y/o remuever el ScopeWidget del layout
        if self.fft_window_flag == True:
            self.fft_widget.setGeometry(QtCore.QRect(10, 0, 1201, 871))
            self.ScopeWidget.setGeometry(QtCore.QRect(1230, 0, 591, 481))
            self.ScopeWidget.show()
            self.fft_widget.show()
            self.label_status.setText("Se ha cambiado Osciloscopio por FFT")
        else:
            self.fft_widget.setGeometry(QtCore.QRect(1230, 0, 591, 481))
            self.ScopeWidget.setGeometry(QtCore.QRect(10, 0, 1201, 871))
            self.ScopeWidget.show()
            self.fft_widget.show()
            self.label_status.setText("Se ha cambiado FFT por Osciloscopio")

        self.fft_window_flag^= True

    def send_command(self, cmd):
        """
        Envía un comando al microcontrolador mediante el puerto serial.
        """
        if self.port and self.port.is_open:
            try:
                self.port.write(cmd.encode())
                self.label_status.setText(f"Comando enviado: {cmd}")
            except Exception as e:
                self.label_status.setText(f"Error al enviar comando: {e}")
        else:
            self.label_status.setText("Puerto no conectado.")

    def plot_fft(self, fft_data):

        self.fft_canvas.axes.clear()
        # Convertir la lista a array de numpy
        fft_data = np.array(fft_data)


        # Obtener el sampling rate del comando; convertir a entero
        freqs = np.linspace(0, self.sampling_rate / 2, len(fft_data), endpoint=False)        
        self.fft_canvas.axes.set_ylim(0, 1)
        self.fft_canvas.axes.plot(freqs, fft_data/255)
        self.fft_canvas.axes.set_title("FFT")
        self.fft_canvas.axes.set_xlabel("Frecuencia (Hz)")
        self.fft_canvas.axes.set_ylabel("Magnitud")
        self.fft_canvas.draw()

        peak_index = np.argmax(fft_data)
        peak_frequency = round(peak_index * (self.sampling_rate / (self.fft_size*2)))

        self.label_freqcueny.setText(f"{peak_frequency} Hz")



if __name__ == "__main__":
    # Punto de entrada de la aplicación
    # Crea una aplicación de PyQt5
    app = QtWidgets.QApplication(sys.argv)
    # Crea una instancia de la ventana principal
    main_window = MainApp()
    # Muestra la ventana principal
    main_window.show()
    # Inicia el bucle principal de la aplicación
    sys.exit(app.exec_())
