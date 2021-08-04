/** @file teclas.c
 *  @brief Archivo con definiciones de funciones para la MEF
 *  que habilita el control anti-rebote del pulso de una tecla en
 *  la placa EDU-CIAA.
 *
 *  @author Gonzalo N. Vaca <vacagonzalo@gmail.com>
 *  @author Luis I. Minchala <ismael.minchala@ucuenca.edu.ec>
 */
#include "teclas.h"

#define TIME_GUARD 20

/** @brief Esta función resuelve las acciones correspondientes al
 *  flanco descendente.
 *
 *  @param tecla es un puntero que pasa por referencia la tecla que se
 *  requiere evaluar, una estructura de tiempo no bloqueante y una variable
 *  que contiene el valor del estado más reciente.
 */
void buttonPressed(struct Tecla_t *tecla);

/** @brief Esta función resuelve las acciones correspondientes al
 *  flanco ascendente.
 *
 *  @param tecla es un puntero que pasa por referencia la tecla que se
 *  requiere evaluar, una estructura de tiempo no bloqueante y una variable
 *  que contiene el valor del estado más reciente.
 */
void buttonReleased(struct Tecla_t *tecla);

void inicializarMEF(struct Tecla_t *tecla, gpioMap_t pin)
{
	delayInit(&tecla->delay, TIME_GUARD);
	tecla->estado = UP;
	tecla->tecla = pin;
}

void actualizarMEF(struct Tecla_t *tecla)
{
	switch(tecla->estado)
	{
	case UP:
		if(!gpioRead(tecla->tecla)) {
			tecla->estado = FALLING;
		}
		break;
	case FALLING:
		buttonPressed(tecla);
		break;
	case DOWN:
		if(gpioRead(tecla->tecla)) {
			tecla->estado = RISING;
		}
		break;
	case RISING:
		buttonReleased(tecla);
		break;
	default:
		gpioWrite(LEDR,ON);
    }
}

void buttonPressed(struct Tecla_t *tecla)
{
	if(delayRead(&tecla->delay)) {
		if(!gpioRead(tecla->tecla)) {
			tecla->estado = DOWN;
		} else {
			tecla->estado = UP;
		}
		delayWrite(&tecla->delay, TIME_GUARD);
	}
}

void buttonReleased(struct Tecla_t *tecla)
{
	if(delayRead(&tecla->delay)) {
		if(!gpioRead(tecla->tecla)) {
			tecla->estado = DOWN;
		} else {
			tecla->estado = UP;
		}
		delayWrite(&tecla->delay, TIME_GUARD);
	}
}


