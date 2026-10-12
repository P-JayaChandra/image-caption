"""
Hindi (hi-IN) and Japanese (ja-JP) Localization Packs
"""
from visionspeak.engines.multilingual import MultilingualCaptionAdapter

HINDI_DICT = {
    "Chasing quiet moments in full color": "रंगों में शांत पलों को संजोते हुए",
    "A frame where the stillness speaks": "एक ऐसा दृश्य जहां खामोशी भी बोलती है",
    "Some memories never lose their warmth": "कुछ यादें कभी अपनी गर्माहट नहीं खोतीं"
}

JAPANESE_DICT = {
    "Chasing quiet moments in full color": "色鮮やかな静けさの瞬間を求めて",
    "A frame where the stillness speaks": "静寂が語りかける一枚",
    "Some memories never lose their warmth": "色褪せない温もりのある記憶"
}

MultilingualCaptionAdapter.register_dictionary("hi", HINDI_DICT)
MultilingualCaptionAdapter.register_dictionary("ja", JAPANESE_DICT)
