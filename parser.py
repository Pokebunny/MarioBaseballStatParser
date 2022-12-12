import json
import os

# import time
# import wpcc
# from scipy.stats import pearsonr

print("Enter username of player (blank for all stats):")
user = input()
print("Enter '0' for stars-off data; '1' for stars-on")
stars = int(input())
print("Enter '0' for all data, '1' for ranked only")
ranked = int(input())

directory = "C:\\Users\\nrtab\\Documents\\Project Rio\\StatFiles\\"
if user != "Pokebunny" and user != "ajkei":
    directory += user
if directory.endswith("."):
    directory = directory[:-1]

game_id_list = []
outs_pitched_list = []
runs_allowed_list = []
hits_allowed_list = []
walks_allowed_list = []
homeruns_allowed_list = []
strikeouts_list = []
batters_faced_list = []

player_dict = {}
contact_events = 0
character_dict = {}

pa_count = 0
total_states = {"0000": 0, "0100": 0, "0020": 0, "0003": 0, "0120": 0, "0103": 0, "0023": 0, "0123": 0,
                "1000": 0, "1100": 0, "1020": 0, "1003": 0, "1120": 0, "1103": 0, "1023": 0, "1123": 0,
                "2000": 0, "2100": 0, "2020": 0, "2003": 0, "2120": 0, "2103": 0, "2023": 0, "2123": 0}
total_runs = {"0000": 0, "0100": 0, "0020": 0, "0003": 0, "0120": 0, "0103": 0, "0023": 0, "0123": 0,
              "1000": 0, "1100": 0, "1020": 0, "1003": 0, "1120": 0, "1103": 0, "1023": 0, "1123": 0,
              "2000": 0, "2100": 0, "2020": 0, "2003": 0, "2120": 0, "2103": 0, "2023": 0, "2123": 0}


