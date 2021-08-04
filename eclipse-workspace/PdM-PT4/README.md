# PdM - Práctica 4 (MEF)

_Este proyecto implementa un modelo de máquina de estados finita (MEF) para la operación de una emulación de un semáforo simple_

## Condiciones de funcionamiento

Dependencias externas:
* sAPI.h
* Usar retrasos no bloqueantes

Mira **Deployment** para conocer como desplegar el proyecto.

### Módulos de software del sistema

* pdm_tp4.c, pdm_tp4.h (este es el main)
* secuencias.c, secuencias.h
* led.c, led.h
* teclas.c, teclas.h
* semaforo.c, semaforo.h

### Descripción del funcionamiento

Las descripción de cada módulo de software es la siguiente:

* main: ejecuta la lógica de alto nivel para activar la MEF asociada a la operación del semáforo. En este caso en particular, se desarrollan secuencias asociadas a la operación de un semáforo con tres modos de operación (normal, desconectado y alarma).

* secuencias: este módulo implementa funciones que configuran, inician y actualizan secuencias de leds de acuerdo a parámetros asociados a arreglos de LEDs y tiempos de encendido de cada LED del arreglo.

* led: este módulo implementa funciones asociadas al control de los LEDs de la placa EDU-CIAA.

* teclas: este módulo implementa funciones asociadas a la lectura de los estados de las teclas de la placa EDU-CIAA. Este módulo de software implementa una MEF que permite habilitar el anti-rebote que implica la pulsación de una tecla. Los estados de la MEF asociada al anti-rebote son: i) UP; ii) DOWN; iii) FALLING; y iv) RISING.

Los modos de operación de las secuencias de LEDs que implementa la MEF asociada a un semáforo simple son:

Normal: secuencia de leds: rojo 3 s, amarillo 500 ms, verde 1s, rojo.
Desconectado: led amarillo intermitente cada 500 ms.
Alarma: rojo intermitente cada 1 s


### Instalación 🔧

_Es recomendable clonar el repositorio usando el siguiente comando_

_Dí cómo será ese paso_

```
git clone https://github.com/vacagonzalo/PdM-TP4.git  
```

Luego, desde la plataforma [Eclipse] compilar y descargar a la placa EDU-CIAA. Finalmente, comprobar el funcionamiento usando la TECLA1 de la placa.


## Autores ✒️


* **Gonzalo N. Vaca** - (vacagonzalo@gmail.com)
* **Luis I. Minchala** - (ismael.minchala@ucuenca.edu.ec) 