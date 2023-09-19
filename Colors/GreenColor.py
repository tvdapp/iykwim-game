from Colors import ColorStrategy


class GreenColor(ColorStrategy):
    def get_color(self):
        return (0, 255, 0)