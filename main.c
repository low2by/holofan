/**
  ******************************************************************************
  * File Name          : main.c
  * Description        : Main program body
  ******************************************************************************
  *
  * COPYRIGHT(c) 2021 STMicroelectronics
  *
  * Redistribution and use in source and binary forms, with or without modification,
  * are permitted provided that the following conditions are met:
  *   1. Redistributions of source code must retain the above copyright notice,
  *      this list of conditions and the following disclaimer.
  *   2. Redistributions in binary form must reproduce the above copyright notice,
  *      this list of conditions and the following disclaimer in the documentation
  *      and/or other materials provided with the distribution.
  *   3. Neither the name of STMicroelectronics nor the names of its contributors
  *      may be used to endorse or promote products derived from this software
  *      without specific prior written permission.
  *
  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
  * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
  * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
  * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  *
  ******************************************************************************
  */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stm32f0xx_hal.h"

/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
/* Private variables ---------------------------------------------------------*/

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
void Error_Handler(void);

/* USER CODE BEGIN PFP */
/* Private function prototypes -----------------------------------------------*/
/* USER CODE END PFP */

/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

//flag to track stepper movement
volatile uint8_t flag = 1;
	
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration----------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* Configure the system clock */
  SystemClock_Config();

  /* Initialize all configured peripherals */

  /* USER CODE BEGIN 2 */
	
	RCC->AHBENR |= RCC_AHBENR_GPIOBEN;
	RCC->AHBENR |= RCC_AHBENR_GPIOCEN;
	RCC->APB1ENR |= RCC_APB1ENR_I2C2EN;
	
	
	//init LED's
	GPIOC->MODER |= (1 << 12) | (1 << 14) | (1 << 16) | (1 << 18);
	GPIOC->MODER &= ~((1 << 13) | (1 << 15) | (1 << 17) | (1 << 19));
	GPIOC->OTYPER &= ~((1 << 6) | (1 << 7) | (1 << 8) | (1 << 9));
	GPIOC->OSPEEDR &= ~((1 << 12) | (1 << 14) | (1 << 16) | (1 << 18));
	GPIOC->PUPDR &= ~((1 << 12) | (1 << 13) | (1 << 14) | (1 << 15) | (1 << 16) | (1 << 17) | (1 << 18) | (1 << 19));
	
	//set PB11 to alt func mode
	GPIOB->MODER |= (1<<23);
	GPIOB->MODER &= ~(1<<22);
	
	//set PB13 to alt func mode
	GPIOB->MODER |= (1<<27);
	GPIOB->MODER &= ~(1<<26);
	
	//set PB14 to output mode
	GPIOB->MODER &= ~(1<<29);
	GPIOB->MODER |= (1<<28);
	
	//set PC0 to output mode
	GPIOC->MODER &= ~(1<<1);
	GPIOC->MODER |= (1<<0);
	
	//set PB11, PB13 to open drain
	GPIOB->OTYPER |= (1<<11);
	GPIOB->OTYPER |= (1<<13);
	
	//set PB14 to push-pull
	GPIOB->OTYPER &= ~(1<<14);
	
	//set PC0 to push-pull
	GPIOC->OTYPER &= ~(1<<0);
	
	//set PB11 to alt func 1
	GPIOB->AFR[1] |= (1<<12);
	GPIOB->AFR[1] &= ~((1<<13) | (1<<14) | (1<<15));
	
	//set PB13 to alt func 5
	GPIOB->AFR[1] |= (1<<20) | (1<<22);
	GPIOB->AFR[1] &= ~((1<<23) | (1<<21));
	
	//initialize PB14 and PC0 high
	GPIOB->ODR |= (1<<14);
	GPIOC->ODR |= (1<<0);
	
	//set I2C 100kHz
	I2C2->TIMINGR |= (0x1<<28); //PRESC
	I2C2->TIMINGR |= 0x13; //SCLL
	I2C2->TIMINGR |= (0xF<<8); //SCLH
	I2C2->TIMINGR |= (0x2<<16); //SDADEL
	I2C2->TIMINGR |= (0x4<<20); //SCLDEL
	
