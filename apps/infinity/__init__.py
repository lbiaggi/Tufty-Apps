# Load the images from assets folder
lt_order_icon = image.load("assets/lt_order.png")  # For counter LT
order_icon = image.load("assets/order.png")        # For counters G1 and G2
command_token_icon = image.load("assets/command_token.png")  # For counter CT

# Display Constants
ICON_SPACING = 8  # Space between icons (vertical and horizontal)
HIGHLIGHT_PADDING_H = 2  # Horizontal highlight padding
HIGHLIGHT_PADDING_V = -2  # Vertical highlight padding
IMAGE_PADDING_Y = 4 
CT_TOP_MARGIN = 0  # CT text distance from screen top
CT_IMAGE_PADDING_X = 0

# Screen Layout Constants  
SCREEN_THIRDS = 3  # Number of bottom counter sections
CT_POSITION_DIVISOR = 6  # Screen width divisor for CT positioning (1/6 = left half center)

# Color Constants
BG_COLOR = color.rgb(20, 25, 40)  # Dark blue background
HIGHLIGHT_COLOR = color.rgb(60, 80, 120)  # Active counter highlight
SHADOW_COLOR = color.rgb(0, 0, 0)  # Text shadow
ACTIVE_TEXT_COLOR = color.rgb(233, 123, 22)  # Orange for active counter
HOLD_TEXT_COLOR = color.rgb(233, 233, 100)  # Yellow for active counter
INACTIVE_TEXT_COLOR = color.rgb(180, 180, 180)  # Gray for inactive counter

# Counter state
counters = {"LT": 1, "G1": 5, "G2": 10, "CT": 4, "G1I": 0, "G2I": 0}
default_counters = {"LT": 1, "G1": 5, "G2": 10, "CT": 4, "G1I": 0, "G2I": 0}  # Store default values for reset
active_counter = "LT"  # Which counter is currently selected
MIN_COUNT = 0
MAX_COUNT_LT = 2  # LT has different max count
MAX_COUNT_G = 10  # G1 and G2 max count
MAX_COUNT_CT = 5  # CT max count

large_font = pixel_font.load("/system/assets/fonts/ignore.ppf")

