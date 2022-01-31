
# https://www.youtube.com/watch?v=n6I58WJiKGU&t=368s


from pywebio import *
from pywebio.input import *
from pywebio.output import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image
import random
import copy
from pywebio import start_server
import argparse

def main():


    # for multiple inputs to be on the same page you need ot use the name argument for each input

    user_inputs = input_group('Roll information.', [

        input('How many Attack dice are you rolling?', name='attack', required=True,
              help_text='This Field cannot be empty',
              placeholder='Attack Dice'
              ),

        #radio(label='How many Dice does the Attacker roll?', options=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        #      required=True, name='attack'),

        radio(label='How many Dice can the Attacker re-roll?', options=[0, 1, 2, 3, 'All'],
              required=True, name='attack_reroll'),

        input('How many Defense dice are you rolling?', name='defend', required=True,
              help_text='This Field cannot be empty',
              placeholder='Defense Dice'
              ),

        #radio(label='How many Dice does the Defender roll?', options=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        #      required=True, name='defend'),

        radio(label='How many Dice can the Defender re-roll?', options=[0, 1, 2, 3, 'All'],
              required=True, name='defend_reroll'),

        checkbox(label='Defending model power dice mods.',
                 options=['Remove wilds from attacker? (is MODOK defending)',
                          'Reduce damage by 1 to a minimum of 1? (Iron Man''s ability)',
                          'Count blanks on defense? (Black Panthers ability)',
                          'Reduce damage by 1 with no minimum (Crossbones, Thanos)',
                          'Count fails as success (Scarlet witch)',
                          'Defender can reroll fails',
                          'Reality gem on defense',
                          ], name='checkboxdefend'),

        checkbox(label='Attacking model power dice mods.',
                 options=['Pierce, change one hit, crit, or wild to blank',
                          'Count blanks as success on attack roll (Corvus Glaive)',
                          'Count fails as success (Scarlet Witch)',
                          'Do not add dice for crit rolls (Scarlet Witch, Carnage)',
                          'Do not count crits as success(Scarlet Witch)',
                          'Attacker can reroll fails',
                          'Reality gem on attack',
                          ], name='checkboxattack')

    ])

    attack_user_input_roll = int(user_inputs['attack'])
    attack_user_input_reroll = user_inputs['attack_reroll']
    if attack_user_input_reroll == 'All':
        attack_user_input_reroll = 100
    defend_user_input_roll = int(user_inputs['defend'])
    defend_user_input_reroll = user_inputs['defend_reroll']
    if defend_user_input_reroll == 'All':
        defend_user_input_reroll = 100

    display_attack_user_input_reroll = copy.deepcopy(attack_user_input_reroll)
    display_defend_user_input_reroll = copy.deepcopy(defend_user_input_reroll)

    #print(user_inputs['checkbox'])

# defense power mods

    if 'Remove wilds from attacker? (is MODOK defending)' in user_inputs['checkboxdefend']:
        modok = True
    else:
        modok = False

    if 'Reduce damage by 1 to a minimum of 1? (Iron Man''s ability' in user_inputs['checkboxdefend']:
        reduce_damage = True
    else:
        reduce_damage = False

    if 'Count blanks on defense? (Black Panthers ability)' in user_inputs['checkboxdefend']:
        defense_blanks_count = True
    else:
        defense_blanks_count = False

    if 'Count fails as success (Scarlet witch)' in user_inputs['checkboxdefend']:
        defense_fails_count = True
    else:
        defense_fails_count = False

    if 'Reduce damage by 1 with no minimum (Crossbones, Thanos)' in user_inputs['checkboxdefend']:
        reduce_damage_no_min = True
    else:
        reduce_damage_no_min = False

    if 'Defender can reroll fails' in user_inputs['checkboxdefend']:
        d_reroll_fails = True
    else:
        d_reroll_fails = False

    if 'Reality gem on defense' in user_inputs['checkboxdefend']:
        d_reality = True
    else:
        d_reality = False

