

# altitude = -20

def get_moon_position(altitude):
    if altitude > 0:
        moon_display = f" ↑ {altitude:.0f}°"
    else:
        moon_display = f" ↓ {abs(altitude):.0f}°"
        if abs(altitude) >= 18:
            moon_display += " ✨"

    return moon_display


def get_moon_phase(phase_num):

    if phase_num <= 3.5:
        phase_emoji = "🌑"
    elif phase_num <= 7:
        phase_emoji = "🌒"
    elif phase_num <= 10.5:
        phase_emoji = "🌓"
    elif phase_num <= 14:
        phase_emoji = "🌔"
    elif phase_num <= 17.5:
        phase_emoji = "🌕"
    elif phase_num <= 21:
        phase_emoji = "🌖"
    elif phase_num <= 24.5:
        phase_emoji = "🌗"
    else:
        phase_emoji = "🌘"

    return phase_emoji