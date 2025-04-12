from app.pystamp import generate_profile_stamp


if __name__ == '__main__':
    generate_profile_stamp(
        profile_path="cleiton.png",
        stamp_text="#PROFILESTAMP",
        stamp_color="light_blue",
        text_color="white",
        gradient=True
    )