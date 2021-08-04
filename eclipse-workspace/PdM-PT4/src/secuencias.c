/** @file secuencias.c
 *  @brief Archivo con definiciones de funciones para el
 *  módulo de secuencias de LEDs para la placa EDU-CIAA
 *
 *  @author Gonzalo N. Vaca <vacagonzalo@gmail.com>
 *  @author Luis I. Minchala <ismael.minchala@ucuenca.edu.ec>
 */

#include "secuencias.h"
#include "led.h"

/** @brief Actualiza el valor de la variable que controla el led que
 * se activa en la secuencia (incrementa su valor si el sentido es
 * ascendente, de lo contrario lo decrementa).
 *
 * Esta función actualiza el valor de la variable que controla el
 * apuntador de los arreglos de leds y tiempos, una vez que se ha
 * ha encendido el led por el tiempo correspondiente. La variable que
 * define la orientación del barrido de los leds determina si el valor
 * del apuntador increta o decrementa su valor.
 *
 *  @param sec es un puntero que pasa por referencia el arreglo
 *  de leds, la posición más reciente de la secuencia, el sentido de
 *  la secuencia, los tiempos de encendido de cada led y la definición
 *  de una estructura de tiempo para el uso de un retardo no bloquente.
 */
void actualizarPosicion(struct Secuencia_t *sec);

void activarSecuencia(struct Secuencia_t *psecuencia, gpioMap_t *leds, tick_t *tiempos, int8_t cuenta)
{
	psecuencia->leds = leds;
	psecuencia->tiempos = tiempos;
	psecuencia->len = cuenta;
	psecuencia->pos = 0;
	psecuencia->sentido = true;
	delayInit(&psecuencia->myDelay, psecuencia->tiempos[psecuencia->pos]);
	apagarLeds();
	encenderLed(psecuencia->leds[psecuencia->pos]);
}

void actualizarSecuencia(struct Secuencia_t *psecuencia)
{
	if (delayRead(&psecuencia->myDelay))
	{
		apagarLeds();
		actualizarPosicion(psecuencia);
		encenderLed(psecuencia->leds[psecuencia->pos]);
		delayWrite(&psecuencia->myDelay, psecuencia->tiempos[psecuencia->pos]);
	}
}

void invertirSecuencia(struct Secuencia_t *psecuencia)
{
	psecuencia->sentido = !psecuencia->sentido;
}

void ascendenteSecuencia(struct Secuencia_t *psecuencia)
{
	psecuencia->sentido = true;
}

void descendenteSecuencia(struct Secuencia_t *psecuencia)
{
	psecuencia->sentido = false;
}

void actualizarPosicion(struct Secuencia_t *sec)
{
	if(sec->sentido) {
		if(sec->pos < (sec->len - 1)) {
			++sec->pos;
		} else {
			sec->pos = 0;
		}
	} else {
		if(sec->pos > 0) {
			--sec->pos;
		} else {
			sec->pos = sec->len - 1;
		}
	}
}
