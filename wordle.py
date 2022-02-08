GREEN = '#00FF00'
YELLOW = '#FFFF00'
DARK_GRAY = '#404040'

def square(hex_code: str) -> None:
    hex_code = hex_code.strip('#')
    red = int(hex_code[:2], 16)
    green = int(hex_code[2:4], 16)
    blue = int(hex_code[4:6], 16)

    return f"\033[48:2::{red}:{green}:{blue}m  \033[49m "

if __name__ == "__main__":
    print(square(GREEN) * 5)

