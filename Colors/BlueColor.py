from Colors import ColorStrategy


class BlueColor(ColorStrategy):
    def get_color(self):
        return (0, 0, 255)