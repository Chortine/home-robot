import numpy as np

from home_robot.core.interfaces import DiscreteNavigationAction


def print_dict(a_dict):
    print_string = ""
    for key, value in a_dict.items():
        print_string += f'{key.ljust(30, "`")}: {str(value).rjust(20, "`")}\n'
    print(print_string)


class KB_Handler:
    def __init__(self):
        pass

    def main_step(self, env, action):
        raise NotImplementedError

    # @staticmethod
    def keyboard_control_on_env(self, env):
        import time

        from pynput.keyboard import Key, Listener

        def on_press(key):
            if isinstance(key, Key):
                return
            # print(key)
            if key.char == "w":
                # print('w_pressed')
                global w_pressed
                w_pressed = True
            if key.char == "a":
                # print('a_pressed')
                global a_pressed
                a_pressed = True
            if key.char == "s":
                # print('a_pressed')
                global s_pressed
                s_pressed = True
            if key.char == "d":
                # print('a_pressed')
                global d_pressed
                d_pressed = True
            if key.char == "r":
                # print('a_pressed')
                global r_pressed
                r_pressed = True

        def on_release(key):
            if isinstance(key, Key):
                return
            # print(key)
            if key.char == "w":
                # print('w_released')
                global w_pressed
                w_pressed = False
            if key.char == "a":
                # print('a_released')
                global a_pressed
                a_pressed = False
            if key.char == "s":
                # print('a_pressed')
                global s_pressed
                s_pressed = False
            if key.char == "d":
                # print('a_pressed')
                global d_pressed
                d_pressed = False
            if key.char == "r":
                # print('a_pressed')
                global r_pressed
                r_pressed = False

            # print('{0} release'.format(
            #     key))
            if key == Key.esc:
                # Stop listener
                return False

        # Collect events until released

        with Listener(on_press=on_press, on_release=on_release) as listener:
            global w_pressed
            global a_pressed
            global s_pressed
            global d_pressed
            global r_pressed

            w_pressed = False
            a_pressed = False
            s_pressed = False
            d_pressed = False
            r_pressed = False

            env.reset()
            done = False
            steering = 0
            acceleration = 0

            while True:
                pressed = True
                if w_pressed:
                    acceleration += 0.01
                if a_pressed:
                    steering -= 0.1
                if s_pressed:
                    acceleration -= 0.01
                if d_pressed:
                    steering += 0.1
                if r_pressed:
                    env.reset()
                    steering = 0
                    acceleration = 0
                if not (w_pressed or a_pressed or s_pressed or d_pressed):
                    pressed = False

                if not (w_pressed or s_pressed):
                    # all values tend to be zero
                    # print('not pressing')
                    acceleration *= 1 / 4
                    if np.abs(acceleration) < 0.005:
                        acceleration = 0
                if not (a_pressed or d_pressed):
                    steering *= 1 / 2

                steering = np.clip(steering, -1, 1)
                acceleration = np.clip(acceleration, -1, 1)
                # print(f'steering={steering}, acceleration={acceleration}')
                if done:
                    env.reset()
                    steering = 0
                    acceleration = 0

                if pressed:
                    if w_pressed:
                        action = DiscreteNavigationAction.MOVE_FORWARD
                    elif a_pressed:
                        action = DiscreteNavigationAction.TURN_LEFT
                    elif d_pressed:
                        action = DiscreteNavigationAction.TURN_RIGHT
                    elif s_pressed:
                        action = DiscreteNavigationAction.SNAP_OBJECT
                    else:
                        action = DiscreteNavigationAction.EMPTY_ACTION

                else:
                    print("###### no key pressed, apply empty action #######")
                    action = DiscreteNavigationAction.EMPTY_ACTION

                done = self.main_step(env, action)

            listener.join()
            print("aaaaaaaaa")