def add_files(dir):
    global total_states, total_runs
    for entry in os.scandir(dir):
        if entry.is_dir():
            # uncomment the following line to add subdirectories
            # add_files(entry)
            pass
        elif (entry.name.startswith("decoded.") or entry.name.startswith("crash.decoded")) and entry.name.endswith(".json"):
            full_path = os.path.join(dir, entry.name)
            print(full_path)
            file = open(full_path, encoding='utf-8')
            stat_file = json.load(file)
            stars_on = 0
            for character in stat_file["Character Game Stats"].values():
                if character["Superstar"] == 1:
                    stars_on = 1
            if stat_file["GameID"] not in game_id_list and stat_file["Ranked"] >= ranked and stars == stars_on:
                game_id_list.append(stat_file["GameID"])
                for character in stat_file["Character Game Stats"].values():
                    char_name = character["CharID"]

                    if ((character["Team"] == "0" and stat_file["Away Player"] == user)
                            or (character["Team"] == "1" and stat_file["Home Player"] == user) or user == ""):
                        if char_name not in character_dict:
                            character_dict[char_name] = {}
                            character_dict[char_name]["Offensive Stats"] = character["Offensive Stats"]
                            character_dict[char_name]["Defensive Stats"] = character["Defensive Stats"]
                            character_dict[char_name]["Fielding Stats"] = {}
                            character_dict[char_name]["Winrate Stats"] = {"Games Played": 0, "Wins": 0}
                        else:
                            for stat in character["Offensive Stats"]:
                                if stat in character_dict[char_name]["Offensive Stats"]:
                                    character_dict[char_name]["Offensive Stats"][stat] += character["Offensive Stats"][stat]
                                else:
                                    character_dict[char_name]["Offensive Stats"][stat] = character["Offensive Stats"][stat]
                            for stat in character["Defensive Stats"]:
                                if stat in character_dict[char_name]["Defensive Stats"]:
                                    character_dict[char_name]["Defensive Stats"][stat] += character["Defensive Stats"][stat]
                                else:
                                    character_dict[char_name]["Defensive Stats"][stat] = character["Defensive Stats"][stat]

                            # CHARACTER FIP STUFF
                            # if outs_pitched > 5:
                            #     outs_pitched_list.append(outs_pitched)
                            #     runs_allowed_list.append(character["Defensive Stats"]["Runs Allowed"] / outs_pitched)
                            #     hits_allowed_list.append(character["Defensive Stats"]["Hits Allowed"] / outs_pitched)
                            #     walks_allowed_list.append(
                            #         character["Defensive Stats"]["Batters Walked"] + character["Defensive Stats"][
                            #             "Batters Hit"] / outs_pitched)
                            #     homeruns_allowed_list.append(character["Defensive Stats"]["HRs Allowed"] / outs_pitched)
                            #     strikeouts_list.append(character["Defensive Stats"]["Strikeouts"] / outs_pitched)
                            #     batters_faced_list.append(character["Defensive Stats"]["Batters Faced"])

                            # PLAYER FIP STUFF
                            # player = ""
                            # if character["Team"] == "Away" and stat_file["Away Player"] != "Netplayer~" and stat_file["Away Player"] != "CPU":
                            #     player = stat_file["Away Player"]
                            # if character["Team"] == "Home" and stat_file["Home Player"] != "Netplayer~" and stat_file["Home Player"] != "CPU":
                            #     player = stat_file["Home Player"]
                            #
                            # if player != "":
                            #     if player in player_dict:
                            #         for stat in character["Defensive Stats"]:
                            #             if stat in player_dict[player]:
                            #                 player_dict[player][stat] += character["Defensive Stats"][stat]
                            #             else:
                            #                 player_dict[player][stat] = character["Defensive Stats"][stat]
                            #     else:
                            #         player_dict[player] = {}
                            #         for stat in character["Defensive Stats"]:
                            #             player_dict[player][stat] = character["Defensive Stats"][stat]

                        # Character winrates
                        if (character["Team"] == "0" and stat_file["Away Score"] > stat_file["Home Score"]) \
                                or (character["Team"] == "1" and stat_file["Home Score"] > stat_file["Away Score"]):
                            character_dict[char_name]["Winrate Stats"]["Wins"] += 1
                        character_dict[char_name]["Winrate Stats"]["Games Played"] += 1

                        # Fielding stats

                        # for pitch_summary in character["Pitch Summary"]:
                        #     if "Fielding Summary" in pitch_summary["Contact Summary"][0]:
                        #         contact_events += 1
                        #         if pitch_summary["Number Outs During Play"] > 0:
                        #             fielding_summary = pitch_summary["Contact Summary"][0]["Fielding Summary"]
                        #             fielder = fielding_summary[0]["Fielder Character"]
                        #             fielder_position = fielding_summary[0]["Fielder Position"]
                        #             # if

                # DERIVE RUN EXPECTANCY

                # Base out states are represented as a four-digit number where the first digit is the number of outs,
                # and the remaining digits represent baserunners on corresponding bases.
                # 1103 = Runners on first and third, one out
                """
                curr_states = {"0000": 0, "0100": 0, "0020": 0, "0003": 0, "0120": 0, "0103": 0, "0023": 0, "0123": 0,
                               "1000": 0, "1100": 0, "1020": 0, "1003": 0, "1120": 0, "1103": 0, "1023": 0, "1123": 0,
                               "2000": 0, "2100": 0, "2020": 0, "2003": 0, "2120": 0, "2103": 0, "2023": 0, "2123": 0}
                curr_runs = {"0000": 0, "0100": 0, "0020": 0, "0003": 0, "0120": 0, "0103": 0, "0023": 0, "0123": 0,
                             "1000": 0, "1100": 0, "1020": 0, "1003": 0, "1120": 0, "1103": 0, "1023": 0, "1123": 0,
                             "2000": 0, "2100": 0, "2020": 0, "2003": 0, "2120": 0, "2103": 0, "2023": 0, "2123": 0}

                prev_event = {}
                prev_base_out_state = "0000"
                curr_inning = 1
                curr_half_inning = 0
                for event in stat_file["Events"]:
                    outs = event["Outs"]
                    baserunners = [0, 0, 0]
                    if "Runner 1B" in event:
                        baserunners[0] = 1
                    if "Runner 2B" in event:
                        baserunners[1] = 2
                    if "Runner 3B" in event:
                        baserunners[2] = 3
                    base_out_state = str(outs) + str(baserunners[0]) + str(baserunners[1]) + str(baserunners[2])

                    # if this is the first batter of the game... we skip it because everything relies on the previous event?
                    if prev_event == {}:
                        prev_event = event
                        continue

                    # If the at-bat has ended or the base-out state has changed, add the previous base-out state to the inning
                    if prev_base_out_state != base_out_state or \
                            prev_event["Away Score"] != event["Away Score"] or prev_event["Home Score"] != event["Home Score"]:
                        curr_states[prev_base_out_state] += 1

                    # If the score has changed, add the runs to all base out states in the inning for each time the base out state occurred.
                    if prev_event["Away Score"] != event["Away Score"] or prev_event["Home Score"] != event["Home Score"]:
                        runs_on_play = (event["Away Score"] - prev_event["Away Score"]) + (event["Home Score"] - prev_event["Home Score"])
                        for state in curr_runs:
                            curr_runs[state] += (runs_on_play * curr_states[state])

                    # If we're in a new inning, reset the run and state counts and add them to the total.
                    if prev_event["Inning"] != event["Inning"] or prev_event["Half Inning"] != event["Half Inning"]:
                        # add the state counts
                        for state in curr_states:
                            total_states[state] += curr_states[state]
                        # add the run counts
                        for state in curr_runs:
                            total_runs[state] += curr_runs[state]

                        # reset state and run counts to zero
                        curr_states = {"0000": 0, "0100": 0, "0020": 0, "0003": 0, "0120": 0, "0103": 0, "0023": 0, "0123": 0,
                                       "1000": 0, "1100": 0, "1020": 0, "1003": 0, "1120": 0, "1103": 0, "1023": 0, "1123": 0,
                                       "2000": 0, "2100": 0, "2020": 0, "2003": 0, "2120": 0, "2103": 0, "2023": 0, "2123": 0}
                        curr_runs = {"0000": 0, "0100": 0, "0020": 0, "0003": 0, "0120": 0, "0103": 0, "0023": 0, "0123": 0,
                                     "1000": 0, "1100": 0, "1020": 0, "1003": 0, "1120": 0, "1103": 0, "1023": 0, "1123": 0,
                                     "2000": 0, "2100": 0, "2020": 0, "2003": 0, "2120": 0, "2103": 0, "2023": 0, "2123": 0}

                    # print(base_out_state, prev_base_out_state)
                    prev_event = event
                    prev_base_out_state = base_out_state
                """
    return character_dict


