from Colors import ColorStrategy


class RedColor(ColorStrategy):
    def get_color(self):
        return (255, 0, 0)