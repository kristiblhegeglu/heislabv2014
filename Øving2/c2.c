#include <pthread.h>
#include <stdio.h>

int i = 0;
pthread_mutex_t lock;

// Note the return type: void*
void* adder(){
	
	for(int x = 0; x < 1000000; x++){
		pthread_mutex_lock(&lock);
        	i++;
		pthread_mutex_unlock(&lock);
	}
	return NULL;
}

void* subtract(){
	for(int x = 0; x < 1000000; x++){
		pthread_mutex_lock(&lock);
		i--;
		pthread_mutex_unlock(&lock);
	}
	return NULL;
}


int main(){
	pthread_mutex_init(& lock, NULL);
	pthread_t adder_thr;
	pthread_t subtract_thr;
	pthread_create(&adder_thr, NULL, adder, NULL);
	pthread_create(&subtract_thr, NULL, subtract, NULL);
	for(int x = 0; x < 50; x++){
		printf("%i\n", i);
	}

    
	pthread_join(adder_thr, NULL);
	pthread_join(subtract_thr, NULL);
	printf("Done: %i\n", i);
	pthread_mutex_destroy(&lock);
	return 0;    
}