def output_results(char_dict):
    # Print run expectancy matrix
    # for s in total_states:
    #     print(s, "{:.3f}".format(total_runs[s] / total_states[s]))
    sorted_batter_list = sorted(char_dict.keys(), key=lambda x: (char_dict[x]["Offensive Stats"]["At Bats"] +
                                                                 char_dict[x]["Offensive Stats"]["Walks (4 Balls)"] +
                                                                 char_dict[x]["Offensive Stats"]["Walks (Hit)"]), reverse=True)

    print("Files counted:", len(game_id_list))
    print("BATTERS: AVG / OBP / SLG / OPS")

    # Print offensive stats for each
    o_totals = {}
    for char in sorted_batter_list:
        o_stats = char_dict[char]["Offensive Stats"]
        if o_stats["At Bats"] > 0:
            avg = o_stats["Hits"] / o_stats["At Bats"]
            pa = o_stats["At Bats"] + o_stats["Walks (4 Balls)"] + o_stats["Walks (Hit)"]
            obp = (o_stats["Hits"] + o_stats["Walks (4 Balls)"] + o_stats["Walks (Hit)"]) / pa
            slg = (o_stats["Singles"] + (o_stats["Doubles"] * 2) + (o_stats["Triples"] * 3) + (o_stats["Homeruns"] * 4)) / (o_stats["At Bats"])

            print(str(char) + " (" + str(pa) + " PA): " + "{:.3f}".format(avg) + " / " + "{:.3f}".format(obp) + " / " +
                  "{:.3f}".format(slg) + " / " + "{:.3f}".format(obp + slg) + ", " + str(o_stats["Homeruns"]) + " HR")

            for stat in o_stats:
                if stat in o_totals:
                    o_totals[stat] += o_stats[stat]
                else:
                    o_totals[stat] = o_stats[stat]

    # print offensive stat totals
    avg = o_totals["Hits"] / o_totals["At Bats"]
    pa = o_totals["At Bats"] + o_totals["Walks (4 Balls)"] + o_totals["Walks (Hit)"]
    obp = (o_totals["Hits"] + o_totals["Walks (4 Balls)"] + o_totals["Walks (Hit)"]) / pa
    slg = (o_totals["Singles"] + (o_totals["Doubles"] * 2) + (o_totals["Triples"] * 3) + (o_totals["Homeruns"] * 4)) / (
        o_totals["At Bats"])
    print("\nTOTAL (" + str(pa) + " PA): " + "{:.3f}".format(avg) + " / " + "{:.3f}".format(
        obp) + " / " + "{:.3f}".format(
        slg) + " / " + "{:.3f}".format(obp + slg) + ", " + str(o_totals["Homeruns"]) + " HR")

    # Print pitching stats for each character
    sorted_pitcher_list = sorted(char_dict.keys(), key=lambda x: char_dict[x]["Defensive Stats"]["Batters Faced"],
                                 reverse=True)
    d_totals = {}
    print("\nPITCHERS")
    for char in sorted_pitcher_list:
        d_stats = char_dict[char]["Defensive Stats"]
        outs_pitched = d_stats["Outs Pitched"]
        if outs_pitched > 0:
            IP = (outs_pitched // 3) + (0.1 * (outs_pitched % 3))
            ERA = d_stats["Runs Allowed"] / (outs_pitched / 27)
            K = d_stats["Strikeouts"]
            print(str(char) + " (" + str(IP) + " IP): " + "{:.2f}".format(ERA) + " ERA, " + str(K) + " K")
            # PITCHES PER INNING
            # if d_stats["Outs Pitched"] > 0:
            #     print("Pitches per Inning: " + "{:.2f}".format(d_stats["Pitches Thrown"] / d_stats["Outs Pitched"] * 3))
            #     print("Walks/Hits per Inning: " + "{:.2f}".format((d_stats["Hits Allowed"] + d_stats["Batters Walked"] + d_stats["Batters Hit"]) / d_stats["Outs Pitched"] * 3))
            #     print("Runs per Inning: " + "{:.2f}".format(d_stats["Runs Allowed"] / d_stats["Outs Pitched"] * 3))

            for stat in d_stats:
                if stat in d_totals:
                    d_totals[stat] += d_stats[stat]
                else:
                    d_totals[stat] = d_stats[stat]

    # Print pitching stat totals
    outs_pitched = d_totals["Outs Pitched"]
    IP = str((outs_pitched // 3) + (0.1 * (outs_pitched % 3)))
    ERA = d_totals["Runs Allowed"] / (outs_pitched / 27)
    K = d_totals["Strikeouts"]

    print("\nTOTAL (" + IP + " IP): " + "{:.2f}".format(ERA) + " ERA, " + str(K) + " K")

    sorted_winrate_list = sorted(char_dict.keys(),
                                 key=lambda x: char_dict[x]["Winrate Stats"]["Games Played"],
                                 reverse=True)

    # Print winrate stats
    print("\nWINRATES")
    total_games_played = 0
    total_wins = 0
    for char in sorted_winrate_list:
        if char_dict[char]["Winrate Stats"]["Games Played"] > 0:
            print(str(char), "(" + str(char_dict[char]["Winrate Stats"]["Games Played"]) + " Games):", "{:.2f}".format(
                char_dict[char]["Winrate Stats"]["Wins"] / char_dict[char]["Winrate Stats"][
                    "Games Played"] * 100) + "%")
            total_games_played += char_dict[char]["Winrate Stats"]["Games Played"]
            total_wins += char_dict[char]["Winrate Stats"]["Wins"]
    print("TOTAL (" + str(total_games_played // 9) + " Games):", "{:.2f}".format(total_wins / total_games_played * 100) + "%")


output_results(add_files(directory))

# FIP CALCULATIONS
# hits_allowed = d_totals["Hits Allowed"]
# walks_allowed = d_totals["Batters Walked"] + d_totals["Batters Hit"]
# home_runs_allowed = d_totals["HRs Allowed"]

# print("TOTALS")
# print("Hits: " + str(hits_allowed / true_IP) + ", Walks: " + str(walks_allowed / true_IP) + ", Home Runs: " + str(
#     home_runs_allowed / true_IP))
# print("Correlation between strikeouts and runs allowed:",
#       wpcc.wpearson(strikeouts_list, runs_allowed_list, batters_faced_list))

# print("Correlation between hits and runs allowed:",
#       wpcc.wpearson(hits_allowed_list, runs_allowed_list, batters_faced_list))
# print("Correlation between walks and runs allowed:",
#       wpcc.wpearson(walks_allowed_list, runs_allowed_list, batters_faced_list))
# print("Correlation between homeruns and runs allowed:",
#       wpcc.wpearson(homeruns_allowed_list, runs_allowed_list, batters_faced_list))

# char_outs_pitched_list = []
# char_runs_allowed_list = []
# char_hits_allowed_list = []
# char_walks_allowed_list = []
# char_homeruns_allowed_list = []
# char_strikeouts_list = []
# char_batters_faced_list = []

# for char in sorted_pitcher_list:
#     d_stats = character_dict[char]["Defensive Stats"]
#     if d_stats["Batters Faced"] > 1000:
#         outs_pitched = d_stats["Batters Faced"] - d_stats["Batters Walked"] - d_stats["Batters Hit"] - d_stats[
#             "Hits Allowed"]
#         outs_pitched = round(outs_pitched * 1.078)
#         char_outs_pitched_list.append(outs_pitched)
#         char_batters_faced_list.append(d_stats["Batters Faced"])
#         char_runs_allowed_list.append(d_stats["Runs Allowed"] / outs_pitched)
#         char_hits_allowed_list.append(d_stats["Hits Allowed"] / outs_pitched)
#         char_walks_allowed_list.append(d_stats["Batters Hit"] + d_stats["Batters Walked"] / outs_pitched)
#         char_homeruns_allowed_list.append(d_stats["HRs Allowed"] / outs_pitched)
#         char_strikeouts_list.append(d_stats["Strikeouts"] / outs_pitched)

# print("CHARACTERS", len(char_outs_pitched_list))
# print("Correlation between strikeouts and runs allowed:",
#       wpcc.wpearson(char_strikeouts_list, char_runs_allowed_list, char_batters_faced_list))
# print("Correlation between hits and runs allowed:",
#       wpcc.wpearson(char_hits_allowed_list, char_runs_allowed_list, char_batters_faced_list))
# print("Correlation between walks and runs allowed:",
#       wpcc.wpearson(char_walks_allowed_list, char_runs_allowed_list, char_batters_faced_list))
# print("Correlation between homeruns and runs allowed:",
#       wpcc.wpearson(char_homeruns_allowed_list, char_runs_allowed_list, char_batters_faced_list))

# player_outs_pitched_list = []
# player_runs_allowed_list = []
# player_hits_allowed_list = []
# player_walks_allowed_list = []
# player_homeruns_allowed_list = []
# player_strikeouts_list = []
# player_batters_faced_list = []

# for player in player_dict:
#     p_stats = player_dict[player]
#     if p_stats["Batters Faced"] > 1000:
#         outs_pitched = p_stats["Batters Faced"] - p_stats["Batters Walked"] - p_stats["Batters Hit"] - p_stats[
#             "Hits Allowed"]
#         outs_pitched = round(outs_pitched * 1.078)
#         player_outs_pitched_list.append(outs_pitched)
#         player_batters_faced_list.append(p_stats["Batters Faced"])
#         player_runs_allowed_list.append(p_stats["Runs Allowed"] / outs_pitched)
#         player_hits_allowed_list.append(p_stats["Hits Allowed"] / outs_pitched)
#         player_walks_allowed_list.append(p_stats["Batters Hit"] + p_stats["Batters Walked"] / outs_pitched)
#         player_homeruns_allowed_list.append(p_stats["HRs Allowed"] / outs_pitched)
#         player_strikeouts_list.append(p_stats["Strikeouts"] / outs_pitched)

# print("PLAYERS", len(player_outs_pitched_list))
# print("Correlation between strikeouts and runs allowed:",
#       wpcc.wpearson(player_strikeouts_list, player_runs_allowed_list, player_batters_faced_list))
# print("Correlation between hits and runs allowed:",
#       wpcc.wpearson(player_hits_allowed_list, player_runs_allowed_list, player_batters_faced_list))
# print("Correlation between walks and runs allowed:",
#       wpcc.wpearson(player_walks_allowed_list, player_runs_allowed_list, player_batters_faced_list))
# print("Correlation between homeruns and runs allowed:",
#       wpcc.wpearson(player_homeruns_allowed_list, player_runs_allowed_list, player_batters_faced_list))
# print(player_dict)

# print("AVG: " + "{:.3f}".format(character["Offensive Stats"]["Hits"] / character["Offensive Stats"]["At Bats"]))
