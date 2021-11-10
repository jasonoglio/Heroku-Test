
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

        checkbox(options=['Remove wilds from attacker? (Are you attacking MODOK)',
                          'Reduce damage by 1 to a minimum of 1? (Iron Man''s ability',
                          'Count blanks on defense? (Black Panthers ability)',
                          'Pierce, change one hit, crit, or wild to blank'
                          ], name='checkbox'),


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

    if 'Remove wilds from attacker? (Are you attacking MODOK)' in user_inputs['checkbox']:
        modok = True
    else:
        modok = False

    if 'Reduce damage by 1 to a minimum of 1? (Iron Man''s ability' in user_inputs['checkbox']:
        reduce_damage = True
    else:
        reduce_damage = False

    if 'Count blanks on defense? (Black Panthers ability)' in user_inputs['checkbox']:
        defense_blanks_count = True
    else:
        defense_blanks_count = False

    if 'Pierce, change one hit, crit, or wild to blank' in user_inputs['checkbox']:
        pierce = True
    else:
        pierce = False


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
    attack_rerolls_complete = 0
    attack_number_of_dice_removed = 0
    roll_count = 20000
    pierce_count = 0

    defend_result_list = []
    defend_reroll_result_list = []
    defend_list_of_lists = []
    defend_crit = 0
    defend_rerolls_complete = 0
    defend_number_of_dice_removed = 0

    # required variables end -----------------------------------------------------

    for n in range(roll_count):
        # original roll
        for i in range(attack_user_input_roll):
            attack_result_list.append(random.choice(roll))

        # count crits
        for i in attack_result_list:
            if i == 'crit':
                attack_crit += 1

        # add rolls for crits
        for i in range(attack_crit):
            attack_result_list.append(random.choice(roll))

        # commented out because this was used to check the pierce ability
        # attack_copy = attack_result_list.copy()

        if pierce == True and pierce_count == 0:
            if 'wild' in attack_result_list:
                attack_result_list.remove('wild')
                pierce_count += 1
            elif 'crit' in attack_result_list:
                attack_result_list.remove('crit')
                pierce_count += 1
            elif 'hit' in attack_result_list:
                attack_result_list.remove('hit')
                pierce_count += 1

        # count total possible rerolls
        attack_block_count = attack_result_list.count('block')
        attack_blank_count = attack_result_list.count('blank')
        attack_total_possible_re_roll = attack_blank_count + attack_block_count

        # set actual reroll amount
        if attack_total_possible_re_roll < attack_user_input_reroll:
            attack_user_input_reroll = attack_total_possible_re_roll

        # commented out because this is a variable for double checking reroll and crit
        # attack_copy = attack_result_list.copy()

        # perform rerolls
        while attack_rerolls_complete < attack_user_input_reroll:
            attack_reroll_result_list.append(random.choice(roll))
            attack_rerolls_complete += 1

        # remove rerolled dice
        while attack_block_count > 0 and attack_total_possible_re_roll > 0 and attack_user_input_reroll > 0:
            attack_result_list.remove('block')
            attack_block_count -= 1
            attack_total_possible_re_roll -= 1
            attack_number_of_dice_removed += 1
            attack_user_input_reroll -= 1

        while attack_blank_count > 0 and attack_total_possible_re_roll > 0 and attack_user_input_reroll > 0:
            attack_result_list.remove('blank')
            attack_blank_count -= 1
            attack_total_possible_re_roll -= 1
            attack_number_of_dice_removed += 1
            attack_user_input_reroll -= 1

        # combine reroll list to original roll list which has had dice removed
        attack_result_list = attack_result_list + attack_reroll_result_list

        attack_list_of_lists.append(attack_result_list)

        # reset all required variables to 0
        attack_crit = 0
        attack_rerolls_complete = 0
        attack_number_of_dice_removed = 0
        attack_block_count = 0
        attack_blank_count = 0
        attack_result_list = []
        attack_reroll_result_list = []
        pierce_count = 0

        # SINGLE ATTACK ROLL DONE -------------------------------------------------

        # original roll
        for i in range(defend_user_input_roll):
            defend_result_list.append(random.choice(roll))

        # count crits
        for i in defend_result_list:
            if i == 'crit':
                defend_crit += 1

        # add rolls for crits
        for i in range(defend_crit):
            defend_result_list.append(random.choice(roll))

        # count total possible rerolls
        defend_hit_count = defend_result_list.count('hit')
        defend_blank_count = defend_result_list.count('blank')
        defend_total_possible_re_roll = defend_blank_count + defend_hit_count

        # set actual reroll amount
        if defend_total_possible_re_roll < defend_user_input_reroll:
            defend_user_input_reroll = defend_total_possible_re_roll

        # commented out because this is a variable for double checking reroll and crit
        # defend_copy = defend_result_list.copy()

        # perform rerolls
        while defend_rerolls_complete < defend_user_input_reroll:
            defend_reroll_result_list.append(random.choice(roll))
            defend_rerolls_complete += 1

        # remove rerolled dice
        while defend_hit_count > 0 and defend_total_possible_re_roll > 0 and defend_user_input_reroll > 0:
            defend_result_list.remove('hit')
            defend_hit_count -= 1
            defend_total_possible_re_roll -= 1
            defend_number_of_dice_removed += 1
            defend_user_input_reroll -= 1

        while defend_blank_count > 0 and defend_total_possible_re_roll > 0 and defend_user_input_reroll > 0:
            defend_result_list.remove('blank')
            defend_blank_count -= 1
            defend_total_possible_re_roll -= 1
            defend_number_of_dice_removed += 1
            defend_user_input_reroll -= 1

        # combine reroll list to original roll list which has had dice removed
        defend_result_list = defend_result_list + defend_reroll_result_list

        defend_list_of_lists.append(defend_result_list)

        # reset all required variables to 0
        defend_crit = 0
        defend_rerolls_complete = 0
        defend_number_of_dice_removed = 0
        defend_hit_count = 0
        defend_blank_count = 0
        defend_result_list = []
        defend_reroll_result_list = []

        # SINGLE DEFENSE ROLL DONE ------------------------------------------------

    # LOOPS n times ---------------------------------------------------------------

    attack_df = pd.DataFrame(attack_list_of_lists)

    defend_df = pd.DataFrame(defend_list_of_lists)

    # powers that effect attack calculation ---------------------------------------

    if modok == True:
        attack_df['success count'] = attack_df.eq('crit').sum(axis=1) + attack_df.eq('hit').sum(axis=1)
    else:
        attack_df['success count'] = attack_df.eq('crit').sum(axis=1) + attack_df.eq('hit').sum(axis=1) + attack_df.eq(
            'wild').sum(axis=1)

    # powers that effect defense calculation --------------------------------------

    # pierce added to individual roll for ease
    # reduce damage power added in the end at success calculation

    if defense_blanks_count == True:
        defend_df['success count'] = defend_df.eq('crit').sum(axis=1) + defend_df.eq('wild').sum(axis=1) + defend_df.eq(
            'block').sum(axis=1) + defend_df.eq('blank').sum(axis=1)
    else:
        defend_df['success count'] = defend_df.eq('crit').sum(axis=1) + defend_df.eq('wild').sum(axis=1) + defend_df.eq(
            'block').sum(axis=1)

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

    comparison_df['hits through'][comparison_df['hits through'] < 0] = 0

    final_comparison_df = comparison_df['hits through'].value_counts().reset_index().values
    final_comparison_df = pd.DataFrame(final_comparison_df)
    final_comparison_df.rename(columns={0: 'hits through', 1: 'hits through count'}, inplace=True)
    final_comparison_df = final_comparison_df.sort_values(by=['hits through'])
    # final_comparison_df['pareto'] = 100 * final_comparison_df['hits through count'].cumsum() / final_comparison_df['hits through count'].sum()
    final_comparison_df['percentage'] = 100 * final_comparison_df['hits through count'] / roll_count

    fig, final_comparison_df_ax = plt.subplots()
    ax1 = final_comparison_df.plot(x='hits through', y='hits through count', kind='bar', ax=final_comparison_df_ax)
    ax2 = final_comparison_df.plot(x='hits through', y='percentage', marker='D', color='k', kind='line',
                                   ax=final_comparison_df_ax, secondary_y=True)
    ax2.set_ylim([0, 110, ])
    ax2.set_ylabel('percentage')

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
    put_text('defense counts blanks = ', defense_blanks_count)
    put_text('attacking MODOK = ', modok)
    put_text('reduce damage by 1 to a minimum of 1 = ', reduce_damage)
    put_text('pierce = ', pierce)

    put_text('Bar Chart showing distribution of attack dice outcomes.')
    put_image(src=im_a_final)
    put_text('Bar Chart showing distribution of defense dice outcomes.')
    put_image(src=im_d_final)
    put_text('Bar Chart showing distribution of opposing roll dice outcomes.')
    put_text('The black line shows the % chance of each outcome using the right y axis.')
    put_image(src=im_final)

    print('process complete')
    put_text('process complete')


    

    #print(modok)
    #print(reduce_damage)
    #print(defense_blanks_count)


# https://www.youtube.com/watch?v=sqR154NkwZk

# this section is for Heroku
#if __name__ == '__main__':
#    parser = argparse.ArgumentParser()
#    parser.add_argument("-p", "--port", type=int, default=8080)
#    args = parser.parse_args()

#    start_server(main, port=args.port)

if __name__ == '__main__':
    main()

# create requirements text document
# https://stackoverflow.com/questions/31684375/automatically-create-requirements-txt


#start your virtual environment inside your project directory with "pipenv install FIRST PACKAGE"

#start the virtual env with "pipenv shell"


#making requiremnts file:
#	pip install pipreqs

#	pipreqs /path/to/project
