# holofan

The purpose of this mini project was to demonstrate what we have learned in this embedded systems class. We decided to combine it with our senior project prototype that we created for ECE3992. Our prototype was designed to have a webcam detect the user's face and rotate the stepper motor connected to our designed base to move our display monitor. In this mini project, we had to reimplement some parts to satisfy the requirements for this class. The three milestones that we were able to accomplish  succesfully included GPIO, Interrupt, and I2C. The parts we needed to implement this project include the STM32F0 board, Raspberry Pi, stepper motor, stepper motor hat, webcam, and a monitor. The stm32 board is connected to the stepper motor hat that transmits data with I2C as well as the Pi. We used OpenCV to help us implement facial tracking written in python on the Pi. Unfortunately the design of our prototype with a monitor is too heavy for our stepper motor to properly spin, so our demonstration only shows the stepper rotating based on the location of the user instead of actually having the monitor rotate as well. 

Shown below is the schematic for our final electrical design
![alt text](https://raw.githubusercontent.com/low2by/holofan/main/figs/diagram_battery.png)

Shown below is the flow chart for our software.
