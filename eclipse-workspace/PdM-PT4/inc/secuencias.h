/** @file secuencias.h
 *  @brief Prototipos de funciones de secuencias de los leds
 *  de la placa EDU-CIAA.
 *
 *  Este archivo contiene los prototipos de funciones que
 *  se usan para controlar secuencias de los leds de la placa
 *  EDU-CIAA. Este archivo fue realizado en el marco de la
 *  especialización en sistemas embebidos de la Universidad
 *  de Buenos Aires
 *
 *  @author Gonzalo N. Vaca <vacagonzalo@gmail.com>
 *  @author Luis I. Minchala <ismael.minchala@ucuenca.edu.ec>
 */

#ifndef _SECUENCIAS_H_
#define _SECUENCIAS_H_

#include "macros.h"

/** Estructura de secuencia de LEDs
 *
 */
struct Secuencia_t
{
	gpioMap_t *leds;
	int8_t pos;
	bool_t sentido;
	tick_t *tiempos;
	delay_t myDelay;
	int8_t len;
};

/** @brief Función que activa una secuencia específca de leds
 *
 *  Esta función activa una secuencia de encendido de leds. Mantiene
 *  encendido un led por vez y al paso de la secuencia apaga todos los
 *  leds para activar un nuevo led direccionado por un puntero.
 *
 *  @param psecuencia es un puntero que pasa por referencia el arreglo
 *  de leds, la posición más reciente de la secuencia, el sentido de
 *  la secuencia, los tiempos de encendido de cada led y la definición
 *  de una estructura de tiempo para el uso de un retardo no bloquente.
 *
 *  @param leds corresponde al arreglo de leds que forman parte de la
 *  secuencia.
 *
 *  @param tiempos corresponde al arreglo de tiempos que permance encen-
 *  dido cada led de la secuencia.
 *
 *  @param cuenta corresponde a la longitud de los arreglos leds o tiempos.
 */
void activarSecuencia(struct Secuencia_t *psecuencia, gpioMap_t *leds, tick_t *tiempos, int8_t cuenta);

/** @brief Actualiza el valor de la secuencia si se cumple el tiempo
 * de retardo no bloqueante asociado a cada led del arreglo.
 *
 *  Esta función consulta la función de retardo no bloqueante
 *  delayRead(myDelay). Cuando se cumple el tiempo asociado a un led
 *  del arreglo, se actualizan los punteros del control de secuencia
 *  con los siguientes valores de led a encender y el tiempo asociado.
 *
 *  @param psecuencia es un puntero que pasa por referencia el arreglo
 *  de leds, la posición más reciente de la secuencia, el sentido de
 *  la secuencia, los tiempos de encendido de cada led y la definición
 *  de una estructura de tiempo para el uso de un retardo no bloquente.
 */
void actualizarSecuencia(struct Secuencia_t *psecuencia);

/** @brief Cambia el sentido del barrido de los leds de la secuencia.
 *
 *  Esta función cambia el valor de la variable <<sentido>> que controla
 *  la dirección de barrido de los leds de la placa EDU-CIAA.
 *
 *  @param psecuencia es un puntero que pasa por referencia el arreglo
 *  de leds, la posición más reciente de la secuencia, el sentido de
 *  la secuencia, los tiempos de encendido de cada led y la definición
 *  de una estructura de tiempo para el uso de un retardo no bloquente.
 */
void invertirSecuencia(struct Secuencia_t *psecuencia);

/** @brief Fija del valor del sentido del barrido de los leds en forma
 * ascendente.
 *
 *  @param psecuencia es un puntero que pasa por referencia el arreglo
 *  de leds, la posición más reciente de la secuencia, el sentido de
 *  la secuencia, los tiempos de encendido de cada led y la definición
 *  de una estructura de tiempo para el uso de un retardo no bloquente.
 */
void ascendenteSecuencia(struct Secuencia_t *psecuencia);

/** @brief Fija del valor del sentido del barrido de los leds en forma
 * descendente.
 *
 *  @param psecuencia es un puntero que pasa por referencia el arreglo
 *  de leds, la posición más reciente de la secuencia, el sentido de
 *  la secuencia, los tiempos de encendido de cada led y la definición
 *  de una estructura de tiempo para el uso de un retardo no bloquente.
 */
void descendenteSecuencia(struct Secuencia_t *psecuencia);


#endif /* _SECUENCIAS_H_ */
