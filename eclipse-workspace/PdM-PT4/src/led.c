/** @file led.c
 *  @brief Archivo con las definiciones de funciones del módulo de control
 *  para los LEDs de la placa EDU-CIAA
 * 
 *  @author Gonzalo N. Vaca <vacagonzalo@gmail.com>
 *  @author Luis I. Minchala <ismael.minchala@ucuenca.edu.ec>
 */

#include "led.h"

const gpioMap_t EDU_CIAA_LEDS[] = {LED1, LED2, LED3, LEDR, LEDG, LEDB, OSCURIDAD};
const int8_t EDU_CIAA_LEDS_COUNT = _countof(EDU_CIAA_LEDS);

bool_t apagarLeds(void)
{
	for (int8_t i = 0; i < EDU_CIAA_LEDS_COUNT; ++i)
	{
		gpioWrite(EDU_CIAA_LEDS[i], OFF);
	}
	for (int8_t i = 0; i < EDU_CIAA_LEDS_COUNT; ++i)
	{
		if (gpioRead(EDU_CIAA_LEDS[i]))
			return false;
	}
	return true;
}

bool_t encenderLed(gpioMap_t led)
{
	if (led == OSCURIDAD){
		return true;
	}
	bool_t state = false;
	for (int8_t i = 0; i < EDU_CIAA_LEDS_COUNT; ++i)
	{
		if (led == EDU_CIAA_LEDS[i])
		{
			state = true;
			break;
		}
	}
	if (!state)
	{
		return false;
	}
	return gpioWrite(led, ON);
}
