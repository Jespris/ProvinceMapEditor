

def log_message(message):
    # Open the file in read mode to read its content
    with open('output/game_log.txt', 'r') as file:
        # Read the existing content
        file_content = file.read()

    # Open the file in write mode to overwrite its content
    with open('output/game_log.txt', 'w') as file:
        # Write your message at the beginning of the file
        file.write(message + '\n')

        # Write back the existing content
        file.write(file_content)


def reset_log():
    with open('output/game_log.txt', 'w'):
        pass
