from PIL import Image, ImageDraw, ImageFont
import os

def generate_mockup(screenshot_file, banner_text, bg_color, output_path):
    """
    Generates a basic mockup by putting the screenshot on a colored background 
    with a banner text.
    """
    screenshot = Image.open(screenshot_file).convert("RGBA")
    
    canvas_width = int(screenshot.width * 1.5)
    canvas_height = int(screenshot.height * 1.3)
    
    canvas = Image.new("RGBA", (canvas_width, canvas_height), bg_color)
    
    paste_x = (canvas_width - screenshot.width) // 2
    paste_y = canvas_height - screenshot.height - 50
    canvas.paste(screenshot, (paste_x, paste_y), screenshot)
    
    draw = ImageDraw.Draw(canvas)
    try:
        font_size = int(canvas_height * 0.05)
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    text_bbox = draw.textbbox((0, 0), banner_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (canvas_width - text_width) // 2
    text_y = 50
    
    draw.text((text_x, text_y), banner_text, fill="white", font=font)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canvas.save(output_path, "PNG")
    return output_path
