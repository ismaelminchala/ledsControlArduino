/** @file semaforo.c
 *  @brief Archivo con definiciones de funciones para la operación de un semáforo
 *  usando definición de máquina de estados finita.
 *
 *  @author Gonzalo N. Vaca <vacagonzalo@gmail.com>
 *  @author Luis I. Minchala <ismael.minchala@ucuenca.edu.ec>
 */

#include "semaforo.h"
#include "macros.h"
#include "led.h"
#include "teclas.h"
#include "secuencias.h"

/** Definición de la variable enumerada <estados> que contiene los siguientes
 * estados asociados a la operación del sistema: i) normal; ii) desconectado; y,
 * iii) alarma.
 */
enum estados{normal, desconectado, alarma};

/** @brief Activa la funcionalidad de operación normal del semáforo. Adicionalmente,
 *         verifica la pulsación de una tecla de la placa EDU-CIAA para actualizar
 *         el estado hacia <desconectado>
 *
 *  @param control es un puntero que pasa por referencia el arreglo
 *  de leds, la posición más reciente de la secuencia, el sentido de
 *  la secuencia, los tiempos de encendido de cada led y la definición
 *  de una estructura de tiempo para el uso de un retardo no bloquente.
 *
 *  @param boton es una variable que almacena el estado de la tecla de la placa
 *  EDU-CIAA, a cargo de la actualización del estado del semáforo.
 */
enum estados semaforoNormal(struct Secuencia_t *control, enum estadoMEF boton);

/** @brief Activa la funcionalidad de operación en moddo desconectdado del semáforo.
 *         Adicionalmente, verifica la pulsación de una tecla de la placa EDU-CIAA
 *         para actualizar el estado hacia <alarma>
 *
 *  @param control es un puntero que pasa por referencia el arreglo
 *  de leds, la posición más reciente de la secuencia, el sentido de
 *  la secuencia, los tiempos de encendido de cada led y la definición
 *  de una estructura de tiempo para el uso de un retardo no bloquente.
 *
 *  @param boton es una variable que almacena el estado de la tecla de la placa
 *  EDU-CIAA, a cargo de la actualización del estado del semáforo.
 */
enum estados semaforoDesconectado(struct Secuencia_t *control, enum estadoMEF boton);

/** @brief Activa la funcionalidad de operación en moddo desconectdado del semáforo.
 *         Adicionalmente, verifica la pulsación de una tecla de la placa EDU-CIAA
 *         para actualizar el estado hacia <normal>
 *
 *  @param control es un puntero que pasa por referencia el arreglo
 *  de leds, la posición más reciente de la secuencia, el sentido de
 *  la secuencia, los tiempos de encendido de cada led y la definición
 *  de una estructura de tiempo para el uso de un retardo no bloquente.
 *
 *  @param boton es una variable que almacena el estado de la tecla de la placa
 *  EDU-CIAA, a cargo de la actualización del estado del semáforo.
 */
enum estados semaforoAlarma(struct Secuencia_t *control, enum estadoMEF boton);

int launch( void )
{
	enum estados estado;
	estado = normal;
	const gpioMap_t ledsNormal[] = {LED3, LED1, LED2};
	const tick_t tiemposNormal[] = {3000, 500, 1000};
	const int8_t countNormal = _countof(ledsNormal);
	struct Secuencia_t controlNormal;
	activarSecuencia(&controlNormal, &ledsNormal, &tiemposNormal, countNormal);

	const gpioMap_t ledsDesconectado[] = {LED1, OSCURIDAD};
	const tick_t tiemposDesconectado[] = {500, 500};
	const int8_t countDesconectado = _countof(ledsDesconectado);
	struct Secuencia_t controlDesconectado;
	activarSecuencia(&controlDesconectado, &ledsDesconectado, &tiemposDesconectado, countDesconectado);

	const gpioMap_t ledsAlarma[] = {LED2, OSCURIDAD};
	const tick_t tiemposAlarma[] = {500, 500};
	const int8_t countAlarma = _countof(ledsAlarma);
	struct Secuencia_t controlAlarma;
	activarSecuencia(&controlAlarma, &ledsAlarma, &tiemposAlarma, countAlarma);

	struct Tecla_t tecla;
	inicializarMEF(&tecla, TEC2);

	while( true ) {
	switch ( estado ){
		case normal:
			estado = semaforoNormal(&controlNormal, tecla.estado);
			break;
		case desconectado:
			estado = semaforoDesconectado(&controlDesconectado, tecla.estado);
			break;
		case alarma:
			estado = semaforoAlarma(&controlAlarma, tecla.estado);
			break;
		}
	actualizarMEF(&tecla);
	}
	return 0;
}

enum estados semaforoNormal(struct Secuencia_t *control, enum estadoMEF boton){
	enum estados estado = normal;
	if (boton == DOWN){
		estado = desconectado;
	}
	actualizarSecuencia(control);
	return estado;
}

enum estados semaforoDesconectado(struct Secuencia_t *control, enum estadoMEF boton){
	enum estados estado = desconectado;
	if (boton == DOWN){
		estado = alarma;
	}
	actualizarSecuencia(control);
	return estado;
}

enum estados semaforoAlarma(struct Secuencia_t *control, enum estadoMEF boton){
	enum estados estado = alarma;
	if (boton == DOWN){
		estado = normal;
	}
	actualizarSecuencia(control);
	return estado;
}