# attack power mods

    if 'Pierce, change one hit, crit, or wild to blank' in user_inputs['checkboxattack']:
        pierce = True
    else:
        pierce = False

    if 'Count blanks as success on attack roll (Corvus Glaive)' in user_inputs['checkboxattack']:
        attack_blanks_count = True
    else:
        attack_blanks_count = False

    if 'Count fails as success (Scarlet Witch)' in user_inputs['checkboxattack']:
        attack_fails_count = True
    else:
        attack_fails_count = False

    if 'Do not count crits as success(Scarlet Witch)' in user_inputs['checkboxattack']:
        no_count_crit = True
    else:
        no_count_crit = False

    if 'Attacker can reroll fails' in user_inputs['checkboxattack']:
        a_reroll_fails = True
    else:
        a_reroll_fails = False

    if 'Do not add dice for crit rolls (Scarlet Witch, Carnage)' in user_inputs['checkboxattack']:
        no_add_crit = True
    else:
        no_add_crit = False

    if 'Reality gem on attack' in user_inputs['checkboxattack']:
        a_reality = True
    else:
        a_reality = False




    ### VARIABLES SET PROCESS CODE STARTS HERE

    # setting decimals

    np.set_printoptions(precision=2, suppress=True)

    # user inputs


    # required inputs and variables
    roll = ['crit', 'wild', 'hit', 'hit', 'block', 'blank', 'blank', 'failure']
    attack_result_list = []
    attack_reroll_result_list = []
    attack_list_of_lists = []
    attack_crit = 0
    attack_reroll_count = 0


    roll_count = 20000
    pierce_count = 0

    defend_result_list = []
    defend_reroll_result_list = []
    defend_list_of_lists = []
    defend_crit = 0
    defend_reroll_count = 0



    # required variables end -----------------------------------------------------

    for n in range(roll_count):
        # original roll
        for i in range(attack_user_input_roll):
            attack_result_list.append(random.choice(roll))


        # count crits
        for i in attack_result_list:
            if i == 'crit':
                attack_crit += 1
        # reality gem
        if a_reality == True and 'failure' in attack_result_list:
            attack_crit += 1

        if a_reality == True and 'failure' in attack_result_list:
            attack_result_list.remove('failure')
            attack_result_list.append('failure reality')

        # add rolls for crits

        for i in range(attack_crit):
            attack_result_list.append(random.choice(roll))

        # commented out because this was used to check the pierce ability
        # attack_copy = attack_result_list.copy()




        # perform rerolls
        while attack_reroll_count < attack_user_input_reroll and 'failure' in attack_result_list and a_reroll_fails == True:
            attack_reroll_result_list.append(random.choice(roll))
            attack_reroll_count += 1
            attack_result_list.remove('failure')

        while attack_reroll_count < attack_user_input_reroll and 'blank' in attack_result_list:
            attack_reroll_result_list.append(random.choice(roll))
            attack_reroll_count += 1
            attack_result_list.remove('blank')

        while attack_reroll_count < attack_user_input_reroll and 'block' in attack_result_list:
            attack_reroll_result_list.append(random.choice(roll))
            attack_reroll_count += 1
            attack_result_list.remove('block')

        attack_result_list = attack_result_list + attack_reroll_result_list

        if 'failure reality' not in attack_result_list and 'failure' in attack_result_list:
            attack_result_list.remove('failure')
            attack_result_list.append('failure reality')

            ## SHORTER WAY OF CHECKING A LIST AND MODIFYING IT, use this code in other places
        while modok == True and 'wild' in attack_result_list:
            attack_result_list.remove('wild')

        attack_list_of_lists.append(attack_result_list)

        # reset all required variables to 0
        attack_crit = 0
        attack_result_list = []
        attack_reroll_result_list = []
        pierce_count = 0
        attack_reroll_count = 0


        # SINGLE ATTACK ROLL DONE -------------------------------------------------

        # original roll
        for i in range(defend_user_input_roll):
            defend_result_list.append(random.choice(roll))

        # count crits
        for i in defend_result_list:
            if i == 'crit':
                defend_crit += 1
        # reality gem
        if d_reality == True and 'failure' in defend_result_list:
            defend_crit += 1

        if d_reality == True and 'failure' in defend_result_list:
            defend_result_list.remove('failure')
            defend_result_list.append('failure reality')


        # add rolls for crits
        if no_add_crit == False:
            for i in range(defend_crit):
                defend_result_list.append(random.choice(roll))



        # perform rerolls
        while defend_reroll_count < defend_user_input_reroll and 'failure' in defend_result_list and d_reroll_fails == True:
            defend_reroll_result_list.append(random.choice(roll))
            defend_reroll_count += 1
            defend_result_list.remove('failure')

        while defend_reroll_count < defend_user_input_reroll and 'blank' in defend_result_list:
            defend_reroll_result_list.append(random.choice(roll))
            defend_reroll_count += 1
            defend_result_list.remove('blank')

        while defend_reroll_count < defend_user_input_reroll and 'hit' in defend_result_list:
            defend_reroll_result_list.append(random.choice(roll))
            defend_reroll_count += 1
            defend_result_list.remove('hit')

        defend_result_list = defend_result_list + defend_reroll_result_list
        if 'failure reality' not in defend_result_list and 'failure' in defend_result_list:
            defend_result_list.remove('failure')
            defend_result_list.append('failure reality')

        if pierce == True and pierce_count == 0:
            if 'wild' in defend_result_list:
                defend_result_list.remove('wild')
                defend_result_list.append('blank')
                pierce_count += 1
            elif 'crit' in defend_result_list:
                defend_result_list.remove('crit')
                defend_result_list.append('blank')
                pierce_count += 1
            elif 'hit' in defend_result_list:
                defend_result_list.remove('hit')
                defend_result_list.append('blank')
                pierce_count += 1

        defend_list_of_lists.append(defend_result_list)

        # reset all required variables to 0
        defend_crit = 0
        defend_result_list = []
        defend_reroll_count = 0
        defend_reroll_result_list = []



        # SINGLE DEFENSE ROLL DONE ------------------------------------------------

    # LOOPS n times ---------------------------------------------------------------

    attack_df = pd.DataFrame(attack_list_of_lists)

    defend_df = pd.DataFrame(defend_list_of_lists)

    # powers that effect attack calculation ---------------------------------------

    attack_df['success count'] = attack_df.eq('crit').sum(axis=1) + attack_df.eq('hit').sum(axis=1) + attack_df.eq(
        'wild').sum(axis=1)


    if a_reality == True:
        attack_df['success count'] = attack_df['success count'] + attack_df.eq('failure reality').sum(axis=1)

    if attack_blanks_count == True:
        attack_df['success count'] = attack_df['success count'] + attack_df.eq('blank').sum(axis=1)

    if attack_fails_count == True:
        attack_df['success count'] = attack_df['success count'] + attack_df.eq('failure').sum(axis=1)

    # powers that effect defense calculation --------------------------------------

    defend_df['success count'] = defend_df.eq('crit').sum(axis=1) + defend_df.eq('wild').sum(axis=1) + defend_df.eq(
        'block').sum(axis=1)

    if d_reality == True:
        defend_df['success count'] = defend_df['success count'] + defend_df.eq('failure reality').sum(axis=1)

    if defense_blanks_count == True:
        defend_df['success count'] = defend_df['success count'] + defend_df.eq('blank').sum(axis=1)

    if defense_fails_count == True:
        defend_df['success count'] = defend_df['success count'] + defend_df.eq('failure').sum(axis=1)

    if no_count_crit == True:
        defend_df['success count'] = defend_df['success count'] - defend_df.eq('crit').sum(axis=1)

    # Comparison starts here ------------------------------------------------------

    # plot attack
    attack_bar_chart = attack_df['success count'].value_counts().reset_index().values
    attack_bar_chart = pd.DataFrame(attack_bar_chart)
    attack_bar_chart.rename(columns={0: 'Hits', 1: 'Hits Count'}, inplace=True)
    attack_bar_chart = attack_bar_chart.sort_values(by=['Hits'])
    attack_ax = attack_bar_chart.plot.bar(x='Hits', y='Hits Count', rot=0)

    a_result_image = io.BytesIO()
    plt.savefig(a_result_image, format='png')
    im_a_final = Image.open(a_result_image)
    # im_a_final.show(title="My Image")

    # plot defense
    defend_bar_chart = defend_df['success count'].value_counts().reset_index().values
    defend_bar_chart = pd.DataFrame(defend_bar_chart)
    defend_bar_chart.rename(columns={0: 'Blocks', 1: 'Blocks Count'}, inplace=True)
    defend_bar_chart = defend_bar_chart.sort_values(by=['Blocks'])
    defend_ax = defend_bar_chart.plot.bar(x='Blocks', y='Blocks Count', rot=0)

    d_result_image = io.BytesIO()
    plt.savefig(d_result_image, format='png')
    im_d_final = Image.open(d_result_image)
    # im_d_final.show(title="My Image")

    data = [attack_df['success count'], defend_df['success count']]
    headers = ['attack success', 'defend success']
    comparison_df = pd.concat(data, axis=1, keys=headers)
    comparison_df['hits through'] = comparison_df['attack success'] - comparison_df['defend success']

    # reduce damage power
    if reduce_damage == True:
        comparison_df['hits through'][comparison_df['hits through'] > 1] = [comparison_df['hits through'] - 1]

    # reduce magame power no min
    if reduce_damage_no_min == True:
        comparison_df['hits through'][comparison_df['hits through'] > 0] = [comparison_df['hits through'] - 1]

    comparison_df['hits through'][comparison_df['hits through'] < 0] = 0

    final_comparison_df = comparison_df['hits through'].value_counts().reset_index().values
    final_comparison_df = pd.DataFrame(final_comparison_df)
    final_comparison_df.rename(columns={0: 'hits through', 1: 'hits through count'}, inplace=True)
    final_comparison_df = final_comparison_df.sort_values(by=['hits through'])
    # final_comparison_df['pareto'] = 100 * final_comparison_df['hits through count'].cumsum() / final_comparison_df['hits through count'].sum()
    final_comparison_df['percentage'] = 100 * final_comparison_df['hits through count'] / roll_count
    final_comparison_df['percentage'] = final_comparison_df['percentage'].round(1)

    fig, final_comparison_df_ax = plt.subplots()
    ax1 = final_comparison_df.plot(x='hits through', y='hits through count', kind='bar', ax=final_comparison_df_ax)
    ax2 = final_comparison_df.plot(x='hits through', y='percentage', marker='D', color='C1', kind='line',
                                   ax=final_comparison_df_ax, secondary_y=True)
    ax2.set_ylim([0, 110, ])
    ax2.set_ylabel('percentage')

    for a, b in zip(final_comparison_df['hits through'], final_comparison_df['percentage']):
        plt.text(a, b, str(b), color='k')

    final_result_image = io.BytesIO()
    plt.savefig(final_result_image, format='png')
    im_final = Image.open(final_result_image)
    # im_final.show(title="My Image")

    if display_attack_user_input_reroll == 100:
        attack_user_input_reroll = 'All'

    if display_defend_user_input_reroll == 100:
        defend_user_input_reroll = 'All'

    put_text('Here are the results of 20,000 opposing dice rolls!')
    put_text('Your selections for this analysis are as follows:')
    put_text('attacker rolled' , attack_user_input_roll, 'dice. with', display_attack_user_input_reroll, 'possible re-rolls.')
    put_text('defender rolled', defend_user_input_roll, 'dice. with', display_defend_user_input_reroll, 'possible re-rolls.')
    put_text('Active dice mods are:')
    if pierce == True:
        put_text('pierce = ', pierce)
    if modok == True:
        put_text('attacking MODOK = ', modok)
    if attack_blanks_count == True:
        put_text('attack counts blanks = ', attack_blanks_count)
    if attack_fails_count == True:
         put_text('attack counts fails = ', attack_fails_count)
    if defense_blanks_count == True:
        put_text('defense counts blanks = ', defense_blanks_count)
    if defense_fails_count == True:
        put_text('defense counts fails = ', defense_fails_count)
    if reduce_damage == True:
        put_text('reduce damage by 1 to a minimum of 1 = ', reduce_damage)
    if reduce_damage_no_min == True:
        put_text('reduce damage by 1 no minimum = ', reduce_damage_no_min)
    if no_add_crit == True:
        put_text('Do not add dice for crit rolls = ', no_add_crit)
    if no_count_crit == True:
        put_text('do not count crits on defense = ', no_count_crit)
    if a_reroll_fails == True:
        put_text('attacker can reroll fails = ', a_reroll_fails)
    if d_reroll_fails == True:
        put_text('defender can reroll fails = ', d_reroll_fails)
    if a_reality == True:
        put_text('Reality gem on attack  = ', a_reality)
    if d_reality == True:
        put_text('Reality gem on defense  = ', d_reality)

    put_text('If you like this tool and want to support my plastic habit Venmo me a Dollar!')

    put_image('https://raw.githubusercontent.com/jasonoglio/Heroku-Test/main/IMG_0760.jpg', format=None, title='',
              width='200px')
    put_html(
        '<br>'
        '<a href="https://venmo.com/code?user_id=2476107391565824379&created=1643651982.598431&printed=1">My Venmo</a>'
        '<br>'
        '<br>')

    put_text("Thanks Nick T. and Richard M. Gamora's super power is in the works!")
    put_text('Bar Chart showing distribution of attack dice outcomes.')
    put_image(src=im_a_final)
    put_text('Bar Chart showing distribution of defense dice outcomes.')
    put_image(src=im_d_final)
    put_text('Bar Chart showing distribution of opposing roll dice outcomes.')
    put_text('The yellow line shows the % chance of each outcome using the right y axis.')
    put_image(src=im_final)

    print('process complete')
    put_text('process complete')
    put_text('for questions comments or requesting changes')
    put_text('contact jasonoglio@gmail.com')
    put_text('If you like this tool and want to support my plastic habit Venmo me a Dollar!')

    
    put_html(
        '<br>'
        '<a href="https://venmo.com/code?user_id=2476107391565824379&created=1643651982.598431&printed=1">My Venmo</a>'
        '<br>'
        '<br>')

    put_text("Thanks Nick T. and Richard M. Gamora's super power is in the works!")


    

    #print(modok)
    #print(reduce_damage)
    #print(defense_blanks_count)


# https://www.youtube.com/watch?v=sqR154NkwZk

# this section is for Heroku
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port)

#if __name__ == '__main__':
#    main()

# create requirements text document
# https://stackoverflow.com/questions/31684375/automatically-create-requirements-txt


#start your virtual environment inside your project directory with "pipenv install FIRST PACKAGE"

#start the virtual env with "pipenv shell"


#making requiremnts file:
#	pip install pipreqs

#	pipreqs /path/to/project
