class ColorType:
    
    color: list
    
    message: str
    
    type: str
    
    
class Color:
    
    color: list
    
    type: "Color"
    
    no: int
    
    
class Style:
    
    style: list
    
    type: "Style"
    
    no: int
    

class BackGround:
    
    background: list
    
    type: "BackGround"
    
    no: int


class Black(ColorType, Color):
    
    color = ["\033[30m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 30
    """颜色代号"""
    
    message = "<Black Message>"
    
    type = "Color"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.color[0]}{self.message}{self.color[1]}"
    
    def __str__(self):
        return self()


class Red(ColorType, Color):
    
    color = ["\033[31m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 31
    """颜色代号"""
    
    message = "<Red Message>"
    
    type = "Color"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.color[0]}{self.message}{self.color[1]}"
    
    def __str__(self):
        return self()


class Green(ColorType, Color):
    
    color = ["\033[32m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 32
    """颜色代号"""
    
    message = "<Green Message>"
    
    type = "Color"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.color[0]}{self.message}{self.color[1]}"
    
    def __str__(self):
        return self()


class Yellow(ColorType, Color):
    
    color = ["\033[33m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 33
    """颜色代号"""
    
    message = "<Yellow Message>"
    
    type = "Color"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.color[0]}{self.message}{self.color[1]}"
    
    def __str__(self):
        return self()


class Blue(ColorType, Color):
    
    color = ["\033[34m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 34
    """颜色代号"""
    
    message = "<Blue Message>"
    
    type = "Color"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.color[0]}{self.message}{self.color[1]}"
    
    def __str__(self):
        return self()


class Magenta(ColorType, Color):
    
    color = ["\033[35m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 35
    """颜色代号"""
    
    message = "<Magenta Message>"
    
    type = "Color"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.color[0]}{self.message}{self.color[1]}"
    
    def __str__(self):
        return self()


class Cyan(ColorType, Color):
    
    color = ["\033[36m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 36
    """颜色代号"""
    
    message = "<Cyan Message>"
    
    type = "Color"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.color[0]}{self.message}{self.color[1]}"
    
    def __str__(self):
        return self()


class Grey(ColorType, Color):
    
    color = ["\033[37m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 37
    """颜色代号"""
    
    message = "<Grey Message>"
    
    type = "Color"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.color[0]}{self.message}{self.color[1]}"
    
    def __str__(self):
        return self()


class White(ColorType, Color):
    
    color = ["\033[38m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 38
    """颜色代号"""
    
    message = "<White Message>"
    
    type = "Color"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.color[0]}{self.message}{self.color[1]}"
    
    def __str__(self):
        return self()


class Normal(ColorType, Style):
    
    style = ["\033[0m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 0
    """颜色代号"""
    
    message = "<Normal Message>"
    
    type = "Style"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.style[0]}{self.message}{self.style[1]}"
    
    def __str__(self):
        return self()


class Bold(ColorType, Style):
    
    style = ["\033[1m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 1
    """颜色代号"""
    
    message = "<Bold Message>"
    
    type = "Style"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.style[0]}{self.message}{self.style[1]}"
    
    def __str__(self):
        return self()


class Dim(ColorType, Style):
    
    style = ["\033[2m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 2
    """颜色代号"""
    
    message = "<Dim Message>"
    
    type = "Style"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.style[0]}{self.message}{self.style[1]}"
    
    def __str__(self):
        return self()


class Italic(ColorType, Style):
    
    style = ["\033[3m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 3
    """颜色代号"""
    
    message = "<Italic Message>"
    
    type = "Style"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.style[0]}{self.message}{self.style[1]}"
    
    def __str__(self):
        return self()


class UnderLine(ColorType, Style):
    
    style = ["\033[4m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 4
    """颜色代号"""
    
    message = "<UnderLine Message>"
    
    type = "Style"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.style[0]}{self.message}{self.style[1]}"
    
    def __str__(self):
        return self()


class Blink(ColorType, Style):
    
    style = ["\033[5m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 5
    """颜色代号"""
    
    message = "<Blink Message>"
    
    type = "Style"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.style[0]}{self.message}{self.style[1]}"
    
    def __str__(self):
        return self()


class Reverse(ColorType, Style):
    
    style = ["\033[7m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 7
    """颜色代号"""
    
    message = "<Reverse Message>"
    
    type = "Style"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.style[0]}{self.message}{self.style[1]}"
    
    def __str__(self):
        return self()


class Hidden(ColorType, Style):
    
    style = ["\033[8m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 8
    """颜色代号"""
    
    message = "<Hidden Message>"
    
    type = "Style"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.style[0]}{self.message}{self.style[1]}"
    
    def __str__(self):
        return self()


class StrikeThrough(ColorType, Style):
    
    style = ["\033[9m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 9
    """颜色代号"""
    
    message = "<StrikeThrough Message>"
    
    type = "Style"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.style[0]}{self.message}{self.style[1]}"
    
    def __str__(self):
        return self()


class BlackBackGround(ColorType, BackGround):
    
    background = ["\033[40m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 40
    """颜色代号"""
    
    message = "<Black Message>"
    
    type = "BackGround"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.background[0]}{self.message}{self.background[1]}"
    
    def __str__(self):
        return self()


class RedBackGround(ColorType, BackGround):
    
    background = ["\033[41m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 41
    """颜色代号"""
    
    message = "<Red Message>"
    
    type = "BackGround"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.background[0]}{self.message}{self.background[1]}"
    
    def __str__(self):
        return self()


class GreenBackGround(ColorType, BackGround):
    
    background = ["\033[42m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 42
    """颜色代号"""
    
    message = "<Green Message>"
    
    type = "BackGround"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.background[0]}{self.message}{self.background[1]}"
    
    def __str__(self):
        return self()


class YellowBackGround(ColorType, BackGround):
    
    background = ["\033[43m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 43
    """颜色代号"""
    
    message = "<Yellow Message>"
    
    type = "BackGround"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.background[0]}{self.message}{self.background[1]}"
    
    def __str__(self):
        return self()


class BlueBackGround(ColorType, BackGround):
    
    background = ["\033[44m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 44
    """颜色代号"""
    
    message = "<Blue Message>"
    
    type = "BackGround"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.background[0]}{self.message}{self.background[1]}"
    
    def __str__(self):
        return self()


class MagentaBackGround(ColorType, BackGround):
    
    background = ["\033[45m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 45
    """颜色代号"""
    
    message = "<Magenta Message>"
    
    type = "BackGround"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.background[0]}{self.message}{self.background[1]}"
    
    def __str__(self):
        return self()


class CyanBackGround(ColorType, BackGround):
    
    background = ["\033[46m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 46
    """颜色代号"""
    
    message = "<Cyan Message>"
    
    type = "BackGround"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.background[0]}{self.message}{self.background[1]}"
    
    def __str__(self):
        return self()


class GreyBackGround(ColorType, BackGround):
    
    background = ["\033[47m", "\033[0m"]
    """内置的颜色属性，用于生成颜色"""
    
    no = 47
    """颜色代号"""
    
    message = "<Grey Message>"
    
    type = "BackGround"
    
    def __init__(self, __message):
        self.message = __message if __message else self.message

    def __call__(self):
        return f"{self.background[0]}{self.message}{self.background[1]}"
    
    def __str__(self):
        return self()
