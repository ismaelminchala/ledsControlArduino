#include "pdm_tp4.h"
#include "sapi.h"
#include "semaforo.h"
int main( void )
{
	boardInit();
	while( true ) {
		launch();
	}
	return 0;
}
