# This program is used for identifying how many buttons are needed to be created
# if the results are greater than 200.

# Used math for rounding up
import math

# Asks user for an input number (this is done according to the result length in the main program)
numinput = int(input("Enter number: "))

# If it's greater than 100
if numinput > 100:
    # _count is used for counting each number from the input
    several_btn_count = 0
    # _length same as numinput, just as a backup so main wouldn't be modified
    several_btn_length = numinput
    # _list to append the amount for each button
    several_btn_list = list()

    # Divides the input by 100 (to get appx how many buttons it needs)
    # and rounds it up to highest with math.ceil, highest because for example
    # 4.25 is 4 buttons = 800 results, the .25 is considered as a separate button.
    btn_count = math.ceil(numinput/100)

    # For b in the range of btn_count...
    for b in range(btn_count):
        # for i in the range of the input plus one...
        for i in range(several_btn_length + 1):      
            
            # If the _count reached 100
            if several_btn_count == 100:
                # append it to the list
                several_btn_list.append(several_btn_count)
                # deduct from _length the appended amount
                several_btn_length = several_btn_length - several_btn_count
                # reset the btn count to 0
                several_btn_count = 0
                # break and start over
                break

            # if the b is the last button count and the _count matches the _length, which means
            # it's the last button's amount...
            if b == btn_count - 1 and several_btn_count == several_btn_length:
                # append _count to the list
                several_btn_list.append(several_btn_count)

            # Increment several_btn_count by 1
            several_btn_count += 1

    # Prints the list for checking if it worked
    print(several_btn_list)

# If less than 100, it states that the input is less than 100
else:
    print("Less than 100")


