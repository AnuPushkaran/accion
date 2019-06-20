import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', help='Input file for the formatting scripts', required=False)

format_chars = ("*", ".")
bullet_tab_space = 2
bullet_sub_tab_space = 1
line_index = 0

def get_next_formatting(data):
    global line_index	
    line = ""
    format = ""
    flag = True
    non_formatting_lines = []
    
    if isinstance(data, list):
        if line_index >= len(data):
            return line, non_formatting_lines, format
        for line in data[line_index:]:
            if line_index >= len(data):
                break
            line_index = line_index + 1
			
            arr = line.lstrip().split(" ", 1)
            if arr and len(arr):
                format = arr[0].rstrip()
                if re.match('^[\*\.]', format):
                    break
                else:
                    format = ""
            l = re.sub(r"\s", "", line)
            if len(l) == 0:
                continue
            non_formatting_lines.append(line.lstrip())
    else:
        while True:
            line = data.readline()
            if not line:
                break
            arr = line.lstrip().split(" ", 1)
            if arr and len(arr):
                format = arr[0].rstrip()
                if re.match('^[\*\.]', format):
                    break
                else:
                    format = ""
            if not line or len(line.lstrip()) == 0:
                break
            non_formatting_lines.append(line.lstrip())
    return line, non_formatting_lines, format


def is_nmbering_format(format):
    return re.match('^\*', format)


def is_bulletting_format(format):
    return re.match('^\.', format)


def exclude_format_string(line):
    arr = line.split(" ", 1)
    if arr and len(arr) > 1:
        return arr[1].lstrip()
    return ""


def format_generator(data):
    
    current_line = current_format = next_line = next_format = None
    non_formatting_line = []
    current_numbering = current_numbering_format = ""
    current_indent = ""

    while True:
        if not current_line:
            current_line, non_formatting_line, current_format = get_next_formatting(data)
        if not current_line:
            return False
        if non_formatting_line and not next_line:
            for line in non_formatting_line[:]:
                text = text = current_indent + line
                print(text)
                non_formatting_line = []
        next_line, non_formatting_line, next_format = get_next_formatting(data)
        text = exclude_format_string(current_line)
        level = len(current_format)
        if is_nmbering_format(current_format):
            
            prev_level = len(current_numbering_format)
            current_numbering_format = current_format
            if current_numbering == "":
                current_numbering = "1"
            else:
                num_arr = current_numbering.split('.')
                if level == prev_level:
                    current_numbering = ".".join(num_arr[:-1]) + str(int(num_arr[-1])) + 1 if len(
                        num_arr) > 1 else str(int(current_numbering) + 1)
                elif level < prev_level:
                    index = level - 1
                    num_arr[index] = str(int(num_arr[index]) + 1)
                    current_numbering = ".".join(num_arr[:level])
                elif level > prev_level:
                    current_numbering = ".".join(num_arr[:]) + ".1"
            text = current_numbering + " " + text
            current_indent = " "*len(current_numbering)+" "
        else:
            bullet = "+ "
            space = " " * bullet_tab_space
            if not next_format or is_nmbering_format(next_format) or level == len(next_format):
                bullet = "- "
            if level > 1:
                space = space + " " * (bullet_sub_tab_space * (level - 1))
            current_indent = space + "  "
            text = space + bullet + text
        print(text)
        if non_formatting_line:
            for line in non_formatting_line[:]:
                text = current_indent + line
                print(text)
                non_formatting_line = []
        if not next_line:
            return False
        current_format = next_format
        current_line = next_line
def main():
    data = ""
    args = parser.parse_args()
    if args.input_file:
        input_file_name = args.input_file
        try:
            with open(input_file_name, 'r') as file:
                data = file.read()
        except FileNotFoundError:
            print("File does not exists")
            return
        except:
            print("Error while opening the file")
            return  
            
    else:
        data = sys.stdin.read()
    lines = re.compile("\r|\n|\r\n").split(data)
    if lines:	
        format_generator(lines)
    else:
        print("File is empty or invalid")

if __name__ == '__main__':
    main()

