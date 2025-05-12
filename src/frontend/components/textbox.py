import pygame

class TextBox:
    def __init__(self, x, y, width, font, color, background_color=None):
        """
        Initialize the text wrapper
        
        Parameters:
            x, y (int): Position of the text box
            width (int): Maximum width before wrapping
            font (pygame.font.Font): Font to use for rendering
            color (tuple): Text color (RGB)
            background_color (tuple, optional): Background color (RGB)
        """
        self.x = x
        self.y = y
        self.width = width
        self.font = font
        self.color = color
        self.background_color = background_color
        self.lines = []
        self.rendered_lines = []
        self.total_height = 0
        
    def set_text(self, text):
        """Set the text content and process line wrapping"""
        self.lines = self._wrap_text(text)
        self._render_lines()
        
    def _wrap_text(self, text):
        """Wrap the text to fit within the specified width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Test if adding the word would exceed the width
            test_line = ' '.join(current_line + [word])
            test_width = self.font.size(test_line)[0]
            
            if test_width <= self.width:
                current_line.append(word)
            else:
                if current_line:  # Only add if there's content
                    lines.append(' '.join(current_line))
                current_line = [word]
                
                # Handle case where a single word is too long
                if self.font.size(word)[0] > self.width:
                    # Split the long word
                    self._split_long_word(word, lines)
                    current_line = []
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
    
    def _split_long_word(self, word, lines):
        """Split a word that's too long to fit on one line"""
        current_chunk = ""
        for char in word:
            test_chunk = current_chunk + char
            if self.font.size(test_chunk)[0] <= self.width:
                current_chunk = test_chunk
            else:
                lines.append(current_chunk)
                current_chunk = char
        if current_chunk:
            lines.append(current_chunk)
    
    def _render_lines(self):
        """Render each line as a separate surface"""
        self.rendered_lines = []
        self.total_height = 0
        
        for line in self.lines:
            if self.background_color is not None:
                text_surface = self.font.render(line, True, self.color, self.background_color)
            else:
                text_surface = self.font.render(line, True, self.color)
            self.rendered_lines.append(text_surface)
            self.total_height += text_surface.get_height()
    
    def draw(self, surface):
        """Draw all text lines on the given surface"""
        y_offset = self.y
        for line_surface in self.rendered_lines:
            surface.blit(line_surface, (self.x, y_offset))
            y_offset += line_surface.get_height()
    
    def get_height(self):
        """Return the total height of the rendered text"""
        return self.total_height