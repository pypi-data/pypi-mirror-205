# GamepadX

A Python package to read and emulate an Xbox controller

## Requirements

This package is only available on Windows 10 and later operating systems.

You will need to download the [ViGEm Bus Driver](https://github.com/ViGEm/ViGEmBus/releases/latest) to emulate a controller.

You must have Python >= 3.11

## Installation

```powershell
pip install gamepadx
```
## Usage

```python
from time import sleep

from gamepadx import Gamepad, VirtualGamepad
from gamepadx.commons import XInputButtons, XInputThumbs, XInputTriggers


def main():
    gamepad = Gamepad()

    gamepad.update()

    print(gamepad.is_button_pressed(XInputButtons.A))
    print(gamepad.get_trigger_value(XInputTriggers.RIGHT))
    print(gamepad.get_thumb_value(XInputThumbs.RIGHT_X))

    virtual_gamepad = VirtualGamepad()

    virtual_gamepad.press_button(XInputButtons.A)
    virtual_gamepad.release_button(XInputButtons.B)
    virtual_gamepad.set_trigger_value(XInputTriggers.LEFT, 0.2)
    virtual_gamepad.set_thumb_value(XInputThumbs.LEFT_X, 0.8)

    virtual_gamepad.update()

    sleep(1)

    virtual_gamepad.reset()
    virtual_gamepad.update()


if __name__ == "__main__":
    main()
```

## Contributing

If you would like to contribute to GamepadX, please ensure that your code follows the [Black](https://github.com/psf/black) style guide and [isort](https://github.com/PyCQA/isort) import order and submit a pull request on GitHub. Don't forget to add unwanted files and folders to the `.gitignore`

## Acknowledgements

- [Xbox Controller Mapper](https://github.com/izdwuut/xbox-mapper-tutorial)
- [Virtual Gamepad](https://github.com/yannbouteiller/vgamepad)
- [ViGEm Bus Driver](https://github.com/ViGEm/ViGEmBus)