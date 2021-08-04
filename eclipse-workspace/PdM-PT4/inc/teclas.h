/** @file secuencias.h
 *  @brief Prototipos de funciones asociadas a una máquina de
 *  estados finitos para el control del anti-rebote en la pulsación
 *  de las teclas de la placa EDU-CIAA.
 *
 *  @author Gonzalo N. Vaca <vacagonzalo@gmail.com>
 *  @author Luis I. Minchala <ismael.minchala@ucuenca.edu.ec>
 */

#ifndef PROGRAMS_PDM_TP4_INC_TECLAS_H_
#define PROGRAMS_PDM_TP4_INC_TECLAS_H_

#include "sapi.h"

enum estadoMEF {UP, DOWN, FALLING, RISING};

struct Tecla_t {
	gpioMap_t tecla;
	delay_t delay;
	enum estadoMEF estado;
};

/** @brief Esta función inicializa la máquina de estados finita (MEF)
 * asociada a la operación del anti-rebote de una tecla. Los estados
 * de la MEF son: i) UP; ii) DOWN; iii) FALLING; y, iv) RISING.
 *
 *  La función inicializa la estructura <tecla> con los parámetros de
 *  ingreso.
 *
 *  @param tecla es un puntero que pasa por referencia la tecla que se
 *  requiere evaluar, una estructura de tiempo no bloqueante y una variable
 *  que contiene el valor del estado más reciente.
 *
 *  @param pin corresponde a la tecla que se requiere evaluar y controlar
 *  el anti-rebote.
 */
void inicializarMEF(struct Tecla_t *tecla, gpioMap_t pin);

/** @brief Esta función actualiza el estadio de la máquina de estados finita (MEF)
 * asociada a la operación del anti-rebote de una tecla. Esta función activa la operación
 * de la MEF de acuerdo con los siguientes estados: i) UP; ii) DOWN; iii) FALLING; y,
 * iv) RISING.
 *
 *  La función inicializa la estructura <tecla> con los parámetros de
 *  ingreso.
 *
 *  @param tecla es un puntero que pasa por referencia la tecla que se
 *  requiere evaluar, una estructura de tiempo no bloqueante y una variable
 *  que contiene el valor del estado más reciente.
 */
void actualizarMEF(struct Tecla_t *tecla);

#endif 
