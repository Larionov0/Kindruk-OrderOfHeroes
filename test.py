from random import randint


class Hero:
    name = 'Hero'
    hp = max_hp = 20
    attack = 3
    armor = 0
    magic = 0

    alive = True
    did_action = False

    def __init__(self):
        pass

    def normal_attack(self, other):
        print(f"{self.name} копнув героя {other.name}")
        other.get_damage(self.attack)

    def get_damage(self, damage):
        if damage > self.armor:
            remaining_damage = damage - self.armor
        else:
            remaining_damage = 1
        print(f"У {self.name} влітає {remaining_damage}/{damage} урона")
        self.loose_hp(remaining_damage)

    def loose_hp(self, damage):
        self.hp = self.hp - damage
        print(f"{self.name} втратив {damage} hp. Залишилося {self.hp}/{self.max_hp}")
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False
        print(f"{self.name} is dead")

    def cast_1_skill(self, my_team, enemies_team):
        pass

    def cast_2_skill(self, my_team, enemies_team):
        pass

    def make_move_menu(self, my_team, enemies_team):
        self.did_action = False
        while True:
            text = f'--= Хід героя {self.name} =--\n' \
                   f'1 - звичайна атака\n' \
                   f'2 - використати 1 вміння\n' \
                   f'3 - використати 2 вміння\n' \
                   f'4 - закінчити хід\n' \
                   f'5 - подивитися інформацію про героїв\n' \
                   f'6 - ваш вибір: '
            choice = input(text)
            if choice == '1':
                self.normal_attack_menu(enemies_team)
            elif choice == '2':
                pass
            elif choice == '4':
                return

    def normal_attack_menu(self, enemies_team):
        if self.did_action:
            print(f"Ви вже атакували")
            return
        print(f"Виберіть героя для удару:")
        print(f"0 - назад")
        i = 1
        for hero in enemies_team:
            print(f"{i} - {hero.name} ({hero.hp}/{hero.max_hp})")
            i += 1
        choice = int(input())
        if choice == 0:
            return
        elif 1 <= choice <= len(enemies_team):
            target_hero = enemies_team[choice - 1]
            self.normal_attack(target_hero)
            # self.did_action = True


class Archer(Hero):
    name = 'Archer'
    hp = max_hp = 16
    attack = 4

    def normal_attack(self, other):
        lack = randint(1, 100)
        if lack <= 30:
            print(f"{self.name} косий xD")
        else:
            super().normal_attack(other)


class Slime(Hero):
    name = 'Slime'
    hp = max_hp = 30
    attack = 2
    armor = 1

    def get_damage(self, damage):
        super().get_damage(damage)
        lack = randint(1, 100)
        if lack > 50:
            self.hp += 1


class Assassin(Hero):
    name = 'Assassin'
    hp = max_hp = 17
    attack = 5

    def normal_attack(self, other):
        lack = randint(1, 100)
        if lack <= 30:
            print(f"{self.name} Робить критичний удар по {other.name}")
            other.get_damage(round(self.attack * 1.5))
        else:
            print(f"{self.name} копнув героя {other.name}")
            other.get_damage(self.attack)


class Doctor(Hero):
    name = 'Doctor'
    hp = max_hp = 18
    attack = 2
    armor = 0

    def get_damage(self, damage):
        lack = randint(1, 100)
        if lack <= 30:
            print(f"У {self.name} влітає {0}/{damage} урона бо {self.name} ухилився")
        else:
            super().get_damage(damage)


def main():
    team1 = [Assassin(), Doctor()]
    team2 = [Archer(), Slime()]

    round_ = 1
    while True:
        for hero in team1:
            hero.make_move_menu(team1, team2)
        for hero in team2:
            hero.make_move_menu(team2, team1)

        round_ += 1

main()