//	//Set I2C OAR1
//	I2C2->OAR1 |= (1<<15); //enable OAR1
//	I2C2->OAR1 &= ~(1<<10); //7-bit address mode
	
	//disable slave byte control (auto-acknowledge all bytes)
	I2C2->CR1 &= (1<<16);
	
	//enable general call
	I2C2->CR1 &= (1<<19);
	
	//enable addr match interrupt
	I2C2->CR1 |= (1<<3);
	
	//enable I2C2 peripheral
	I2C2->CR1 = I2C_CR1_PE | I2C_CR1_ADDRIE; /* (2) */
	I2C2->OAR1 |= (uint32_t)(0x69 << 1); /* (3) */
	I2C2->OAR1 |= I2C_OAR1_OA1EN; /* (4) */
	
	// initialize PA0 and set to lowspeed, pulldown resistor enabled
	
	RCC ->APB2ENR |= RCC_APB2ENR_SYSCFGCOMPEN; // enable SYSCFG peripheral clock

	GPIOA->MODER &= ~((1<<0) | (1<<1)); 
  GPIOA->OSPEEDR &= ~(1<<0);
	GPIOA->PUPDR |= (1<<1);
	GPIOA->PUPDR &= ~(1<<0);
	
	// enable EXTI interrupt for PA0
	EXTI->IMR |= (1<<0); // enable/unmask interrupt generation
	EXTI->RTSR |= (1<<0); // rising edge trigger
	SYSCFG -> EXTICR[0] &= SYSCFG_EXTICR1_EXTI0_PA; // route PA0 to EXTI0 
	
	// enable and set priority
	__NVIC_EnableIRQ(EXTI0_1_IRQn);
  __NVIC_SetPriority(EXTI0_1_IRQn, 3);
	
	//unset all LED's
	GPIOC->ODR &= ~((1<<9)|(1<<8)|(1<<7)|(1<<6));
	
	RCC->AHBENR |= RCC_AHBENR_GPIOBEN;
	GPIOB->MODER |= (1 << 14) | (1 << 12);
	GPIOB->OTYPER &= ~((1 << 7) | (1 << 6));
	GPIOB->OSPEEDR &= ~((1<<14) | (1 <<12));
	
		
		//set led threshold
//		int32_t threshold = 0x1FFF;
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
  /* USER CODE END WHILE */

  /* USER CODE BEGIN 3 */
		
		
		uint32_t I2C_InterruptStatus = I2C2->ISR; /* Get interrupt status */
		if ((I2C_InterruptStatus & I2C_ISR_ADDR) == I2C_ISR_ADDR)
		{
		 I2C2->ICR |= I2C_ICR_ADDRCF; /* Address match event */
		}
		else if ((I2C_InterruptStatus & I2C_ISR_RXNE) == I2C_ISR_RXNE)
		{
      uint8_t rx_byte = I2C2->RXDR;
			if(flag != 0){
				uint8_t mask = (1<<7);
				//if((uint8_t)(rx_byte & (1<<7)) == (uint8_t)(1<<7)){ // if dir = high
				if((rx_byte & mask) == mask){ // if dir = high
				//if(0x80){ 
					GPIOC->ODR &= ~(1<<8);
					GPIOC->ODR &= ~(1<<7);
					GPIOC->ODR |= (1<<6);
					
					GPIOB->ODR |= (1 << 6);
				}
				else{
					GPIOC->ODR &= ~(1<<8);
	  			GPIOC->ODR |= (1<<7);
  				GPIOC->ODR &= ~(1<<6);
					
					GPIOB->ODR &= ~(1 << 6);
				}
				
				int i;
				uint8_t stepMask = rx_byte & 0x7f;
				
				for(i = 0; i < stepMask; i++)
				{
					GPIOB->ODR |= (1 << 7);
					HAL_Delay(1);
					GPIOB->ODR &= ~(1 << 7);
				}
			}
			else{
				GPIOC->ODR &= ~(1<<8);
				GPIOC->ODR &= ~(1<<7);
				GPIOC->ODR &= ~(1<<6);
			}
			
			
			//Simple test
//		  if (rx_byte == 1)
//		  {
//				GPIOC->ODR &= ~(1<<8);
//				GPIOC->ODR &= ~(1<<7);
//				GPIOC->ODR |= (1<<6);
//		  }
//			else if (rx_byte == 2){
//			 	GPIOC->ODR &= ~(1<<8);
//				GPIOC->ODR |= (1<<7);
//				GPIOC->ODR &= ~(1<<6);
//		  }
//			else if(rx_byte == 3) {
//				GPIOC->ODR |= (1<<8);
//				GPIOC->ODR &= ~(1<<7);
//				GPIOC->ODR &= ~(1<<6);
//			}
		}
  /* USER CODE END 3 */
	}
}

/** System Clock Configuration
*/
void SystemClock_Config(void)
{

  RCC_OscInitTypeDef RCC_OscInitStruct;
  RCC_ClkInitTypeDef RCC_ClkInitStruct;

    /**Initializes the CPU, AHB and APB busses clocks 
    */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = 16;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

    /**Initializes the CPU, AHB and APB busses clocks 
    */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }

    /**Configure the Systick interrupt time 
    */
  HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq()/1000);

    /**Configure the Systick 
    */
  HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);

  /* SysTick_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(SysTick_IRQn, 0, 0);
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @param  None
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler */
  /* User can add his own implementation to report the HAL error return state */
  while(1) 
  {
  }
  /* USER CODE END Error_Handler */ 
}

void EXTI0_1_IRQHandler(void) {
 //GPIOC->ODR ^= (1<<8) | (1<<9) ;
 //uint32_t count = 0;
//while (count != 1500000){
//count += 1;
//}
//GPIOC->ODR ^= (1<<8) | (1<<9) ;
flag = !flag;

EXTI->PR |= (1<<0);
}

#ifdef USE_FULL_ASSERT

/**
   * @brief Reports the name of the source file and the source line number
   * where the assert_param error has occurred.
   * @param file: pointer to the source file name
   * @param line: assert_param error line source number
   * @retval None
   */
void assert_failed(uint8_t* file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
    ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */

}

#endif

/**
  * @}
  */ 

/**
  * @}
*/ 

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
