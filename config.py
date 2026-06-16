import os


def _parse_keys() -> list[str]:
    raw = os.getenv("GEMINI_API_KEYS", "")
    keys = [k.strip() for k in raw.split(",") if k.strip()]
    return keys


# GROQ_API_KEY = [
#     "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",
#     "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",
#     "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",
#     "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",
#     "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",
#     "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",
#     "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",
#     "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",
#     "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",
#     "gsk_TlqnKRbea2Vl90xDdpp3WGdyb3FYnYB1tUfNCg9vNDkBQJpKVNy"
#   ]

#
# GEMINI_API_KEYS = [
#     "AIzaSyDk1hMXLoOOQw4XPn3oR_yz8QL9vnmWN5A",
#     "AIzaSyA7-TLlg4zp6aoPp6idYnVJjBuNwHi-p2w",
#     "AIzaSyDM1CwNtHeIhF9LUlAwNK9j74B0qZn1UQg",
#     "AIzaSyAka-f41FpJM-ydDwmXsEGMCYwlRkGohOg",
#     "AIzaSyDI8TyM2H4D_U3q8D9zJ0j3mFD0MB5PqaI",
#     "AIzaSyDszWCxUUvjLKqGK3yVpEi_RP3ttnls4E4",
#     "AIzaSyAjS4H55ThJGmmnVqtxyMZ1_t58dhoHfuc",
#     "AIzaSyDHszzz-EXNFpxRg_C-XVGaSR-jOUslu8g",
#     "AIzaSyBpcUEKlWPa1HY0sd4JlQMAHCPNcRlOHc8",
#     "AIzaSyBCS9Ay9QBlgB_Oooyg2XGLSOD9pw9EN9s",
#     "AIzaSyDhv3E5PUdXCRehjrhpIDiIMjy2QzQrLYY",
#     "AIzaSyBmyVoi9_zbCfIedrITk1Iem9wGfAfGz30",
#     "AIzaSyDqYHvco1n1_lRyr0uJCEy1DHr9nyoXf2Q",
#     "AIzaSyCS1-eioEoakGqCsP1cprCz0Pvtz7rOVbc",
#     "AIzaSyATKYuSfQtkerBzb67WFGlUYAB8ZPqWLZM",
#     "AIzaSyAUA7piUE-cYl8R8NrsbXNnLoYEqF64S9o",
#     "AIzaSyAdGTzMb-PUdNcuE1LP23kmMGF0MrzfMyM",
#     "AIzaSyC4mVat6UjcJbKFNwplG2Kl4gqLDp08H9w",
#     "AIzaSyBrp40NGWRJ8HNyLQoUI0VAWXHa3PIz6l0",
#     "AIzaSyBIiEt0xP3MUUTG2-quYwnO9TTYBoRBfvo",
#     "AIzaSyCubgw3y5e2UwLIBfgQMN7ZMqY8zFW9wig",
#     "AIzaSyAMX4eXkA-T-cbnbVPQHOV7YERi8OHiEH4",
#     ""]

CEREBRAS_API_KEY = "csk-ttv842pdxtcxec64jn9rdj3we2td29kh3jn6ddkjvempdymk"

CARTESIA_API_KEY = "sk_car_84Gv3EmjBw5RjiGT4pCghA"

# WEATHER_API_KEY = "95388efab77661cbf445d845a9d672ac"
ASSISTANT_NAME = "JOI"
CITY = "Bengaluru"


CONTACTS = {
    "mom":      "+91XXXXXXXXXX",
    "dad":      "+91XXXXXXXXXX",
    "friend":   "+91XXXXXXXXXX",
}