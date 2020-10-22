# Pattern Password Calculator (c)2020 @jekuz
#
# It takes password examples (patterns) from file and generates all the the similar versions
# changing start key. You can change minimum password length and 'shifted' versions ability.
# Using: create 'patterns.txt' including password pattern(s) in line(s) and start the script.
# You will get 'passwords.txt' file with all possible versions.

shift = False
minimum_password_length = 6

keymap = ("`1234567890-= ",
          " qwertyuiop[]\\",
          " asdfghjkl;'  ",
          " zxcvbnm,./   ")
usual_keys = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shift_keys = "~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?"
key_reverse = {**dict(zip(usual_keys, shift_keys)), **dict(zip(shift_keys, usual_keys))}


# Returns key's position(x,y) from keymap
def position(key):
    for y, row in enumerate(keymap):
        for x in range(len(row)):
            if keymap[y][x] == key:
                return x, y


# Returns keymap pattern converted in coordinate offsets
def convert(keyboard_pattern):
    converted_pattern = []
    for key_index in range(len(keyboard_pattern) - 1):
        x1, y1 = position(keyboard_pattern[key_index])
        x2, y2 = position(keyboard_pattern[key_index + 1])
        converted_pattern.append((x2 - x1, y2 - y1))
    return converted_pattern


# Returns password list of keymap pattern from start key or empty list if it's not possible
def password_list(converted_pattern, key):
    # Trying to get password from start key (returns empty password list if impossible)
    password = key
    for way in converted_pattern:
        x, y = position(password[-1])
        x += way[0]
        y += way[1]
        try:
            next_key = keymap[y][x]
        except IndexError:
            return []
        if next_key == " ":
            return []
        password += next_key
    if not shift:
        return [password]

    # Creating 'shifted' versions:
    # Getting all password variants in binary list of password
    # Example: '**' = ['00','01','10','11'] - 1 is shifted, 0 is not
    binary_list = []
    pass_count = 2 ** len(password)
    for i in range(pass_count):
        binary_list.append(str(format((pass_count + i), 'b')[1:]))

    password = [*password]
    pass_list = []

    # Getting all password versions according to binary list
    for binary_pattern in binary_list:
        for n, digit in enumerate(binary_pattern):
            if digit == '1' and password[n] in usual_keys:
                password[n] = key_reverse[password[n]]
            if digit == '0' and password[n] in shift_keys:
                password[n] = key_reverse[password[n]]
        # Convert password into string and adding into password list
        password_string = ''
        for key in password:
            password_string += key
        pass_list.append(password_string)
    return pass_list


# Reading keymap patterns from file and generating passwords into file
def main():
    converted_patterns = []

    # Converting all file's patterns (from min.length) into 'converted_patterns' list
    with open("patterns.txt", 'r') as patterns_file:
        for keyboard_pattern in patterns_file:
            for length in range(minimum_password_length, len(keyboard_pattern)):
                converted_patterns.append(convert(keyboard_pattern[:length]))

    # Creating passwords from all start keys according to 'converted_patterns' list
    total_passwords_counter = 0
    with open("passwords.txt", 'w') as passwords_file:
        for start_key in usual_keys:
            print(f"\nCalculating passwords starting from key '{start_key}'.. ", end='')
            passwords_counter_from_key = 0
            for converted_pattern in converted_patterns:
                for password in (password_list(converted_pattern, start_key)):
                    passwords_file.write(password + '\n')
                    passwords_counter_from_key += 1
            print(f"{passwords_counter_from_key} ok!", end='')
            total_passwords_counter += passwords_counter_from_key
    print(f"\n\nTotal Passwords: {total_passwords_counter}")


if __name__ == "__main__":
    main()
