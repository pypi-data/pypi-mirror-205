import sys
import scalestuff
import modestuff
import intervalstuff

selected_topics = {}

main_menu_prompt = ('Main Menu\n'
                    'Program options:\n'
                    '  (Show) Displays concepts.\n'
                    '  (Hide) Removes concept from final review.\n'
                    'Good to do for accidental searches.\n'
                    '  (Print) Prints list that documents what the user\n'
                    'has searched to review areas of focus for practice.\n'
                    '  (Quit) Terminates program.\n'
                    '\n'
                    'Enter input: ')
main_menu_options = ['Show', 'Hide', 'Print', 'Quit']

table_of_contents_prompt = ('Concept options:\n'
                            '  (Scales) Displays Scales.\n'
                            '  (Modes) Displays Modes.\n'
                            '  (Intervals) Displays basic Interval information.\n'
                            '  (More Intervals) Displays information about Circle of Fifths/Fourths, Order of\n'
                            'Sharps/Flats, etc.\n'
                            '\n'
                            'Enter concept: ')
table_of_contents = ['Scales', 'Modes', 'Intervals', 'More Intervals']

print("Welcome to Michael's Music Theory Program!\n")
user_input = input(main_menu_prompt).strip().lower().title()

while user_input != 'Quit':
    if user_input == 'Show':
        index_name = input(table_of_contents_prompt).strip().lower().title()
        if index_name == 'Scales':
            search = input(scalestuff.scales_prompt).strip().lower().title()
            while len(search) == 0:
                search = input(scalestuff.scales_prompt).strip().lower().title()
            while (search not in scalestuff.scale_list) and (search != 'Quit'):
                print('Unknown, please use correct spelling and don\'t worry about case-sensitivity\n')
                search = input(scalestuff.scales_prompt).strip().lower().title()
                if search in scalestuff.scale_list:
                    continue
            if search in scalestuff.scale_list:
                if search == 'Major':
                    print(scalestuff.major_scale_prompt)
                    selected_topics[search] = 'Scale'
                elif search == 'Major Pentatonic':
                    print(scalestuff.major_penta_scale_prompt)
                    selected_topics[search] = 'Scale'
                elif search == 'Minor':
                    print(scalestuff.minor_scale_prompt)
                    selected_topics[search] = 'Scale'
                elif search == 'Melodic Minor':
                    print(scalestuff.melminor_scale_prompt)
                    selected_topics[search] = 'Scale'
                elif search == 'Harmonic Minor':
                    print(scalestuff.harminor_scale_prompt)
                    selected_topics[search] = 'Scale'
                elif search == 'Minor Pentatonic':
                    print(scalestuff.minor_penta_scale_prompt)
                    selected_topics[search] = 'Scale'
                elif search == 'Quit':
                    sys.exit()
                else:
                    pass
            continue
        elif index_name == 'Modes':
            search = input(modestuff.modes_prompt).strip().lower().title()
            while len(search) == 0:
                search = input(modestuff.modes_prompt).strip().lower().title()
            while (search not in modestuff.mode_list) and (search != 'Quit'):
                print('Unknown, please use correct spelling and don\'t worry about case-sensitivity\n')
                search = input(modestuff.modes_prompt).strip().lower().title()
                if search in modestuff.mode_list:
                    continue
            if search in modestuff.mode_list:
                if search == 'Ionian':
                    print(modestuff.ionian_mode_prompt)
                    selected_topics[search] = 'Mode'
                elif search == 'Dorian':
                    print(modestuff.dorian_mode_prompt)
                    selected_topics[search] = 'Mode'
                elif search == 'Phrygian':
                    print(modestuff.phrygian_mode_prompt)
                    selected_topics[search] = 'Mode'
                elif search == 'Lydian':
                    print(modestuff.lydian_mode_prompt)
                    selected_topics[search] = 'Mode'
                elif search == 'Mixolydian':
                    print(modestuff.mixolydian_mode_prompt)
                    selected_topics[search] = 'Mode'
                elif search == 'Aeolian':
                    print(modestuff.aeolian_mode_prompt)
                    selected_topics[search] = 'Mode'
                elif search == 'Locrian':
                    print(modestuff.locrian_mode_prompt)
                    selected_topics[search] = 'Mode'
                elif search == 'Quit':
                    sys.exit()
                else:
                    pass
            continue
        elif index_name == 'Intervals':
            search = input(intervalstuff.interval_menu).strip().lower().title()
            while len(search) == 0:
                search = input(intervalstuff.interval_menu).strip().lower().title()
            while (search not in intervalstuff.interval_topics) and (search != 'Quit'):
                print('Unknown, please use correct spelling and don\'t worry about case-sensitivity\n')
                search = input(intervalstuff.interval_menu).strip().lower().title()
                if search in intervalstuff.interval_topics:
                    continue
            if search in intervalstuff.interval_topics:
                if search == 'Interval Basics':
                    print(intervalstuff.interval_basics)
                    selected_topics[search] = 'Interval'
                elif search == 'Chord Basics':
                    print(intervalstuff.chord_basics)
                    selected_topics[search] = 'Interval'
                elif search == 'Chord Progressions':
                    print(intervalstuff.chord_progs)
                    selected_topics[search] = 'Interval'
                elif search == 'Arpeggio Basics':
                    print(intervalstuff.arpeggio_basics)
                    selected_topics[search] = 'Interval'
                elif search == 'Quit':
                    sys.exit()
                else:
                    pass
            continue
        elif index_name == 'More Intervals':
            search = input(intervalstuff.more_intervals_menu).strip().lower().title()
            while len(search) == 0:
                search = input(intervalstuff.more_intervals_menu).strip().lower().title()
            while (search not in intervalstuff.more_intervals) and (search != 'Quit'):
                print('Unknown, please use correct spelling and don\'t worry about case-sensitivity\n')
                search = input(intervalstuff.interval_menu).strip().lower().title()
                if search in intervalstuff.more_intervals:
                    continue
            if search in intervalstuff.more_intervals:
                if search == 'Circles':
                    print(intervalstuff.circles_prompt)
                    selected_topics[search] = 'More Intervals'
                elif search == 'Orders':
                    print(intervalstuff.orders_prompt)
                    selected_topics[search] = 'More Intervals'
                elif search == 'Quit':
                    sys.exit()
                else:
                    pass
            continue
        elif index_name == 'Quit':
            sys.exit()

    elif user_input == 'Hide':
        topic = input('Enter topic you wish to remove from topic review:\n').strip().lower().title()
        if topic in selected_topics:
            selected_topics.__delitem__(topic)
        else:
            print("Topic already removed OR hasn't been searched for")

    elif user_input == 'Print':
        for topic in selected_topics:
            if topic in scalestuff.scale_list:
                print('{} found within {}'.format(topic.title(), table_of_contents[0]))
            if topic in modestuff.mode_list:
                print('{} found within {}'.format(topic.title(), table_of_contents[1]))
            if topic in intervalstuff.interval_topics:
                print('{} found within {}'.format(topic.title(), table_of_contents[2]))
            if topic in intervalstuff.more_intervals:
                print('{} found within {}'.format(topic.title(), table_of_contents[3]))
        if len(selected_topics) == 0:
            print('Nothin\' here.')
    else:
        print('Unknown command.')

    user_input = input(main_menu_prompt[26:]).strip().lower().title()
