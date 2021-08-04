/** @file macros.h
 *  @brief Bibliotecas comunes de los módulos y macros útiles
 * 
 *  Este archivo contiene las macros más comunes a utilizar en el
 *  programa, además se agregan las bibliotecas comunes a todos los
 *  módulos con el fin de reducir el tamaño de los archivos
 * 
 *  @author Gonzalo N. Vaca <vacagonzalo@gmail.com>
 *  @author Luis I. Minchala <ismael.minchala@ucuenca.edu.ec>
 */

#ifndef _MACROS_H_
#define _MACROS_H_

#include "sapi.h"

/** @brief Obtiene el tamaño de un array
 */
#define _countof(_Array) (sizeof(_Array) / sizeof(_Array[0]))

#endif /* _MACROS_H_ */