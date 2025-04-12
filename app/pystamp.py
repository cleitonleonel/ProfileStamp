from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "src"
FONT_DIR = BASE_DIR / "fonts"
OUTPUT_DIR = SOURCE_DIR / "img"

COLORS = {
    "purple": (75, 0, 130, 255),
    "blue": (0, 102, 204, 255),
    "light_blue": (0, 191, 255, 255),
    "green": (0, 128, 0, 255),
    "light_green": (0, 200, 100, 255),
    "red": (200, 0, 0, 255),
    "orange": (255, 140, 0, 255),
    "yellow": (255, 215, 0, 255),
    "pink": (255, 105, 180, 255),
    "gray": (100, 100, 100, 255),
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
}


def load_profile_image(profile_path, img_size):
    profile = Image.open(profile_path).convert("RGBA").resize((img_size, img_size))
    mask = Image.new(
        "L",
        (img_size, img_size),
        0
    )
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, img_size, img_size), fill=255)
    background = Image.new(
        "RGBA",
        (img_size, img_size),
        (0, 0, 0, 0)
    )
    background.paste(profile, (0, 0), mask)
    return background


def create_stamp_mask(img_size, center, outer_radius, inner_radius, start_angle, end_angle):
    mask = Image.new("L", (img_size, img_size), 0)
    draw = ImageDraw.Draw(mask)
    outer_box = [center[0] - outer_radius, center[1] - outer_radius,
                 center[0] + outer_radius, center[1] + outer_radius]
    inner_box = [center[0] - inner_radius, center[1] - inner_radius,
                 center[0] + inner_radius, center[1] + inner_radius]
    draw.pieslice(outer_box, start_angle, end_angle, fill=255)
    draw.pieslice(inner_box, start_angle, end_angle, fill=0)
    return mask


def apply_gradient(mask, img_size, center, inner_radius, outer_radius, start_angle, end_angle):
    np_mask = np.array(mask).astype(np.uint8)
    angle_span = end_angle - start_angle
    for y in range(img_size):
        for x in range(img_size):
            dx, dy = x - center[0], y - center[1]
            dist = math.hypot(dx, dy)
            angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
            if start_angle <= angle <= end_angle and inner_radius < dist < outer_radius:
                angle_pos = (angle - start_angle) / angle_span
                alpha_fade = min(angle_pos, 1 - angle_pos) * 2
                fade_factor = int(255 * (0.3 + 0.7 * alpha_fade))
                np_mask[y, x] = min(np_mask[y, x], fade_factor)
    return Image.fromarray(np_mask, mode="L")


def draw_curved_text(image, center, radius, text, font, fill, start_angle, end_angle):
    # draw = ImageDraw.Draw(image)
    angle_range = end_angle - start_angle
    spacing_factor = 0.5

    angle_per_char = (
            angle_range / (len(text) + spacing_factor if len(text) > 1 else 1)
    )
    total_text_angle = angle_per_char * len(text)
    angle_offset = (angle_range - total_text_angle) / 2

    for i, char in enumerate(text):
        angle = math.radians(
            start_angle + angle_offset + i * angle_per_char
        )
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)

        char_angle = math.degrees(angle) - 90
        temp_img = Image.new(
            "RGBA",
            (100, 100),
            (255, 255, 255, 0)
        )
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.text((20, 35), char, font=font, fill=fill)
        rotated = temp_img.rotate(-char_angle, expand=4)
        image.alpha_composite(
            rotated,
            (int(x - rotated.width / 2), int(y - rotated.height / 2))
        )


def generate_profile_stamp(
        profile_path: str,
        stamp_text: str,
        output_path: str = (OUTPUT_DIR/"stamp.png").as_posix(),
        stamp_color: str | tuple = "purple",
        text_color: str | tuple = "white",
        gradient: bool = False,
        font_path: str = (FONT_DIR / "DejaVuSans-Bold.ttf").as_posix(),
        font_size: int = 28,
):
    if isinstance(stamp_color, str):
        stamp_color = COLORS.get(stamp_color.lower())
        if stamp_color is None:
            raise ValueError(
                f"Color '{stamp_color}' not found. Choose from: {list(COLORS.keys())}"
            )

    if isinstance(text_color, str):
        text_color = COLORS.get(text_color.lower())
        if text_color is None:
            raise ValueError(
                f"Text color '{text_color}' not found. Choose from: {list(COLORS.keys())}"
            )

    img_size = 512
    center = (img_size // 2, img_size // 2)
    outer_radius = img_size // 2
    padding = 50
    inner_radius = outer_radius - padding
    start_angle = 90
    end_angle = 190
    font = ImageFont.truetype(font_path, font_size)

    background = load_profile_image(profile_path, img_size)
    stamp = Image.new("RGBA", (img_size, img_size), (0, 0, 0, 0))
    mask = create_stamp_mask(
        img_size,
        center,
        outer_radius,
        inner_radius,
        start_angle,
        end_angle
    )

    if gradient:
        mask = apply_gradient(
            mask,
            img_size,
            center,
            inner_radius,
            outer_radius,
            start_angle,
            end_angle
        )

    arc = Image.new("RGBA", (img_size, img_size), stamp_color)
    stamp.paste(arc, (0, 0), mask)

    text_radius = (inner_radius + outer_radius) // 2
    draw_curved_text(
        stamp,
        center,
        text_radius,
        stamp_text[::-1].upper(),
        font,
        text_color,
        start_angle,
        end_angle
    )

    final_image = Image.alpha_composite(background, stamp)
    final_image.save(output_path)
    print(f"✅ Image saved successfully: {output_path}")
