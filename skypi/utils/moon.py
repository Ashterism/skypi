

NEW_MOON = 3.5
WAXING_CRESCENT = 7
FIRST_QUARTER = 10.5
WAXING_GIBBOUS = 14
FULL_MOON = 17.5
WANING_GIBBOUS = 21
LAST_QUARTER = 24.5
WANING_CRESCENT = 29.5 


def get_moon_position(altitude):
    if altitude > 0:
        moon_display = f" ↑ {altitude:.0f}°"
    else:
        moon_display = f" ↓ {abs(altitude):.0f}°"
        if abs(altitude) >= 18:
            moon_display += " ✨"

    return moon_display


def get_moon_phase(phase_num):

    if phase_num <= NEW_MOON:
        phase_emoji = "🌑"
    elif phase_num <= WAXING_CRESCENT:
        phase_emoji = "🌒"
    elif phase_num <= FIRST_QUARTER:
        phase_emoji = "🌓"
    elif phase_num <= WAXING_GIBBOUS:
        phase_emoji = "🌔"
    elif phase_num <= FULL_MOON:
        phase_emoji = "🌕"
    elif phase_num <= WANING_GIBBOUS:
        phase_emoji = "🌖"
    elif phase_num <= LAST_QUARTER:
        phase_emoji = "🌗"
    else:
        phase_emoji = "🌘"

    return phase_emoji


def get_moon_phase_image(phase_num):

    if phase_num <= NEW_MOON:
        return "phase_new.1026_web_8bit.png"
    elif phase_num <= WAXING_CRESCENT:
        return "phase_waxing_crescent.0398_web_8bit.png"
    elif phase_num <= FIRST_QUARTER:
        return "phase_first_quarter.5440_web_8bit.png"
    elif phase_num <= WAXING_GIBBOUS:
        return "phase_waxing_gibbous.4801_web_8bit.png"
    elif phase_num <= FULL_MOON:
        return "phase_full.3492_web_8bit.png"
    elif phase_num <= WANING_GIBBOUS:
        return "phase_waning_gibbous.2172_web_8bit.png"
    elif phase_num <= LAST_QUARTER:
        return "phase_third_quarter.2243_web_8bit.png"
    else:
        return "phase_waning_crescent.0903_web_8bit.png"
