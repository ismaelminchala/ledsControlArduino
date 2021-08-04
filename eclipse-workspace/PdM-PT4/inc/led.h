/** @file led.h
 *  @brief Archivo con los prototipos de funciones del módulo de control
 *  para los LEDs de la placa EDU-CIAA
 * 
 *  @author Gonzalo N. Vaca <vacagonzalo@gmail.com>
 *  @author Luis I. Minchala <ismael.minchala@ucuenca.edu.ec>
 */

#ifndef _LED_H_
#define _LED_H_

#include "macros.h"

#define OSCURIDAD 0

/** @brief Función que apaga todos los LEDs de la placa EDU-CIAA
 * 
 *  La función intentará apagar los LEDs de la placa y luego
 *  verificará que la acción fue exitosa para cada uno de los
 *  LEDs de la placa EDU-CIAA
 * 
 *  @return Indicador del éxito de la operación
 */
bool_t apagarLeds(void);

/** @brief Función que enciende el LED indicado
 * 
 *  La función verificará que el LED ingresado sea válido,
 *  luego intentará encenderlo y reportará si la operación
 *  fue exitosa
 * 
 *  @param led LED que se desea encender
 *  @return Indicador del éxito de la operación
 */
bool_t encenderLed(gpioMap_t led);

#endif /* _LED_H_ */
