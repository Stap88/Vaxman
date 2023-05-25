# monsta_counts_dict = {
#     "Blinky": {
#         "sprite_filepath" : "images/Blinky.png",
#         "count" : 0
#     },
#     "Pinky": {
#         "sprite_filepath" : "images/Blinky.png",
#         "count" : 0
#     },
#     "Inky": {
#         "sprite_filepath" : "images/Blinky.png",
#         "count" : 0
#     },
#     "Clyde": {
#         "sprite_filepath" : "images/Blinky.png",
#         "count" : 0
#     }
# }

# monsta_name_list = ["Blinky", "Pinky", "Inky", "Clyde"]

# monsta_type = monsta_counts_dict[monsta_name_list[0]]

# print(monsta_type["sprite_filepath"])
# print(monsta_type["count"])
###################################

monsta_start_count = 8

monsta_name_list = [ "Blinky", "Pinky", "Inky", "Clyde" ]

monsta_info_dict = {
    "Blinky": {
        "count" : 0
    },
    "Pinky": {
        "count" : 0
    },
    "Inky": {
        "count" : 0
    },
    "Clyde": {
        "count" : 0
    }
}

monsta_name_index = 0

for i in range(monsta_start_count):
    
    monsta_name = monsta_name_list[monsta_name_index]
    new_monsta = monsta_info_dict[monsta_name]
    new_monsta["count"] += 1
    monsta_name_index += 1

    if monsta_name_index == 4:
        monsta_name_index = 0
    
    print(monsta_name_index)
    

