from PIL import Image, ImageDraw, ImageFont
import math
from datetime import datetime

def int_to_english(n):
    if n == 0:
        return "zero"
    
    def one_to_nineteen(num):
        words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                 "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
        return words[num - 1]
    
    def tens(num):
        words = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        return words[num - 2]
    
    def two_digits(num):
        if num < 20:
            return one_to_nineteen(num)
        else:
            tens_word = tens(num // 10)
            remainder = num % 10
            return tens_word + ("-" + one_to_nineteen(remainder) if remainder != 0 else "")
    
    def three_digits(num):
        hundreds_place = num // 100
        remainder = num % 100
        if hundreds_place != 0 and remainder != 0:
            return one_to_nineteen(hundreds_place) + " hundred " + two_digits(remainder)
        elif hundreds_place != 0:
            return one_to_nineteen(hundreds_place) + " hundred"
        else:
            return two_digits(remainder)
    
    def number_to_words(num):
        if num < 100:
            return two_digits(num)
        elif num < 1000:
            return three_digits(num)
        else:
            thousands_place = num // 1000
            remainder = num % 1000
            if thousands_place < 1000:
                return three_digits(thousands_place) + " thousand " + (three_digits(remainder) if remainder != 0 else "")
            else:
                millions_place = num // 1000000
                remainder = num % 1000000
                thousands = remainder // 1000
                remainder = remainder % 1000
                words = three_digits(millions_place) + " million"
                if thousands > 0:
                    words += " " + three_digits(thousands) + " thousand"
                if remainder > 0:
                    words += " " + three_digits(remainder)
                return words

    return number_to_words(n).strip()

def draw_clock(size=400, time=None, font_size_ratio=1, text_too=False):
    # Create a blank image
    image = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Define clock center and radius
    center = (size // 2, size // 2)
    radius = size // 2 - 20

    # Draw the clock circle
    draw.ellipse([20, 20, size - 20, size - 20], outline='black', width=5)

    # Adjust font size based on the font_size_ratio parameter
    font_size = size // font_size_ratio

    # Load a font (optional, system-specific font may need to be adjusted)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    font.size = font_size

    hours = [(int_to_english(hour), hour) for hour in range(1, 13)]
    minutes = [(int_to_english(minute), minute) for minute in range(1, 61)]

    hours.sort()
    minutes.sort()

    # Draw the numbers on the clock face
    for i, (name, hour) in enumerate(hours):
        angle = math.pi / 6 * (i - 3)  # Offset by 3 to start at the top
        x = center[0] + radius * 0.85 * math.cos(angle)
        y = center[1] + radius * 0.85 * math.sin(angle)
        text = f"{hour}\n{name}" if text_too else f"{hour}"
        bbox = draw.textbbox((0, 0), text, font=font)  # Get bounding box of the text
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text((x - text_width / 2, y - text_height / 2), text, font=font, fill='black')

    # Draw minute markers (small lines)
    for minute in range(60):
        angle = math.pi / 30 * (minute - 15)  # Offset by 15 to start at the top
        outer_x = center[0] + radius * math.cos(angle)
        outer_y = center[1] + radius * math.sin(angle)

        # Shorter inner end of the line for minute markers
        if minute % 5 == 0:
            # Longer markers for 5-minute intervals (where the numbers are)
            inner_x = center[0] + (radius * 0.92) * math.cos(angle)
            inner_y = center[1] + (radius * 0.92) * math.sin(angle)
        else:
            # Shorter markers for other minutes
            inner_x = center[0] + (radius * 0.96) * math.cos(angle)
            inner_y = center[1] + (radius * 0.96) * math.sin(angle)

        # Draw minute marker line
        draw.line([inner_x, inner_y, outer_x, outer_y], fill='black', width=2)

    # If no time provided, use current time
    if time is None:
        time = datetime.now()

    # Convert time to angles for hands
    hour_angle = math.pi / 6 * (time.hour % 12 + time.minute / 60 - 3)
    minute_angle = math.pi / 30 * (time.minute - 15)
    second_angle = math.pi / 30 * (time.second - 15)

    hoursMap = {hour: i for i, (_, hour) in enumerate(hours)}
    hoursMap[0] = hoursMap[12]

    minutesMap = {minute: i for i, (_, minute) in enumerate(minutes)}
    minutesMap[0] = minutesMap[60]

    # timeHour = time.hour % 12
    # timeMinute = time.minute

    hour_angle = math.pi / 6 * (hoursMap[time.hour % 12] - 3)
    minute_angle = math.pi / 30 * (minutesMap[time.minute] - 15)
    second_angle = math.pi / 30 * (minutesMap[time.second] - 15)

    # Length of the clock hands
    hour_hand_length = radius * 0.5
    minute_hand_length = radius * 0.75
    second_hand_length = radius * 0.9

    # Calculate hand positions
    hour_hand = (center[0] + hour_hand_length * math.cos(hour_angle),
                 center[1] + hour_hand_length * math.sin(hour_angle))
    minute_hand = (center[0] + minute_hand_length * math.cos(minute_angle),
                   center[1] + minute_hand_length * math.sin(minute_angle))
    second_hand = (center[0] + second_hand_length * math.cos(second_angle),
                   center[1] + second_hand_length * math.sin(second_angle))

    # Draw the clock hands
    draw.line([center, hour_hand], fill='black', width=8)
    draw.line([center, minute_hand], fill='black', width=5)
    draw.line([center, second_hand], fill='red', width=2)

    # Draw clock center
    draw.ellipse([center[0] - 10, center[1] - 10, center[0] + 10, center[1] + 10], fill='black')

    return image
