from PIL import Image, ImageDraw, ImageFont
import os

def generate_mockup(screenshot_file, banner_text, bg_color, output_path):
    """
    Compiles screenshots with a smart wrapper layout and clean smartphone display bezel.
    """
    screenshot = Image.open(screenshot_file).convert("RGBA")
    
    # Use a crisp master canvas resolution
    canvas_width = 1200
    canvas_height = 1600
    
    # Dynamically scale screenshot width to look uniform on canvas
    target_ss_width = 720
    w_ratio = target_ss_width / float(screenshot.width)
    target_ss_height = int(float(screenshot.height) * float(w_ratio))
    screenshot = screenshot.resize((target_ss_width, target_ss_height), Image.Resampling.LANCZOS)
    
    # Initialize the core canvas container
    canvas = Image.new("RGBA", (canvas_width, canvas_height), bg_color)
    
    # Center asset alignment coordinates
    paste_x = (canvas_width - screenshot.width) // 2
    paste_y = canvas_height - screenshot.height - 120
    
    draw = ImageDraw.Draw(canvas)
    
    # Programmatically render a structural bezel
    bezel_padding = 14
    draw.rounded_rectangle(
        [paste_x - bezel_padding, paste_y - bezel_padding, 
         paste_x + screenshot.width + bezel_padding, paste_y + screenshot.height + bezel_padding],
        radius=35, fill="#0F172A"
    )
    
    # Superimpose screenshot into the rendered bezel frame
    canvas.paste(screenshot, (paste_x, paste_y), screenshot)
    
    # Configure context banner lettering layout
    try:
        font_size = 56
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    text_bbox = draw.textbbox((0, 0), banner_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (canvas_width - text_width) // 2
    text_y = 140
    
    draw.text((text_x, text_y), banner_text, fill="#FFFFFF", font=font)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canvas.save(output_path, "PNG")
    return output_path
