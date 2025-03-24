def remove_escape_character_from_command_output(command):
    output = command.stdout
    return output[:len(output) - 1]