def update():
    global active_counter
    
    # Set font and measure text dimensions once for all counters
    screen.font = large_font
    sample_text_width, sample_text_height = screen.measure_text("0")  # Measure once for consistent sizing
    
    # Check if A button is being held down
    a_held = badge.held(BUTTON_A)
    b_held = badge.held(BUTTON_B)
    c_held = badge.held(BUTTON_C)
    
    # Handle counter selection and modification
    if a_held:
        active_counter = "LT"
        # When A is held, UP/DOWN modifies CT counter directly
        if badge.pressed(BUTTON_UP):
            if counters["CT"] < MAX_COUNT_CT:
                counters["CT"] += 1
        elif badge.pressed(BUTTON_DOWN):
            if counters["CT"] > MIN_COUNT:
                counters["CT"] -= 1
    elif b_held:
        active_counter = "G1"
        # When B is held, UP/DOWN modifies G1I counter directly
        if badge.pressed(BUTTON_UP):
            if counters["G1I"] < MAX_COUNT_G:
                counters["G1I"] += 1
        elif badge.pressed(BUTTON_DOWN):
            if counters["G1I"] > MIN_COUNT:
                counters["G1I"] -= 1
    elif c_held:
        active_counter = "G2"
        # When C is held, UP/DOWN modifies G2I counter directly
        if badge.pressed(BUTTON_UP):
            if counters["G2I"] < MAX_COUNT_G:
                counters["G2I"] += 1
        elif badge.pressed(BUTTON_DOWN):
            if counters["G2I"] > MIN_COUNT:
                counters["G2I"] -= 1
    else:
        # Handle up/down for the active counter (only nothing is held)
        if badge.pressed(BUTTON_UP):
            if active_counter == "LT":
                if counters[active_counter] < MAX_COUNT_LT:
                    counters[active_counter] += 1
            elif active_counter == "CT":
                if counters[active_counter] < MAX_COUNT_CT:
                    counters[active_counter] += 1
            elif active_counter in ["G1I", "G2I"]:
                if counters[active_counter] < MAX_COUNT_G:
                    counters[active_counter] += 1
            else:
                if counters[active_counter] < MAX_COUNT_G:
                    counters[active_counter] += 1
        
        if badge.pressed(BUTTON_DOWN):
            if counters[active_counter] > MIN_COUNT:
                counters[active_counter] -= 1
    
    # Clear the screen with a nice background color
    screen.pen = BG_COLOR
    screen.shape(shape.rectangle(0, 0, screen.width, screen.height))
    
    # Display CT command token images horizontally from left edge
    ct_count = counters["CT"]
    if ct_count > 0:
        ct_start_x = CT_IMAGE_PADDING_X  # Start from left edge
        # Draw each CT icon from left to right
        for j in range(ct_count):
            icon_x = ct_start_x + (j * ICON_SPACING)
            icon_y = CT_TOP_MARGIN
            screen.blit(command_token_icon, vec2(icon_x, icon_y))
    
    # Display icons for all three counters
    section_width = screen.width // SCREEN_THIRDS
    
    # Reserve space for counter text at bottom
    
    for i, counter_name in enumerate(["LT", "G1", "G2"]):
        current_count = counters[counter_name]
        
        if current_count > 0:
            # Select the appropriate icon for this counter
            current_icon = lt_order_icon if counter_name == "LT" else order_icon
            
            # Calculate x position for this counter's section
            section_center = (i * section_width) + (section_width // 2)
            icon_base_x = section_center - (current_icon.width // 2)
            
            # Start from bottom and work up
            bottom_y = screen.height - sample_text_height - current_icon.height - HIGHLIGHT_PADDING_V + IMAGE_PADDING_Y
            
            # Draw each icon for this counter, starting from the bottom (index 0) going up
            for j in range(current_count):
                icon_y = bottom_y - (j * ICON_SPACING)
                screen.blit(current_icon, vec2(icon_base_x, icon_y))
    # Display LT, G1, G2 counters at the bottom edge (CT displayed at top)
    counter_y = screen.height - sample_text_height - HIGHLIGHT_PADDING_V  # Position text to touch bottom of screen
    
    # Calculate positions for bottom counters (1/3 of screen width each)
    section_width = screen.width // SCREEN_THIRDS
    
    # Choose which counters to display at the bottom based on button states
    counter_1 = "CT" if a_held else "LT"
    counter_2 = "G1I" if b_held else "G1"
    counter_3 = "G2I" if c_held else "G2"
    bottom_counters = [counter_1, counter_2, counter_3]
    
    for i, counter_name in enumerate(bottom_counters):
        # Position each counter in its section
        section_center = (i * section_width) + (section_width // 2)
        
        counter_text = str(counters[counter_name])  # Just show the number  
        text_width, text_height = screen.measure_text(counter_text)  # Measure actual text for proper centering
        text_x = section_center - (text_width // 2)
        
        # Determine text color based on button state
        if ((a_held and counter_name == "CT") or
            (b_held and counter_name == "G1I") or
            (c_held and counter_name == "G2I")):
            # Button held and showing corresponding counter - use hold color with highlight
            screen.pen = HIGHLIGHT_COLOR
            screen.shape(shape.rectangle(text_x - HIGHLIGHT_PADDING_H, counter_y - HIGHLIGHT_PADDING_V, text_width + (HIGHLIGHT_PADDING_H * 2), text_height + (HIGHLIGHT_PADDING_V * 2)))
            
            # Draw text with shadow effect
            screen.pen = SHADOW_COLOR  # Black shadow
            screen.text(counter_text, text_x + 1, counter_y + 1)
            screen.pen = HOLD_TEXT_COLOR  # Yellow text for held
        elif counter_name == active_counter:
            # Active counter (not held) - use active color with highlight
            screen.pen = HIGHLIGHT_COLOR
            screen.shape(shape.rectangle(text_x - HIGHLIGHT_PADDING_H, counter_y - HIGHLIGHT_PADDING_V, text_width + (HIGHLIGHT_PADDING_H * 2), text_height + (HIGHLIGHT_PADDING_V * 2)))
            
            # Draw text with shadow effect
            screen.pen = SHADOW_COLOR  # Black shadow
            screen.text(counter_text, text_x + 1, counter_y + 1)
            screen.pen = ACTIVE_TEXT_COLOR  # Orange text for active
        else:
            # Inactive counter - use inactive color, no highlight
            screen.pen = SHADOW_COLOR  # Black shadow
            screen.text(counter_text, text_x + 1, counter_y + 1)
            screen.pen = INACTIVE_TEXT_COLOR  # Gray text for inactive
        
        screen.text(counter_text, text_x, counter_y)

run(update)
