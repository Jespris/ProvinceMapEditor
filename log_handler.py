

def log_message(message):
    # Open the file in read mode to read its content
    with open('output/game_log.txt', 'r') as file:
        # Read the existing content
        file_content = file.read()

    # Open the file in write mode to overwrite its content
    with open('output/game_log.txt', 'w') as file:
        # Write the existing content
        file.write(file_content)
        # Write your message at the end of the file
        file.write('\n' + message)


def reset_log():
    with open('output/game_log.txt', 'w'):
        pass
