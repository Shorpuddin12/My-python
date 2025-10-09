def convert_seconds(N):
    hours = N // 3600
    remaining_seconds = N % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    print(f"{hours}:{minutes}:{seconds}")


convert_seconds(556)
convert_seconds(1)
convert_seconds(140153)