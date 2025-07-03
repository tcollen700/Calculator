from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

class CalculatorApp(App):
    def build(self):
        # Set full screen for Pydroid
        Window.fullscreen = 'auto'
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Display
        self.display = Label(
            text='0',
            font_size=dp(50),
            size_hint=(1, 0.25),
            halign='right',
            valign='center',
            text_size=(Window.width - dp(40), None)
        )
        with self.display.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(pos=self.display.pos, size=self.display.size)
        self.display.bind(size=self._update_rect)
        
        # Button grid - 5 rows, 4 columns with equal width
        button_grid = GridLayout(cols=4, spacing=dp(10), size_hint=(1, 0.75))
        
        # Button definitions (20 buttons)
        buttons = [
            ('C', self.clear, 'light_gray'),
            ('±', self.toggle_sign, 'light_gray'),
            ('%', self.percent, 'light_gray'),
            ('÷', self.set_operation, 'orange'),
            ('7', self.add_digit, 'dark_gray'),
            ('8', self.add_digit, 'dark_gray'),
            ('9', self.add_digit, 'dark_gray'),
            ('×', self.set_operation, 'orange'),
            ('4', self.add_digit, 'dark_gray'),
            ('5', self.add_digit, 'dark_gray'),
            ('6', self.add_digit, 'dark_gray'),
            ('-', self.set_operation, 'orange'),
            ('1', self.add_digit, 'dark_gray'),
            ('2', self.add_digit, 'dark_gray'),
            ('3', self.add_digit, 'dark_gray'),
            ('+', self.set_operation, 'orange'),
            ('0', self.add_digit, 'dark_gray'),
            ('.', self.add_decimal, 'dark_gray'),
            ('⌫', self.backspace, 'light_gray'),
            ('=', self.calculate, 'orange')
        ]
        
        # Create buttons with equal size
        for text, callback, color in buttons:
            btn = Button(
                text=text,
                font_size=dp(30),
                on_press=callback,
                background_normal='',
                background_color=self.get_color(color),
                color=(1,1,1,1) if color != 'light_gray' else (0,0,0,1),
                size_hint=(1, 1)  # Equal size for all buttons
            )
            button_grid.add_widget(btn)
        
        main_layout.add_widget(self.display)
        main_layout.add_widget(button_grid)
        
        # Calculator state
        self.current = '0'
        self.previous = None
        self.operation = None
        self.reset = False
        
        return main_layout
    
    def get_color(self, color_name):
        colors = {
            'orange': (1, 0.6, 0, 1),
            'dark_gray': (0.2, 0.2, 0.2, 1),
            'light_gray': (0.8, 0.8, 0.8, 1)
        }
        return colors.get(color_name, (0.5, 0.5, 0.5, 1))
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def update_display(self):
        self.display.text = self.current
    
    def add_digit(self, instance):
        digit = instance.text
        if self.reset:
            self.current = digit
            self.reset = False
        else:
            self.current = self.current + digit if self.current != '0' else digit
        self.update_display()
    
    def add_decimal(self, instance):
        if '.' not in self.current:
            self.current += '.'
            self.update_display()
    
    def toggle_sign(self, instance):
        self.current = str(-float(self.current)) if self.current != '0' else '0'
        self.update_display()
    
    def percent(self, instance):
        self.current = str(float(self.current) / 100)
        self.update_display()
    
    def backspace(self, instance):
        self.current = self.current[:-1] if len(self.current) > 1 else '0'
        self.update_display()
    
    def clear(self, instance):
        self.current = '0'
        self.previous = None
        self.operation = None
        self.update_display()
    
    def set_operation(self, instance):
        if self.operation and not self.reset:
            self.calculate(instance)
        self.previous = self.current
        self.operation = instance.text
        self.reset = True
    
    def calculate(self, instance):
        if not self.previous or not self.operation:
            return
            
        try:
            a = float(self.previous)
            b = float(self.current)
            
            if self.operation == '+':
                result = a + b
            elif self.operation == '-':
                result = a - b
            elif self.operation == '×':
                result = a * b
            elif self.operation == '÷':
                result = a / b
                
            self.current = str(result)
            self.previous = None
            self.operation = None
            self.reset = True
            self.update_display()
        except:
            self.current = 'Error'
            self.update_display()

if __name__ == '__main__':
    CalculatorApp().run()