import csv
import itertools
from collections import defaultdict


def load_shift_availability(path):
    """Load availability from shift.csv.

    Returns
    -------
    days: list of day strings
    availability: dict mapping day -> list of available names
    names: list of all names in the order of appearance
    """
    availability = defaultdict(list)
    names = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        days = header[1:]
        for row in reader:
            name = row[0]
            names.append(name)
            for day, mark in zip(days, row[1:]):
                if mark == '○':
                    availability[day].append(name)
    return days, availability, names


def load_attributes(path):
    """Load attributes from attribute.csv.

    Returns dict mapping name -> {'gender': str, 'committee': bool}
    """
    attr = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            name, gender, committee = row
            attr[name] = {
                'gender': gender,
                'committee': committee == '〇'
            }
    return attr


def count_gender(team, attributes):
    male = sum(1 for n in team if attributes[n]['gender'] == 'male')
    female = sum(1 for n in team if attributes[n]['gender'] == 'female')
    return male, female


def has_committee(team, attributes):
    return any(attributes[n]['committee'] for n in team)


def choose_team(candidates, attributes, counts, prev_team):
    """Select best team from candidate combinations."""
    best_team = None
    best_score = float('inf')
    for team in itertools.combinations(candidates, 4):
        if not has_committee(team, attributes):
            continue  # must have committee
        score = 0
        male, female = count_gender(team, attributes)
        if male == 0:
            score += 5
        if female == 0:
            score += 5
        for name in team:
            if counts[name] >= 2:
                score += (counts[name] - 1) * 10
            if prev_team and name in prev_team:
                score += 3
        if score < best_score:
            best_score = score
            best_team = team
    if best_team is None:
        # fallback: ignore committee requirement if necessary
        for team in itertools.combinations(candidates, 4):
            score = 100  # large base penalty for not having committee
            male, female = count_gender(team, attributes)
            if male == 0:
                score += 5
            if female == 0:
                score += 5
            for name in team:
                if counts[name] >= 2:
                    score += (counts[name] - 1) * 10
                if prev_team and name in prev_team:
                    score += 3
            if score < best_score:
                best_score = score
                best_team = team
    return best_team


def build_schedule(days, availability, attributes):
    schedule = {}
    counts = defaultdict(int)
    prev_team = None
    for day in days:
        candidates = availability.get(day, [])
        team = choose_team(candidates, attributes, counts, prev_team)
        if team is None:
            raise ValueError(f"No valid team for {day}")
        schedule[day] = team
        for name in team:
            counts[name] += 1
        prev_team = team
    return schedule, counts


def output_schedule(schedule, out_path):
    days = list(schedule.keys())
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['day', 'member1', 'member2', 'member3', 'member4'])
        for day in days:
            writer.writerow([day] + list(schedule[day]))


def main():
    shift_path = input('shift.csvのパスを入力してください: ')
    attr_path = input('attribute.csvのパスを入力してください: ')
    out_path = input('出力先csvのパスを入力してください: ')

    days, availability, names = load_shift_availability(shift_path)
    attributes = load_attributes(attr_path)
    schedule, counts = build_schedule(days, availability, attributes)
    output_schedule(schedule, out_path)
    unique_committee = {n for n in counts if attributes.get(n, {}).get("committee") and counts[n] > 0}
    unique_male = {n for n in counts if attributes.get(n, {}).get("gender") == "male" and counts[n] > 0}
    unique_female = {n for n in counts if attributes.get(n, {}).get("gender") == "female" and counts[n] > 0}

    print('各メンバーのアサイン回数:')
    for name, c in counts.items():
        print(f'{name}: {c}')
    print('推進委員の人数:', len(unique_committee))
    print('男性の人数:', len(unique_male))
    print('女性の人数:', len(unique_female))


if __name__ == '__main__':
    main()
