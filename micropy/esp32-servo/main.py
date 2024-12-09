from machine import Pin, PWM
import time
import math

motor1 = PWM(Pin(2), freq=50) 
motor2 = PWM(Pin(4), freq=50)  
motor3 = PWM(Pin(16), freq=50) 
motor4 = PWM(Pin(17), freq=50)

# Map the control signal to a PWM duty cycle range
def control_to_duty(ctrl_value, ctrl_min, ctrl_max, pwm_min=25, pwm_max=125):
    # Map `ctrl_value` in range `ctrl_min` to `ctrl_max` into PWM range
    return int(pwm_min + (ctrl_value - ctrl_min) * (pwm_max - pwm_min) / (ctrl_max - ctrl_min))

# Jahnav's function
def gen_controller(f, A00, A11, t0_1, t0_2, t0_3, t0_4, b1, b2, b3, b4):
    def my_controller(t):
        
        j1 = A00 * math.sin(2 * math.pi * (f * t - t0_1)) + b1
        j2 = A11 * math.sin(2 * math.pi * (f * t - t0_2)) + b2
        j3 = A00 * math.sin(2 * math.pi * (f * t - t0_3)) + b3
        j4 = A11 * math.sin(2 * math.pi * (f * t - t0_4)) + b4

        duty1 = control_to_duty(j1, 0, math.pi, 25, 125) 
        duty2 = control_to_duty(j2, -math.pi, math.pi, 25, 125)
        duty3 = control_to_duty(j3, 0, math.pi, 25, 125)
        duty4 = control_to_duty(j4, -math.pi, math.pi, 25, 125)

        motor1.duty(duty1)
        motor2.duty(duty2)
        motor3.duty(duty3)
        motor4.duty(duty4)

        return
    return my_controller

# Define the gait parameters
gait = "walk"

if gait == "walk":
    A00 = 20 * math.pi / 180
    A11 = 20 * math.pi / 180
    f = 1
    t0_1 = 0
    t0_2 = 0.25
    t0_3 = 0.5
    t0_4 = 0.75
    b1 = 70 * math.pi / 180
    b2 = -60 * math.pi / 180
    b3 = 70 * math.pi / 180
    b4 = -60 * math.pi / 180


my_controller = gen_controller(f, A00, A11, t0_1, t0_2, t0_3, t0_4, b1, b2, b3, b4)


try:
    start_time = time.ticks_ms()  # Start time in milliseconds
    while True:
        # Calculate elapsed time in seconds
        t = time.ticks_diff(time.ticks_ms(), start_time) / 1000.0

        # Run the controller at the current time
        my_controller(t)

        # Control loop timing
        time.sleep(1 / 30)  # Match the framerate (30 Hz)

except KeyboardInterrupt:
    # Stop all motors/servos on exit
    motor1.deinit()
    motor2.deinit()
    motor3.deinit()
    motor4.deinit()
